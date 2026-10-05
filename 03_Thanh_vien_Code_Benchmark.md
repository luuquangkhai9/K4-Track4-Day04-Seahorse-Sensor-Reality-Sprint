# Thành viên 3 — Code và chạy benchmark

## Thông tin

- Họ tên: [Điền]
- Mã sinh viên: [Điền]
- Đội trưởng: Lưu Quang Khải — 2A202602599
- Chủ đề: T1 — Camera degradation health score
- Thiết kế chung: [File đội trưởng](01_Luu_Quang_Khai_Doi_truong.md)

## Nhiệm vụ

1. Kiểm tra notebook/code và dữ liệu có sẵn; tái sử dụng phần phù hợp với thiết kế đã chốt.
2. Tạo baseline và 3–5 mức degradation từ cùng ảnh/frame gốc.
3. Giữ nguyên tiền xử lý và cách tính metric giữa các điều kiện; ghi mọi tham số.
4. Chạy benchmark, lưu metric từng ảnh/frame, log và ảnh minh chứng.
5. Bàn giao dữ liệu cùng hướng dẫn chạy lại cho thành viên 4.

## Cấu hình chạy có thể tái lập

| Mục | Giá trị thực tế |
| --- | --- |
| Code/notebook và commit | [Điền] |
| Môi trường, Python, thư viện | [Điền phiên bản] |
| Nguồn và danh sách ảnh/frame | [Điền] |
| Số ảnh/frame, tiêu chí chọn | [Điền] |
| Kích thước, grayscale, dtype, thang pixel | [Điền] |
| Baseline | [Điền] |
| Các mức blur: kernel/sigma | [Điền 3–5 mức] |
| Cách tính Laplacian và variance | [Điền tham số] |
| Seed nếu có ngẫu nhiên | [Điền hoặc không áp dụng] |
| Công thức health score nếu có | [Điền hoặc chưa triển khai] |
| Lệnh/các cell để chạy | [Điền] |
| Vị trí log, CSV, ảnh | [Điền] |

## Định dạng kết quả đề xuất

CSV tối thiểu: `image_id, condition, blur_kernel, blur_sigma, blur_score`.

Nếu có health score hoặc metric bổ sung, thêm cột và ghi rõ công thức. Không điền số giả cho kết quả chưa chạy.

## Kiểm tra trước khi bàn giao

- [ ] Mọi mức lỗi dùng cùng danh sách ảnh với baseline.
- [ ] Các cấu hình chỉ khác tham số corruption đã chốt.
- [ ] Baseline thực sự không thêm corruption.
- [ ] Log ghi số mẫu chạy thành công/thất bại và nguyên nhân.
- [ ] CSV không thiếu ID, điều kiện hoặc giá trị metric mà không giải thích.
- [ ] Có ảnh baseline và degraded của cùng một mẫu.
- [ ] Người khác có thể chạy lại theo hướng dẫn.

## Mốc và đầu ra

- **Trước phút 35:** Chạy thử được baseline và một mức lỗi.
- **Trước phút 80:** Hoàn thành benchmark, lưu code/cấu hình/log/CSV/ảnh.
- **Trước phút 105:** Giải quyết sai lệch hoặc lỗi do thành viên 4 phát hiện.
- File/commit bàn giao: [Điền]
- Lỗi còn tồn tại và ảnh hưởng tới kết quả: [Điền]
- Chuẩn bị bản nộp riêng trên VLearn: [Trạng thái]

## Nhật ký đóng góp cá nhân

| Thời điểm | Việc đã làm | File/commit/bằng chứng | Kết quả hoặc vấn đề |
| --- | --- | --- | --- |
| [Điền] | [Điền] | [Điền] | [Điền] |
