# Hướng dẫn chạy lại (phần cơ bản)

Python 3.11+, Docker Desktop, các gói: `psycopg[binary]`, `sentence-transformers`, `numpy`, `pymupdf` (chỉ cho phần nâng cao).
Key và địa chỉ model nằm trong `.env` (không commit; mẫu ở `.env.example`).

1. **Pgvector và dữ liệu Day 6** (repo Day 6 đặt cạnh repo này): `docker compose up -d` trong `starter/` của Day 6, rồi
   `python scripts/ingest_pgvector.py --day6 <repo Day 6>` (340 chunk chiến lược B, e5-small 384 chiều).
2. **Dữ liệu Day 7:** `python scripts/build_heldout.py` (13 câu held-out) rồi
   `python scripts/export_day6.py --day6 <repo Day 6> --output data/day6_raw` và
   `python starter/convert_day6.py --chunks data/day6_raw/chunks.json --questions data/day6_raw/questions.json --output data/converted`.
   Câu thiếu bằng chứng: `data/absent_questions.json`.
3. **Retrieval (không cần model ngoài):** `python scripts/run_retrieval.py --method dense|tfidf|hybrid|rerank [--fuse] --split dev --top-k 5 --budget-tokens 2400`
   (kết quả `results/<split>-<tên>/`, bảng `results/comparison.md`; mặc định split là dev).
4. **Agent:** chạy notebook `notebooks/kaggle_llm_server.ipynb` trên Kaggle (GPU T4 x2, Internet bật, secret `SERVER_API_KEY`), đặt cùng giá trị vào `.env`
   dưới tên `KAGGLE_LLM_API_KEY`, rồi
   `python scripts/run_agent.py --split dev --force-first-search --base-url <tunnel>/v1 --key-env KAGGLE_LLM_API_KEY --model qwen2.5-7b-instruct`
   (kết quả `results/<split>-agent-*/` gồm `traces.json`, `cases.json`, `summary.json`, `review.md` để chấm tay).
5. **Test:** chỉ chạy `--split test` sau khi đã chốt cấu hình trong `results/selection.md`; kiểm thử code: `python -m unittest discover -s tests -v`.
6. Trên Windows đặt `PYTHONUTF8=1`. Phần nâng cao (IEA Global EV Outlook 2025): xem `adv/PROGRESS.md`, `adv/SOURCE.md`.
