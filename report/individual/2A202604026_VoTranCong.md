# Báo cáo Day 7 - Võ Trần Công (2A202604026, L3B)

> Trạng thái (2026-11-16): phần cơ bản đã có số liệu thật (dev, test, nhãn chấm). Còn thiếu trước khi nộp: (1) sinh viên đối chiếu và xác nhận nhãn chấm test và 19 câu do AI soạn (6 câu thiếu bằng chứng, 13 câu held-out) với sách gốc; (2) phiên bản vLLM của lần chạy text trên Kaggle. Phần nâng cao chưa hoàn thành nên mục tương ứng ghi **CHƯA CÓ**.

## Dữ liệu và benchmark

- **Nguồn, quyền, số trang, số chunk:** OpenStax *Principles of Data Science*, chương 2 và 3, trang PDF vật lý 68-103 và 114-148 (71 trang, 191.779 ký tự), giấy phép CC BY-NC-SA 4.0 (dùng giáo dục phi thương mại, ghi nguồn); URL và snapshot trong `starter/data/manifest.json` của repo Day 6. 340 chunk chiến lược B (theo đoạn/câu, tối đa 800 ký tự, không vượt trang hoặc heading).
- **Vector store, embedding:** PostgreSQL + pgvector (Docker `pgvector/pgvector:0.8.7-pg16`), tìm cosine chính xác (không ANN); `intfloat/multilingual-e5-small`, 384 chiều, chạy CPU, tiền tố `query:`/`passage:`. Nạp bằng `scripts/ingest_pgvector.py`, dữ liệu chuyển bằng `scripts/export_day6.py` và `starter/convert_day6.py`.
- **Agent model, cách chạy, dev/test:** `Qwen2.5-7B-Instruct-AWQ` phục vụ bằng vLLM trên Kaggle (2 GPU T4) qua tunnel Cloudflare, API tương thích OpenAI, tool calling (notebook `notebooks/kaggle_llm_server.ipynb`, phiên bản vLLM ghi trong lần chạy: **CHƯA CÓ phiên bản của lần chạy text**). Dev = 30 câu có đáp án (D01-D15 và 15 câu T01-T05, S01-S10; 15 câu này là test cũ của Day 6 đã bị xem nên chỉ dùng làm dev) + 3 câu thiếu bằng chứng. Test = 13 câu held-out H01-H13 (trang gold không trùng trang gold của dev, viết sau khi chia split, chưa dùng để chỉnh) + 3 câu thiếu bằng chứng.
- **Xác định câu có/thiếu evidence, tiêu chí chấm:** câu có đáp án: evidence là chuỗi con chính xác trong một chunk của đúng trang (`scripts/export_day6.py`, `scripts/build_heldout.py` kiểm tra). Câu thiếu bằng chứng: chủ đề gần nhưng các từ khóa chính không xuất hiện trong corpus (`data/absent_questions.json`, trường `absence_check`); 6 câu này và 13 câu held-out do trợ lý AI soạn nháp; **CHƯA CÓ: sinh viên đối chiếu với sách gốc** (đã kiểm bằng máy rằng evidence nằm trọn trong một chunk và từ khóa của câu thiếu bằng chứng không có trong corpus). Chấm theo BENCHMARK.md (context 0/1/2, grounded answer 0/1/2, citation, abstention): **nhãn trên test do trợ lý soạn nháp từ việc đọc văn bản sách trong corpus (`scripts/make_reviews.py`, lý do từng câu trong `results/test-review/reviews_*.json`); CHƯA CÓ: sinh viên xác nhận lại từng nhãn.**

## Retrieval và thử nghiệm

Dev = 30 câu. Chi phí dịch vụ: 0 USD (chạy cục bộ). Nhật ký giả thuyết: `results/experiments.md`; bảng đầy đủ: `results/comparison.md`.

