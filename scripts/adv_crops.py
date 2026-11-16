"""Detect every table/figure element on the IEA report pages and save a crop + its exact text layer.

Each IEA element sits between two thin blue horizontal rules (colour ~ #1F4A7D, width > 60% of the page): a rule above the
title and one below the Notes/Sources lines. Elements are the consecutive (top, bottom) pairs; an unpaired top rule extends to
the page footer. Usage: python -I scripts/adv_crops.py --pdf adv/source/GlobalEVOutlook2025.pdf --out adv/work [--dpi 170]
Writes adv/work/crops/p###_e#.png and adv/work/elements.jsonl:
  element_id, page, bbox (PDF points), title, kind ('figure' if the "IEA. CC BY 4.0" credit line is inside, else 'table'),
  text (text layer inside the crop), crop (path), drawings (vector items inside).
"""
import argparse
import json
import re
from pathlib import Path

import pymupdf

BLUE = (0.122, 0.286, 0.490)
ap = argparse.ArgumentParser()
ap.add_argument('--pdf', required=True, type=Path)
ap.add_argument('--out', required=True, type=Path)
ap.add_argument('--dpi', type=int, default=170)
ap.add_argument('--fallback-pages', default='', help='pages with a figure but no blue rules: crop the whole content area (flagged fallback)')
a = ap.parse_args()
doc = pymupdf.open(a.pdf)
(a.out / 'crops').mkdir(parents=True, exist_ok=True)
CREDIT = re.compile(r'IEA\.\s*CC BY 4\.0')


def is_blue(color):
    return color is not None and len(color) == 3 and all(abs(c - b) < 0.02 for c, b in zip(color, BLUE))


FALLBACK = {int(x) for x in a.fallback_pages.split(',') if x}
rows = []
for pno, page in enumerate(doc, start=1):
    W, H = page.rect.width, page.rect.height
    rules = sorted({(round(d['rect'].y0, 1), round(d['rect'].x0, 1), round(d['rect'].x1, 1))
                    for d in page.get_drawings()
                    if d['rect'].width > 0.6 * W and d['rect'].height < 2.5 and is_blue(d.get('color') or d.get('fill'))})
    footer_y = H - 20
    for blk in page.get_text('blocks'):
        if re.search(r'PAGE\s*\|\s*\d+', blk[4]):
            footer_y = blk[1] - 6
    if not rules and pno in FALLBACK:
        rect = pymupdf.Rect(40, 60, W - 40, footer_y)
        text = page.get_text('text', clip=rect).strip()
        eid = f'p{pno:03d}_f1'
        page.get_pixmap(dpi=a.dpi, clip=rect).save(a.out / 'crops' / f'{eid}.png')
        rows.append({'element_id': eid, 'page': pno, 'bbox': [round(v, 1) for v in rect], 'title': ' '.join([l.strip() for l in text.splitlines() if l.strip()][:2]),
                     'kind': 'figure' if CREDIT.search(text) else 'table', 'text': text, 'crop': f'crops/{eid}.png',
                     'drawings': sum(1 for d in page.get_drawings() if rect.intersects(d['rect'])), 'unpaired_rule': False, 'fallback': True})
        continue
    if not rules:
        continue
    pairs = []
    i = 0
    while i < len(rules):
        top = rules[i]
        if i + 1 < len(rules):
            pairs.append((top, rules[i + 1]))
            i += 2
        else:
            # unpaired top rule: end the element right after the last "Source(s):" block above the footer
            # (so footnotes below the figure are not included); fall back to the footer
            src = [b for b in page.get_text('blocks') if b[1] >= top[0] and b[3] <= footer_y + 6
                   and re.search(r'Sources?\s*:', b[4])]
            pairs.append((top, ((max(b[3] for b in src) if src else footer_y), top[1], top[2])))
            i += 1
    for k, (top, bot) in enumerate(pairs, start=1):
        rect = pymupdf.Rect(max(0, top[1] - 4), max(0, top[0] - 3), min(W, top[2] + 4), min(H, bot[0] + 3))
        text = page.get_text('text', clip=rect).strip()
        title_lines = [l.strip() for l in text.splitlines() if l.strip()][:2]
        eid = f'p{pno:03d}_e{k}'
        crop = a.out / 'crops' / f'{eid}.png'
        page.get_pixmap(dpi=a.dpi, clip=rect).save(crop)
        ndraw = sum(1 for d in page.get_drawings() if rect.intersects(d['rect']))
        rows.append({'element_id': eid, 'page': pno, 'bbox': [round(v, 1) for v in rect], 'title': ' '.join(title_lines),
                     'kind': 'figure' if CREDIT.search(text) else 'table', 'text': text, 'crop': f'crops/{eid}.png',
                     'drawings': ndraw, 'unpaired_rule': len(rules) % 2 == 1 and k == len(pairs)})
(a.out / 'elements.jsonl').write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n', encoding='utf-8')
pages = {r['page'] for r in rows}
print(f"elements={len(rows)} on {len(pages)} pages | figures={sum(r['kind'] == 'figure' for r in rows)} "
      f"tables={sum(r['kind'] == 'table' for r in rows)} | unpaired-rule elements={sum(r['unpaired_rule'] for r in rows)}")
print('pages with >=2 elements:', sorted(p for p in pages if sum(r['page'] == p for r in rows) >= 2))
