# Thành viên 1 — Đội trưởng và tổng hợp quyết định kỹ thuật

## Thông tin

- Họ tên: **Lưu Quang Khải**
- Mã sinh viên: **2A202602599**
- Chủ đề: **T1 — Camera degradation health score**
- Vai trò: Chốt phạm vi, điều phối, kiểm tra bằng chứng và tổng hợp báo cáo.
- Quy mô thực tế: **4 thành viên**. Hướng dẫn LAB yêu cầu đúng 5 người; ghi nhận khác biệt này và trao đổi với giảng viên.
- Repository chung: [Điền URL]

## Thiết kế thử nghiệm chung — chốt trong phút 0–15

Các giá trị bên dưới là đề xuất ban đầu, có thể cập nhật theo dữ liệu/code nhóm đang có. Sau khi chốt, cả nhóm dùng cùng cấu hình.

| Nội dung | Thiết kế / thông tin cần điền |
| --- | --- |
| Nền tảng | Xe ADAS |
| Tính năng | Giám sát chất lượng ảnh đầu vào cho nhận diện đối tượng |
| Sensor | Camera |
| Failure case | Ảnh nhòe do mô phỏng Gaussian blur; chưa đại diện cho mọi dạng nhòe thực tế |
| Claim ban đầu | Khi mức Gaussian blur tăng, variance of Laplacian dự kiến giảm trên cùng ảnh gốc; đây là proxy độ sắc nét, chưa chứng minh chất lượng detector giảm |
| Metric chính | Variance of Laplacian trên ảnh grayscale; phương sai đáp ứng Laplacian, không phải đại lượng vật lý |
| Quy ước tính | [Chốt thư viện, grayscale, dtype, thang pixel, resize và tham số Laplacian] |
| Baseline | Ảnh gốc, không thêm corruption; áp dụng cùng tiền xử lý và metric |
| Điều kiện lỗi | 3–5 mức blur; [điền kernel/sigma cụ thể], chỉ thay đổi blur |
| Dữ liệu | [Nguồn, danh sách ảnh/frame, số lượng, giấy phép nếu có] |
| Tổng hợp | Đo từng ảnh ở mọi mức; báo cáo trung bình và độ phân tán, kèm ví dụ ngoại lệ |
| Health score | [Công thức, khoảng giá trị và cách chuẩn hóa]; nếu chưa xây dựng thì báo cáo metric thô và nêu rõ |
| Metric bổ sung | [Tùy chọn: saturation ratio, entropy hoặc detector confidence; ghi công thức/đơn vị] |

## Phân công nhóm 4 người

| Thành viên | Phụ trách chính | Đầu ra |
| --- | --- | --- |
| Lưu Quang Khải — 2A202602599 | Điều phối, thiết kế thử nghiệm, quyết định kỹ thuật | Bảng chốt thiết kế, báo cáo tổng hợp và đề xuất |
| [Thành viên 2] | Paper/repository và giới hạn nguồn | Bảng nguồn, claim được hỗ trợ, giới hạn áp dụng |
| [Thành viên 3] | Code, corruption và chạy benchmark | Code/notebook, cấu hình, lệnh chạy và log |
| [Thành viên 4] | Kiểm tra benchmark, plot và trình bày | Bảng kết quả, hình minh chứng, slide/kịch bản |

## Mốc phối hợp trong 120 phút

- **0–15:** Chốt thiết kế, điền tên/MSSV và phân công.
- **15–35:** Thành viên 2 đọc nguồn; thành viên 3 chạy thử; thành viên 4 chuẩn bị bảng kết quả; đội trưởng kiểm tra phạm vi.
- **35–80:** Chạy benchmark, lưu bằng chứng, đối chiếu metric và ghi failure case.
- **80–105:** Tổng hợp kết quả, giới hạn và đề xuất cải tiến.
- **105–120:** Kiểm tra sản phẩm, tập trình bày 3–5 phút và chuẩn bị bản nộp riêng.

## Quyết định kỹ thuật sau khi có kết quả

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
