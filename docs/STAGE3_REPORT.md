# Giai đoạn 3 — Demo nhỏ xác nhận tính khả thi

**Phạm vi theo yêu cầu nhóm:** một cảnh S01, clean và **3 mức motion blur s1/s2/s5**, tổng **4 clip**. Không chạy mới bộ 24 clip. Các mức được chọn có chủ đích từ kết quả lịch sử để tái hiện baseline, mức lỗi nhẹ và failure case; không phải mẫu ngẫu nhiên để đánh giá tổng quát.

**Trạng thái:** PASS trên CPU. Có 32 output health/frame, 4 hàng metric frame54, log/manifest và ảnh trước/sau. Giữ riêng kết quả lịch sử ở gốc và kết quả mới trong `outputs/stage3_small/`.

## 1. Cấu hình và đường chạy

- Source tag `v1.0.1`, commit `caf16657b87cec8518008b74c72dd0dcb6088eb6`; tracked source không sửa.
- Checkpoint `epoch_021_best.pth`, SHA-256 đã kiểm tra đúng cấu hình.
- CPU, 4 thread, eval, `torch.inference_mode()`; batch 8 frame/clip.
- Sampling: 0/18/36/54/73/91/109/127; RGB resize H=384/W=1280, chia 255, CHW.
- B/S/H đo trên frame 54 gốc 1280 × 720, cùng công thức cho mọi điều kiện.
- Clip lấy từ DRIVE-C phát hành, CRC khi đọc ZIP và SHA-256 khớp manifest dữ liệu cũ; không tạo thêm corruption.
- Dùng [configs/benchmark_small.json](../configs/benchmark_small.json); model/metric kế thừa [cấu hình gốc](../configs/benchmark.json).

Chạy lại từ gốc:

```powershell
python scripts/stage3_small_demo.py --threads 4
```

Nếu muốn lưu riêng một lần mới: thêm `--output outputs/stage3_small_repeat`. Source/checkpoint/môi trường được chuẩn bị ở [giai đoạn 2](STAGE2_REPORT.md). Script tái sử dụng video đã cache trong `.lab_cache/`; nếu thiếu thì chỉ tải clip được chọn qua HTTP Range.

## 2. Kết quả mới [NHÓM ĐO]

| Điều kiện | Kernel (px) | B | S_pct (%) | H_bit (bit) | Health frame54 | Health mean8 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Clean | Không thêm blur | 3544,1384 | 1,6558 | 7,5152 | 0,148770 | 0,221979 |
| Motion blur s1 | 11 | 292,6951 | 1,0954 | 7,4132 | 0,275987 | 0,318326 |
| Motion blur s2 | 13 | 199,4923 | 0,9299 | 7,4035 | 0,407456 | 0,356979 |
| Motion blur s5 | 33 | 14,2645 | 0,4564 | 7,3848 | 0,076573 | 0,059943 |

CSV lưu số đầy đủ; bảng trên làm tròn để trình bày. B là phương sai đáp ứng Laplacian trên thang pixel, không phải đơn vị vật lý; S_pct gồm pixel rất tối/rất sáng. Health là nhánh dự đoán trực tiếp, không phải nhãn `gshi_gt`.

![Metric trên bốn điều kiện](../outputs/stage3_small/metric_curves.png)

![Ảnh cùng cảnh/frame với các mức blur](../outputs/stage3_small/image_grid.png)

## 3. Kiểm tra tái hiện và thời gian

Sai lệch lớn nhất giữa health mean8 và số tác giả cho bốn clip là **0,0003229279**, dưới ngưỡng cố định **0,001**. Các ID/frame và tham số được đối chiếu metadata; video đều 128 frame, 1280 × 720.

Lần chạy có đầy đủ cache, dùng để xuất artifact cuối cùng:

- Tổng forward bốn batch: **7,20 giây**.
- Toàn script, gồm import, load/check/hash/decode/inference và xuất CSV/ảnh/plot: **13,33 giây**.
- Không tải clip mới trong lần cache này. Lần đầu cần tải ba clip blur; thời gian mạng không nằm trong 13,33 giây và có thể lớn hơn inference.

Đây là timing của demo, không phải FPS chuẩn hóa hay latency end-to-end ADAS. Không cần GPU/Colab/Kaggle cho bộ mẫu hiện tại. Chi tiết môi trường và hash script/source/data nằm trong [run_manifest.json](../outputs/stage3_small/run_manifest.json).

