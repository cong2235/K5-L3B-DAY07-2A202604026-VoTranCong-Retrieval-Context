"""Export Day 6 chunks (strategy B) and benchmark questions to raw JSON arrays for starter/convert_day6.py.

Usage (from the Day 7 repo root):
    python scripts/export_day6.py --day6 <path to Day 6 repo> --output data/day6_raw

Reuses the Day 6 chunking code, so chunk IDs match what is stored in pgvector (strategy "B").
Also checks that every answerable evidence quote lies inside one chunk of the right page, and that
each absent question's topic keywords really do not occur in the corpus.
"""
import argparse
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--day6', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--absent', type=Path, default=Path('data/absent_questions.json'))
    a = ap.parse_args()
    starter = a.day6 / 'starter'
    sys.path.insert(0, str(starter))
    from src.chunking import by_paragraph  # noqa: E402  (Day 6 code)
    from src.ingestion import flat, load_corpus  # noqa: E402

    pages = load_corpus(starter / 'data' / 'corpus_pages.jsonl')
    chunks = [c for p in pages for c in by_paragraph(p, 800)]
    raw_chunks = [asdict(c) for c in chunks]

    questions, bad_pages = [], []
    for fname, origin in (('benchmark.json', 'day6-main'), ('benchmark_test2.json', 'day6-test2')):
        for q in json.loads((starter / 'data' / fname).read_text(encoding='utf-8'))['questions']:
            q = dict(q)
            q['origin'] = origin
            q['origin_split'] = q['split']
            # Day 6 test/test2 were seen during Day 6, so Day 7 uses them as extra DEV data (30 questions);
            # the Day 7 test set is the held-out set below, never used for tuning.
            q['split'] = 'dev'
            questions.append(q)
    held = json.loads((Path(__file__).resolve().parents[1] / 'data' / 'heldout_questions.json').read_text(encoding='utf-8'))
    dev_pages = {q['gold_page'] for q in questions}
    for q in held:
        q['origin'] = 'day7-heldout'
        q['origin_split'] = 'test'
        if q['gold_page'] in dev_pages:
            print(f"WARN {q['id']}: gold page {q['gold_page']} is also a dev gold page")
            bad_pages.append(q['id'])
    questions.extend(held)

    bad = len(bad_pages)
    for q in questions:
        # Day 7 matches evidence as an exact substring of a chunk, but Day 6 matched whitespace/case-folded.
        # Rewrite the quote to the exact chunk text (same words, original line breaks); fail if not found.
        pat = re.compile(r'\s+'.join(re.escape(w) for w in q['evidence_quote'].split()), re.I)
        exact = None
        for c in chunks:
            m = pat.search(c.text) if c.page == q['gold_page'] else None
            if m:
                exact = m.group(0)
                break
        if exact is None:
            bad += 1
            print(f"WARN {q['id']}: evidence not inside a single chunk of page {q['gold_page']}")
        else:
            q['evidence_quote_day6'] = q['evidence_quote']
            q['evidence_quote'] = exact

    corpus = ' '.join(flat(p.text) for p in pages)
    absent = json.loads(a.absent.read_text(encoding='utf-8'))
    for x in absent:
        for term in x['absence_check']:
            if term in corpus:
                bad += 1
                print(f"WARN {x['id']}: term '{term}' occurs in corpus -> question may be answerable")

    a.output.mkdir(parents=True, exist_ok=True)
    (a.output / 'chunks.json').write_text(json.dumps(raw_chunks, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (a.output / 'questions.json').write_text(json.dumps(questions, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    count = lambda s, ans: sum(1 for x in (questions if ans else absent) if x['split'] == s)
    print(f"chunks={len(raw_chunks)} answerable dev={count('dev', True)} test={count('test', True)} "
          f"absent dev={count('dev', False)} test={count('test', False)} warnings={bad}")
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
