# Kế hoạch hoàn thành LAB — T1 Camera degradation health score

## Phạm vi thực hiện hiện tại — demo nhỏ theo yêu cầu nhóm

Nhóm yêu cầu thu nhỏ giai đoạn 3 để xác nhận tính khả thi. **Đường chạy chính hiện tại là 4 clip S01: clean + motion blur s1/s2/s5 (kernel 11/13/33 px), 32 health/frame và 4 ảnh frame 54.** Ba mức lỗi đủ phần tạo/đánh giá mức suy giảm tối thiểu của T1. Chỉ kiểm tra một cảnh, một loại lỗi; chưa suy rộng sang ngày/đêm hoặc underexposure.

Dùng [configs/benchmark_small.json](configs/benchmark_small.json) và [scripts/stage3_small_demo.py](scripts/stage3_small_demo.py); kết quả mới lưu trong `outputs/stage3_small/`. Phần kế hoạch 24 clip phía dưới là thiết kế ban đầu và nguồn kết quả lịch sử, không phải yêu cầu phải chạy tiếp. Lần chạy mới của nhóm cần ưu tiên bộ nhỏ này khi viết báo cáo/pitch.

Sau demo: Nam kiểm tra bảng/plot/ảnh bốn clip; Hưng rà trích dẫn và giới hạn; Đoàn bàn giao script/log; Khải tổng hợp failure/decision; bốn người viết bản riêng. Không cần chạy đủ 24 clip để hoàn thiện LAB trong phạm vi mới.

**Giai đoạn 3 đã thực hiện:** PASS bốn clip/32 health-frame trên CPU, sai lệch nguồn tối đa 0,000323. B/health/entropy/ratio, ảnh và kiểm tra đơn điệu đã lưu. Xem [STAGE3_REPORT.md](STAGE3_REPORT.md). Tiếp theo hoàn thiện báo cáo/failure/decision/pitch từ bộ nhỏ.

**Giai đoạn 4 đã chuẩn bị:** [ENGINEERING_DECISION.md](ENGINEERING_DECISION.md), bốn báo cáo trong `reports/`, [PITCH.md](PITCH.md) và [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md). Xem [STAGE4_REPORT.md](STAGE4_REPORT.md). Còn hai MSSV, xác nhận đóng góp, tập pitch, chia sẻ và nộp bài; không coi chúng là đã hoàn thành.

## 1. Mục tiêu và phạm vi

Nhóm Seahorse gồm **4 người**, đội trưởng **Lưu Quang Khải — 2A202602599**. Kế hoạch cập nhật sau khi đọc hai bài báo, đối chiếu source code và kết quả đã lưu, bám toàn bộ hướng dẫn LAB.

Repository chung: <https://github.com/luuquangkhai9/K4-Track4-Day04-Seahorse-Sensor-Reality-Sprint>.

**Cập nhật giai đoạn 1:** Đã chuẩn bị [thiết kế benchmark](BENCHMARK_DESIGN.md), [cấu hình đối chiếu](configs/benchmark.json) và [TEAMMATES](TEAMMATES.md); đã đồng bộ phân công. Lê Hưng phụ trách tài liệu, Đặng ĐỈnh Đoàn phụ trách code/benchmark, Nguyễn Hồ Nam — 2A202602788 phụ trách kết quả/pitch. Giảng viên đã chấp thuận nhóm 4 người theo thông tin đội trưởng cung cấp. Chỉ còn thiếu MSSV của Hưng và Đoàn. Chi tiết kiểm kê dữ liệu/môi trường nằm trong thiết kế; chưa chạy inference mới.

**Cập nhật giai đoạn 2:** Đã hoàn thiện [paper–code mapping](PAPER_CODE_MAPPING.md), xác minh source/checkpoint và chạy mới S01 clean trên CPU. Mean8 = 0,221979, sai lệch nguồn = 0,000074; forward 8 frame khoảng 3,62 giây. Đủ đường chạy tối thiểu, chưa cần Colab/Kaggle. Xem [STAGE2_REPORT.md](STAGE2_REPORT.md). Giai đoạn 3 còn tải 23 clip và chạy/kiểm tra benchmark đầy đủ.

