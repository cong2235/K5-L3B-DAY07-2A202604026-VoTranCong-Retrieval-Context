"""Index Day 6 strategy-B chunks into the Day 6 pgvector database (read-only use of the Day 6 code).

Usage: python scripts/ingest_pgvector.py --day6 <Day 6 repo> [--database-url ...]
Chunk IDs, embedding model and schema are identical to Day 6; the table is only (re)filled for strategy 'B'.
"""
import argparse
import sys
import time
from pathlib import Path

DEFAULT_URL = 'postgresql://day6:day6_local_only@127.0.0.1:55433/day6_lab'  # local-only Docker credentials


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--day6', required=True, type=Path)
    ap.add_argument('--database-url', default=DEFAULT_URL)
    a = ap.parse_args()
    starter = a.day6 / 'starter'
    sys.path.insert(0, str(starter))
    from src.chunking import by_paragraph
    from src.embeddings import MyEmbedder
    from src.ingestion import load_corpus
    from src.store import PgVectorStore

    pages = load_corpus(starter / 'data' / 'corpus_pages.jsonl')
    chunks = [c for p in pages for c in by_paragraph(p, 800)]
    t0 = time.time()
    emb = MyEmbedder()
    vectors = emb.embed_documents([c.text for c in chunks])
    store = PgVectorStore(a.database_url, emb.dimensions)
    store.create_schema()
    store.upsert('B', chunks, vectors)
    print(f"model={emb.model_name} dims={emb.dimensions} chunks={store.count('B')} seconds={time.time() - t0:.1f}")


if __name__ == '__main__':
    main()
