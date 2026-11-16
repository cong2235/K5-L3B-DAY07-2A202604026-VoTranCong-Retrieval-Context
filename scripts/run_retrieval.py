"""Evaluate one retrieval method on one split (retrieval + context only, no LLM).

Usage: python scripts/run_retrieval.py --method dense|tfidf|hybrid --split dev [--top-k 3] [--budget 800] [--use-filter]
Writes results/<split>-<name>/{summary,traces}.json and appends one row to results/comparison.md.
The default split is dev; test must be requested explicitly after the configuration is frozen.
Gold is used only to label hits after retrieval, never inside a query.
"""
import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'starter'))
from baseline import hit, pack_context, validate  # noqa: E402
from src.retrieval import DenseRetriever, HybridRetriever, LexicalRetriever, RerankRetriever  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--method', required=True, choices=('dense', 'tfidf', 'hybrid', 'rerank'))
    ap.add_argument('--split', default='dev', choices=('dev', 'test'))
    ap.add_argument('--top-k', type=int, default=3)
    ap.add_argument('--budget', type=int, default=800, help='context budget in characters')
    ap.add_argument('--budget-tokens', type=int, help='context budget in estimated tokens (chars/4); overrides --budget')
    ap.add_argument('--dense-weight', type=float, default=1.0, help='hybrid: RRF weight of dense ranking')
    ap.add_argument('--lexical-weight', type=float, default=1.0)
    ap.add_argument('--candidates', type=int, default=20, help='hybrid: candidates per retriever')
    ap.add_argument('--reranker', default='BAAI/bge-reranker-base', help='rerank: cross-encoder model')
    ap.add_argument('--fuse', action='store_true', help='rerank: fuse base and cross-encoder ranks with RRF')
    ap.add_argument('--use-filter', action='store_true', help='apply the user-supplied question filter')
    ap.add_argument('--name')
    ap.add_argument('--chunks', type=Path, default=ROOT / 'data/converted/chunks.json')
    ap.add_argument('--questions', type=Path, default=ROOT / 'data/converted/questions.json')
    a = ap.parse_args()
    if a.budget_tokens:
        a.budget = a.budget_tokens * 4  # rough English estimate; real token use is measured later from API usage

    chunks = json.loads(a.chunks.read_text(encoding='utf-8'))
    questions = [q for q in json.loads(a.questions.read_text(encoding='utf-8')) if q['split'] == a.split]
    validate(chunks, questions)
    lexical = LexicalRetriever(chunks)
    retriever = lexical
    if a.method in ('dense', 'hybrid', 'rerank'):
        dense = DenseRetriever(chunks)
        if a.method == 'rerank':
            retriever = RerankRetriever(dense, a.reranker, a.candidates, fuse=a.fuse)
        else:
            retriever = dense if a.method == 'dense' else HybridRetriever(dense, lexical, a.candidates, dense_weight=a.dense_weight, lexical_weight=a.lexical_weight)
    name = a.name or (f"{a.method}-k{a.top_k}-b{a.budget_tokens}t" if a.budget_tokens else f"{a.method}-k{a.top_k}-b{a.budget}")         + (f"-w{a.dense_weight:g}" if a.method == 'hybrid' and a.dense_weight != 1.0 else '') + ('-rrf' if a.method == 'rerank' and a.fuse else '') + ('-filter' if a.use_filter else '')

    traces = []
    for q in questions:
        filters = q.get('filter') if a.use_filter else None
        t0 = time.perf_counter()
        results = retriever.search(q['question'], top_k=max(a.top_k, 3), filters=filters)
        context, ids = pack_context(results[:a.top_k], a.budget)
        ms = (time.perf_counter() - t0) * 1000
        marked = [{**{k: v for k, v in c.items() if k != 'text'}, 'text': c['text'], 'hit': hit(c, q['gold'])}
                  for c in results]
        traces.append({'query_id': q['id'], 'question': q['question'], 'method': a.method, 'filter': filters,
                       'gold': q['gold'], 'results': marked, 'context': context, 'context_ids': ids,
                       'hit1': bool(marked and marked[0]['hit']), 'hit3': any(c['hit'] for c in marked[:3]), 'hitk': any(c['hit'] for c in marked[:a.top_k]),
                       'context_hit': any(c['hit'] and c['id'] in ids for c in marked), 'elapsed_ms': ms})
    n = len(traces)
    ms = sorted(t['elapsed_ms'] for t in traces)
    summary = {'name': name, 'method': a.method, 'split': a.split, 'n': n, 'top_k': a.top_k, 'budget_chars': a.budget,
               'filter': a.use_filter, 'hit1': sum(t['hit1'] for t in traces), 'hit3': sum(t['hit3'] for t in traces),
               'hitk': sum(t['hitk'] for t in traces), 'context_hit': sum(t['context_hit'] for t in traces),
               'avg_context_chars': round(statistics.mean(len(t['context']) for t in traces)),
               'median_ms': round(statistics.median(ms), 1), 'p90_ms': round(ms[int(0.9 * (n - 1))], 1),
               'service_cost_usd': 0, 'failed_q_hit3': [t['query_id'] for t in traces if not t['hit3']]}
    out = ROOT / 'results' / f'{a.split}-{name}'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'traces.json').write_text(json.dumps(traces, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    table = ROOT / 'results' / 'comparison.md'
    if not table.exists():
        table.write_text('| split | name | method | top_k | budget | filter | Hit@1 | Hit@3 | Hit@k | Context | ctx chars | median ms | p90 ms | miss Hit@3 |\n'
                         '|---|---|---|---|---|---|---|---|---|---|---|---|\n', encoding='utf-8')
    with table.open('a', encoding='utf-8') as f:
        f.write(f"| {a.split} | {name} | {a.method} | {a.top_k} | {a.budget} | {a.use_filter} | {summary['hit1']}/{n} | "
                f"{summary['hit3']}/{n} | {summary['hitk']}/{n} | {summary['context_hit']}/{n} | {summary['avg_context_chars']} | {summary['median_ms']} | {summary['p90_ms']} | "
                f"{', '.join(summary['failed_q_hit3']) or '-'} |\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