**Đích hoàn thành hiện tại:** script demo chạy được; baseline + **3 mức motion blur**; health score và ba metric thủ công; CSV/log/plot/ảnh minh chứng; một failure case và một engineering decision; README, TEAMMATES, bốn báo cáo cá nhân và pitch 3–5 phút. Các checkbox chưa đánh dấu là công việc còn phải thực hiện.

**Bài toán:** Camera trên xe ADAS bị motion blur hoặc thiếu sáng; kiểm tra các metric chất lượng ảnh và health score của PerceptionHealthNet có phản ánh mức suy giảm trên cùng cảnh hay không. Tính năng liên quan là giám sát chất lượng ảnh trước nhận diện đối tượng.

**Giả thuyết gốc:** Khi motion blur tăng trên cùng cảnh/frame, variance of Laplacian và health score dự kiến giảm. Khi underexposure tăng, kiểm tra health score, entropy và tỷ lệ pixel ở hai đầu thang sáng. Kết quả hiện có đã bộc lộ ngoại lệ; lần chạy tiếp theo nhằm tái hiện và kiểm tra ngoại lệ, không trình bày giả thuyết như được đặt ra trước khi xem toàn bộ kết quả. Các metric này là proxy chất lượng đầu vào, không phải mAP hay độ an toàn của ADAS.

Giữ **T1** làm chủ đề duy nhất. Hai loại lỗi được phân tích riêng, không trộn blur và underexposure trong cùng một điều kiện. Ưu tiên motion blur làm câu chuyện chính; underexposure là phép thử bổ sung đã có trong notebook. Dùng checkpoint phát hành cùng DRIVE-C; không huấn luyện lại trong 120 phút. Detector, early-warning benchmark, uncertainty overlay và ngưỡng ngày/đêm là phần mở rộng sau khi đủ sản phẩm tối thiểu.

Giảng viên đã chấp thuận nhóm **4 người**, theo thông tin đội trưởng cung cấp. Kế hoạch thực hiện bốn báo cáo và bốn lượt nộp riêng, cùng dẫn tới repository chung.

## 2. Trạng thái hiện có và phần còn thiếu

| Hạng mục | Bằng chứng hiện có | Việc còn phải làm |
| --- | --- | --- |
| Định nghĩa chủ đề | `T1_camera_degradation_health_score.md` | Đưa phạm vi cụ thể vào README/báo cáo |
| Tài liệu nguồn | Đã đọc hai PDF: bài phương pháp và DRIVE-C; đã đối chiếu một số phần code | Lưu ghi chú và bảng paper–code mapping có trang/bảng/file hỗ trợ |
| Code và lịch sử chạy | `test-drivec.ipynb`, có output tải dữ liệu/nạp checkpoint/inference | Kiểm tra chạy lại, lưu phiên bản môi trường và cấu hình thực tế |
| Kết quả | `phn_24_results.csv`: 24 dòng; `phn_per_frame.csv`: 192 dòng, 8 frame/clip | Tổng hợp so sánh theo từng cảnh; không coi 192 frame là 192 cảnh độc lập |
| Plot | `phn_curve.png` | Kiểm tra nhãn, bổ sung plot metric thủ công nếu cần |
| Truy vết dữ liệu | `fetch_sha256.txt` | Ghi nguồn tải, cách chọn clip/frame; hash không thay thế dữ liệu hay ảnh minh chứng |
| Ảnh trước/sau | Notebook có cell xuất `phn_grid.png`; chưa thấy file này ở gốc | Xuất và lưu grid hoặc cặp ảnh cùng frame |
| Phân công | Đã có tên và vai trò của cả bốn người | Bổ sung MSSV của Lê Hưng và Đặng ĐỈnh Đoàn |
| README | Đã có | Cập nhật vai trò hai bài báo và khác biệt paper–code |
| Hồ sơ nộp | TEAMMATES đã có đủ bốn tên, thiếu hai MSSV; chưa có đủ bộ bốn báo cáo cuối cùng | Hoàn thiện MSSV/bản riêng, kiểm tra repo URL và quyền truy cập |

