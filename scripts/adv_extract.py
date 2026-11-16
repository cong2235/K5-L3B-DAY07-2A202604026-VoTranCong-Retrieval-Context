"""Extract per-page text, TOC path and a page image from the IEA PDF; flag pages with figures/tables.

Usage: python -I scripts/adv_extract.py --pdf adv/source/GlobalEVOutlook2025.pdf --out adv/work [--dpi 130]
Writes adv/work/pages.jsonl (one JSON per physical page, 1-based) and adv/work/pages/p###.png.
The PDF is untrusted input: this script only reads it with PyMuPDF (no find_tables: it segfaults on this file).
"""
import argparse
import json
import re
from pathlib import Path

import pymupdf

ap = argparse.ArgumentParser()
ap.add_argument('--pdf', required=True, type=Path)
ap.add_argument('--out', required=True, type=Path)
ap.add_argument('--dpi', type=int, default=130)
a = ap.parse_args()

doc = pymupdf.open(a.pdf)
(a.out / 'pages').mkdir(parents=True, exist_ok=True)

# TOC path per page: the last TOC entries at or before the page (levels 1-3).
toc = [(lvl, title.replace('�', "'").strip(), pg) for lvl, title, pg in doc.get_toc() if pg >= 1]
path_at = {}
cur = {}
by_page = {}
for lvl, title, pg in toc:
    by_page.setdefault(pg, []).append((lvl, title))
for pg in range(1, len(doc) + 1):
    for lvl, title in by_page.get(pg, []):
        cur[lvl] = title
        for deeper in [k for k in cur if k > lvl]:
            del cur[deeper]
    path_at[pg] = ' > '.join(cur[k] for k in sorted(cur) if k <= 2)

FIG = re.compile(r'IEA\.\s*CC BY 4\.0', re.I)     # every figure ends with this credit line; the page header repeats it once
TAB = re.compile(r'^\s*Table\s+\d+|^\s*Table\b', re.M)
rows = []
for i, p in enumerate(doc, start=1):
    text = p.get_text('text')
    pix = p.get_pixmap(dpi=a.dpi)
    pix.save(a.out / 'pages' / f'p{i:03d}.png')
    imgs = len(p.get_images(full=True))
    draws = len(p.get_drawings())
    credits = len(FIG.findall(text))
    figures = max(0, credits - (1 if re.search(r'PAGE\s*\|\s*\d+', text) else 0))   # subtract the page-header credit
    rows.append({'page': i, 'section': path_at.get(i, ''), 'text': text, 'chars': len(text), 'images': imgs,
                 'drawings': draws, 'figures': figures, 'table_mentions': len(TAB.findall(text)),
                 'visual': bool(imgs or draws >= 30 or figures or TAB.search(text)),
                 'width': pix.width, 'height': pix.height})
(a.out / 'pages.jsonl').write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n', encoding='utf-8')
vis = [r['page'] for r in rows if r['visual']]
print(f'pages={len(rows)} visual_pages={len(vis)} figure_pages={sum(r["figures"] > 0 for r in rows)} figures_total={sum(r["figures"] for r in rows)} '
      f'table_pages={sum(r["table_mentions"] > 0 for r in rows)} image_size={rows[0]["width"]}x{rows[0]["height"]}')
print('visual pages:', vis)
