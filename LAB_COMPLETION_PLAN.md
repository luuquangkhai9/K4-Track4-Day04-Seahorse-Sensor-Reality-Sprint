# Kế hoạch hoàn thành LAB — T1 Camera degradation health score

## 1. Mục tiêu và phạm vi

Nhóm Seahorse gồm **4 người**, đội trưởng **Lưu Quang Khải — 2A202602599**. Kế hoạch được đối chiếu với toàn bộ hướng dẫn LAB do người dùng cung cấp.

**Bài toán:** Camera trên xe ADAS bị motion blur hoặc thiếu sáng; kiểm tra các metric chất lượng ảnh và health score của PerceptionHealthNet có phản ánh mức suy giảm trên cùng cảnh hay không. Tính năng liên quan là giám sát chất lượng ảnh trước nhận diện đối tượng.

**Claim cần kiểm tra:** Khi motion blur tăng trên cùng cảnh/frame, variance of Laplacian dự kiến giảm; health score dự kiến giảm nhưng có thể không đơn điệu. Khi underexposure tăng, kiểm tra health score, entropy và tỷ lệ pixel ở hai đầu thang sáng. Đây là các proxy chất lượng đầu vào, không phải mAP hay độ an toàn của ADAS.

Giữ **T1** làm chủ đề duy nhất. Hai loại lỗi được phân tích riêng, không trộn blur và underexposure trong cùng một điều kiện. Ưu tiên motion blur làm câu chuyện chính; underexposure là phép thử bổ sung đã có trong notebook.

Hướng dẫn yêu cầu đúng 5 thành viên, 5 báo cáo và 5 lượt nộp. Nhóm thực tế có 4 người: cần xác nhận với giảng viên cách xử lý; kế hoạch chuẩn bị 4 bản thật, không tự coi yêu cầu 5 người đã được miễn và không thêm người giả.

## 2. Trạng thái hiện có và phần còn thiếu

| Hạng mục | Bằng chứng hiện có | Việc còn phải làm |
| --- | --- | --- |
| Định nghĩa chủ đề | `T1_camera_degradation_health_score.md` | Đưa phạm vi cụ thể vào README/báo cáo |
| Tài liệu nguồn | PDF DRIVE-C, URL repo và dataset trong notebook | Đọc/đối chiếu nguồn; ghi input/output, phương pháp, limitation và thông tin xuất bản |
| Code và lịch sử chạy | `test-drivec.ipynb`, có output tải dữ liệu/nạp checkpoint/inference | Kiểm tra chạy lại, lưu phiên bản môi trường và cấu hình thực tế |
| Kết quả | `phn_24_results.csv`: 24 dòng; `phn_per_frame.csv`: 192 dòng, 8 frame/clip | Tổng hợp so sánh theo từng cảnh; không coi 192 frame là 192 cảnh độc lập |
| Plot | `phn_curve.png` | Kiểm tra nhãn, bổ sung plot metric thủ công nếu cần |
| Truy vết dữ liệu | `fetch_sha256.txt` | Ghi nguồn tải, cách chọn clip/frame; hash không thay thế dữ liệu hay ảnh minh chứng |
| Ảnh trước/sau | Notebook có cell xuất `phn_grid.png`; chưa thấy file này ở gốc | Xuất và lưu grid hoặc cặp ảnh cùng frame |
| Phân công | 4 file `01_...md` đến `04_...md` | Điền tên/MSSV; cập nhật thiết kế đề xuất Gaussian blur sang motion blur của DRIVE-C |
| Hồ sơ nộp | Chưa có README, TEAMMATES và 4 báo cáo cá nhân ở gốc | Hoàn thiện, ghi repo URL và kiểm tra truy cập |

Đã kiểm tra tính nhất quán CSV: trung bình 8 frame so với cột kết quả nguồn đã làm tròn có chênh lệch tối đa khoảng **0,000599**. Notebook lưu output khoảng **0,000626** khi so với metadata trước làm tròn. Hai cách kiểm tra dùng độ chính xác khác nhau; cần lưu bảng đối chiếu không làm tròn khi chạy lại. Khớp số là kiểm tra tái hiện, chưa xác nhận model đánh giá đúng sensor health.

