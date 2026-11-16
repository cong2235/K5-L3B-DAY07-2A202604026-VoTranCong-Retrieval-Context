"""Build the advanced-challenge index (IEA Global EV Outlook 2025) and load it into pgvector.

Chunk kinds (each keeps document page, section, element id, crop path and bbox so evidence can be verified on the original):
  text      body text outside tables/figures (paragraph packing, <= 900 chars)
  caption   VLM description of a table/figure crop (title + caption, split <= 1500 chars)
  layer     exact PDF text layer of the crop (numbers/labels/notes; split <= 1200 chars)
  chartdata numbers rebuilt from vector geometry (scripts/adv_charts.py) for charts listed in adv/verified_charts.json
Usage: python -I scripts/adv_index.py --pdf adv/source/GlobalEVOutlook2025.pdf --work adv/work [--load]
Writes adv/work/index_chunks.json; with --load also (re)creates table adv_chunks in the Day 6 pgvector database.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import adv_charts as C  # noqa: E402

NOISE = re.compile(r'^(Global EV Outlook 2025|PAGE\s*\|\s*\d+|IEA\.\s*CC BY 4\.0\.?)\s*$', re.I)
DEFAULT_URL = 'postgresql://day6:day6_local_only@127.0.0.1:55433/day6_lab'  # local-only Docker credentials


def clean(t):
    t = re.sub(r'T�rkiye', 'Türkiye', t).replace('�', "'")
    return re.sub(r'[ \t]+', ' ', t).strip()


def pack(parts, limit):
    out, cur = [], ''
    for p in parts:
        if cur and len(cur) + len(p) + 1 > limit:
            out.append(cur)
            cur = ''
        while len(p) > limit:                      # a single over-long paragraph: cut at a sentence/space boundary
            cut = max(p.rfind('. ', 0, limit), p.rfind(' ', 0, limit))
            cut = cut if cut > limit * 0.5 else limit
            out.append((cur + ' ' + p[:cut]).strip() if cur else p[:cut])
            cur, p = '', p[cut:].strip()
        cur = (cur + '\n' + p).strip() if cur else p
    if cur:
        out.append(cur)
    return out


def chart_text(res, title):
    lines = [f'Chart data rebuilt from the PDF vector geometry: {title}']
    if 'bars' in res:
        series = sorted({b['series'] for b in res['bars']})
        table = {}
        for b in res['bars']:
            table.setdefault(b['category'], {})[b['series']] = b['value']
        lines.append('category | ' + ' | '.join(series))
        for c in res['categories']:
            lines.append(f'{c} | ' + ' | '.join(str(table[c].get(s, '')) for s in series))
    else:
        for s in res['series']:
            pts = s['points']
            lines.append(f"{s['series']} ({s['kind']}, {s['axis']} axis): " + '; '.join(f'{x:g}: {v:g}' for x, v in pts))
            hi, lo = max(pts, key=lambda p: p[1]), min(pts, key=lambda p: p[1])
            lines.append(f"  maximum {hi[1]:g} at {hi[0]:g}; minimum {lo[1]:g} at {lo[0]:g}")
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', required=True, type=Path)
    ap.add_argument('--work', required=True, type=Path)
    ap.add_argument('--load', action='store_true')
    ap.add_argument('--database-url', default=DEFAULT_URL)
    a = ap.parse_args()
    doc = pymupdf.open(a.pdf)
    pages = {r['page']: r for r in map(json.loads, (a.work / 'pages.jsonl').read_text(encoding='utf-8').splitlines())}
    els = [json.loads(l) for l in (a.work / 'elements.jsonl').read_text(encoding='utf-8').splitlines()]
    caps = {r['element_id']: r for r in map(json.loads, (a.work / 'element_captions.jsonl').read_text(encoding='utf-8').splitlines())}
    verified = json.loads((ROOT / 'adv' / 'verified_charts.json').read_text(encoding='utf-8')) if (ROOT / 'adv' / 'verified_charts.json').exists() else []
    chunks = []

    counters = {}

    def add(kind, page, element, text, section, **meta):
        key = (kind, element or 'p%03d' % page)
        n = counters[key] = counters.get(key, -1) + 1
        chunks.append({'id': f'{kind}:{key[1]}:{n}', 'kind': kind, 'page': page, 'element_id': element,
                       'section': section, 'text': text, **meta})

    for pno, page in enumerate(doc, start=1):
        rects = [pymupdf.Rect(e['bbox']) for e in els if e['page'] == pno]
        blocks = [b for b in page.get_text('blocks') if b[6] == 0 and not any(pymupdf.Rect(b[:4]).intersects(r) for r in rects)]
        paras = [clean(b[4].replace('\n', ' ')) for b in sorted(blocks, key=lambda b: (round(b[1]), b[0]))]
        paras = [p for p in paras if p and not NOISE.match(p) and len(p) > 2]
        sec = pages[pno]['section']
        for piece in pack(paras, 900):
            add('text', pno, None, f'[page {pno}, {sec}]\n{piece}', sec)
    by_id = {e['element_id']: e for e in els}
    for e in els:
        eid, pno, sec = e['element_id'], e['page'], pages[e['page']]['section']
        head = f"[{e['kind']} on page {pno}: {clean(e['title'])[:160]}]"
        meta = {'crop': e['crop'], 'bbox': e['bbox'], 'fallback': bool(e.get('fallback'))}
        if eid in caps:
            for piece in pack([clean(caps[eid]['caption'])], 1500):
                add('caption', pno, eid, f'{head}\n{piece}', sec, **meta)
        for piece in pack([clean(l) for l in e['text'].splitlines() if l.strip() and not NOISE.match(l.strip())], 1200):
            add('layer', pno, eid, f'{head}\n{piece}', sec, **meta)
    for eid in verified:
        e = by_id[eid]
        page = doc[e['page'] - 1]
        try:
            res = C.extract_bars(page, e['bbox'])
        except ValueError:
            res = C.extract_lines(page, e['bbox'])
        for piece in pack(chart_text(res, clean(e['title'])).split('\n'), 1200):
            add('chartdata', e['page'], eid, f"[chart data on page {e['page']}]\n{piece}", pages[e['page']]['section'],
                crop=e['crop'], bbox=e['bbox'], fallback=False)
    ids = [c['id'] for c in chunks]
    assert len(ids) == len(set(ids)), 'duplicate chunk ids'
    (a.work / 'index_chunks.json').write_text(json.dumps(chunks, ensure_ascii=False, indent=1), encoding='utf-8')
    kinds = {k: sum(c['kind'] == k for c in chunks) for k in ('text', 'caption', 'layer', 'chartdata')}
    print('chunks', len(chunks), kinds, '| pages covered', len({c['page'] for c in chunks}), 'of', len(doc),
          '| max chars', max(len(c['text']) for c in chunks))
    if a.load:
        import psycopg
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('intfloat/multilingual-e5-small', device='cpu')
        vecs = model.encode([f"passage: {c['text']}" for c in chunks], batch_size=32, normalize_embeddings=True, show_progress_bar=False)
        with psycopg.connect(a.database_url) as conn:
            conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
            conn.execute('DROP TABLE IF EXISTS adv_chunks')
            conn.execute("""CREATE TABLE adv_chunks (chunk_id text PRIMARY KEY, page integer NOT NULL, kind text NOT NULL,
                            element_id text, section text, text text NOT NULL, metadata jsonb NOT NULL DEFAULT '{}',
                            embedding vector(384) NOT NULL)""")
            with conn.cursor() as cur:
                cur.executemany('INSERT INTO adv_chunks VALUES (%s,%s,%s,%s,%s,%s,%s,%s::vector)',
                                [(c['id'], c['page'], c['kind'], c['element_id'], c['section'], c['text'],
                                  json.dumps({k: c[k] for k in ('crop', 'bbox', 'fallback') if k in c}),
                                  '[' + ','.join(f'{x:.7f}' for x in v) + ']') for c, v in zip(chunks, vecs)])
            n = conn.execute('SELECT count(*) FROM adv_chunks').fetchone()[0]
        print('loaded into pgvector table adv_chunks:', n)


if __name__ == '__main__':
    main()