Đã kiểm tra tính nhất quán CSV: trung bình 8 frame so với cột kết quả nguồn đã làm tròn có chênh lệch tối đa khoảng **0,000599**. Notebook lưu output khoảng **0,000626** khi so với metadata trước làm tròn. Hai cách kiểm tra dùng độ chính xác khác nhau; cần lưu bảng đối chiếu không làm tròn khi chạy lại. Khớp số là kiểm tra tái hiện, chưa xác nhận model đánh giá đúng sensor health.

## 3. Hai nguồn phương pháp/dữ liệu và đường chạy — Bước 2

| Nguồn | Vai trò trong LAB | Phạm vi kết luận |
| --- | --- | --- |
| *Safety-Critical Camera Reliability Monitoring for ADAS via Degradation-Aware Uncertainty Pattern Analysis*, arXiv:2605.05439v1, 06/05/2026 | GSHI, model EfficientNet-B2 nhiều nhánh, synthetic supervision, early-warning protocol | Kết quả tác giả trên KITTI/DAWN; không gán cho lần chạy DRIVE-C của nhóm |
| *DRIVE-C: A Controlled Corruption Dataset for Autonomous Driving*, arXiv:2605.09774v1, 10/05/2026 | Dữ liệu có đối chứng, severity/metadata, baseline và failure cases | Căn cứ thiết kế benchmark và giới hạn dữ liệu |
| Source code/checkpoint thực sự dùng khi chạy | Output, preprocessing, sampling, công thức nhãn và hash | Căn cứ mô tả triển khai nhóm đã dùng |

Đường chạy chính: dùng notebook hiện có, nạp checkpoint tác giả, inference trên mẫu DRIVE-C; không huấn luyện model mới.

Thông tin lấy từ notebook; xác nhận lại trong log của lần chạy tiếp theo:

- Repository: <https://github.com/shiv-aher/drive-c-dataset>, tag `v1.0.1`, commit được log là `caf16657b87cec8518008b74c72dd0dcb6088eb6`.
- Dataset: <https://zenodo.org/records/19656444>, tải các clip cần dùng qua HTTP Range.
- Checkpoint: `epoch_021_best.pth`; SHA-256 ghi trong notebook và được kiểm tra khi nạp.
- Input của phép thử: 8 frame RGB mỗi clip, resize về 384 × 1280 cho model.
- Output đang sử dụng: health score, xác suất loại lỗi, severity dự đoán; metric thủ công đo trên frame 54 ở 1280 × 720.

**Provenance cần xử lý:** Notebook dùng source trong `<WORK>/drive-c-dataset`, không tự động dùng bản sao `drive-c-dataset/` ở gốc. Nếu bản sao ở gốc không có `.git` riêng, lệnh `git -C drive-c-dataset rev-parse HEAD` sẽ trả commit repository nhóm; không ghi nhầm đó là commit nguồn. Lưu commit thực tế được clone/import, checkpoint SHA-256, source URL và mọi chỉnh sửa cục bộ.

**Thành viên 2 hoàn thiện `PAPER_CODE_MAPPING.md`:** tên/tác giả/phiên bản; trang/bảng và file/hàm hỗ trợ từng claim; input → output; công thức metric; requirements; phạm vi tái hiện; limitation của nguồn và nhận định nhóm ghi riêng.

Các điểm bắt buộc trong bảng đối chiếu:

