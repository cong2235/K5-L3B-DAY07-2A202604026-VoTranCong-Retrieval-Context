"""Build the held-out test set from data/heldout_spec.json: the evidence quote is cut verbatim from a chunk
of the stated page (start phrase .. end phrase, or first sentence end), so it is an exact substring.
Fails if a quote spans two chunks. Pages used here are not gold pages of any dev question."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
chunks = json.loads((ROOT / 'data/converted/chunks.json').read_text(encoding='utf-8'))
spec = json.loads((ROOT / 'data/heldout_spec.json').read_text(encoding='utf-8'))
out, bad = [], 0
for s in spec:
    pat = re.compile(r'\s+'.join(map(re.escape, s['start'].split())) + r'.*?' +
                     (r'\s+'.join(map(re.escape, s['end'].split())) if s['end'] else r'[.!?](?=\s|$)'), re.S)
    quote = next((m.group(0) for c in chunks if c['page'] == s['page'] for m in [pat.search(c['text'])] if m), None)
    if not quote:
        bad += 1; print('FAIL', s['id']); continue
    q = {'id': s['id'], 'split': 'test', 'type': 'heldout', 'question': s['question'], 'expected_answer': s['answer'],
         'filter': s.get('filter'), 'gold_source_id': 'openstax-pds', 'gold_page': s['page'], 'evidence_quote': quote}
    out.append(q)
(ROOT / 'data/heldout_questions.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'heldout={len(out)} failures={bad}')
for q in out: print(q['id'], q['gold_page'], repr(q['evidence_quote'][:110]))
sys.exit(1 if bad else 0)
