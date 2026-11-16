# Advanced challenge - source document

| Field | Value |
|---|---|
| Title | Global EV Outlook 2025 (International Energy Agency) |
| Version | Published May 2025; PDF created 2025-07-30 (PDF 1.7, Adobe PDF Library 25.1.97) |
| Landing page | https://www.iea.org/reports/global-ev-outlook-2025 |
| PDF URL | https://www.iea.org/files/7ea38b60-3033-42a6-9589-71134f4229f4/GlobalEVOutlook2025.pdf |
| Licence | CC BY 4.0 (stated on the IEA report page and in the report's citation block); attribution to the IEA is required |
| Accessed | 2026-11-16 |
| Pages | 173 (physical PDF pages, 1-based; page numbering in the benchmark is the physical page) |
| File | 4,996,288 bytes; SHA-256 `7522F23A3844C6A51190D6A6B70DD348FF1CC8061B1F5D8BE2EECB25D6C20CE6` |
| Survey (scripts/adv_inspect.py) | 417,027 chars of text; 2 pages with <200 chars (cover, back page); 10 pages with embedded images; 38 pages with >=50 vector drawings (charts): 19, 21, 22, 32, 35, 37, 41, 43, 50, 52, 54, 55, 58, 62, 77, 79, 80, 101, 106, 107, 109, 110, 124, 125, 132, 136, 138, 145, 153, 157, 158, 159, 160, 161, 162, 163, 164, 171; 167 TOC entries |
| Known tool issue | PyMuPDF `find_tables()` crashes (segfault) on this PDF; tables need another extraction route |

The PDF is not committed (listed in .gitignore); reviewers re-download it from the URL above and verify the SHA-256.

## Ghi chú kiểm chứng mô tả của model thị giác (Qwen2.5-VL-7B-Instruct-AWQ, 2026-11-16)
- p160 (bảng chi phí xe tải): mọi ô số khớp ảnh gốc; model tự thêm nhãn "Table 1/2" không có trên trang; hàng tiêu đề dựng lệch.
- p22 (biểu đồ cột chồng + chấm): tiêu đề/chú giải/danh mục đúng nhưng giá trị đọc sai hoặc bịa (ví dụ Argentina, Viet Nam). Mô tả biểu đồ chỉ dùng để tìm kiếm; câu trả lời về giá trị biểu đồ phải đối chiếu ảnh trang gốc.
- Text layer có ký tự thay thế (ví dụ "T�rkiye" = Türkiye): cần chuẩn hóa khi lập chỉ mục.
