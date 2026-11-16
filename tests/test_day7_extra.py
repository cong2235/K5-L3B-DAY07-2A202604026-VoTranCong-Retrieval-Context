"""Offline tests for the Day 7 retrieval fusion/rerank logic and the agent loop (fake model and retriever; no network).
These check the code only; they are NOT benchmark results."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'starter'))
from src.agent import ABSTAIN, parse_answer, run_agent  # noqa: E402
from src.retrieval import HybridRetriever, RerankRetriever, _rank  # noqa: E402


def chunk(i, text='x', page=1):
    return {'id': i, 'text': text, 'source_id': 's', 'source': 's', 'page': page, 'metadata': {'section': '1'}}


class Fixed:
    """Retriever returning a fixed ranking."""

    def __init__(self, ids):
        self.ids = ids

    def search(self, question, top_k=3, filters=None):
        return _rank([{**chunk(i), 'score': 1.0 / (n + 1)} for n, i in enumerate(self.ids[:top_k])], 'fixed')


class FakeCross:
    def __init__(self, scores):
        self.scores = scores

    def predict(self, pairs, show_progress_bar=False):
        return [self.scores[c] for _, c in pairs]


def reranker(base, scores, fuse):
    r = object.__new__(RerankRetriever)   # skip loading a real cross-encoder
    r.base, r.candidates, r.model_name, r.fuse, r.rrf_k = base, 10, 'fake', fuse, 60
    r.model = type('M', (), {'predict': lambda self, pairs, show_progress_bar=False: [scores[c['text']] for c in pairs_map(pairs)]})()
    return r


def pairs_map(pairs):
    return [{'text': p[1]} for p in pairs]


class RetrievalTests(unittest.TestCase):
    def test_hybrid_rrf_prefers_chunks_found_by_both(self):
        h = HybridRetriever(Fixed(['a', 'b', 'c']), Fixed(['b', 'z', 'y']), candidates=3)
        self.assertEqual(h.search('q', top_k=1)[0]['id'], 'b')

    def test_hybrid_weight_changes_order(self):
        h = HybridRetriever(Fixed(['a', 'b']), Fixed(['c', 'a']), candidates=2, dense_weight=3.0)
        self.assertEqual(h.search('q', top_k=1)[0]['id'], 'a')

    def test_rerank_orders_by_cross_encoder_score(self):
        base = Fixed(['a', 'b', 'c'])
        # make chunk text equal to its id so the fake model can score it
        base.search = lambda q, top_k=3, filters=None: _rank(
            [{**chunk(i, text=i), 'score': 1.0} for i in ['a', 'b', 'c'][:top_k]], 'fixed')
        r = reranker(base, {'a': 0.1, 'b': 0.2, 'c': 0.9}, fuse=False)
        self.assertEqual([c['id'] for c in r.search('q', top_k=3)], ['c', 'b', 'a'])

    def test_rerank_fusion_keeps_top_dense_chunk(self):
        base = Fixed(['a', 'b', 'c'])
        base.search = lambda q, top_k=3, filters=None: _rank(
            [{**chunk(i, text=i), 'score': 1.0} for i in ['a', 'b', 'c'][:top_k]], 'fixed')
        # the cross-encoder wrongly puts 'a' last; fusion with the dense rank must keep it in the top 2
        r = reranker(base, {'a': 0.0, 'b': 0.5, 'c': 0.9}, fuse=True)
        self.assertIn('a', [c['id'] for c in r.search('q', top_k=2)])


class FakeClient:
    """Model stub: optionally forced to search first, then answers with a citation or abstains."""

    def __init__(self, answer, tool_first=True):
        self.answer, self.tool_first, self.calls, self.forced = answer, tool_first, 0, []

    def start(self, question):
        return []

    def step(self, state, no_tools, force_tool=False):
        self.forced.append(force_tool)
        self.calls += 1
        usage = {'prompt': 10, 'output': 5, 'thoughts': 0, 'cost_usd': None}
        if self.calls == 1 and (self.tool_first or force_tool):
            return [('id1', 'search_documents', 'my query')], '', usage, 1.0
        return [], self.answer, usage, 1.0

    def add_results(self, state, calls, shown):
        state.append(shown)


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.ret = type('R', (), {'search': lambda s, q, top_k=3, filters=None: _rank(
            [{**chunk('B:openstax-pds:p1:0', 'evidence text'), 'score': 0.9}], 'dense')})()

    def test_answer_with_valid_citation(self):
        t = run_agent('q', self.ret, FakeClient('It is X [B:openstax-pds:p1:0].'))
        self.assertEqual(t['status'], 'answered')
        self.assertEqual(t['citations_in_context'], ['B:openstax-pds:p1:0'])
        self.assertEqual(t['searches'], 1)
        self.assertEqual(t['events'][0]['type'], 'search')

    def test_citation_outside_context_is_flagged(self):
        t = run_agent('q', self.ret, FakeClient('Y [B:openstax-pds:p9:9].'))
        self.assertEqual(t['citations'], ['B:openstax-pds:p9:9'])
        self.assertEqual(t['citations_in_context'], [])

    def test_abstention_status(self):
        t = run_agent('q', self.ret, FakeClient(f'{ABSTAIN}: nothing relevant.'))
        self.assertEqual(t['status'], 'abstain')

    def test_force_first_search_flag_reaches_the_client(self):
        c = FakeClient('A [B:openstax-pds:p1:0]', tool_first=False)
        t = run_agent('q', self.ret, c, force_first_search=True)
        self.assertEqual(c.forced[0], True)
        self.assertEqual(t['searches'], 1)
        c2 = FakeClient('A', tool_first=False)
        self.assertEqual(run_agent('q', self.ret, c2)['searches'], 0)   # without forcing, the stub skips the tool

    def test_context_budget_blocks_extra_chunks(self):
        t = run_agent('q', self.ret, FakeClient('ok'), budget_chars=3)
        self.assertEqual(t['context_ids'], [])


class ParseTests(unittest.TestCase):
    ctx = ['B:openstax-pds:p1:0', 'B:openstax-pds:p2:1']

    def test_leading_bracket_abstention(self):
        self.assertEqual(parse_answer('[INSUFFICIENT_EVIDENCE: nothing]', self.ctx)[0], 'abstain')
        self.assertEqual(parse_answer('INSUFFICIENT_Evidence: nothing', self.ctx)[0], 'abstain')
        self.assertEqual(parse_answer('It is X.', self.ctx)[0], 'answered')

    def test_garbled_citation_is_recorded_as_invalid(self):
        st, cited, valid = parse_answer('Yes [B:openst:openstax-pds:p98:0] and [B:openstax-pds:p1:0].', self.ctx)
        self.assertEqual(cited, ['B:openst:openstax-pds:p98:0', 'B:openstax-pds:p1:0'])
        self.assertEqual(valid, ['B:openstax-pds:p1:0'])

    def test_multiple_ids_in_one_bracket(self):
        _, cited, valid = parse_answer('Z [B:openstax-pds:p1:0, B:openstax-pds:p2:1]', self.ctx)
        self.assertEqual(valid, self.ctx)


if __name__ == '__main__':
    unittest.main()
