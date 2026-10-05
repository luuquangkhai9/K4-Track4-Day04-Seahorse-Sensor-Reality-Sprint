# Thành viên 3 — Code và chạy benchmark

## Thông tin

- Họ tên: **Đặng ĐỈnh Đoàn**
- Mã sinh viên: [Chờ bổ sung]
- Đội trưởng: Lưu Quang Khải — 2A202602599
- Chủ đề: T1 — Camera degradation health score
- Thiết kế chung: [BENCHMARK_DESIGN.md](docs/BENCHMARK_DESIGN.md); [File đội trưởng](01_LuuQuangKhai_2A202602599.md).
- Cấu hình đối chiếu: [configs/benchmark.json](configs/benchmark.json), chưa tự tích hợp vào notebook.

## Nhiệm vụ

**Ưu tiên hiện tại theo yêu cầu thu nhỏ:** chạy [stage3_small_demo.py](scripts/stage3_small_demo.py) với [benchmark_small.json](configs/benchmark_small.json), chỉ bốn clip S01 clean + motion blur s1/s2/s5. Phần kế hoạch 24 clip dưới đây là lịch sử; không bắt buộc thực hiện mới. Bàn giao CSV 4 dòng/32 frame, log, manifest, bốn ảnh frame54 và hai hình tổng hợp.

1. Kiểm tra notebook/code và dữ liệu có sẵn; tái sử dụng phần phù hợp với thiết kế đã chốt.
2. Dùng 24 clip DRIVE-C đã chọn: clean và biến thể motion blur/underexposure ở 5 mức từ cùng cảnh; không thêm corruption lần hai.
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
| Mức lỗi | Motion blur kernel 11/13/19/27/33 px; underexposure delta_ev −0,16/−0,36/−0,70/−1,10/−1,50 |
| Cách tính Laplacian và variance | [Điền tham số] |
| Seed nếu có ngẫu nhiên | [Điền hoặc không áp dụng] |
| Công thức health score nếu có | [Điền hoặc chưa triển khai] |
| Lệnh/các cell để chạy | [Điền] |
| Vị trí log, CSV, ảnh | [Điền] |

## Định dạng kết quả đề xuất

Giữ schema `phn_24_results.csv` và `phn_per_frame.csv` hiện có, dùng `sample_id` để nối dữ liệu. Lưu thêm manifest/log thực tế; không làm tròn health trước khi kiểm tra tái hiện. Tham số corruption nằm trong cột `param`.

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

Giai đoạn 4 đã soạn [bản báo cáo riêng của Đoàn](reports/DangDinhDoan.md). Cần bổ sung MSSV, rà khả năng chạy lại/provenance và ghi đóng góp thực tế trước nộp. Phần nói của Đoàn nằm trong [PITCH.md](reports/PITCH.md).

**Giai đoạn 2 đã có bằng chứng chạy CPU:** [báo cáo](docs/STAGE2_REPORT.md), [script](scripts/stage2_smoke_test.py), [manifest](outputs/stage2/run_manifest.json). Baseline thật S01 clean đạt ngưỡng tái hiện. Đặng ĐỈnh Đoàn dùng đường chạy này cho bước tiếp theo; chưa chạy mới đủ 24 clip ở giai đoạn 2. Không tự gán lần chạy hỗ trợ này vào nhật ký đóng góp cá nhân nếu chưa thực hiện/kiểm tra.

- **Trước phút 45:** Môi trường/dữ liệu sẵn sàng, baseline smoke test chạy được.
- **Trước phút 75:** Hoàn thành benchmark, lưu code/cấu hình/log/CSV/ảnh.
- **Trước phút 95:** Giải quyết sai lệch do Nam phát hiện; bàn giao gói bằng chứng.
- **Trước phút 115:** Hoàn thiện hướng dẫn chạy và bản riêng.
- File/commit bàn giao: [Điền]
- Lỗi còn tồn tại và ảnh hưởng tới kết quả: [Điền]
- Chuẩn bị bản nộp riêng trên VLearn: [Trạng thái]

## Nhật ký đóng góp cá nhân

| Thời điểm | Việc đã làm | File/commit/bằng chứng | Kết quả hoặc vấn đề |
| --- | --- | --- | --- |
| [Điền] | [Điền] | [Điền] | [Điền] |
