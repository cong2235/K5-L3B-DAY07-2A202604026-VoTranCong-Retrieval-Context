"""Survey a PDF: pages, text volume, embedded images, vector-drawing density and detected tables per page.
Usage: python -I scripts/adv_inspect.py <pdf> [--out adv/survey.json]"""
import json
import sys
from pathlib import Path

import pymupdf

pdf = Path(sys.argv[1])
out = Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else None
doc = pymupdf.open(pdf)
rows = []
for i, p in enumerate(doc, start=1):
    text = p.get_text()
    tabs = -1  # PyMuPDF find_tables() segfaults on the IEA GEVO2025 PDF, so tables are not detected here
    rows.append({'page': i, 'chars': len(text), 'images': len(p.get_images(full=True)),
                 'drawings': len(p.get_drawings()), 'tables': tabs})
n = len(rows)
print('file', pdf.name, 'pages', n, 'metadata', {k: v for k, v in doc.metadata.items() if v})
print('total chars', sum(r['chars'] for r in rows), '| pages <200 chars:', sum(r['chars'] < 200 for r in rows))
print('pages with embedded images:', sum(r['images'] > 0 for r in rows), '| pages with >=50 vector drawings (likely charts):',
      sum(r['drawings'] >= 50 for r in rows))
print('toc entries:', len(doc.get_toc()))
for lvl, title, pg in doc.get_toc()[:40]:
    print('  ' * (lvl - 1) + f'{title} .... p{pg}')
if out:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=1), encoding='utf-8')
