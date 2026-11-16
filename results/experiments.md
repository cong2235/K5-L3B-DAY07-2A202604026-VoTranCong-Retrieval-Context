# Nhật ký thí nghiệm dev (giả thuyết ghi TRƯỚC khi chạy)

Cửa sổ làm việc giả định 4k–6k token; context = 60% => ~2400–3600 token (ước lượng chars/4 => 9600–14400 ký tự).
Budget 800 ký tự của starter là baseline (chưa tối ưu). Chỉ chạy **dev**; test chưa chạy.

| ID | Cấu hình | Giả thuyết |
|---|---|---|
| E0 | dense/tfidf/hybrid, k=3, 800 ký tự | Baseline starter. Context Rate thấp hơn Hit@3 vì 800 ký tự chỉ vừa ~1 chunk. |
| E1 | k=3, 2400 token | Đủ chỗ cho cả 3 chunk => Context Rate = Hit@3 (không thêm Hit@3). |
| E2 | k=5, 2400 token | D08/D15 có chunk đúng ở hạng 5 => Context Rate tăng, Hit@3 giữ nguyên; chi phí token tăng. |
| E3 | k=8, 3600 token | Thêm nhiễu, lợi ích giảm dần so với k=5. |
| E4 | hybrid dense-weight 2, k=3 | RRF không trọng số làm mất D07 (dense hạng 1, tfidf hạng 44); trọng số dense cao cứu D07 mà không làm hỏng D15. |

## Kết quả dev (n=15; chi tiết trong results/comparison.md)
| ID | Kết quả | Kết luận |
|---|---|---|
| E0 | Context 9/15 (cả 3 phương pháp), Hit@3 13/15 | Baseline. |
| E1 | Context 13/15 = Hit@3 | **Giả thuyết đúng**: budget 800 ký tự là điểm nghẽn, không phải ranking. |
| E2 | dense Context 15/15 (k=5), tfidf 14/15, hybrid 14/15; Hit@3 không đổi | Đúng: D08/D15 được cứu bởi top-5. Dense k=5 tốt nhất, ~3.3k ký tự (~820 token). |
| E3 | k=8 không tăng so với dense k=5 (15/15) nhưng ~5.3k ký tự | Đúng: lợi ích giảm dần, tốn token hơn. |
| E4 | hybrid dense-weight 2: không đổi (vẫn trượt D07, D08 ở Hit@3) | **Giả thuyết sai**: chunk có mặt ở cả hai ranking (p86:3) vẫn vượt chunk chỉ dense hạng 1. Hybrid chưa hơn dense. |
Giới hạn: n=15, chọn cấu hình trên dev dễ overfit; D08 vẫn chỉ ở hạng 5 (Hit@3 chưa sửa).

# Agent (dev, 30 câu có đáp án + 3 thiếu bằng chứng; qwen2.5-7b-instruct AWQ trên Kaggle, dense k=5, ~2400 token)
| ID | Cấu hình | Giả thuyết / kết quả |
|---|---|---|
| A0 | tool_choice=auto (baseline) | Kết quả: tool use 22/33; 11 câu không search (8 từ chối oan, 2 trả lời từ trí nhớ kèm citation bịa D10/D12); auto context hit 20/30; 0 lỗi hệ thống; 5,8 s/câu. |
| A1 | --force-first-search (tool_choice=required ở lượt 1) | Giả thuyết (ghi TRƯỚC khi chạy): tool use lên 33/33, auto context hit tiến gần retrieval-only (~dense k=5), từ chối oan và citation bịa giảm. Rủi ro: câu thiếu bằng chứng bị trả lời nhiều hơn vì luôn có passage. |

## Kết quả A0 vs A1 (dev, máy chấm `auto_*`, CHƯA phải nhãn chấm tay)
| Chỉ số | A0 auto | A1 force-first-search |
|---|---|---|
| Tool use | 22/33 | **33/33** (32 câu 1 lượt, 1 câu 2 lượt) |
| Context chứa evidence (30 câu có đáp án) | 20/30 | **28/30** (trượt S04, S05) |
| Từ chối câu có đáp án | 8/30 | **1/30** (S05) |
| Từ chối câu thiếu bằng chứng | 2/3 | 2/3 (X-D02 vẫn bị trả lời, trích p144:1) |
| Citation nằm trong context | 29/31 (D10, D12 bịa ID) | **41/41** |
| Câu trả lời có citation | 23/23 | 29/30 |
| Thời gian trung vị / câu | 5.8 s | 12.3 s |
| Token prompt / output / lời gọi | 40.4k / 2.6k / 55 | 56.2k / 3.2k / 67 |
| Lỗi hệ thống | 0 | 0 |
Kết luận sơ bộ: giả thuyết A1 đúng; chi phí là thời gian ~2.1x và token prompt ~1.4x (nguyên nhân chậm chưa kiểm chứng).
Việc còn lại: chấm tay (answer 0-2, citation support, abstention); X-D02 cần đọc p144 xem có hỗ trợ khẳng định CLT không;
S04/S05 là lỗi retrieval (truy vấn do model viết lại), cần đọc top-5.