## 3. Chốt đường chạy và đọc nguồn — Bước 2

Đường chạy chính: dùng notebook hiện có, nạp checkpoint tác giả, inference trên mẫu DRIVE-C; không huấn luyện model mới.

Thông tin lấy từ notebook, cần đối chiếu trực tiếp với nguồn trước khi đưa vào phần mô tả tác giả:

- Repository: <https://github.com/shiv-aher/drive-c-dataset>, tag `v1.0.1`, commit được log là `caf16657b87cec8518008b74c72dd0dcb6088eb6`.
- Dataset: <https://zenodo.org/records/19656444>, tải các clip cần dùng qua HTTP Range.
- Checkpoint: `epoch_021_best.pth`; SHA-256 ghi trong notebook và được kiểm tra khi nạp.
- Input của phép thử: 8 frame RGB mỗi clip, resize về 384 × 1280 cho model.
- Output đang sử dụng: health score, xác suất loại lỗi, severity dự đoán; metric thủ công đo trên frame 54 ở 1280 × 720.

Lần kiểm tra web khi lập kế hoạch chưa truy cập được URL tag GitHub. Các thông tin trên là thông tin trong artifact địa phương, chưa phải xác minh độc lập nguồn. Không dùng tuyên bố về dữ liệu huấn luyện, kiến trúc hay limitation của tác giả trước khi đọc đúng phần nguồn tương ứng.

**Phiếu đọc nguồn cần hoàn thành:** tên/tác giả/năm; URL đã đọc; input → output; kiến trúc/cách tạo health score; metric/dataset của nguồn; requirements; lệnh chạy; limitation nguồn thực sự nêu; limitation nhóm tự nhận định ghi riêng. Kiểm tra tiêu chí paper/repository mới theo yêu cầu môn học, không suy ra tính mới chỉ từ tên file PDF.

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

### Metric cố định trước khi tổng hợp

| Metric | Định nghĩa theo code hiện có | Thang/đơn vị | Giới hạn diễn giải |
| --- | --- | --- | --- |
| B — blur score | `var(Laplacian(grayscale))`, OpenCV `CV_64F`, grayscale uint8 | Phương sai đáp ứng Laplacian trên thang pixel 0–255; không là đơn vị vật lý | Proxy độ sắc nét, phụ thuộc texture, exposure và kích thước ảnh |
| S_pct | `100 × mean((gray >= 250) OR (gray <= 5))` | % pixel | Tỷ lệ ở hai đầu thang sáng; gồm pixel tối, không chỉ overexposure |
| H_bit | `−sum(p × log2(p))`, histogram grayscale 256 bin | bit | Entropy mức xám; không đo độ đúng của detector |
| gshi_pred_f54 | Health model dự đoán cho frame 54 | Không đơn vị, thang 0–1 theo notebook | Điểm model, cần xác minh chiều tốt/xấu từ nguồn |
| gshi_pred_tb8 | Trung bình health của 8 frame/clip | Như trên | Dùng kiểm tra tái hiện với kết quả clip của nguồn |

Không gọi `top1_prob` của model chẩn đoán lỗi là confidence của object detector. Không gọi `gshi_gt` là ground truth về độ tin cậy ADAS: notebook mô tả đây là nhãn tính từ severity, cần kiểm tra công thức ở nguồn.

### Phép phân tích và bằng chứng

1. Xác nhận baseline chạy được, log phiên bản thư viện, thiết bị, commit và checkpoint hash.
2. Chạy từng điều kiện, giữ nguyên tiền xử lý và model; lưu kết quả từng frame trước làm tròn.
3. Với mỗi scenario/loại lỗi, đặt clean cạnh 5 mức lỗi. Tính chênh lệch tuyệt đối so với clean; nếu dùng %, nêu công thức và tránh chia cho 0.
4. Vẽ B, S_pct, H_bit và health theo tham số lỗi, tách S01/S06 và từng corruption. Không yêu cầu mọi metric đều đơn điệu.
5. Lưu ít nhất một cặp ảnh baseline/degraded cùng frame, CSV và log tương ứng.
6. Kiểm tra số mẫu, ID, frame và metric; báo mẫu lỗi/thiếu thay vì bỏ âm thầm.

