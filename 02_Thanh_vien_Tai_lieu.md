# Thành viên 2 — Tìm tài liệu và kiểm tra cơ sở khoa học

## Thông tin

- Họ tên: **Lê Hưng**
- Mã sinh viên: [Chờ bổ sung]
- Đội trưởng: Lưu Quang Khải — 2A202602599
- Chủ đề: T1 — Camera degradation health score
- Thiết kế chung: [BENCHMARK_DESIGN.md](docs/BENCHMARK_DESIGN.md); [File đội trưởng](01_LuuQuangKhai_2A202602599.md).

## Nhiệm vụ

**Phạm vi báo cáo đang thực hiện:** demo nhỏ S01 clean + motion blur s1/s2/s5; nguồn phương pháp/dữ liệu giữ nguyên. Phân biệt kết quả mới bốn clip với số paper và kết quả 24 clip lịch sử; không đưa kết luận ngày/đêm hay underexposure vào phần nhóm đo mới.

1. Đọc hai nguồn đã chọn: *Safety-Critical Camera Reliability Monitoring…* (arXiv:2605.05439v1) và *DRIVE-C* (arXiv:2605.09774v1).
2. Hoàn thiện `PAPER_CODE_MAPPING.md`: vai trò từng nguồn, health head trực tiếp so với công thức GSHI, beta/clipping, loss, taxonomy và phiên bản code thực sự chạy.
3. Giải thích metric đo điều gì, điều gì không thể kết luận từ metric đó.
4. Gửi thành viên 3 cách tính/thiết lập liên quan; gửi thành viên 4 nội dung trích dẫn và giới hạn.

Từ khóa tham khảo: `camera image quality assessment autonomous driving`, `blur detection`, `image corruption autonomous driving`.

## Bảng đọc nguồn

| Paper/repository và URL/đường dẫn | Tác giả, năm, phiên bản | Phương pháp/dữ liệu liên quan | Bằng chứng hỗ trợ claim nào? | Giới hạn khi áp dụng vào LAB |
| --- | --- | --- | --- | --- |
| [Điền] | [Điền] | [Điền] | [Điền] | [Điền] |
| [Điền] | [Điền] | [Điền] | [Điền] | [Điền] |

## Phiếu giải thích metric

- Tên metric: [Điền]
- Công thức và nguồn: [Điền]
- Tiền xử lý bắt buộc: [Điền]
- Đơn vị/thang giá trị: [Điền]
- Chiều thay đổi dự đoán khi blur tăng: [Điền]
- Metric là proxy cho: [Điền]
- Failure case của chính metric: [Điền; ví dụ cảnh ít texture]
- Những kết luận chưa được phép suy ra: [Điền]

## Đầu ra và bàn giao

Giai đoạn 4 đã soạn [bản báo cáo riêng của Hưng](reports/LeHung.md). Cần bổ sung MSSV, rà trích dẫn/đối chiếu triển khai và ghi đóng góp thực tế trước khi nộp. Phần nói của Hưng nằm trong [PITCH.md](reports/PITCH.md).

**Giai đoạn 2 đã có đầu ra chung:** [PAPER_CODE_MAPPING.md](reports/PAPER_CODE_MAPPING.md). Lê Hưng phụ trách rà và sử dụng nội dung/trích dẫn khi viết bản riêng. File ghi nguồn là công việc hỗ trợ đã thực hiện trong repository, không tự gán toàn bộ đóng góp này cho cá nhân trước khi người đó xác nhận.

- **Trước phút 45:** Bảng paper–code và cách tính metric đủ để người chạy dùng đúng nguồn.
- **Trước phút 95:** Kiểm tra cách nhóm diễn giải bảng kết quả và limitation.
- **Trước phút 115:** Trích dẫn/Method hoàn chỉnh cho báo cáo, hoàn thiện bản riêng.
- File ghi chú/commit: [Điền]
- Vấn đề cần đội trưởng quyết định: [Điền]

## Checklist

- [ ] Đã đọc nguồn, ghi đường dẫn và phiên bản/năm.
- [ ] Không coi kết quả trong paper là kết quả nhóm đã chạy.
- [ ] Nêu khác biệt giữa dữ liệu/phương pháp của nguồn và benchmark LAB.
- [ ] Nêu ít nhất một giới hạn của metric hoặc nguồn.
- [ ] Đã bàn giao cho thành viên 3 và 4.
- [ ] Chuẩn bị bản nộp riêng trên VLearn.

## Nhật ký đóng góp cá nhân

| Thời điểm | Việc đã làm | File/commit/bằng chứng | Kết quả hoặc vấn đề |
| --- | --- | --- | --- |
| [Điền] | [Điền] | [Điền] | [Điền] |