## Qwen2.5-VL-7B-Instruct-AWQ trên Kaggle (advanced), kiểm tra tool calling (2026-11-16)
| tool_choice | Kết quả |
|---|---|
| auto | Không gọi tool; trả lời từ trí nhớ bằng văn bản thường (finish=stop). |
| required | Gọi đúng search_documents(query="MCAR missing data"). |
Kết luận: với Qwen2.5-VL phải dùng --force-first-search; đọc ảnh hoạt động (đọc đúng "4242" ở fp16 trên T4).

# Chạy lại trên dev 30 câu (15 dev cũ + 15 test/test2 của Day 6; bản dev 15 câu lưu ở results/archive-dev15)
| Cấu hình | Hit@1 | Hit@3 | Hit@k | Context |
|---|---|---|---|---|
| tfidf k3 800 ký tự | 19/30 | 25/30 | 25/30 | 13/30 |
| dense k3 800 ký tự | 20/30 | 26/30 | 26/30 | 14/30 |
| hybrid k3 800 ký tự | 20/30 | 26/30 | 26/30 | 13/30 |
| dense k3 2400 token | 20/30 | 26/30 | 26/30 | 26/30 |
| dense k5 2400 token | 20/30 | 26/30 | 29/30 | 29/30 |
| hybrid k5 2400 token | 20/30 | 26/30 | 29/30 | 29/30 |
| tfidf k5 2400 token | 19/30 | 25/30 | 27/30 | 27/30 |
Dense trượt Hit@3 ở D08, D15, T01, S04; hybrid trượt D07, D08, T01, T04. Kết luận: giống dev 15 câu (budget là nút cổ chai context; dense k5 tốt nhất; hybrid chưa hơn dense).

## E5 - Rerank bằng cross-encoder trên CPU (BAAI/bge-reranker-base, 20 ứng viên từ dense)
Giả thuyết (ghi TRƯỚC khi chạy): các lỗi Hit@3 của dense (D08, D15, T01, S04) là lỗi xếp hạng (chunk đúng ở hạng 4-5 trong ứng viên), nên rerank sẽ đưa
chúng lên top-3: Hit@3 tăng từ 26/30; Hit@k (k=5) khó tăng vì tập ứng viên không đổi; chi phí: thêm vài trăm ms/câu trên CPU.

## E5 kết quả (dev 30, rerank bge-reranker-base trên 20 ứng viên dense)
| | Hit@1 | Hit@3 | Hit@5 | Context k5 | trung vị |
|---|---|---|---|---|---|
| dense k5 | 20 | 26 | 29 | 29 | 33 ms |
| rerank k5 | 24 | 27 | 27 | 27 | 9.6 s |
Giả thuyết đúng MỘT PHẦN: sửa D08, D15, T01 (hạng 5 -> 1-2); Hit@1 +4. Nhưng mất D04 và D09 (dense xếp hạng 2 và 1): reranker tổng quát chấm 0.98 cho đoạn "gán ngẫu nhiên nhóm tập thể dục" (p75, hạng dense 12) thay vì đoạn cluster sampling, và chọn đoạn về độ lệch chuẩn thay vì đoạn "range chỉ dùng min và max". Nguyên nhân: cross-encoder chưa điều chỉnh miền, nhầm chủ đề gần nghĩa.

## E6 - Rerank + RRF với thứ hạng dense (giả thuyết ghi TRƯỚC khi chạy)
Hợp nhất rank dense và rank reranker bằng RRF sẽ giữ D04 và D09 (dense hạng 2 và 1) và vẫn giữ lợi ích D08/D15/T01: Hit@3 >= 28/30, context k5 >= 29/30. Chi phí thời gian giống E5 (~9.6 s/câu).

## E6 kết quả (dev 30)
| | Hit@1 | Hit@3 | Hit@5 | Context k5 | trung vị | p90 |
|---|---|---|---|---|---|---|
| dense k5 | 20 | 26 | 29 | 29 | 33 ms | 39 ms |
| rerank k5 | 24 | 27 | 27 | 27 | 9.6 s | 14.0 s |
| rerank + RRF k5 | 20 | **28** | 29 | 29 | 5.4 s | 7.4 s |
Giả thuyết E6 ĐÚNG (Hit@3 >= 28, context >= 29). Còn trượt Hit@3: D09 (dense hạng 1, rerank kéo xuống), S04 (dense hạng 8, tfidf hạng 1: dense chọn đoạn liệt kê chung về outlier ở p87).
Lỗi đã phân tích (>= 2): D08/D15/T01 (xếp hạng, rerank sửa), D04/D09 (rerank gây lỗi, RRF giữ lại D04), S04 (dense hụt, lexical đúng).
Giới hạn: n=30, chọn trên dev dễ overfit; các câu T/S đã bị xem ở Day 6 nên chỉ dùng làm dev.

