"""Describe tables, charts and figures of PDF pages with a vision-language model (OpenAI-compatible endpoint).

Usage:
  python scripts/adv_caption.py --base-url https://<tunnel>/v1 --key-env KAGGLE_LLM_API_KEY \
      --model qwen2.5-vl-7b-instruct [--pages 22,160 | --all-visual] [--out adv/work/captions.jsonl]
Reads adv/work/pages.jsonl and adv/work/pages/p###.png (made by scripts/adv_extract.py). Appends one JSON line per page
and skips pages already done, so an interrupted run resumes. The model output is NOT ground truth: captions are checked
against the original pages when the benchmark is written and graded.
"""
import argparse
import base64
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.agent import _post, load_key  # noqa: E402

PROMPT = """You are transcribing one page of the IEA report "Global EV Outlook 2025" so that it can be searched later.
Describe ONLY the tables, charts, maps, diagrams and photos visible on this page (ignore ordinary running text, which is already indexed).
For every such element write:
- TITLE: the exact title printed above it.
- TYPE: table / bar chart / line chart / stacked chart / scatter / map / diagram / photo.
- For a TABLE: reproduce it as a markdown table with the exact numbers, row/column labels and units printed.
- For a CHART: axis titles and units, the legend entries, the categories or years shown, and the data values you can read.
  Give numbers only when you can read them (printed labels or clear gridlines) and mark estimates with "~". Say which series is highest/lowest and the trend.
- NOTES/SOURCES: copy the notes and sources lines.
Never invent a number or label; write "unreadable" when you cannot read something. If the page has no table, chart or figure, answer exactly: NO_VISUAL_CONTENT.
Text of the page, for reference (labels and units may be taken from it):
---
{text}
---"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-url', required=True)
    ap.add_argument('--key-env', default='KAGGLE_LLM_API_KEY')
    ap.add_argument('--model', default='qwen2.5-vl-7b-instruct')
    ap.add_argument('--work', type=Path, default=ROOT / 'adv' / 'work')
    ap.add_argument('--out', type=Path)
    ap.add_argument('--pages', help='comma-separated physical page numbers')
    ap.add_argument('--all-visual', action='store_true', help='every page flagged visual by adv_extract.py')
    ap.add_argument('--max-tokens', type=int, default=1800)
    ap.add_argument('--frequency-penalty', type=float, default=0.0, help='mild value (e.g. 0.2) discourages degenerate repetition')
    ap.add_argument('--redo', action='store_true', help='re-caption the given --pages; old records move to captions_replaced.jsonl')
    a = ap.parse_args()
    out = a.out or a.work / 'captions.jsonl'
    pages = {r['page']: r for r in map(json.loads, (a.work / 'pages.jsonl').read_text(encoding='utf-8').splitlines())}
    todo = sorted(int(x) for x in a.pages.split(',')) if a.pages else sorted(p for p, r in pages.items() if r['visual'])
    if not a.pages and not a.all_visual:
        sys.exit('pass --pages or --all-visual')
    if a.redo and out.exists():
        recs = [json.loads(l) for l in out.read_text(encoding='utf-8').splitlines()]
        old = [r for r in recs if r['page'] in set(todo)]
        with (out.parent / 'captions_replaced.jsonl').open('a', encoding='utf-8') as f:
            f.writelines(json.dumps(r, ensure_ascii=False) + '\n' for r in old)
        out.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs if r['page'] not in set(todo)),
                       encoding='utf-8')
    done = {json.loads(l)['page'] for l in out.read_text(encoding='utf-8').splitlines()} if out.exists() else set()
    key, url = load_key(a.key_env), a.base_url.rstrip('/') + '/chat/completions'
    for n, pg in enumerate([p for p in todo if p not in done], start=1):
        img = base64.b64encode((a.work / 'pages' / f'p{pg:03d}.png').read_bytes()).decode()
        body = {'model': a.model, 'temperature': 0, 'max_tokens': a.max_tokens, 'frequency_penalty': a.frequency_penalty, 'messages': [{'role': 'user', 'content': [
            {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + img}},
            {'type': 'text', 'text': PROMPT.format(text=pages[pg]['text'][:3500])}]}]}
        t0 = time.perf_counter()
        try:
            d = _post(url, {'Authorization': 'Bearer ' + key}, body, retries=4, timeout=300)
            msg = d['choices'][0]['message']['content'].strip()
            rec = {'page': pg, 'caption': msg, 'finish': d['choices'][0]['finish_reason'], 'usage': d.get('usage', {}),
                   'seconds': round(time.perf_counter() - t0, 1), 'model': a.model}
        except Exception as e:  # recorded, not faked; rerun to retry
            print(f'p{pg} ERROR {str(e)[:150]}', flush=True)
            continue
        with out.open('a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        print(f'[{n}/{len(todo) - len(done)}] p{pg} {rec["seconds"]}s finish={rec["finish"]} chars={len(msg)}', flush=True)


if __name__ == '__main__':
    main()
