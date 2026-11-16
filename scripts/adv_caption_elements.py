"""Caption each cropped table/figure element (adv/work/elements.jsonl) with a vision-language model.

Usage: python scripts/adv_caption_elements.py --base-url https://<tunnel>/v1 [--key-env KAGGLE_LLM_API_KEY]
       [--model qwen2.5-vl-7b-instruct] [--only p160_e1,p161_e2] [--limit N] [--redo]
Appends to adv/work/element_captions.jsonl (resumable by element_id). The text layer of the crop is given to the model as the
authority for labels/numbers/units; captions are NOT ground truth and chart values must still be checked against the page.
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

PROMPT = """You are transcribing ONE {kind} cropped from page {page} of the IEA report "Global EV Outlook 2025" so it can be searched later.
The exact text layer of this crop (characters copied from the PDF) is given below. Use it as the authority for every label, number,
unit and note it contains; use the image only for structure, colours and visual encodings.
Write:
- TITLE: the printed title.
- TYPE: table / bar chart / line chart / stacked chart / scatter / map / diagram / heat-map table.
- For a TABLE: a markdown table with the exact values, row/column labels and units. If cells carry meaning by colour (for example green /
  orange / red) say, for each row, the colour and what the legend or notes say it means.
- For a CHART: axis titles and units, legend entries, categories or years, and the trend or ranking you can SEE (highest, lowest,
  increases, decreases). Give a number only when it is printed in the text layer; otherwise describe qualitatively or mark an estimate with "~".
- NOTES and SOURCES: copy them exactly.
Never invent labels or numbers. If something is unreadable write "unreadable".
TEXT LAYER:
---
{text}
---"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-url', required=True)
    ap.add_argument('--key-env', default='KAGGLE_LLM_API_KEY')
    ap.add_argument('--model', default='qwen2.5-vl-7b-instruct')
    ap.add_argument('--work', type=Path, default=ROOT / 'adv' / 'work')
    ap.add_argument('--only', help='comma-separated element ids')
    ap.add_argument('--limit', type=int)
    ap.add_argument('--max-tokens', type=int, default=3000)
    ap.add_argument('--frequency-penalty', type=float, default=0.0)
    ap.add_argument('--redo', action='store_true', help='re-caption the --only elements (old records move to *_replaced.jsonl)')
    a = ap.parse_args()
    out = a.work / 'element_captions.jsonl'
    els = [json.loads(l) for l in (a.work / 'elements.jsonl').read_text(encoding='utf-8').splitlines()]
    if a.only:
        want = set(a.only.split(','))
        els = [e for e in els if e['element_id'] in want]
    if a.redo and out.exists():
        ids = {e['element_id'] for e in els}
        recs = [json.loads(l) for l in out.read_text(encoding='utf-8').splitlines()]
        with (a.work / 'element_captions_replaced.jsonl').open('a', encoding='utf-8') as f:
            f.writelines(json.dumps(r, ensure_ascii=False) + '\n' for r in recs if r['element_id'] in ids)
        out.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs if r['element_id'] not in ids), encoding='utf-8')
    done = {json.loads(l)['element_id'] for l in out.read_text(encoding='utf-8').splitlines()} if out.exists() else set()
    todo = [e for e in els if e['element_id'] not in done][:a.limit]
    key, url = load_key(a.key_env), a.base_url.rstrip('/') + '/chat/completions'
    for n, e in enumerate(todo, start=1):
        img = base64.b64encode((a.work / e['crop']).read_bytes()).decode()
        body = {'model': a.model, 'temperature': 0, 'max_tokens': a.max_tokens, 'frequency_penalty': a.frequency_penalty,
                'messages': [{'role': 'user', 'content': [
                    {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + img}},
                    {'type': 'text', 'text': PROMPT.format(kind=e['kind'], page=e['page'], text=e['text'][:6000])}]}]}
        t0 = time.perf_counter()
        try:
            d = _post(url, {'Authorization': 'Bearer ' + key}, body, retries=4, timeout=300)
            msg = d['choices'][0]['message']['content'].strip()
            rec = {'element_id': e['element_id'], 'page': e['page'], 'kind': e['kind'], 'caption': msg,
                   'finish': d['choices'][0]['finish_reason'], 'usage': d.get('usage', {}),
                   'seconds': round(time.perf_counter() - t0, 1), 'model': a.model}
        except Exception as ex:  # recorded, not faked; rerun to retry
            print(f'{e["element_id"]} ERROR {str(ex)[:150]}', flush=True)
            continue
        with out.open('a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        print(f'[{n}/{len(todo)}] {e["element_id"]} {e["kind"]} {rec["seconds"]}s finish={rec["finish"]} chars={len(msg)}', flush=True)


if __name__ == '__main__':
    main()
