# Thiết kế benchmark — Giai đoạn 1

**Cập nhật phạm vi khi thực hiện giai đoạn 3:** Theo yêu cầu nhóm, dùng bộ nhỏ **S01 clean + motion blur s1/s2/s5**, tương ứng kernel **11/13/33 px**. Tổng **4 clip / 32 health/frame / 4 ảnh frame 54**. Ba mức lỗi, một cảnh, một loại corruption; giữ nguyên model, preprocessing và metric bên dưới. Bộ 24 clip mô tả phía dưới là thiết kế ban đầu/lịch sử, không bắt buộc chạy mới.

Cấu hình đang thực thi: [configs/benchmark_small.json](../configs/benchmark_small.json), kế thừa model/metric từ cấu hình gốc. Chạy [scripts/stage3_small_demo.py](../scripts/stage3_small_demo.py); lưu bằng chứng riêng ở `outputs/stage3_small/`. Không kiểm tra các mức s3/s4, underexposure hoặc ảnh đêm trong demo mới. Monotonicity chỉ xét **các mức đã chọn s1/s2/s5**, báo riêng clean → s1.

**Đã chạy bộ nhỏ thành công:** [STAGE3_REPORT.md](STAGE3_REPORT.md). Metadata blur thay nhiều tham số PSF cùng severity, không chỉ kernel; xem report khi diễn giải đối chứng.

**Ngày lập:** 05/10/2026 (Asia/Bangkok).  
**Trạng thái giai đoạn 1:** Đã chuẩn bị phạm vi, cấu hình và phân công đủ bốn người. Giai đoạn 1 chưa chạy inference; baseline mới đã chạy ở giai đoạn 2, xem [STAGE2_REPORT.md](STAGE2_REPORT.md).

## Bảng chốt trước khi chạy

| Nội dung | Thiết kế |
| --- | --- |
| Chủ đề/nền tảng | T1; xe ADAS |
| Sensor/tính năng | Camera RGB phía trước; giám sát chất lượng đầu vào cho nhận diện đối tượng |
| Failure case chính | Motion blur làm mất chi tiết; health dự đoán có thể phản ứng không nhất quán với mức lỗi |
| Failure bổ sung | Underexposure làm tối ảnh, thay đổi phân bố mức xám |
| Câu hỏi | Khi chỉ tăng một loại corruption trên cùng cảnh/frame, health có giảm nhất quán và đồng thuận với các metric ảnh không? |
| Claim và metric | Motion blur tăng → B = Var(Laplacian(gray)) dự kiến giảm và health trực tiếp dự kiến giảm; đo delta với clean cùng cảnh/frame. B là phương sai đáp ứng pixel, health không đơn vị trên thang 0–1 |
| Baseline | Clip clean cùng scenario, cùng frame, cùng tiền xử lý và cách tính metric; clean không đồng nghĩa chất lượng hoàn hảo |
| Thiết kế | Một loại corruption mỗi phép thử; sử dụng biến thể có sẵn của DRIVE-C |
| Nguồn phương pháp | *Safety-Critical Camera Reliability Monitoring…*, arXiv:2605.05439v1 |
| Nguồn dữ liệu/đánh giá | *DRIVE-C*, arXiv:2605.09774v1; Zenodo 19656444 |
| Phạm vi thực hiện | Inference checkpoint phát hành, đo B/S/H, đối chiếu bảng/plot/ảnh; chưa huấn luyện lại hoặc đo object detector |

Giả thuyết trên là giả thuyết gốc. Nhóm đã có kết quả lưu từ trước và đã thấy ngoại lệ; lần thực hiện tiếp theo là tái hiện/kiểm tra, không coi đây là đăng ký giả thuyết trước khi xem dữ liệu.

## Dữ liệu và cấu hình cố định

| Nhóm clip | Số lượng | Vai trò |
| --- | ---: | --- |
| S01 clean + motion_blur s1–s5 + underexposure s1–s5 | 11 | Cảnh ngày, phép so sánh có đối chứng |
| S06 clean + motion_blur s1–s5 + underexposure s1–s5 | 11 | Cảnh đêm, phép so sánh có đối chứng |
| S07 clean và S08 clean | 2 | Ví dụ bổ sung, không làm baseline cho S01/S06 |
| Tổng | 24 | 192 health/frame; 24 ảnh frame 54 cho metric thủ công |

- Severity: **0,08; 0,18; 0,35; 0,55; 0,75**, tương ứng s1–s5.
- Motion blur kernel: **11, 13, 19, 27, 33 px**. Không dùng Gaussian blur thay cho corruption này.
- Underexposure delta_ev: **−0,16; −0,36; −0,70; −1,10; −1,50**.
- Frame index (bắt đầu từ 0): **0, 18, 36, 54, 73, 91, 109, 127**. Xác minh mỗi clip có 128 frame trước khi dùng.
- Model: RGB, resize `INTER_AREA` về **H=384, W=1280**, chia 255, CHW; eval và không gradient; không ImageNet normalization.
- Metric thủ công: **frame 54**, RGB gốc **H=720, W=1280** → grayscale uint8 thang 0–255.
- Source dự kiến: tag `v1.0.1`, commit theo notebook `caf16657b87cec8518008b74c72dd0dcb6088eb6`; phải xác minh bản thực sự import ở lần chạy tiếp theo.
- Checkpoint: `epoch_021_best.pth`, SHA-256 `c210d9a4f207584687583d1ab5b96a99e12b2f3dbb2727464c6c039e44fb8c0b`.

Các giá trị có cấu trúc nằm trong [configs/benchmark.json](../configs/benchmark.json). File này là đặc tả để đối chiếu; notebook hiện chưa tự đọc nó. Người chạy phải kiểm tra cấu hình notebook khớp trước khi Run All.