- Phân biệt H_net (nhánh health trực tiếp), H_gshi (tính từ severity dự đoán), gshi_gt (nhãn tính từ severity thật). Code đã đọc lấy `pred_health` trực tiếp; xác nhận trên đúng bản của lần chạy.
- Công thức nhãn trong source có beta 0,85 và clipping; phân biệt với công thức tích cơ bản trong PDF.
- Paper mô tả năm loss; script huấn luyện đã đọc cộng bốn loss với trọng số khác. Ghi khác biệt, không tự gán nguyên nhân hoặc tuyên bố tái hiện trọn bài phương pháp.
- Taxonomy model có vignetting và exposure_shift; DRIVE-C không tạo vignetting và tách overexposure/underexposure.
- MAE 0,064, issue mAP 0,891 và lead 0,47 là số tác giả; issue mAP không phải detector mAP, lead có đơn vị severity chứ không phải giây.
- FPS của paper đo trên RTX 5090 ở 224 × 224; không dùng làm tốc độ notebook 384 × 1280.
- DRIVE-C: 6/12 loại lỗi đơn điệu xét đường trung bình qua cảnh; 47,5% xét từng cặp cảnh–loại lỗi. Cả hai xét s1–s5, không gồm clean.

**Điều kiện đạt:** một thành viên khác giải thích được nhóm dùng phần nào của mỗi nguồn và chỉ đúng bằng chứng của claim. Không ghi số paper vào bảng [NHÓM ĐO].

**Đường dự phòng:** Nếu tải/model không chạy được trong thời gian lớp, dùng ảnh sạch hợp lệ có sẵn, tạo 3–5 mức blur với tham số cố định và đo ba metric thủ công. Lưu seed nếu có ngẫu nhiên. Ghi rõ đây là benchmark mô phỏng; không gán kết quả mô phỏng cho PerceptionHealthNet. Nếu chỉ phân tích CSV lịch sử, ghi đó là kết quả lần chạy đã lưu, không mô tả là lần chạy mới.

## 4. Thiết kế benchmark có đối chứng — Bước 3–4

### Dữ liệu và điều kiện

- S01: clean + motion blur s1–s5 + underexposure s1–s5.
- S06: cùng bộ điều kiện như S01.
- S07/S08 clean: ví dụ bổ sung về độ phụ thuộc cảnh; không phải đối chứng cho lỗi ở S01/S06.
- Tổng: 24 clip, 8 frame/clip cho inference; 24 ảnh frame 54 cho metric thủ công và minh họa.
- Baseline của mỗi phép thử là **clean cùng scenario và frame**. “Clean” nghĩa là không chủ động thêm corruption, không đồng nghĩa ảnh hoàn hảo.
- Motion blur: kernel trong CSV là **11, 13, 19, 27, 33 pixel**.
- Underexposure: `delta_ev` trong CSV là **−0,16; −0,36; −0,70; −1,10; −1,50**.
- Đọc code tạo corruption/metadata để xác nhận ý nghĩa và đơn vị tham số. Đối chiếu vị trí frame và cặp clip, không mặc định chúng khớp chỉ từ tên.
- Nhóm sử dụng các biến thể corruption phát hành sẵn; không thêm blur lên clip đã corrupted. Ghi rõ cách này trong báo cáo.
- Kiểm tra mỗi clip có 128 frame trước khi dùng các chỉ số 0, 18, 36, 54, 73, 91, 109, 127. Không coi 192 health/frame là 192 cảnh độc lập.

### Metric cố định trước khi tổng hợp