## 5. Failure case và quyết định kỹ thuật — Bước 5

**Failure case chính đã thấy trong CSV, cần gắn ảnh minh chứng:**

| Frame 54, cảnh S01 | B | gshi_pred_f54 |
| --- | --- | --- |
| Clean | 3544,1 | 0,1488 |
| Motion blur, kernel 13 px | 199,5 | 0,4075 |
| Motion blur, kernel 33 px | 14,3 | 0,0766 |

Quan sát: ở kernel 13 px, B giảm khoảng **94,4%** so với clean nhưng health tăng **0,2587**. Health không giảm đơn điệu theo mức blur trên mẫu này. Không giải thích nguyên nhân bằng kiến trúc, domain shift hoặc lỗi nhãn nếu chưa có kiểm chứng; ghi chúng là giả thuyết.

Ví dụ bổ sung: S06 clean có health 0,2794, underexposure nhẹ có thể lên 0,3286. Không kết luận toàn bộ ảnh đêm luôn bị chấm thấp hơn ảnh ngày; chính S06 clean có score cao hơn S01 clean.

**Đề xuất kỹ thuật để trình bày:** ghi log đa metric và cảnh/ngày đêm; dùng health model cùng B/S/H để phát hiện trường hợp bất đồng trước khi chọn quy tắc giảm trọng số camera. Chưa đặt một ngưỡng tuyệt đối áp dụng cho mọi cảnh từ hai scenario.

**Cách kiểm chứng vòng sau:** thử trên nhiều cảnh sạch/lỗi, chốt ngưỡng trên tập dev rồi kiểm tra tập khác; đo cảnh sạch bị cảnh báo nhầm và lỗi bị bỏ sót theo nhãn corruption. Nếu muốn kết luận về tính năng ADAS, chạy detector cùng cấu hình và có nhãn đối tượng để đánh giá. Kết quả chẩn đoán corruption vẫn không tự chứng minh detector an toàn.

Trade-off cần nêu: metric thủ công dễ tính nhưng phụ thuộc cảnh/exposure; model health có thể cần tài nguyên và vẫn sai trên mẫu cụ thể; ngưỡng theo ngữ cảnh cần thêm dữ liệu. Hiện chưa đo latency end-to-end, mAP hoặc hiệu quả fusion.

## 6. Phân công và lịch 120 phút theo hướng dẫn

| Giai đoạn | Khải — đội trưởng | Thành viên 2 — nguồn | Thành viên 3 — code | Thành viên 4 — kết quả/pitch |
| --- | --- | --- | --- | --- |
| 0–15: Chuẩn bị | Chốt claim, baseline, vai trò; ghi vấn đề nhóm 4 người | Kiểm tra nguồn đã có | Kiểm tra môi trường/notebook | Chuẩn bị bảng metric |
| 15–45: Nguồn và đường chạy | Chốt khả năng thực hiện, tránh mở rộng quá mức | Hoàn thành phiếu nguồn và trích dẫn | Setup, kiểm tra checkpoint/dữ liệu | Chuẩn bị khung 5 mục báo cáo |
| 45–95: Thiết kế và chạy | Theo dõi tiến độ, kiểm tra đối chứng | Đối chiếu tham số, định nghĩa metric | Chạy/lưu CSV, log và ảnh | Kiểm tra CSV, plot và chênh lệch |
| 95–115: Failure và cải tiến | Chốt engineering decision | Tách limitation nguồn/nhóm | Truy xuất mẫu và cấu hình failure | Hoàn thiện bảng/ảnh, câu chuyện trình bày |
| 115–120: Hoàn thiện | Kiểm tra rubric và tập pitch | Hoàn thiện bản cá nhân | Hoàn thiện bản cá nhân | Hoàn thiện bản cá nhân và slide chung |

