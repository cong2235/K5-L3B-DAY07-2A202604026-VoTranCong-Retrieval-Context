# Day 7 — Agentic RAG (bài cá nhân, Võ Trần Công, 2A202604026, L3B)

Đề bài và rubric: README.md, GUIDE.md, BENCHMARK.md, RUBRIC.md, RULES.md, ADVANCED.md (bonus +15). Trả lời bằng tiếng Việt.

## Dữ liệu (tiếp nối Day 6)
- Day 6 repo: `D:\VinLearn\K5-L3B-DAY06-VoTranCong-2A202604026-DataIngestionEngineering` (chỉ đọc, không sửa).
- Corpus: OpenStax *Principles of Data Science*, chương 2–3, 71 trang (CC BY-NC-SA 4.0).
- Chiến lược chunk đã chọn: **B** (structure-aware, ≤800 ký tự, không vượt trang/heading), 340 chunk, ID dạng `B:openstax-pds:p87:1`.
- Embedding: `intfloat/multilingual-e5-small` (384 chiều, CPU, L2-normalize; tiền tố `query: ` / `passage: `).
- Vector store: PostgreSQL + pgvector (Docker, `starter/docker-compose.yml` của Day 6, cổng 55433). Docker thường đang tắt: bật Docker Desktop và kiểm tra bảng `chunks` (strategy `B`) trước khi chạy dense retrieval.
- Xuất dữ liệu: `python scripts/export_day6.py --day6 <repo Day 6> --output data/day6_raw` rồi `starter/convert_day6.py` → `data/converted/`. Evidence được viết lại thành chuỗi con chính xác của chunk (baseline so khớp chính xác).
- Câu thiếu bằng chứng: `data/absent_questions.json` (3 dev + 3 test, do AI soạn nháp, người dùng cần tự kiểm tra trong sách).
- Dev = 30 câu có đáp án (D01-D15 + T01-T05 + S01-S10: các câu T/S đã bị xem ở Day 6 nên dùng làm dev) + 3 câu thiếu bằng chứng (X-D01..03). Test = 13 câu held-out H01-H13 (data/heldout_spec.json) + 3 câu thiếu bằng chứng (X-T01..03). Cấu hình và tiêu chí chọn đã chốt trong results/selection.md trước khi chạy test.
- Phần nâng cao: IEA Global EV Outlook 2025, xem adv/PROGRESS.md.

## Quy tắc làm việc
- Chọn và chỉnh cấu hình chỉ bằng **dev**; chốt tiêu chí trước khi chạy **test**. Không đưa gold vào agent/retrieval/query.
- Không dùng mock hay vector ngẫu nhiên để báo kết quả; lỗi kết nối phải báo, không thay bằng kết quả giả.
- Không ghi `.env`, API key, token vào repo. Kiểm tra quyền trước khi gửi dữ liệu lên dịch vụ ngoài.
- Không bịa số liệu; báo cả kết quả không cải thiện. Citation phải được đọc đối chiếu, không chỉ kiểm ID.
- Chỉ commit khi người dùng yêu cầu.

## Lệnh
- Test: `python -m unittest discover -s tests -v`
- Baseline: `python starter/baseline.py --chunks data/converted/chunks.json --questions data/converted/questions.json --split dev --output starter/results/dev-tfidf`
- Trên Windows đặt `PYTHONUTF8=1` để tránh lỗi in tiếng Việt.

## Kế hoạch
Dense (pgvector) + TF-IDF baseline + hybrid (RRF), sau đó rerank / parent-child như cấu hình cải thiện; agent dùng model thật; Hit@1, Evidence Hit@3, Context Evidence Rate, chấm tay theo BENCHMARK.md. Bonus (tài liệu ≥100 trang, test ≥30 câu, ≥90%) làm sau cùng nếu còn thời gian.