| Metric | Định nghĩa theo code hiện có | Thang/đơn vị | Giới hạn diễn giải |
| --- | --- | --- | --- |
| B — blur score | `var(Laplacian(grayscale))`, OpenCV `CV_64F`, grayscale uint8 | Phương sai đáp ứng Laplacian trên thang pixel 0–255; không là đơn vị vật lý | Proxy độ sắc nét, phụ thuộc texture, exposure và kích thước ảnh |
| S_pct | `100 × mean((gray >= 250) OR (gray <= 5))` | % pixel | Tỷ lệ ở hai đầu thang sáng; gồm pixel tối, không chỉ overexposure |
| H_bit | `−sum(p × log2(p))`, histogram grayscale 256 bin | bit | Entropy mức xám; không đo độ đúng của detector |
| gshi_pred_f54 | `pred_health` model dự đoán cho frame 54 | Không đơn vị, thang 0–1; cao hơn được diễn giải là khỏe hơn | Nhánh học trực tiếp, không bảo đảm đơn điệu theo corruption |
| gshi_pred_tb8 | Trung bình health của 8 frame/clip | Như trên | Dùng kiểm tra tái hiện với kết quả clip của nguồn |

Không gọi `top1_prob` của model chẩn đoán lỗi là confidence của object detector. `gshi_gt` là nhãn từ severity, không phải ground truth về độ tin cậy ADAS. Không tự ghép B/S/H thành health score bằng trọng số tùy ý chỉ để làm đẹp kết quả.

### Phép phân tích và bằng chứng

1. Xác nhận baseline chạy được, log phiên bản thư viện, thiết bị, commit và checkpoint hash.
2. Chạy từng điều kiện, giữ nguyên tiền xử lý và model; lưu kết quả từng frame trước làm tròn.
3. Với mỗi scenario/loại lỗi, đặt clean cạnh 5 mức lỗi. Tính chênh lệch tuyệt đối so với clean; nếu dùng %, nêu công thức và tránh chia cho 0.
4. Vẽ B, S_pct, H_bit và health theo tham số lỗi, tách S01/S06 và từng corruption. Không yêu cầu mọi metric đều đơn điệu.
5. Lưu ít nhất một cặp ảnh baseline/degraded cùng frame, CSV và log tương ứng.
6. Kiểm tra số mẫu, ID, frame và metric; báo mẫu lỗi/thiếu thay vì bỏ âm thầm.

**Bổ sung từ CSV, ít tốn thời gian:**

7. Kiểm tra 24 ID duy nhất, đủ 8 frame/clip và frame 54 khớp bảng tổng hợp trong sai số làm tròn.
8. Tạo `benchmark_summary.csv`: scenario, corruption, severity, tham số, metric và delta so với clean cùng cảnh. Nếu dùng %, nêu công thức và xử lý baseline bằng 0.
9. Tạo `monotonicity.csv` cho bốn cặp S01/S06 × loại lỗi; kiểm tra riêng health frame 54 và health trung bình clip từ s1 đến s5. Báo riêng thay đổi clean → s1 để không trộn hai tiêu chí.
10. Lưu bảng đầy đủ, gồm cả điểm trái dự đoán. Không loại mẫu chỉ vì không khớp claim.

`run_manifest.json` tối thiểu ghi thời điểm, thiết bị, phiên bản Python/thư viện, source URL/commit thực tế, checkpoint hash, nguồn/hash clip, danh sách frame, preprocessing, tham số metric và đường dẫn output. Ngưỡng sai lệch `1e-3` là kiểm tra tái hiện; nếu vượt, kiểm tra version/frame/preprocessing và lưu lỗi, không đổi ngưỡng sau khi xem số chỉ để báo PASS.

## 5. Failure case và quyết định kỹ thuật — Bước 5

**Failure case chính đã thấy trong CSV, cần gắn ảnh minh chứng:**

| Frame 54, cảnh S01 | B | gshi_pred_f54 |
| --- | --- | --- |
| Clean | 3544,1 | 0,1488 |
| Motion blur, kernel 13 px | 199,5 | 0,4075 |
| Motion blur, kernel 33 px | 14,3 | 0,0766 |