| Cấu hình | Phương pháp, top-k, filter, rerank, context budget | Giả thuyết / thay đổi | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Thời gian trung vị |
|---|---|---|---|---|---|---|---|
| Baseline | dense (pgvector), k=3, không filter, 800 ký tự | điểm xuất phát của starter | dev | 20/30 | 26/30 | 14/30 | 35 ms |
| Phương pháp 2 | TF-IDF (lexical), k=3, 800 ký tự | lexical bắt từ khóa nhưng không hiểu diễn đạt lại | dev | 19/30 | 25/30 | 13/30 | 2,9 ms |
| Phương pháp 3 | hybrid dense + TF-IDF, RRF (k=60), k=3, 800 ký tự | hợp nhất hai thứ hạng | dev | 20/30 | 26/30 | 13/30 | 43 ms |
| Cải thiện 1 | dense, k=3 rồi k=5, budget 2400 token ước lượng (~9600 ký tự) | 800 ký tự chỉ vừa khoảng 1 chunk nên làm mất evidence trong context | dev | 20/30 | 26/30 | 26/30 (k=3), **29/30** (k=5) | 32-33 ms |
| Cải thiện 2 | dense 20 ứng viên + rerank cross-encoder `BAAI/bge-reranker-base` (CPU), k=5 | sửa lỗi xếp hạng (chunk đúng ở hạng 4-5) | dev | 24/30 | 27/30 | 27/30 | 9,6 s |
| Cải thiện 3 | rerank + RRF với thứ hạng dense, k=5, 2400 token | giữ lại câu mà reranker làm hỏng | dev | 20/30 | **28/30** | 29/30 | 5,4 s |
| **Cấu hình đã chọn** | = Cải thiện 3 (xem `results/selection.md`, chốt trước khi chạy test) | | test (13) | 8/13 | 13/13 | **13/13** | 4,8 s |
| Baseline | = baseline dev | | test (13) | 8/13 | 13/13 | 7/13 | 41 ms |

Tham chiếu test: dense k=5, 2400 token cũng đạt Hit@3 13/13 và Context 13/13. Hybrid không hơn dense (hybrid có trọng số dense x2 cũng không đổi kết quả, `results/archive-dev15`).

**Hai lỗi dev, nguyên nhân, cách thử:**
1. *D08 ("What problem does the trimmed mean address?"), D15, T01*: chunk đúng ở hạng 5 của dense (lỗi xếp hạng, không phải thiếu chunk). Thử rerank: chunk lên hạng 1-2, Hit@1 tăng 20 lên 24. Nhưng rerank làm mất D04 ("How is a cluster sample selected?", reranker cho 0,98 điểm đoạn gán ngẫu nhiên nhóm tập thể dục) và D09 (chọn đoạn độ lệch chuẩn thay vì "range chỉ dùng min và max") vì reranker tổng quát nhầm chủ đề gần nghĩa; context giảm từ 29 xuống 27. Thử hợp nhất RRF với thứ hạng dense: Hit@3 lên 28/30, context 29/30; còn D09 và S04.
2. *S04 ("Should outliers be handled before or after validating the data?")*: dense xếp chunk đúng ở hạng 8 (chọn danh sách xử lý outlier chung ở trang 87), TF-IDF xếp hạng 1; mọi cấu hình dense và rerank đều trượt Hit@3.

**Lý do chọn:** tiêu chí xếp thứ tự ưu tiên (context, rồi Hit@3, rồi chi phí; ngoại lệ chấp nhận thêm tối đa 10 s nếu Hit@3 tăng >= 2 câu) đặt trước khi chạy test (`results/selection.md`). Rerank+RRF hòa context với dense k=5 nhưng hơn 2 câu Hit@3 trên dev, nên được chọn. **Trên test lợi thế này không xuất hiện** (cả hai 13/13); cấu hình tốt hơn baseline chỉ nhờ budget context (7/13 lên 13/13). n nhỏ (30 dev, 13 test) nên mọi chênh lệch nhỏ có thể là ngẫu nhiên.

## Agent và đánh giá

- **Tool, lượt gọi, điều kiện dừng, context, lỗi:** một tool `search_documents(query)` (dense k=5, hoặc cấu hình chọn); tối đa 4 lần tìm, sau đó bắt buộc trả lời; context gom các chunk chưa trùng cho tới hết ngân sách 2400 token ước lượng; trả lời kèm `[chunk-id]` hoặc `INSUFFICIENT_EVIDENCE: ...`. Lỗi HTTP 429/5xx thử lại có chờ, lỗi còn lại ghi `status: error` (không thay bằng kết quả giả). Cấu hình A1 ép gọi search ở lượt đầu (`--force-first-search`).

