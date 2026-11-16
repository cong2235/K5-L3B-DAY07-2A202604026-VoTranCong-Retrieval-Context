# Tiêu chí chọn cấu hình và cấu hình đã chốt (viết TRƯỚC khi chạy test held-out)

Ngày chốt: 2026-11-16. Dev = 30 câu có đáp án (D01-D15, T01-T05, S01-S10 từ Day 6) + 3 câu thiếu bằng chứng (X-D01..03).
Test = 13 câu held-out (H01-H13) + 3 câu thiếu bằng chứng (X-T01..03). Chưa chạy test với bất kỳ cấu hình nào tại thời điểm này.

## Tiêu chí (theo thứ tự ưu tiên)
1. Context Evidence Rate trên dev (đủ evidence trong context cuối gửi model).
2. Nếu hòa: Evidence Hit@3 trên dev.
3. Nếu vẫn hòa: chọn cấu hình rẻ và nhanh hơn. Ngoại lệ: chấp nhận thêm tối đa 10 giây mỗi lần tìm nếu Hit@3 tăng >= 2 câu trên dev.
4. Với agent: chọn chế độ gọi tool theo kết quả dev của A0 so với A1 (tool use, context hit, từ chối oan, citation ngoài context).

## Cấu hình đã chốt
- Baseline (để so sánh trên test): dense k=3, budget 800 ký tự, agent tool_choice=auto.
- Chọn (C1): retrieval = rerank + RRF với dense (BAAI/bge-reranker-base, 20 ứng viên, RRF k=60), top-5, context budget 2400 token ước lượng
  (9600 ký tự), agent ép gọi search ở lượt đầu (--force-first-search), tối đa 4 lần tìm, model qwen2.5-7b-instruct (AWQ) trên Kaggle.
- Lý do: dense k5 và rerank+RRF k5 hòa Context (29/30); rerank+RRF có Hit@3 28/30 so với 26/30 (+2 câu, đúng ngoại lệ ở tiêu chí 3, chi phí khoảng 5 giây mỗi lần tìm);
  A1 hơn A0 ở mọi chỉ số chất lượng (tool use 33/33 so với 22/33; context 28/30 so với 20/30; từ chối oan 1/30 so với 8/30; citation ngoài context 0 so với 2) với giá thời gian x2.1.
- Quy tắc dự phòng đặt trước: nếu khi chạy agent trên dev với rerank+RRF mà context hit tự động thấp hơn agent + dense k5 (28/30) thì dùng dense k5 thay thế. Sau khi chạy test không đổi cấu hình nào.

## Giới hạn đã biết
- Agent + rerank chưa được chạy trên dev tại thời điểm chốt (cần Kaggle); quy tắc dự phòng ở trên xử lý việc này.
- 30 câu dev nhỏ nên dễ overfit; 15 câu dev là câu T/S đã bị xem ở Day 6.
- 6 câu thiếu bằng chứng và 13 câu held-out do AI soạn nháp, người dùng chưa đối chiếu với sách.