Quan sát: ở kernel 13 px, B giảm khoảng **94,4%** so với clean nhưng health tăng **0,2587**. Health không giảm đơn điệu theo mức blur trên mẫu này. Kiểm tra thêm trung bình 8 frame để biết ngoại lệ có chỉ xuất hiện ở frame đã chọn hay không. Không giải thích nguyên nhân bằng kiến trúc, domain shift hoặc lỗi nhãn nếu chưa có kiểm chứng; ghi chúng là giả thuyết.

DRIVE-C báo tương quan motion blur tương đối tốt ở mức tổng hợp nhiều cảnh. Một frame/cảnh ngoại lệ không trực tiếp bác bỏ bảng trung bình đó. Công thức GSHI đơn điệu theo severity cũng không bảo đảm nhánh health trực tiếp của model đơn điệu theo ảnh đầu vào.

Ví dụ bổ sung: S06 clean có health 0,2794, underexposure nhẹ có thể lên 0,3286. Không kết luận toàn bộ ảnh đêm luôn bị chấm thấp hơn ảnh ngày; chính S06 clean có score cao hơn S01 clean.

**Đề xuất kỹ thuật để trình bày:** ghi log đa metric và cảnh/ngày đêm; dùng health model cùng B/S/H để phát hiện trường hợp bất đồng trước khi chọn quy tắc giảm trọng số camera. Đề xuất giảm trọng số khi nhiều tín hiệu chất lượng xấu nhất quán sau khi ngưỡng được hiệu chỉnh/kiểm chứng. Nhóm chưa đo hiệu quả fusion hay down-weighting nên chỉ trình bày đây là đề xuất. Không áp thẳng ngưỡng 0,9/0,6 của paper như ngưỡng đã xác thực trên DRIVE-C.

**Cách kiểm chứng vòng sau:** thử trên nhiều cảnh sạch/lỗi, chốt ngưỡng trên tập dev rồi kiểm tra tập khác; đo cảnh sạch bị cảnh báo nhầm và lỗi bị bỏ sót theo nhãn corruption. Nếu muốn kết luận về tính năng ADAS, chạy detector cùng cấu hình và có nhãn đối tượng để đánh giá. Kết quả chẩn đoán corruption vẫn không tự chứng minh detector an toàn.

Nếu chọn ngưỡng riêng ngày/đêm, cần tập hiệu chỉnh có cảnh đêm: dev gốc DRIVE-C S01–S05 không có cảnh đêm. Không dùng các cảnh test để vừa chọn ngưỡng vừa báo cáo khả năng tổng quát hóa trên chính chúng.

Trade-off cần nêu: metric thủ công dễ tính nhưng phụ thuộc cảnh/exposure; model health có thể cần tài nguyên và vẫn sai trên mẫu cụ thể; ngưỡng theo ngữ cảnh cần thêm dữ liệu. Hiện chưa đo latency end-to-end, mAP hoặc hiệu quả fusion.

## 6. Phân công và lịch 120 phút theo hướng dẫn

### Gói công việc và điều kiện bàn giao

| Gói | Người chính | Đầu ra | Điều kiện đạt |
| --- | --- | --- | --- |
| A — Điều phối | **Khải** | Thiết kế thống nhất, TEAMMATES, engineering decision | Có tên/MSSV thật; scope rõ; quyết định gắn số đo |
| B — Paper/code | **Lê Hưng** | `PAPER_CODE_MAPPING.md`, trích dẫn | Mỗi claim chính có trang/bảng/file; phân biệt phương pháp và bản triển khai |
| C — Tái hiện | **Đặng ĐỈnh Đoàn** | Notebook output, CSV, manifest/log, ảnh | Truy vết được model/data/frame; kiểm tra số mẫu và tái hiện |
| D — Phân tích/pitch | **Thành viên 4** | Bảng delta, monotonicity, plot, `PITCH.md` | Số khớp CSV; hình có baseline/tham số/đơn vị; failure có ảnh |
| E — Bản cá nhân | **Cả bốn người** | `reports/<MSSV>_<HoTen>.md` | Mỗi bản đủ năm mục, có đóng góp cá nhân và link bằng chứng chung |