Chuẩn bị khung báo cáo từ sớm để 5 phút cuối chỉ kiểm tra và tập nói. Các file phân công trước đây dùng mốc và Gaussian blur đề xuất; khi thực hiện ưu tiên lịch/cấu hình trong kế hoạch này, rồi đồng bộ lại các template.

## 7. Sản phẩm cần lưu và nộp — Bước 6–7

Giữ tên thư mục gốc hiện tại `K4-Track4-Day04-Seahorse-Sensor-Reality-Sprint`, phù hợp mẫu tên nhóm nếu tên chính thức là Seahorse. Không cần chuyển các artifact hiện có để bắt đầu.

| File/thư mục dự kiến | Nội dung bắt buộc |
| --- | --- |
| `README.md` | Problem, nguồn, môi trường, cách chạy, đường dẫn kết quả và giới hạn |
| `TEAMMATES.md` ở gốc | Khải và 3 thành viên thật với họ tên/MSSV; ghi vấn đề yêu cầu 5 người và cách xử lý được giảng viên xác nhận |
| `test-drivec.ipynb` | Code cùng output, cấu hình và kiểm tra tái hiện |
| `phn_24_results.csv`, `phn_per_frame.csv` | Số đo và ID/frame truy vết |
| `fetch_sha256.txt`, log chạy | Truy vết dữ liệu, commit/checkpoint/môi trường |
| `phn_curve.png`, `phn_grid.png`, plot bổ sung | Bảng/plot/ảnh có baseline, mức lỗi và nhãn đúng |
| `reports/<MSSV>_<HoTen>.md` | 4 bản cá nhân, mỗi bản có đủ 5 mục và dẫn bằng chứng chung |

Mỗi báo cáo gồm đúng luồng: **Problem → Method → Benchmark → Failure case → Engineering decision**. Có tên/MSSV, đóng góp cá nhân, URL repo, nguồn đã đọc, commit/version, dataset và cách chạy. Nếu VLearn yêu cầu định dạng khác Markdown, xuất sang định dạng được yêu cầu trước khi nộp.

Pitch 3–5 phút: khoảng 30 giây problem, 45 giây method, 90 giây benchmark, 45 giây failure, 45 giây decision. Mở được notebook/CSV/ảnh khi được hỏi. Mỗi người nộp bản riêng và cùng URL repository; kiểm tra truy cập sau khi gửi.

## 8. Tiêu chí hoàn thành

- [ ] **40% — Benchmark:** code chạy được, có baseline/5 mức lỗi, số đo, log và ảnh/plot truy vết.
- [ ] **25% — Failure thực tế:** chỉ đúng một mẫu lỗi, tham số, chênh lệch metric và giới hạn tác động tới tính năng.
- [ ] **20% — Thuật toán:** giải thích input/output, phương pháp, metric và limitation từ nguồn đã đọc.
- [ ] **15% — Trade-off:** đề xuất liên hệ số đo, nêu rủi ro cảnh báo sai và phép thử kiểm chứng tiếp theo.
- [ ] Tách rõ **[NGUỒN]**, **[NHÓM ĐO]**, **[GIẢ THUYẾT]**; không trình bày số liệu nguồn như nhóm tự đo.
- [ ] README, TEAMMATES, tên/MSSV 4 người và 4 báo cáo cá nhân đầy đủ.
- [ ] Có xác nhận cách xử lý quy mô nhóm 4 người so với yêu cầu 5 người.
- [ ] Mỗi thành viên đã nộp và mở lại được bản riêng cùng bằng chứng chung trên VLearn.

Thứ tự thực hiện tiếp theo: **đọc/đối chiếu nguồn → hoàn thiện cấu hình và kiểm tra chạy → bổ sung ảnh/plot → viết failure/decision → hoàn thiện repo và 4 báo cáo → pitch/nộp riêng**.
