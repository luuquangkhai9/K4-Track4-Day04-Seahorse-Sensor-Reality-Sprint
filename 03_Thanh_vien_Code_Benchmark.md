# Thành viên 3 — Code và chạy benchmark

## Thông tin

- Họ tên: **Đặng ĐỈnh Đoàn**
- Mã sinh viên: **2A202602927**
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
| Code/notebook và commit | [stage3_small_demo.py](scripts/stage3_small_demo.py) (runner SHA-256 `16b653f4…0789`, trùng lần chạy gốc), [setup_demo.py](scripts/setup_demo.py); repo nhóm từ commit `9ebfb6d`. Source DRIVE-C tag v1.0.1, commit `caf16657b87cec8518008b74c72dd0dcb6088eb6`; checkpoint `epoch_021_best.pth`, SHA-256 `c210d9a4…8c0b` |
| Môi trường, Python, thư viện | WSL2 Ubuntu (kernel 6.6.87.2), Intel i5-12500H, CPU 4 thread, không GPU. Python 3.13.15 (venv tạo bằng `uv`); torch 2.14.1+cpu, torchvision 0.29.1+cpu, numpy 2.5.3, opencv-python-headless 5.0.0.93, remotezip 0.12.6, requests 2.34.2, PyYAML 6.0.3, matplotlib 3.11.2 — trùng [requirements-demo.txt](requirements-demo.txt) |
| Nguồn và danh sách ảnh/frame | DRIVE-C `drivec_core_v1.zip` (DOI 10.5281/zenodo.19656444), chỉ tải 4 entry qua RemoteZip, SHA-256 đối chiếu [fetch_sha256.txt](fetch_sha256.txt): `S01_clean`, `S01_motion_blur_s1`, `S01_motion_blur_s2`, `S01_motion_blur_s5`. Frame index 0/18/36/54/73/91/109/127 |
| Số ảnh/frame, tiêu chí chọn | 4 clip × 8 frame = 32 health; 4 ảnh frame54 cho B/S/H. Frame lấy đều bằng `sample_frame_indices` của source; mức s1/s2/s5 chọn có chủ đích theo kết quả lịch sử (không ngẫu nhiên) |
| Kích thước, grayscale, dtype, thang pixel | Video 1280 × 720, 128 frame (script kiểm tra). Model: RGB resize 384 × 1280 INTER_AREA, chia 255, CHW, không chuẩn hoá ImageNet. Metric: frame54 gốc, `COLOR_RGB2GRAY`, uint8, 0–255 |
| Baseline | `S01_clean`, cùng cảnh/frame, cùng pipeline; không thêm corruption (`corruption_parameters.json` của clean là `{}`) |
| Mức lỗi | Phạm vi chạy: motion blur s1/s2/s5, kernel 11/13/33 px, severity 0.08/0.18/0.75 (bản phát hành DRIVE-C, không corruption lần hai; PSF đầy đủ trong [corruption_parameters.json](outputs/stage3_repeat/corruption_parameters.json)). Thiết kế lịch sử 24 clip (11/13/19/27/33 px; underexposure −0,16…−1,50 EV) không chạy lại |
| Cách tính Laplacian và variance | `cv2.Laplacian(gray, cv2.CV_64F)` mặc định ksize=1, BORDER_DEFAULT; `.var()` numpy ddof=0. S_pct = 100·mean(gray≤5 ∨ gray≥250); H_bit = −Σ p log2 p, 256 bin, p>0 |
| Seed nếu có ngẫu nhiên | Không áp dụng: không lấy mẫu ngẫu nhiên, không augmentation; model eval + `torch.inference_mode()`. Khác biệt health giữa hai máy ≤3×10⁻⁷ do số học float32 CPU |
| Công thức health score nếu có | Không tự định nghĩa: `pred_health` trực tiếp của PerceptionHealthNet (0–1). Health f54 = output frame 54; mean8 = trung bình số học 8 frame. `gshi_gt` chỉ lưu tham chiếu |
| Lệnh/các cell để chạy | Xem mục *Lệnh chạy lại trên Linux/WSL* bên dưới |
| Vị trí log, CSV, ảnh | Lần chạy của Đoàn: [outputs/stage3_repeat/](outputs/stage3_repeat/run.log) — `run.log`, `run_manifest.json`, `benchmark_summary.csv`, `per_frame.csv`, `monotonicity.csv`, 4 ảnh `*_f54.png`, `image_grid.png`, `metric_curves.png`, [so sánh với bản gốc](outputs/stage3_repeat/comparison_vs_reference.csv). Bản gốc giữ nguyên ở [outputs/stage3_small/](outputs/stage3_small/run.log) |

