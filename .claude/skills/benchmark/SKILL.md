---
name: benchmark
description: Chạy và ghi lại một lần đánh giá retrieval/agent Day 7 trên dev hoặc test theo BENCHMARK.md (Hit@1, Evidence Hit@3, Context Evidence Rate, thời gian, chi phí) và cập nhật bảng so sánh. Dùng khi người dùng yêu cầu chạy benchmark, so sánh cấu hình hoặc đánh giá test.
---

# Benchmark Day 7

Tham chiếu: BENCHMARK.md, GUIDE.md §4, RULES.md. Dữ liệu: `data/converted/chunks.json`, `data/converted/questions.json` (câu có đáp án), `data/absent_questions.json` (câu thiếu bằng chứng).

## Quy tắc bắt buộc
1. **Split**: mặc định chỉ chạy `dev`. Chạy `test` chỉ khi người dùng xác nhận đã chốt cấu hình và tiêu chí chọn (ghi vào `results/selection.md` trước). Nếu test đã dùng để chỉnh, dừng và báo.
2. **Không đưa gold** (`gold`, `expected_answer`, `evidence`, `absence_reason`, `absence_check`) vào agent, query hoặc retriever.
3. **Cùng điều kiện** giữa các cấu hình: cùng corpus, index, câu hỏi, nhãn. Báo query gốc; với query viết lại/multi-hop báo thêm kết quả pipeline và trace từng bước.
4. **Không giả kết quả**: lỗi model/pgvector ghi `status: "error"`, tính vào báo cáo riêng, không thay bằng mock.
5. Metric không dùng câu thiếu bằng chứng làm mẫu số retrieval.

## Quy trình
1. Xác định `config_name`, split, phương pháp (dense / tfidf / hybrid-rrf / rerank / parent-child / agent), top-k, context budget và giả thuyết. Hỏi người dùng nếu thiếu.
2. Chạy bằng script của cấu hình đó, lưu vào `results/<split>-<config_name>/` gồm `summary.json` và `traces.json` (không ghi đè cấu hình khác).
3. Tính, theo `n/N` và tỷ lệ, trên câu có đáp án:
   - **Hit@1**, **Evidence Hit@3** (cùng định nghĩa hit: chunk đúng nguồn + trang và chứa evidence; luôn xuất top-3).
   - **Context Evidence Rate**: câu có đủ evidence trong context cuối gửi model / số câu có đáp án; ghi budget, đơn vị đo, số candidate.
   - Thời gian trung vị/p90, số lượt gọi, token và chi phí.
4. Với agent: lưu model, tool call + tham số, context, câu trả lời, citation, số lượt, lỗi. Chuẩn hóa mỗi lượt retrieval thành event `search` để dùng `starter/agent_metrics.py`.
5. Cập nhật `results/comparison.md` (một dòng mỗi cấu hình: split, phương pháp, tham số, Hit@1, Hit@3, Context Rate, ms, chi phí, ghi chú).
6. Liệt kê lỗi từng câu (câu hỏi, top-3 id, loại lỗi: wrong_page / evidence cắt / filter / context thiếu) để phục vụ phân tích; nêu ít nhất 2 lỗi dev khi báo cáo.

## Phần cần người đọc (không tự động hóa)
Nhắc người dùng chấm tay: context 0/1/2 cho ≥5 câu test có đáp án (baseline và cấu hình chọn); grounded answer 0–2, citation hỗ trợ đúng/sai, abstention cho ≥5 câu có đáp án và ≥2 câu thiếu bằng chứng. Citation ID hợp lệ chưa đủ; cần đối chiếu nội dung. Chỉ tổng hợp nhãn đã chấm, không tự chấm thay.

## Đầu ra khi báo cáo
Bảng so sánh ngắn, cấu hình tốt nhất trên dev theo tiêu chí đã công bố, các lỗi chính, giới hạn (test từng bị xem ở Day 6, kích thước mẫu nhỏ) và việc còn lại cần người dùng.