Kết quả **do máy tính** trên dev (30 có đáp án + 3 thiếu bằng chứng, `results/dev-agent-*`); chưa phải nhãn chấm tay:

| Cấu hình / split | Tool use | Số lượt gọi (phân bố) | Grounded answer 0/1/2 và TB | Citation trong context | Câu có citation | Abstention đúng (thiếu bằng chứng) | Từ chối nhầm (có đáp án) |
|---|---|---|---|---|---|---|---|
| A0 tool_choice=auto, dev | 22/33 | 0: 11, 1: 22 | không chấm tay (chỉ chấm test) | 29/31 | 23/23 | 2/3 (tự động; cần xác nhận tay) | 8/30 |
| A1 ép search lượt đầu, dev | 33/33 | 1: 32, 2: 1 | không chấm tay (chỉ chấm test) | 41/41 | 29/30 | 2/3 (tự động; cần xác nhận tay) | 1/30 |
| C1 = A1 + rerank+RRF, dev | 33/33 | 1: 33 | không chấm tay | 39/39 (máy) | 31/31 | 2/3 (máy) | 0/30 |
| **C1 (chọn), test** | **16/16** | 1: 16 | 0/1/12, TB **1,92**/2 | **12/15** | 13/14 | 2/3 | **0/13** |
| Baseline (dense k=3, 800 ký tự, auto), test | 9/16 | 0: 7, 1: 9 | 8/1/4, TB **0,69**/2 | 3/10 | 7/7 (3 ID viết sai) | 3/3 (X-T02 từ chối mà không tìm kiếm) | 6/13 |

Context chứa evidence (máy kiểm): A0 20/30, A1 28/30. Thời gian trung vị: A0 5,8 s, A1 12,3 s; token prompt 40,4k so với 56,2k. Lỗi hệ thống: 0 ở cả hai lần chạy. Nhận xét: model 7B ở chế độ `auto` thường không gọi tool (11/33 câu): 8 câu từ chối với lý do "passages do not provide" khi chưa tìm, 2 câu trả lời từ trí nhớ kèm citation bịa (D10, D12); ép gọi search ở lượt đầu loại bỏ các lỗi này với giá thời gian gấp 2,1 lần.

**Context 0/1/2 (chấm trên cả 13 câu test có đáp án):** C1 = 13 câu mức 2 (trung bình 2,00); baseline = 8 câu mức 0, 1 câu mức 1 (H04: thiếu ý hiệu chỉnh xác suất), 4 câu mức 2 (trung bình 0,69). Chỉ số tự động (chunk gold có trong context của agent): C1 13/13, baseline 3/13 (H07, H09, H12); nhãn tay của baseline cao hơn một câu (4 câu mức 2) vì H06 có đoạn thay thế hợp lệ p86:1 trong context dù chunk gold p84 vắng. Con số 7/13 ở bảng retrieval là lần chạy retrieval thuần (top-3, 800 ký tự), không phải context của agent.

Ví dụ từng câu (C1, test; đầy đủ 16 câu trong `results/test-grading-sheet.md` và `results/test-review/`):

| Query ID | Loại | Tool call và kết quả | Câu trả lời và citation | Nhãn, lý do |
|---|---|---|---|---|
| H09 | có đáp án | search "home price example upper bound outliers", top-5 có p128:0 | Cận trên 1.159.375 và 5.500.000 vượt cận nên là ngoại lệ [p128:0] | grounded 2; citation đúng; context 2 |
| H10 | có đáp án | search "z-score home sale mean standard deviation" | z = -2, thấp hơn trung bình 2 độ lệch chuẩn [p129:0] | grounded 2; citation đúng; ký hiệu công thức bị mất trong text layer |
| H13 | có đáp án | search "normal curve probability employee salary" | Diện tích bên phải $68.000 [p145:0]; dùng norm.cdf rồi lấy 1 trừ [p148:1] | grounded 2; cả hai citation đúng |
| H05 | có đáp án | search "Poisson distribution used to find the probability of" | Đếm số lần xảy ra trong một khoảng; ví dụ quầy thanh toán và tai nạn giao lộ [p142:1] | grounded 2; citation SAI chunk (ví dụ tai nạn ở p142:0) |
| H06 | có đáp án | search "data cleaning process" | Làm sạch gồm bỏ trùng lặp, xử lý thiếu, sửa định dạng, "cũng gồm" tích hợp và biến đổi [p86:2] | grounded **1**: sai khi gộp tích hợp và biến đổi vào làm sạch (các bước riêng); citation sai |
| X-T01 | thiếu bằng chứng | search "chi-square test of independence" | INSUFFICIENT_EVIDENCE, không thêm khẳng định | abstention đúng |
| X-T02 | thiếu bằng chứng | search "Selenium JavaScript web pages scraping" | Giải thích Selenium bằng kiến thức ngoài sách, không citation, rồi nói passages không nêu | abstention **sai** (khẳng định vô căn cứ) |