## Test held-out (13 câu H01-H13) - retrieval + context, cấu hình đã chốt trong results/selection.md (chạy sau khi chốt, không chỉnh lại)
| Cấu hình | Hit@1 | Hit@3 | Context | trung vị |
|---|---|---|---|---|
| baseline dense k3, 800 ký tự | 8/13 | 13/13 | 7/13 | 41 ms |
| chọn: rerank+RRF k5, 2400 token | 8/13 | 13/13 | 13/13 | 4.8 s |
| tham chiếu dense k5, 2400 token | 8/13 | 13/13 | 13/13 | - |
Nhận xét: retrieval chạm trần ở Hit@3 nên lợi ích chỉ đến từ budget context; rerank không thêm lợi ích so với dense k5 trên test này (chỉ có ở dev, +2 câu Hit@3). n=13 nhỏ.

## A2 - agent với retrieval rerank+RRF (cấu hình C1 đã chốt) trên dev
Giả thuyết/quy tắc đặt trước (results/selection.md): C1 = A1 + rerank+RRF k5. Nếu context hit tự động trên dev < 28/30 (A1 + dense k5) thì dùng dense k5.

## A2 kết quả (dev, máy chấm auto_*, chưa phải nhãn chấm tay)
| Chỉ số | A0 auto, dense k5 | A1 force, dense k5 | **C1 force, rerank+RRF k5** |
|---|---|---|---|
| Tool use | 22/33 | 33/33 | 33/33 |
| Context chứa evidence | 20/30 | 28/30 | **29/30** (trượt S04) |
| Từ chối khi có đáp án | 8/30 | 1/30 | **0/30** |
| Từ chối khi thiếu bằng chứng | 2/3 | 2/3 | 2/3 (X-D02 vẫn bị trả lời) |
| Câu trả lời có citation | 23/23 | 29/30 | 31/31 |
| Citation nằm trong context | 29/31 | 41/41 | 39/39 |
| Trung vị / câu | 5.8 s | 12.3 s | 13.0 s |
| Token prompt / output / lời gọi | 40.4k / 2.6k / 55 | 56.2k / 3.2k / 67 | 56.0k / 3.2k / 67 |
| Lỗi hệ thống | 0 | 0 | 0 |
Quy tắc đặt trước (context hit C1 >= 28/30) thỏa mãn -> giữ C1. Tiếp theo: chạy test một lần cho baseline và C1 (không chỉnh sau đó).

## Test held-out - agent (một lần chạy mỗi cấu hình, máy kiểm auto_*; chưa chấm tay), 13 có đáp án + 3 thiếu bằng chứng
| Chỉ số | Baseline (dense k3, 800 ký tự, auto) | Chọn C1 (ép search + rerank+RRF k5, 2400 token) |
|---|---|---|
| Tool use | 9/16 | 16/16 |
| Context chứa evidence | 3/13 | 13/13 |
| Từ chối nhầm câu có đáp án | 5/13 | 0/13 |
| Từ chối câu thiếu bằng chứng | 3/3 (nhưng không tìm kiếm ở một số câu) | 2/3 (X-T02 bị trả lời) |
| Citation trong context | 5/8 | 15/15 |
| Trung vị | 5.2 s | 10.7 s |
| Lỗi hệ thống | 0 | 0 |
Bảng chấm tay: results/test-grading-sheet.md.

## Test held-out - sau khi chấm (nhãn do trợ lý soạn nháp từ văn bản sách trong corpus; cần sinh viên xác nhận) - results/test-review/
| Chỉ số | Baseline | C1 (chọn) |
|---|---|---|
| Tool use | 9/16 | 16/16 |
| Grounded answer 0/1/2 (13 câu có đáp án) | 8 / 1 / 4, TB 0,69/2 | 0 / 1 / 12, TB 1,92/2 |
| Citation hợp lệ (hỗ trợ + trong context) | 3/10 | 12/15 |
| Câu trả lời có citation | 7/7 (3 ID viết sai) | 13/14 |
| Abstention đúng (3 câu thiếu bằng chứng) | 3/3 (X-T02 không tìm kiếm) | 2/3 |
| Từ chối nhầm (câu có đáp án) | 6/13 | 0/13 |
| Context 0/1/2 | 8 / 1 / 4 | 0 / 0 / 13 |
Đính chính trạng thái: baseline H05 là từ chối (bộ phân tích cũ xếp nhầm); ID citation sai (H07, H12) tính là citation không hợp lệ.