## Metric và cách phân tích

| Metric | Định nghĩa | Đơn vị/chiều diễn giải |
| --- | --- | --- |
| B | `cv2.Laplacian(gray, cv2.CV_64F, ksize=1).var(ddof=0)`; border mặc định OpenCV | Phương sai đáp ứng Laplacian; dự kiến giảm khi blur tăng trên cùng ảnh, phụ thuộc texture/exposure |
| S_pct | `100 * mean((gray <= 5) OR (gray >= 250))` | % pixel ở hai đầu thang sáng; không có chiều tốt/xấu chung cho mọi cảnh |
| H_bit | `-sum(p * log2(p))` với histogram 256 bin, bỏ bin p=0 | bit; entropy mức xám, không phải độ đúng của detector |
| Health frame 54 | `pred_health` trực tiếp ở frame 54 | [0,1], không đơn vị; cao được diễn giải là khỏe hơn |
| Health clip | Trung bình số học của 8 health/frame | Cùng thang; dùng đối chiếu metadata nguồn |

1. Giữ riêng S01/S06, mỗi loại lỗi và cách tổng hợp; tính delta với clean cùng cảnh. Nếu có % thay đổi thì ghi công thức và xử lý baseline bằng 0.
2. Kiểm tra health không tăng từ s1 đến s5; báo riêng clean → s1. Làm riêng cho frame 54 và clip mean.
3. Giữ ngoại lệ; không thay metric hoặc loại mẫu vì trái dự đoán.
4. Không coi 192 frame là 192 cảnh độc lập. Không diễn giải so sánh S01/S06 như đã tách riêng tác động ngày/đêm.
5. So health clip với nguồn bằng giá trị chưa làm tròn khi có thể; ngưỡng kiểm tra notebook là `1e-3`. Khớp số chỉ chứng minh tính nhất quán tái hiện.

`gshi_gt` là nhãn từ severity; `pred_health` là output học trực tiếp. Issue probability không phải confidence của object detector. Các metric thủ công không phải phép đo vật lý trực tiếp về độ an toàn của camera.

## Phân công và bàn giao giai đoạn 2

| Người | Nhiệm vụ tiếp theo | Đầu ra |
| --- | --- | --- |
| Khải — 2A202602599 | Bổ sung hai MSSV còn thiếu, rà scope và paper–code mapping | TEAMMATES đầy đủ, scope ổn định |
| Lê Hưng — MSSV chờ bổ sung | Đối chiếu hai nguồn với đúng phiên bản code: health head, công thức beta/clipping, loss, taxonomy | `PAPER_CODE_MAPPING.md` có trang/bảng/file hỗ trợ |
| Đặng ĐỈnh Đoàn — 2A202602927 | Chọn môi trường, cài dependency thiếu, lấy 24 clip, xác minh source/checkpoint, chạy smoke test clean | Baseline chạy được, log và manifest thực tế |
| Nguyễn Hồ Nam — 2A202602788 | Chuẩn bị bảng tách theo cảnh, layout plot và ảnh failure; giữ bảng gộp ngày/đêm hiện có làm bổ sung | Khung bảng/plot, ID ảnh cần xuất, kịch bản báo cáo |

Mốc tiếp theo: **phút 15–45** hoàn thiện nguồn và đường chạy; **45–75** chạy, **75–95** kiểm tra/plot; **95–115** báo cáo; **115–120** tập pitch. Tham khảo lịch đầy đủ trong [kế hoạch](../reports/LAB_COMPLETION_PLAN.md).

## Kiểm tra sẵn sàng ở máy hiện tại

Kiểm tra này chỉ đọc artifact, tìm module và kiểm tra hash; không phải một lần inference hoặc xác nhận các thư viện đã import tương thích.

**Lưu ý trạng thái lịch sử:** Danh sách dưới đây là kiểm kê lúc giai đoạn 1. Giai đoạn 2 đã xác nhận đủ dependency, có một clip và chạy baseline CPU thành công; thông tin hiện tại nằm trong [báo cáo giai đoạn 2](STAGE2_REPORT.md).

- Python đang gọi: **3.13.15**.
- Tìm thấy module torch, torchvision, numpy, pandas, matplotlib và yaml.
- Chưa tìm thấy cv2, remotezip và requests trong Python đang gọi; giai đoạn 2 cần chuẩn bị môi trường chạy phù hợp.
- Có checkpoint **94.255.859 byte**, SHA-256 khớp giá trị notebook.
- Có 24 dòng kết quả, 24 sample ID duy nhất; 192 dòng từng frame với đúng 8 frame/clip.
- Chưa thấy video MP4 trong workspace. Hash clip hiện có không thay thế dữ liệu cần inference.
- Notebook có output đã lưu, không thấy output kiểu error; chưa xác nhận chạy lại thành công ở máy này.
- Chưa có `phn_grid.png` ở gốc; cần xuất ảnh minh chứng trong giai đoạn chạy.

## Checklist kết thúc giai đoạn 1

- [x] Phạm vi T1, sensor, tính năng và failure case cụ thể.
- [x] Claim, baseline, mức lỗi, metric/công thức/đơn vị và cách tổng hợp đã ghi rõ.
- [x] Phân công đủ bốn vai trò và đầu ra bàn giao.
- [x] Kiểm kê CSV, checkpoint, dữ liệu và môi trường cục bộ.
- [x] Nhận họ tên và phân công của Lê Hưng, Đặng ĐỈnh Đoàn.
- [ ] Nhận MSSV của Lê Hưng và Đặng ĐỈnh Đoàn.

Các mục nhân sự còn chờ không ngăn việc chuẩn bị kỹ thuật giai đoạn 2, nhưng phải hoàn thiện trước khi coi hồ sơ nộp đạt yêu cầu.