## 4. Failure case và phạm vi kết luận

**Quan sát chính:** S01 s2 so với clean, B giảm **94,37%**, từ 3544,1384 xuống 199,4923; nhưng health frame54 tăng **0,258686**, từ 0,148770 lên 0,407456. Health mean8 cũng tăng **0,135000**, từ 0,221979 lên 0,356979. Ngoại lệ không chỉ xuất hiện ở frame54 đã chọn.

Trên các mức đã chạy **s1 → s2 → s5**:

- B giảm đều.
- Health frame54 và health mean8 đều tăng ở s1 → s2 rồi giảm ở s5; không đơn điệu.
- Không tuyên bố kiểm tra đủ s1–s5 vì không chạy s3/s4.

**Giới hạn đối chứng cần ghi:** Kernel là nhãn mô tả dễ đọc, nhưng generator thay đồng thời các tham số trong cùng chế độ motion blur: n_points, accel, linear và psf_smooth_sigma cũng khác theo metadata. Ví dụ s1/s2/s5 có n_points 11/14/32 và linear false/true/false. Vì vậy, kết luận là phản ứng theo **các biến thể severity của DRIVE-C**, không phải tác động riêng biệt của kernel khi mọi đặc điểm PSF khác được giữ cố định. Xem [corruption_parameters.json](../outputs/stage3_small/corruption_parameters.json).

**Điều đã xác nhận:** Pipeline inference + metric + CSV/plot/ảnh chạy được trên CPU và tái hiện gần số nguồn ở bốn clip; phát hiện health chưa xếp đúng thứ tự mức suy giảm trên mẫu này.

**Điều chưa xác nhận:** chất lượng mọi cảnh/ngày đêm/underexposure, nguyên nhân model phản ứng sai, mAP của object detector, early-warning lead, độ an toàn camera hoặc hiệu quả down-weighting/fusion. Một cảnh và bốn ảnh metric không đủ để khái quát thống kê.

## 5. Engineering decision để bàn giao báo cáo

Dùng health như tín hiệu giám sát bổ sung và ghi log cùng metric ảnh. Đánh dấu mẫu bất đồng để kiểm tra; chưa dùng một ngưỡng health tuyệt đối cho quyết định giảm trọng số camera. Metric thủ công cũng phụ thuộc texture/exposure; chưa chứng minh rằng một công thức kết hợp sẽ khắc phục được lỗi.

Nếu có vòng kiểm chứng sau LAB, giữ nhiều cảnh sạch/lỗi, chọn ngưỡng trên tập hiệu chỉnh và đo cảnh báo nhầm/bỏ sót trên tập khác; dùng detector có nhãn nếu muốn đánh giá tác động lên tính năng. Đây là đề xuất, chưa là cải tiến đã benchmark.

## 6. Bằng chứng và bàn giao

| Artifact | Nội dung |
| --- | --- |
| [benchmark_summary.csv](../outputs/stage3_small/benchmark_summary.csv) | Bốn hàng, metric đầy đủ và delta so với clean |
| [per_frame.csv](../outputs/stage3_small/per_frame.csv) | 32 health/frame mới |
| [monotonicity.csv](../outputs/stage3_small/monotonicity.csv) | Kiểm tra riêng B/health54/mean8 ở các mức đã chọn và clean |
| [run.log](../outputs/stage3_small/run.log) | Trình tự chạy và kiểm tra tái hiện |
| [run_manifest.json](../outputs/stage3_small/run_manifest.json) | Môi trường, cấu hình, source/checkpoint/video/script hashes, timing |
| [corruption_parameters.json](../outputs/stage3_small/corruption_parameters.json) | Toàn bộ extra_json của bốn clip |
| [metric_curves.png](../outputs/stage3_small/metric_curves.png) | Plot đa metric |
| [image_grid.png](../outputs/stage3_small/image_grid.png) | Cặp ảnh cùng frame và số metric |
| [Script](../scripts/stage3_small_demo.py) | Đường chạy lại bộ nhỏ |

Nam dùng bảng/plot mới này làm chính; Hưng rà Method/limitations với [PAPER_CODE_MAPPING.md](../reports/PAPER_CODE_MAPPING.md); Đoàn bàn giao script và cấu hình; Khải tổng hợp quyết định và báo cáo. Giai đoạn tiếp theo tập trung bốn báo cáo riêng và pitch, không cần mở rộng bộ chạy lên 24 clip.