Thành viên 2 và 4 làm song song trong khi thành viên 3 chạy code. Mỗi file có một người biên tập chính; Khải rà tổng thể. Tận dụng phần đọc nguồn/kết quả đã có thay vì bắt đầu lại từ đầu.

### Mốc 120 phút

| Giai đoạn | Khải — đội trưởng | Lê Hưng — nguồn | Đặng ĐỈnh Đoàn — code | Nguyễn Hồ Nam — kết quả/pitch |
| --- | --- | --- | --- | --- |
| 0–15: Chuẩn bị | Chốt claim, baseline, vai trò; bổ sung thông tin nhân sự | Kiểm tra nguồn đã có | Kiểm tra môi trường/notebook | Chuẩn bị bảng metric |
| 15–45: Nguồn và đường chạy | Chốt khả năng thực hiện, tránh mở rộng quá mức | Hoàn thành phiếu nguồn và trích dẫn | Setup, kiểm tra checkpoint/dữ liệu | Chuẩn bị khung 5 mục báo cáo |
| 45–95: Thiết kế và chạy | Theo dõi tiến độ, kiểm tra đối chứng | Đối chiếu tham số, định nghĩa metric | Chạy/lưu CSV, log và ảnh | Kiểm tra CSV, plot và chênh lệch |
| 95–115: Failure và cải tiến | Chốt engineering decision | Tách limitation nguồn/nhóm | Truy xuất mẫu và cấu hình failure | Hoàn thiện bảng/ảnh, câu chuyện trình bày |
| 115–120: Hoàn thiện | Kiểm tra rubric và tập pitch | Hoàn thiện bản cá nhân | Hoàn thiện bản cá nhân | Hoàn thiện bản cá nhân và slide chung |

Chia giai đoạn 45–95 thành **45–75 chạy/lưu bằng chứng**, **75–95 kiểm tra và tổng hợp**. Đến phút 95 dừng thêm tính năng. Đến phút 115 phải có bốn bản nháp hoàn chỉnh để năm phút cuối chỉ rà và tập nói.

**Mốc chuyển phương án:** Nếu phút 45 chưa chạy được model vì môi trường/mạng, dùng kết quả lịch sử có nguồn gốc rõ ràng để tái tính phân tích; không mô tả là inference mới. Nếu có ảnh sạch hợp lệ, có thể chạy phép blur thủ công 3–5 mức để có benchmark mới, đặt tên riêng. Không tải toàn bộ dataset hoặc huấn luyện lại để cứu một demo quá phạm vi.

Chuẩn bị khung báo cáo từ sớm để 5 phút cuối chỉ kiểm tra và tập nói. Các file phân công đã được liên kết tới thiết kế giai đoạn 1; dùng cấu hình chung và lịch trong kế hoạch này khi thực hiện.

## 7. Sản phẩm cần lưu và nộp — Bước 6–7

Giữ tên thư mục gốc hiện tại `K4-Track4-Day04-Seahorse-Sensor-Reality-Sprint`, phù hợp mẫu tên nhóm nếu tên chính thức là Seahorse. Không cần chuyển các artifact hiện có để bắt đầu.