Lỗi chung đã tìm thấy: (1) ở chế độ `auto`, baseline không gọi search ở 7/16 câu (6 câu từ chối nhầm, 1 câu trả lời với citation bịa p95:1 không có trong context); (2) model 7B đôi khi viết sai ID citation (baseline H07, H12); (3) hai lỗi trong bộ phân tích câu trả lời của chính tôi (câu bắt đầu bằng `[INSUFFICIENT_EVIDENCE` bị xếp nhầm là "answered"; ID citation sai bị bỏ qua) đã sửa trong `src/agent.py` (`parse_answer`, có test) và tính lại trạng thái và citation từ câu trả lời đã lưu (`scripts/make_reviews.py`); trace gốc không bị sửa.

- **Đường dẫn, lệnh, thời gian, chi phí:** `results/` (traces.json, summary.json, review.md trong từng thư mục `*-agent-*`); `python scripts/run_agent.py --split dev --force-first-search --base-url <tunnel>/v1 --key-env KAGGLE_LLM_API_KEY --model qwen2.5-7b-instruct`; retrieval: `python scripts/run_retrieval.py --method rerank --fuse --split test --top-k 5 --budget-tokens 2400`. Chi phí 0 USD (Kaggle miễn phí, CPU cục bộ).
- **Trước/sau, đánh đổi, giới hạn:** xem mục trên. Giới hạn: n nhỏ; 15 câu dev là câu đã bị xem ở Day 6; agent chạy bằng model 7B lượng tử hóa; chưa chấm tay; câu thiếu bằng chứng và held-out chưa được đối chiếu với sách; hai bộ dữ liệu cùng một cuốn sách nên topic giữa dev và test liên quan nhau.

## Thử thách nâng cao (đang thực hiện, chưa hoàn thành)

- **Tài liệu:** IEA *Global EV Outlook 2025*, 173 trang, CC BY 4.0, mã băm SHA-256 và URL trong `adv/SOURCE.md`.
- **Xử lý:** text layer; 91 phần tử bảng/hình cắt ảnh (`scripts/adv_crops.py`, vùng bbox và ảnh cắt được giữ); mô tả bằng Qwen2.5-VL-7B-AWQ (`scripts/adv_caption_elements.py`) có đối chiếu thủ công mẫu: bảng số in sẵn chính xác, giá trị biểu đồ **không** đáng tin; số liệu biểu đồ cột và đường dựng lại từ hình học vector (`scripts/adv_charts.py`): 33/66 hình trích được, 2 hình đã kiểm chứng tay; index 796 chunk trong pgvector (`scripts/adv_index.py`). Phần chưa xử lý và lý do: `adv/PROGRESS.md`.
- **Benchmark, model, cấu hình đã chốt trên dev, kết quả test theo nhóm, trace, nhãn:** **CHƯA CÓ** (chưa soạn benchmark, chưa chạy). Bonus chỉ được cộng khi test đạt ít nhất 90% (27/30); chưa có bằng chứng nên **chưa đề nghị tính điểm bonus**.

| Nhóm test | Đạt / tổng | Tỷ lệ | Lỗi / nhận xét |
|---|---|---|---|
| Bảng | CHƯA CÓ | | |
| Ảnh, sơ đồ | CHƯA CÓ | | |
| Biểu đồ | CHƯA CÓ | | |
| Multi-hop | CHƯA CÓ | | |
| Text | CHƯA CÓ | | |
| Thiếu bằng chứng | CHƯA CÓ | | |
| **Toàn bộ** | CHƯA CÓ | | |

- **Giới hạn, tái lập:** `adv/PROGRESS.md`, `adv/SOURCE.md`; PDF không được commit, tải lại từ URL và kiểm mã băm.