### Lệnh chạy lại trên Linux/WSL

Chạy từ gốc repository; cần Git, Internet và [uv](https://docs.astral.sh/uv/) (hoặc Python 3.13 sẵn có — numpy 2.5.3 không hỗ trợ Python 3.11).

```bash
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python torch==2.14.1 torchvision==0.29.1 --index-url https://download.pytorch.org/whl/cpu
uv pip install --python .venv/bin/python -r requirements-demo.txt
.venv/bin/python scripts/setup_demo.py                       # clone source đúng commit + checkpoint 94 MB
.venv/bin/python scripts/stage3_small_demo.py --threads 4 --output outputs/stage3_repeat
.venv/bin/python scripts/compare_runs.py                     # so với outputs/stage3_small, không inference
.venv/bin/python scripts/verify_submission.py
```

Lần đầu tải 4 clip (~54 MB) mất khoảng 80 giây; forward 4 clip **8,56 giây**, toàn script **101,4 giây** gồm tải. Không có bước huấn luyện, không cần GPU/Kaggle.

### Kết quả lần chạy lại của Đoàn

**[NHÓM ĐO]** PASS 4 clip/32 health; sai lệch mean8 lớn nhất với metadata tác giả **0,00032299 < 0,001**. So với [bằng chứng đã lưu](outputs/stage3_small/benchmark_summary.csv):

| Kiểm tra | Kết quả |
| --- | --- |
| Runner, config, source commit, checkpoint, SHA-256 4 video | Trùng hoàn toàn |
| Ảnh frame54 (PNG) | Trùng từng byte cả 4 ảnh |
| B, S_pct, H_bit | Sai khác 0 |
| Health 32 frame | Sai khác lớn nhất 2,98 × 10⁻⁷ (khác CPU/OS; dưới ngưỡng 10⁻⁶ của [compare_runs.py](scripts/compare_runs.py)) |
| Failure s2 | B −94,37%; health f54 +0,258686; mean8 +0,135000 so với clean — giữ nguyên |
| Đơn điệu | B giảm đơn điệu; health f54/mean8 **không** giảm đơn điệu s1→s2→s5 |

Số trong báo cáo nhóm (6 chữ số thập phân) không đổi.

## Định dạng kết quả đề xuất

Demo nhỏ dùng schema của script: `benchmark_summary.csv` (1 dòng/clip, B/S/H, health f54/mean8, delta so clean, sai lệch với tác giả) và `per_frame.csv` (`sample_id`, `frame_idx`, `gshi_pred`), nối bằng `sample_id`. Schema lịch sử `phn_24_results.csv`/`phn_per_frame.csv` giữ nguyên trong `outputs/`. Lưu thêm manifest/log thực tế; không làm tròn health trước khi kiểm tra tái hiện. Tham số corruption nằm trong cột `param`.

Nếu có health score hoặc metric bổ sung, thêm cột và ghi rõ công thức. Không điền số giả cho kết quả chưa chạy.

## Kiểm tra trước khi bàn giao

- [x] Mọi mức lỗi dùng cùng danh sách ảnh với baseline (cùng 8 frame index, script dừng nếu khác).
- [x] Các cấu hình chỉ khác tham số corruption đã chốt.
- [x] Baseline thực sự không thêm corruption.
- [x] Log ghi số mẫu chạy thành công/thất bại và nguyên nhân (4/4 thành công; lỗi sẽ ghi traceback và `status=failed` trong manifest).
- [x] CSV không thiếu ID, điều kiện hoặc giá trị metric mà không giải thích.
- [x] Có ảnh baseline và degraded của cùng một mẫu.
- [x] Người khác có thể chạy lại theo hướng dẫn (đã chạy lại từ clone mới trên máy khác, khớp bản gốc).

## Mốc và đầu ra

Giai đoạn 4 đã soạn [bản báo cáo riêng của Đoàn](reports/DangDinhDoan.md). Cần bổ sung MSSV, rà khả năng chạy lại/provenance và ghi đóng góp thực tế trước nộp. Phần nói của Đoàn nằm trong [PITCH.md](reports/PITCH.md).

**Giai đoạn 2 đã có bằng chứng chạy CPU:** [báo cáo](docs/STAGE2_REPORT.md), [script](scripts/stage2_smoke_test.py), [manifest](outputs/stage2/run_manifest.json). Baseline thật S01 clean đạt ngưỡng tái hiện. Đặng ĐỈnh Đoàn dùng đường chạy này cho bước tiếp theo; chưa chạy mới đủ 24 clip ở giai đoạn 2. Không tự gán lần chạy hỗ trợ này vào nhật ký đóng góp cá nhân nếu chưa thực hiện/kiểm tra.

- **Trước phút 45:** Môi trường/dữ liệu sẵn sàng, baseline smoke test chạy được.
- **Trước phút 75:** Hoàn thành benchmark, lưu code/cấu hình/log/CSV/ảnh.
- **Trước phút 95:** Giải quyết sai lệch do Nam phát hiện; bàn giao gói bằng chứng.
- **Trước phút 115:** Hoàn thiện hướng dẫn chạy và bản riêng.
- File/commit bàn giao: [outputs/stage3_repeat/](outputs/stage3_repeat/run_manifest.json), [compare_runs.py](scripts/compare_runs.py), sửa [verify_submission.py](scripts/verify_submission.py); commit của Đặng ĐỈnh Đoàn trên `main` (`git log --author=Doan0904`).
- Lỗi còn tồn tại và ảnh hưởng tới kết quả: Không có lỗi kỹ thuật. `verify_submission.py` trước đây báo lỗi link trên clone mới vì submodule `drive-c-dataset/` rỗng — đã sửa để đối chiếu link trong clone đúng commit ở `.lab_cache`; không ảnh hưởng số liệu. Python <3.12 không cài được numpy 2.5.3. Giới hạn phạm vi (1 cảnh, 3 mức) giữ như báo cáo nhóm.
- Chuẩn bị bản nộp riêng trên VLearn: Đã ghi MSSV và đóng góp vào [bản riêng](reports/DangDinhDoan.md); còn lượt nộp VLearn.

## Nhật ký đóng góp cá nhân

| Thời điểm | Việc đã làm | File/commit/bằng chứng | Kết quả hoặc vấn đề |
| --- | --- | --- | --- |
| 2026-10-05 23:50 | Tạo môi trường Python 3.13.15 CPU đúng phiên bản pin; chạy `setup_demo.py` | `.lab_cache/drive-c-source` commit `caf16657`, checkpoint SHA-256 khớp | PASS; Python 3.11 không cài được numpy 2.5.3 nên chuyển sang 3.13 |
| 2026-10-05 23:55–23:57 | Chạy lại benchmark 4 clip trên CPU 4 thread, máy riêng (WSL2) | [outputs/stage3_repeat/](outputs/stage3_repeat/run.log) | PASS 4 clip/32 health; sai lệch với tác giả 0,00032299 |
| 2026-10-05 23:58 | Viết `compare_runs.py`, so sánh với bằng chứng đã lưu | [comparison_vs_reference.json](outputs/stage3_repeat/comparison_vs_reference.json) | Ảnh/B/S/H trùng tuyệt đối; health lệch ≤2,98 × 10⁻⁷ |
| 2026-10-05 23:58 | Sửa `verify_submission.py` cho clone mới (submodule chưa init) | [verify_submission.py](scripts/verify_submission.py), [verification.json](outputs/submission_check/verification.json) | Kiểm tra kỹ thuật PASS; còn pending thông tin cá nhân |
| 2026-10-06 00:00 | Điền bảng cấu hình tái lập, checklist, lệnh Linux; bàn giao cho Nam | File này, [bản riêng](reports/DangDinhDoan.md) | Hoàn tất phần code/benchmark |
