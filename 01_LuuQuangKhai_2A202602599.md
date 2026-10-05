# Thành viên 1 — Đội trưởng và tổng hợp quyết định kỹ thuật

## Thông tin

- Họ tên: **Lưu Quang Khải**
- Mã sinh viên: **2A202602599**
- Chủ đề: **T1 — Camera degradation health score**
- Vai trò: Chốt phạm vi, điều phối, kiểm tra bằng chứng và tổng hợp báo cáo.
- Quy mô thực tế: **4 thành viên**, đã được giảng viên chấp thuận theo thông tin đội trưởng cung cấp.
- Repository chung: <https://github.com/luuquangkhai9/K4-Track4-Day04-Seahorse-Sensor-Reality-Sprint>
- Danh sách nhóm: [TEAMMATES.md](TEAMMATES.md).
- Thiết kế chi tiết: [BENCHMARK_DESIGN.md](docs/BENCHMARK_DESIGN.md); cấu hình đối chiếu: [benchmark.json](configs/benchmark.json).

## Thiết kế thử nghiệm chung — chốt trong phút 0–15

**Phạm vi hiện tại sau yêu cầu thu nhỏ giai đoạn 3:** bốn clip S01 clean + motion blur s1/s2/s5, kernel 11/13/33 px; 32 health/frame, metric thủ công ở frame 54. Ưu tiên kết quả mới trong `outputs/stage3_small/`. Phần thiết kế 24 clip bên dưới giữ làm lịch sử; không yêu cầu chạy mới underexposure/S06 hoặc các mức blur khác.

Thiết kế đã được ghi cụ thể ở giai đoạn 1, dựa trên notebook và kết quả đã lưu. Lần chạy tiếp theo kiểm tra tái hiện; chưa phải inference mới ở bước chuẩn bị này.

| Nội dung | Thiết kế / thông tin cần điền |
| --- | --- |
| Nền tảng | Xe ADAS |
| Tính năng | Giám sát chất lượng ảnh đầu vào cho nhận diện đối tượng |
| Sensor | Camera |
| Failure case | Motion blur; bổ sung underexposure trên DRIVE-C; health có thể không phản ánh nhất quán mức lỗi |
| Claim ban đầu | Motion blur tăng → variance of Laplacian và health dự kiến giảm trên cùng cảnh/frame; kết quả đã có ngoại lệ, cần kiểm tra lại |
| Metric chính | Variance of Laplacian trên ảnh grayscale; phương sai đáp ứng Laplacian, không phải đại lượng vật lý |
| Quy ước tính | Frame 54 gốc 1280 × 720, RGB → gray uint8; Laplacian CV_64F, ksize=1, variance ddof=0 |
| Baseline | Clean cùng scenario/frame; cùng tiền xử lý và metric |
| Điều kiện lỗi | Motion blur kernel 11/13/19/27/33 px; underexposure delta_ev −0,16/−0,36/−0,70/−1,10/−1,50; chạy riêng từng loại |
| Dữ liệu | DRIVE-C: S01/S06 clean và hai loại lỗi × 5 mức, thêm S07/S08 clean; 24 clip |
| Tổng hợp | Tách cảnh/loại lỗi; bảng frame 54; mean 8 frame cho health clip; kiểm tra đơn điệu s1–s5 riêng clean → s1 |
| Health score | `pred_health` trực tiếp của PerceptionHealthNet, thang 0–1; không thay thế bằng nhãn gshi_gt |
| Metric bổ sung | S_pct: % gray ≤5 hoặc ≥250; H_bit: entropy histogram 256 bin, bit; chưa đo detector |

## Phân công nhóm 4 người

| Thành viên | Phụ trách chính | Đầu ra |
| --- | --- | --- |
| Lưu Quang Khải — 2A202602599 | Điều phối, thiết kế thử nghiệm, quyết định kỹ thuật | Bảng chốt thiết kế, báo cáo tổng hợp và đề xuất |
| Lê Hưng — MSSV chờ bổ sung | Paper/repository và giới hạn nguồn | Bảng nguồn, claim được hỗ trợ, giới hạn áp dụng |
| Đặng ĐỈnh Đoàn — MSSV chờ bổ sung | Code, corruption và chạy benchmark | Code/notebook, cấu hình, lệnh chạy và log |
| Nguyễn Hồ Nam — 2A202602788 | Kiểm tra benchmark, plot và trình bày | Bảng kết quả, hình minh chứng, slide/kịch bản |

## Mốc phối hợp trong 120 phút

- **0–15:** Chốt thiết kế, điền tên/MSSV và phân công.
- **15–45:** Thành viên 2 đối chiếu hai nguồn/code; thành viên 3 setup và smoke test; Nam chuẩn bị bảng; Khải rà phạm vi.
- **45–75:** Chạy benchmark, lưu output, log và ảnh.
- **75–95:** Kiểm tra số liệu, plot và failure case; dừng thêm tính năng.
- **95–115:** Hoàn thiện quyết định kỹ thuật, README và bốn báo cáo riêng.
- **115–120:** Kiểm tra link và tập pitch 3–5 phút.

## Quyết định kỹ thuật sau khi có kết quả

Đã soạn [ENGINEERING_DECISION.md](reports/ENGINEERING_DECISION.md), [bản báo cáo riêng](reports/2A202602599_LuuQuangKhai.md) và [pitch](reports/PITCH.md). Khải rà kết luận, ghi đóng góp thực tế và kiểm tra hồ sơ trước nộp; không điền nội dung chưa làm vào nhật ký.

- Claim được hỗ trợ / không được hỗ trợ / chưa đủ bằng chứng: [Điền]
- Bằng chứng định lượng và đường dẫn: [Điền]
- Failure case quan sát được: [Điền]
- Khi nào cân nhắc giảm trọng số camera: [Điền; nếu chọn ngưỡng, giải thích cách chọn]
- Đề xuất cải tiến: [Điền]
- Trade-off: [Ví dụ: cảnh ít texture có score thấp dù ảnh rõ; ngưỡng có thể phụ thuộc cảnh/ngày đêm]
- Giới hạn: [Điền; không suy ra giảm mAP nếu chưa đo detector và nhãn]

## Checklist hoàn thành

- [ ] Nhóm thống nhất baseline, corruption và cách tính metric.
- [ ] Có ít nhất một metric, một failure case và bằng chứng đã chạy.
- [ ] Báo cáo phân biệt kết quả đo, giả thuyết và thông tin từ nguồn tham khảo.
- [ ] Có đề xuất cải tiến gắn với kết quả và trade-off.
- [ ] Đủ thông tin đóng góp của 4 người, trình bày trong 3–5 phút.
- [ ] Mỗi người chuẩn bị và nộp một bản riêng trên VLearn.

## Nhật ký đóng góp cá nhân

| Thời điểm | Việc đã làm | File/commit/bằng chứng | Kết quả hoặc vấn đề |
| --- | --- | --- | --- |
| [Điền] | [Điền] | [Điền] | [Điền] |