| File/thư mục dự kiến | Nội dung bắt buộc |
| --- | --- |
| `README.md` | Problem, nguồn, môi trường, cách chạy, đường dẫn kết quả và giới hạn |
| `TEAMMATES.md` ở gốc | Họ tên/MSSV của bốn người; ghi nhận giảng viên đã chấp thuận nhóm 4 người |
| `test-drivec.ipynb` | Code cùng output, cấu hình và kiểm tra tái hiện |
| `phn_24_results.csv`, `phn_per_frame.csv` | Số đo và ID/frame truy vết |
| `fetch_sha256.txt`, log chạy | Truy vết dữ liệu, commit/checkpoint/môi trường |
| `phn_curve.png`, `phn_grid.png`, plot bổ sung | Bảng/plot/ảnh có baseline, mức lỗi và nhãn đúng |
| `reports/<MSSV>_<HoTen>.md` | 4 bản cá nhân, mỗi bản có đủ 5 mục và dẫn bằng chứng chung |
| `PAPER_CODE_MAPPING.md` | Hai nguồn, đối chiếu paper/code và phạm vi tái hiện |
| `run_manifest.json`, `run.log` | Cấu hình, môi trường và log của lần chạy thực tế |
| `benchmark_summary.csv`, `monotonicity.csv` | Delta so với clean và kiểm tra đơn điệu theo phạm vi rõ ràng |
| `handcrafted_metrics.png` | B, S_pct, H_bit theo mức lỗi, tách cảnh và corruption |
| `PITCH.md` | Kịch bản và phân chia người nói |

Những file chưa có là **đầu ra dự kiến**, không phải artifact đã hoàn thành. Bốn template phân công không thay thế bốn báo cáo cuối cùng. Giữ vị trí các kết quả hiện có để tránh phá liên kết.

Mỗi báo cáo gồm đúng luồng: **Problem → Method → Benchmark → Failure case → Engineering decision**. Có tên/MSSV, đóng góp cá nhân, URL repo, nguồn đã đọc, commit/version, dataset và cách chạy. Nếu VLearn yêu cầu định dạng khác Markdown, xuất sang định dạng được yêu cầu trước khi nộp.

Pitch gợi ý **4 phút 15 giây**: Khải 30 giây problem; thành viên 2 nói 45 giây method/hai nguồn; thành viên 3 nói 60 giây benchmark; thành viên 4 nói 75 giây kết quả/failure; Khải 45 giây decision/trade-off. Mở được notebook/CSV/ảnh khi được hỏi. Mỗi người nộp bản riêng và cùng URL repository; kiểm tra truy cập sau khi gửi.

## 8. Tiêu chí hoàn thành

- [x] **40% — Benchmark:** đã chuẩn bị bằng chứng demo nhỏ, baseline/3 mức lỗi, số đo, log và ảnh/plot.
- [x] **25% — Failure thực tế:** đã viết mẫu lỗi, tham số, chênh lệch và giới hạn tác động.
- [x] **20% — Thuật toán:** đã viết input/output, phương pháp, metric và limitation từ hai nguồn.
- [x] **15% — Trade-off:** đã viết đề xuất liên hệ số đo và phép kiểm chứng tiếp theo.
- [x] Đã tách **[NGUỒN]**, **[NHÓM ĐO]**, **[GIẢ THUYẾT]** trong hồ sơ. Các mục này là kiểm tra nội dung chuẩn bị, không phải điểm đã chấm.
- [ ] README, TEAMMATES, tên/MSSV 4 người và 4 báo cáo cá nhân đầy đủ.
- [x] Đội trưởng đã xác nhận giảng viên chấp thuận nhóm 4 người.
- [ ] Paper–code mapping mô tả đúng triển khai; không gán mAP, lead severity hoặc FPS của paper cho kết quả nhóm.
- [ ] Link artifact hoạt động, không thiếu ảnh hoặc dẫn tới đường dẫn máy cá nhân trong bản nộp.
- [ ] Repository chia sẻ có đủ kết quả, không cần đưa cache dữ liệu lớn vào Git.
- [ ] Mỗi thành viên đã nộp và mở lại được bản riêng cùng bằng chứng chung trên VLearn.

Thứ tự thực hiện tiếp theo: **lưu paper–code mapping và provenance → kiểm tra chạy/CSV → bổ sung ảnh và plot đa metric → viết failure/decision → đồng bộ README/phân công và bốn báo cáo → pitch/nộp riêng**. Chỉ thêm detector, huấn luyện hoặc ngưỡng thích nghi sau khi đạt các đầu ra bắt buộc.
