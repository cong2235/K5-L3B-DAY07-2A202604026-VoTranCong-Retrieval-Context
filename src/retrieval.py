"""Retrieval methods for Day 7: dense (pgvector, Day 6 index), lexical (TF-IDF) and hybrid (RRF).

Every retriever returns chunks (id, text, source_id, source, page, metadata) plus `score`, `rank`
and `method`, so results can be traced and compared. Errors propagate: no mock fallback.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'starter'))
from baseline import TfidfIndex  # noqa: E402

DEFAULT_URL = 'postgresql://day6:day6_local_only@127.0.0.1:55433/day6_lab'  # local-only Docker credentials
FILTERABLE = {'chapter', 'section'}


def _rank(results, method):
    return [{**c, 'rank': i, 'method': method} for i, c in enumerate(results, start=1)]


def _passes(chunk, filters):
    return all(chunk['metadata'].get(k) == v for k, v in (filters or {}).items())


class DenseRetriever:
    """Exact cosine search in the Day 6 pgvector table (strategy 'B'), same e5 model as the index."""

    def __init__(self, chunks, database_url=DEFAULT_URL, strategy='B', model='intfloat/multilingual-e5-small'):
        import psycopg
        from sentence_transformers import SentenceTransformer
        self.by_chunk_id = {c['id']: c for c in chunks}
        self.strategy = strategy
        self.conn = psycopg.connect(database_url)  # fails loudly if the database is down
        self.model_name = model
        self.model = SentenceTransformer(model, device='cpu')

    def embed_query(self, question):
        return self.model.encode([f'query: {question}'], normalize_embeddings=True, show_progress_bar=False)[0].tolist()

    def search(self, question, top_k=3, filters=None):
        bad = set(filters or {}) - FILTERABLE
        if bad:
            raise ValueError(f'unsupported filter keys: {bad}')
        vec = '[' + ','.join(f'{x:.7f}' for x in self.embed_query(question)) + ']'
        where, params = ['strategy = %s'], [self.strategy]
        for key, value in (filters or {}).items():  # whitelisted column names only
            where.append(f'{key} = %s')
            params.append(value)
        sql = (f"SELECT chunk_id, 1 - (embedding <=> %s::vector) FROM chunks WHERE {' AND '.join(where)} "
               'ORDER BY embedding <=> %s::vector LIMIT %s')
        rows = self.conn.execute(sql, [vec, *params, vec, top_k]).fetchall()
        return _rank([{**self.by_chunk_id[cid], 'score': float(s)} for cid, s in rows], 'dense')


class LexicalRetriever:
    def __init__(self, chunks):
        self.index = TfidfIndex(chunks)

    def search(self, question, top_k=3, filters=None):
        if filters:  # post-filter on a larger candidate list
            found = [c for c in self.index.search(question, top_k=len(self.index.chunks)) if _passes(c, filters)]
            return _rank(found[:top_k], 'tfidf')
        return _rank(self.index.search(question, top_k=top_k), 'tfidf')


class HybridRetriever:
    """Reciprocal Rank Fusion of dense and lexical rankings: score = sum 1 / (k + rank). Rank-based, so
    the incomparable dense (cosine) and TF-IDF scales never need normalising."""

    def __init__(self, dense, lexical, candidates=20, rrf_k=60, dense_weight=1.0, lexical_weight=1.0):
        self.dense, self.lexical, self.candidates, self.rrf_k = dense, lexical, candidates, rrf_k
        self.weights = (dense_weight, lexical_weight)

    def search(self, question, top_k=3, filters=None):
        fused, by_id = {}, {}
        for retriever, weight in zip((self.dense, self.lexical), self.weights):
            for c in retriever.search(question, top_k=self.candidates, filters=filters):
                fused[c['id']] = fused.get(c['id'], 0.0) + weight / (self.rrf_k + c['rank'])
                by_id[c['id']] = c
        order = sorted(fused, key=lambda i: (-fused[i], i))[:top_k]
        return _rank([{**{k: v for k, v in by_id[i].items() if k not in ('rank', 'method')}, 'score': fused[i]}
                      for i in order], 'hybrid-rrf')


class RerankRetriever:
    """Retrieve `candidates` chunks with a base retriever, then re-order them with a cross-encoder (runs on CPU).
    The cross-encoder reads (query, chunk) together, so it can fix ranking errors of the bi-encoder; it never adds chunks."""

    def __init__(self, base, model_name='BAAI/bge-reranker-base', candidates=20, fuse=False, rrf_k=60):
        from sentence_transformers import CrossEncoder
        self.base, self.candidates, self.model_name = base, candidates, model_name
        self.fuse, self.rrf_k = fuse, rrf_k   # fuse: RRF of the base rank and the cross-encoder rank (guards against reranker errors)
        self.model = CrossEncoder(model_name, device='cpu', max_length=512)

    def search(self, question, top_k=3, filters=None):
        cands = self.base.search(question, top_k=self.candidates, filters=filters)
        if not cands:
            return []
        scores = self.model.predict([(question, c['text']) for c in cands], show_progress_bar=False)
        by_score = sorted(range(len(cands)), key=lambda i: (-float(scores[i]), i))
        if self.fuse:
            rr = {i: pos for pos, i in enumerate(by_score, start=1)}
            fused = {i: 1.0 / (self.rrf_k + rr[i]) + 1.0 / (self.rrf_k + cands[i]['rank']) for i in range(len(cands))}
            order = sorted(fused, key=lambda i: (-fused[i], i))[:top_k]
            score = lambda i: fused[i]
        else:
            order = by_score[:top_k]
            score = lambda i: float(scores[i])
        return _rank([{**{k: v for k, v in cands[i].items() if k not in ('rank', 'method')},
                       'score': score(i), 'base_rank': cands[i]['rank'], 'rerank_score': float(scores[i])} for i in order],
                     'rerank-rrf' if self.fuse else 'rerank')
