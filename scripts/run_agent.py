"""Run the Gemini agent on a split and save traces for manual grading.

Usage: python scripts/run_agent.py --split dev [--top-k 5] [--max-searches 4] [--budget-tokens 2400] [--limit N]
The default split is dev; test only after the configuration is frozen. Gold is used only to label
`context_hit` after the run; the agent never sees gold, expected answers or absence reasons.
Writes results/<split>-agent-<name>/{traces,cases,summary}.json and review.md (for human grading).
"""
import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'starter'))
from baseline import hit  # noqa: E402
from src.agent import GeminiClient, OpenRouterClient, run_agent  # noqa: E402
from src.retrieval import DenseRetriever, RerankRetriever  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--split', default='dev', choices=('dev', 'test'))
    ap.add_argument('--provider', default='openrouter', choices=('openrouter', 'gemini'))
    ap.add_argument('--model')
    ap.add_argument('--base-url', help='OpenAI-compatible endpoint (e.g. http://localhost:20128/v1 for 9Router)')
    ap.add_argument('--key-env', default='OPENROUTER_API_KEY', help='name of the .env variable holding the API key')
    ap.add_argument('--top-k', type=int, default=5)
    ap.add_argument('--max-searches', type=int, default=4)
    ap.add_argument('--budget-tokens', type=int, default=2400)
    ap.add_argument('--force-first-search', action='store_true', help='require a search_documents call on the first turn')
    ap.add_argument('--retriever', default='dense', choices=('dense', 'rerank-rrf'), help='retrieval backend of the search tool')
    ap.add_argument('--limit', type=int)
    ap.add_argument('--name')
    a = ap.parse_args()
    a.model = a.model or ('mistralai/mistral-small-3.2-24b-instruct' if a.provider == 'openrouter' else 'gemini-2.5-flash')
    name = a.name or f"{a.model.replace('/', '_')}-k{a.top_k}-s{a.max_searches}-b{a.budget_tokens}t"

    chunks = json.loads((ROOT / 'data/converted/chunks.json').read_text(encoding='utf-8'))
    ans = [q for q in json.loads((ROOT / 'data/converted/questions.json').read_text(encoding='utf-8')) if q['split'] == a.split]
    absent = [x for x in json.loads((ROOT / 'data/absent_questions.json').read_text(encoding='utf-8')) if x['split'] == a.split]
    items = [(q, True) for q in ans] + [(x, False) for x in absent]
    if a.limit:
        items = items[:a.limit]
    retriever = DenseRetriever(chunks)
    if a.retriever == 'rerank-rrf':
        retriever = RerankRetriever(retriever, candidates=20, fuse=True)
    if a.provider == 'gemini':
        client = GeminiClient(a.model)
    elif a.base_url:  # any OpenAI-compatible endpoint, e.g. local 9Router: --base-url http://localhost:20128/v1 --key-env NINEROUTER_API_KEY
        client = OpenRouterClient(a.model, base_url=a.base_url, key_env=a.key_env)
    else:
        client = OpenRouterClient(a.model)

    out = ROOT / 'results' / f'{a.split}-agent-{name}'
    out.mkdir(parents=True, exist_ok=True)
    partial = out / 'traces.partial.json'  # saved after every question; rerun the same command to resume
    traces = json.loads(partial.read_text(encoding='utf-8')) if partial.exists() else []
    done = {t['query_id'] for t in traces if t['status'] != 'error'}
    traces = [t for t in traces if t['query_id'] in done]  # errored questions are retried
    cases = [{'id': q['id'], 'split': a.split, 'answerable': ok_} for q, ok_ in items]
    if done:
        print(f'resuming: {len(done)} questions already done', flush=True)
    for n, (q, answerable) in enumerate(items, start=1):
        if q['id'] in done:
            continue
        print(f'[{n}/{len(items)}] {q["id"]} ...', flush=True)
        base = {'query_id': q['id'], 'question': q['question'], 'answerable': answerable}
        try:  # only the question text reaches the agent
            t = run_agent(q['question'], retriever, client, a.top_k, a.max_searches, a.budget_tokens * 4, a.force_first_search)
        except Exception as e:  # recorded as an error, never replaced by a fake result
            traces.append({**base, 'status': 'error', 'error': str(e), 'events': [], 'citations': []})
            print(q['id'], 'ERROR', str(e)[:120], flush=True)
            partial.write_text(json.dumps(traces, ensure_ascii=False, indent=1), encoding='utf-8')
            continue
        if answerable:
            t['context_hit'] = any(hit(c, q['gold']) for c in chunks if c['id'] in t['context_ids'])
        traces.append({**base, **t})
        print(q['id'], t['status'], f"searches={t['searches']}", f"cites={len(t['citations'])}", f"ctx_hit={t.get('context_hit')}", f"{t['total_ms'] / 1000:.1f}s", flush=True)
        partial.write_text(json.dumps(traces, ensure_ascii=False, indent=1), encoding='utf-8')

    ok = [t for t in traces if t['status'] != 'error']
    A = [t for t in ok if t['answerable']]
    X = [t for t in ok if not t['answerable']]
    cites = [c for t in ok for c in t['citations']]
    summary = {
        'name': name, 'split': a.split, 'model': a.model, 'top_k': a.top_k, 'max_searches': a.max_searches,
        'budget_tokens_est': a.budget_tokens, 'n': len(traces), 'errors': len(traces) - len(ok),
        'answerable_n': len(A), 'absent_n': len(X),
        'tool_use': f"{sum(t['searches'] > 0 for t in ok)}/{len(ok)}",
        'search_count_distribution': {str(k): sum(t['searches'] == k for t in ok) for k in sorted({t['searches'] for t in ok})},
        'auto_context_hit': f"{sum(t['context_hit'] for t in A)}/{len(A)}",
        'abstained_when_answerable': f"{sum(t['status'] == 'abstain' for t in A)}/{len(A)}",
        'abstained_when_absent': f"{sum(t['status'] == 'abstain' for t in X)}/{len(X)}",
        'answered_with_citation': f"{sum(bool(t['citations']) for t in ok if t['status'] == 'answered')}/{sum(t['status'] == 'answered' for t in ok)}",
        'citations_in_context': f"{sum(len(t['citations_in_context']) for t in ok)}/{len(cites)}",
        'tokens': {k: sum(t['usage'][k] for t in ok) for k in ('prompt', 'output', 'thoughts', 'llm_calls')},
        'cost_usd': None if any(t['usage']['cost_usd'] is None for t in ok) else round(sum(t['usage']['cost_usd'] for t in ok), 5),
        'provider': a.provider,
        'median_total_ms': round(statistics.median(t['total_ms'] for t in ok)) if ok else None,
        'note': 'auto_* fields are machine checks, NOT the manual grades required by BENCHMARK.md',
    }
    order = {q['id']: i for i, (q, _) in enumerate(items)}
    traces.sort(key=lambda t: order[t['query_id']])
    for fn, obj in (('traces.json', traces), ('cases.json', cases), ('summary.json', summary)):
        (out / fn).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    gold = {q['id']: q for q, ok_ in items if ok_}
    lines = [f'# Review sheet {a.split} / {name}\n', 'Grade each: grounded answer 0-2, each citation supports (T/F), abstention correct (T/F), context 0-2.\n']
    for t in traces:
        lines.append(f"## {t['query_id']} ({'answerable' if t['answerable'] else 'ABSENT'}) - {t['status']}\n**Q:** {t['question']}\n")
        if t['answerable']:
            lines.append(f"**Expected:** {gold[t['query_id']]['expected_answer']}\n")
        lines.append(f"**Answer:** {t.get('answer', t.get('error'))}\n\n**Queries:** {[e['query'] for e in t['events']]}\n**Citations:** {t['citations']}\n")
    (out / 'review.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
