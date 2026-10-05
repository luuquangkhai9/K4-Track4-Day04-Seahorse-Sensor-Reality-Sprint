# Seahorse · Sensor Reality Sprint

LAB **T1 — Camera degradation health score**, nền tảng xe ADAS. Nhóm kiểm tra motion blur ảnh hưởng tới metric ảnh và health score của PerceptionHealthNet trên cùng cảnh như thế nào.

**Kết quả:** demo **4 clip S01**, gồm clean và motion blur s1/s2/s5, đã chạy trên CPU. Ở s2, blur score giảm **94,37%** nhưng health tăng cả tại frame54 và trung bình 8 frame. Đây là failure case về xếp hạng chất lượng trên mẫu đã thử; chưa đo detector/mAP hoặc độ an toàn ADAS.

## Chạy demo nhỏ trên CPU

Cần Git, Python và Internet. Môi trường đã chạy: Python 3.13.15; phiên bản thư viện trong [manifest](outputs/stage3_small/run_manifest.json) và [requirements-demo.txt](requirements-demo.txt). Chạy từ gốc repository:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install torch==2.14.1 torchvision==0.29.1 --index-url https://download.pytorch.org/whl/cpu
.venv\Scripts\python.exe -m pip install -r requirements-demo.txt
.venv\Scripts\python.exe scripts/setup_demo.py
.venv\Scripts\python.exe scripts/stage3_small_demo.py --threads 4 --output outputs/stage3_repeat
.venv\Scripts\python.exe scripts/verify_submission.py
```

Linux/macOS dùng `.venv/bin/python`. Nếu đã đủ thư viện, dùng `python` trực tiếp. Không cần GPU/Colab/Kaggle.

Setup tạo clone riêng tại `.lab_cache/drive-c-source`, chốt commit và kiểm tra checkpoint SHA-256. Nếu checkpoint thiếu, tải riêng khoảng **94 MB** từ nguồn đã chốt. Benchmark chỉ tải **4 clip**, tổng khoảng **54 MB**, khi cache thiếu; không tải toàn dataset. Cache không đưa vào Git.

`--output outputs/stage3_repeat` giữ nguyên bằng chứng đã lưu. Không truyền `--output` sẽ cập nhật `outputs/stage3_small/`. Source sai commit, checkpoint/video sai hash hoặc sai lệch mean8 với nguồn ≥0,001 làm script báo lỗi. [Cấu hình nhỏ](configs/benchmark_small.json) kế thừa thông số model/metric từ [cấu hình cơ sở](configs/benchmark.json).

## Problem và Method

Sensor là camera RGB; failure là motion blur, tính năng liên quan là giám sát chất lượng đầu vào trước nhận diện đối tượng. Baseline là clean cùng cảnh/frame, không chủ động thêm corruption. Claim ban đầu: blur tăng → variance of Laplacian và health dự kiến giảm. Mẫu được chọn có chủ đích sau khi xem kết quả lịch sử để tái hiện ngoại lệ, không phải lấy mẫu ngẫu nhiên.

Hai nguồn của Shiva Aher có vai trò khác nhau:

- *Safety-Critical Camera Reliability Monitoring for ADAS via Degradation-Aware Uncertainty Pattern Analysis*, arXiv:2605.05439v1: phương pháp GSHI/model và giới hạn. [PDF](<paper/Safety-Critical Camera Reliability Monitoring for ADAS via Degradation-Aware Uncertainty Pattern Analysis.pdf>).
- *DRIVE-C: A Controlled Corruption Dataset for Autonomous Driving*, arXiv:2605.09774v1: dữ liệu đối chứng và checkpoint baseline. [PDF](<paper/DRIVE-C A Controlled Corruption Dataset for Autonomous Driving.pdf>).

Nguồn thực thi: [drive-c-dataset v1.0.1](https://github.com/shiv-aher/drive-c-dataset/tree/v1.0.1), commit `caf16657b87cec8518008b74c72dd0dcb6088eb6`. Dữ liệu: [Zenodo 19656444](https://doi.org/10.5281/zenodo.19656444). Checkpoint `epoch_021_best.pth`, SHA-256 `c210d9a4f207584687583d1ab5b96a99e12b2f3dbb2727464c6c039e44fb8c0b`.

Model EfficientNet-B2 nhiều nhánh xuất `pred_health` trực tiếp; nhóm không huấn luyện lại. Input RGB resize 384 × 1280, chia 255, CHW, eval/no gradient. `gshi_gt` tính từ severity, không phải ground truth của detector/an toàn. [PAPER_CODE_MAPPING.md](reports/PAPER_CODE_MAPPING.md) ghi khác biệt công thức, taxonomy và loss giữa paper/source; không tuyên bố tái hiện mọi thí nghiệm paper phương pháp.

## Benchmark và bằng chứng

**[NHÓM ĐO]** S01 clean + blur s1/s2/s5, kernel 11/13/33 px. Mỗi clip lấy frame 0/18/36/54/73/91/109/127, tổng **32 output health**. Metric thủ công đo tại frame54 gốc 1280 × 720:

| Metric | Cách tính | Đơn vị |
| --- | --- | --- |
| B | Variance Laplacian grayscale uint8, CV_64F, ksize=1, ddof=0 | Phương sai đáp ứng trên thang pixel 0–255; proxy độ nét |
| S_pct | 100 × tỷ lệ gray ≤5 hoặc ≥250 | % pixel rất tối/rất sáng |
| H_bit | −Σ p log₂(p), histogram grayscale 256 bin | bit |
| Health | Nhánh health trực tiếp; frame54 và mean8 tách riêng | Không đơn vị, 0–1 |

| Điều kiện | B | S_pct (%) | H_bit (bit) | Health f54 | Health mean8 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Clean | 3544.1384 | 1.6558 | 7.5152 | 0.148770 | 0.221979 |
| Blur s1, 11 px | 292.6951 | 1.0954 | 7.4132 | 0.275987 | 0.318326 |
| Blur s2, 13 px | 199.4923 | 0.9299 | 7.4035 | 0.407456 | 0.356979 |
| Blur s5, 33 px | 14.2645 | 0.4564 | 7.3848 | 0.076573 | 0.059943 |

Tổng forward **7,20 giây**, CPU 4 thread; toàn script đã cache **13,33 giây**, chưa tính tải lần đầu. Sai lệch mean8 lớn nhất với metadata tác giả **0,000322928 < 0,001**. Khớp số hỗ trợ tái hiện pipeline, không xác nhận health đúng.

![Ảnh cùng cảnh, frame54](outputs/stage3_small/image_grid.png)

![Metric theo mức lỗi đã chọn](outputs/stage3_small/metric_curves.png)

Bằng chứng: [CSV tổng hợp](outputs/stage3_small/benchmark_summary.csv), [32 health-frame](outputs/stage3_small/per_frame.csv), [đơn điệu](outputs/stage3_small/monotonicity.csv), [log](outputs/stage3_small/run.log), [manifest](outputs/stage3_small/run_manifest.json), [tham số lỗi](outputs/stage3_small/corruption_parameters.json), [STAGE3_REPORT.md](docs/STAGE3_REPORT.md).

## Failure case và Engineering decision

Ở s2, B giảm **94,37%**, health f54 tăng **0,258686** và mean8 tăng **0,135000** so với clean. Xếp hạng chỉ theo health sẽ ưu tiên s2 hơn clean trong trường hợp này. **[GIẢ THUYẾT]** khác biệt miền/cảnh hoặc calibration có thể góp phần; nguyên nhân chưa được kiểm chứng.

**Đề xuất:** log health cùng B/S/H, kiểm tra mẫu bất đồng trước khi hiệu chỉnh ngưỡng giảm trọng số camera. Thêm cảnh và tập hiệu chỉnh/kiểm tra riêng để đo cảnh báo nhầm/bỏ sót. Chưa triển khai hoặc chứng minh quy tắc tốt hơn. Xem [ENGINEERING_DECISION.md](reports/ENGINEERING_DECISION.md).

Giới hạn: một cảnh, một loại corruption tổng hợp; frame cùng clip không độc lập; chưa chạy s3/s4, cảnh đêm hoặc underexposure trong demo mới. Nhiều tham số PSF đổi cùng severity nên không cô lập riêng kernel. B phụ thuộc texture/exposure; S/H không có chiều tốt/xấu phổ quát. Chưa đo detector/mAP, latency end-to-end, fusion hoặc early warning. Số paper là **[NGUỒN]**, không phải kết quả nhóm.

## Báo cáo và trình bày

| Thành viên | Vai trò | Bản riêng |
| --- | --- | --- |
| Lưu Quang Khải — 2A202602599 | Đội trưởng, thiết kế và quyết định | [Khải](reports/2A202602599_LuuQuangKhai.md) |
| Lê Hưng — MSSV chờ bổ sung | Tài liệu và đối chiếu paper–code | [Hưng](reports/LeHung.md) |
| Đặng ĐỈnh Đoàn — MSSV chờ bổ sung | Code/benchmark | [Đoàn](reports/DangDinhDoan.md) |
| Nguyễn Hồ Nam — 2A202602788 | Kết quả, plot và pitch | [Nam](reports/2A202602788_NguyenHoNam.md) |

[TEAMMATES.md](TEAMMATES.md) · [PITCH.md](reports/PITCH.md) (kịch bản 4 phút 15 giây, chưa bấm giờ thực tế) · [Checklist nộp](reports/SUBMISSION_CHECKLIST.md) · [Kế hoạch/trạng thái](reports/LAB_COMPLETION_PLAN.md).

Mỗi người rà bản riêng, ghi đóng góp thực tế và tự nộp trên VLearn cùng URL repository. Hai MSSV còn thiếu cần bổ sung trước khi nộp. File cục bộ chưa tự xuất hiện trên GitHub.

## Kết quả lịch sử

[test-drivec.ipynb](test-drivec.ipynb), [phn_24_results.csv](outputs/phn_24_results.csv), [phn_per_frame.csv](outputs/phn_per_frame.csv), [phn_curve.png](outputs/phn_curve.png), [fetch_sha256.txt](fetch_sha256.txt) là artifact bộ 24 clip lịch sử. [BENCHMARK_HISTORY.md](docs/BENCHMARK_HISTORY.md) giữ mô tả cũ. **Không cần chạy lại 24 clip**; bộ bốn clip là bằng chứng chính hiện tại.

Source `drive-c-dataset/` tham chiếu bằng submodule đúng commit; setup dùng clone riêng trong cache. Giữ ghi nhận nguồn và điều kiện sử dụng DRIVE-C khi chia sẻ code/checkpoint/dữ liệu.
