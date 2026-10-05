# Đối chiếu hai bài báo với triển khai LAB

**Phụ trách trong nhóm:** Lê Hưng; Khải rà nội dung, Đặng ĐỈnh Đoàn xác minh đường chạy.  
**Bản source được kiểm tra:** tag `v1.0.1`, commit `caf16657b87cec8518008b74c72dd0dcb6088eb6` trong clone riêng `.lab_cache/drive-c-source`. Các file model, inference, training, GSHI, taxonomy, analysis và metadata khớp byte với bản sao `drive-c-dataset/` ở gốc tại lúc kiểm tra. Không suy ra commit nguồn từ repository nhóm.

## 1. Nguồn thực sự đã đọc

| Nguồn | Phiên bản | Vai trò |
| --- | --- | --- |
| [Safety-Critical Camera Reliability Monitoring for ADAS via Degradation-Aware Uncertainty Pattern Analysis](<Safety-Critical Camera Reliability Monitoring for ADAS via Degradation-Aware Uncertainty Pattern Analysis.pdf>) | Shiva Aher; arXiv:2605.05439v1, 06/05/2026; PDF 10 trang | Phương pháp GSHI và model giám sát; thí nghiệm KITTI/DAWN |
| [DRIVE-C: A Controlled Corruption Dataset for Autonomous Driving](<DRIVE-C A Controlled Corruption Dataset for Autonomous Driving.pdf>) | Shiva Aher; arXiv:2605.09774v1, 10/05/2026; PDF 9 trang | Dataset có đối chứng và baseline trên 610 clip; trích dẫn bài phương pháp ở [12] |
| [Source DRIVE-C](https://github.com/shiv-aher/drive-c-dataset/tree/v1.0.1) | Commit cố định ở trên | Mô tả chính xác triển khai/checkpoint dùng cho LAB |
| [Dataset Zenodo](https://doi.org/10.5281/zenodo.19656444) | Phiên bản theo DOI | Video clean/corrupted và metadata |

Hai PDF ghi trạng thái preprint/đang phản biện ở thời điểm của bản đó. Không gọi chúng là bài đã được tạp chí chấp nhận nếu chưa có bằng chứng khác.

## 2. Input → phương pháp → output

**Bài phương pháp:** một ảnh RGB → EfficientNet-B2 với nhiều head → presence, severity, health và spatial uncertainty. Depth hỗ trợ tạo dữ liệu huấn luyện cho một số loại suy giảm; không cần ở inference. Section V phân biệt health từ nhánh hồi quy trực tiếp với health có cấu trúc tính từ severity.

**DRIVE-C:** video thật đã ẩn danh → clip clean → 12 loại corruption × 5 mức → video và metadata. Mỗi clip có một loại corruption; clean và corrupted cùng cảnh/frame. Có 10 clean + 600 corrupted = 610 clip, 128 frame/clip; dev S01–S05, test S06–S10. Bản phát hành không cung cấp dense bbox/segmentation ground truth cho benchmark detector.

**LAB thực sự chạy:** các hàm của source đọc 8 frame/clip, resize RGB về H=384/W=1280, chia 255 → checkpoint PerceptionHealthNet ở eval → `pred_health` trực tiếp mỗi frame; trung bình số học cho clip. B/S/H đo trên frame 54 gốc 1280 × 720. Output chẩn đoán loại lỗi không phải output object detector.

## 3. Bảng đối chiếu chính

| Nội dung | PDF phương pháp | Source phát hành và tác động tới LAB |
| --- | --- | --- |
| Kiến trúc | Section V, trang 5–6: EfficientNet-B2, presence/severity/health/spatial head | [Model](drive-c-dataset/src/models/perception_health_net.py) có các head tương ứng; pixel head tạo lười khi forward lần đầu |
| Health trực tiếp | Eq. 12: H_net = sigmoid(health head) | `pred_health` được tính trực tiếp; đây là điểm notebook và CSV dùng |
| Health có cấu trúc | Eq. 2, 10: tích `(1-s_i)^(w_i * alpha_group)` | [GSHI code](drive-c-dataset/simulation/gshi_utils.py) tạo nhãn bằng công thức có beta và clipping; inference hiện tại không thay `pred_health` bằng tích severity |
| Công thức nhãn | Eq. 10, trang 5: tích cơ bản | `exp(beta * sum(w_i*q_i*log(clip(1-s_i))))`, beta=0,85, floor=0,001, ceil=0,99; [taxonomy](drive-c-dataset/configs/taxonomy/camera_issues.yaml). Clean được script gán 1,0 riêng |
| Training objective | Eq. 19, trang 6: năm loss, trọng số presence/severity/health/GSHI/pixel = 1/2/1/1/0,5 | [Training script](drive-c-dataset/scripts/train_perception_health_net.py): bốn term presence/severity/health/pixel; default 1/1/0,5/0,25, có pixel ramp và severity regularization. Không có term L_gshi riêng trong tổng loss đã đọc |
| Taxonomy | Trang 4: 12 mode, có vignetting và exposure shift | Model có vignetting; DRIVE-C không tạo vignetting, tách overexposure/underexposure và map về exposure_shift |
| Severity | KITTI evaluation trang 6: sweep 0,0–1,0 bước 0,1 | DRIVE-C dùng 0,08/0,18/0,35/0,55/0,75; thông số cụ thể lưu trong extra_json |
| Spatial uncertainty | Eq. 11, 13, 18: mask tổng hợp giám sát pixel output | `pred_pix` là map học theo supervision; notebook LAB hiện chưa đánh giá map, AUSE hoặc reliability theo bbox |
| Clip health | Bài phương pháp mô tả single-image monitor | [Inference script](drive-c-dataset/scripts/add_gshi_pred.py) trung bình 8 frame để ghi `gshi_pred`; frame54 và clip mean phải giữ riêng |

Khác biệt paper–code là quan sát về phiên bản đang có; chưa có bằng chứng xác định nguyên nhân hoặc chứng minh checkpoint này chính là model của mọi bảng thí nghiệm trong PDF. LAB mô tả **checkpoint baseline phát hành cùng DRIVE-C**, không tuyên bố tái hiện toàn bộ paper phương pháp.

## 4. Số liệu nguồn cần diễn giải đúng

| Số liệu [NGUỒN] | Nơi báo cáo | Cách dùng trong LAB |
| --- | --- | --- |
| Health MAE 0,064 | Paper phương pháp, Table VI trang 8 | So với target severity-derived trên KITTI; không phải MAE nhóm trên DRIVE-C |
| Issue mAP 0,891 | Table VI | Nhận diện loại degradation; không phải mAP phát hiện xe/người |
| Early-warning 0,47 ± 0,25 | Table III trang 7 | Tính trên 7 mode đạt detector failure threshold; đơn vị severity, không phải giây |
| Warning H<0,8; failure mAP giảm tương đối 20% | Eq. 21–22, trang 6–7 | Protocol của tác giả. Nhóm chưa chạy YOLOv8 với nhãn để đo protocol này |
| Balanced accuracy 84,2% trên DAWN | Trang 8 | Weather recognition zero-shot; tác giả trang 9 nêu chưa hiệu chỉnh GSHI với health ground truth thực tế |
| 440,5 FPS | Table VII trang 9 | RTX 5090, 224 × 224, batch 1, 50 warm-up và 300 forward; không gán cho máy CPU hoặc input 384 × 1280 |
| Pearson 0,339 / Spearman 0,341 | DRIVE-C, Fig. 4 và trang 5 | Predicted health với gshi_gt trên 610 clip; không phải accuracy |
| Motion blur r=0,73; underexposure r=0,77 | DRIVE-C, Table 3 trang 7 | Correlation theo loại lỗi trên 50 clip/loại; không bảo đảm từng frame/cảnh đơn điệu |
| 6/12 loại lỗi / monotonic fraction 0,475 | DRIVE-C trang 5/7 và [analysis script](drive-c-dataset/scripts/analyze_gshi_pred.py) | 6/12 xét mean qua cảnh; 0,475 xét từng cặp scenario–corruption; đều s1–s5, không gồm clean |

Health target giảm theo severity là tính chất thiết kế công thức. Nhánh hồi quy từ ảnh không được bảo đảm đơn điệu bởi tính chất đó. Correlation với target, correlation với detector mAP và sai số health là ba phép đánh giá khác nhau.

## 5. Giới hạn nguồn và giới hạn phép thử nhóm

**Nguồn nêu:** Paper phương pháp Section VII trang 9 giới hạn synthetic-to-real, thiếu continuous health labels ngoài thực tế, ngưỡng 0,9/0,6 cần hiệu chỉnh, thiếu fault modes và temporal integration. GSHI là tín hiệu bổ sung, không phải cơ chế functional safety độc lập. DRIVE-C trang 5, 7–8 nêu ít cảnh/buổi quay, thiếu multi-sensor/dense labels, imbalance, tất cả cảnh đêm ở test, false positives trên clean và thiếu corruption tổ hợp.

**Nhóm tự giới hạn:** 24 clip được chọn, chỉ hai cảnh có đủ mức lỗi, B/S/H chỉ đo một frame/clip. 192 frame health không phải 192 cảnh độc lập. Chưa đo detector, fusion, lợi ích down-weighting hoặc latency end-to-end. Không dùng ngưỡng paper để gán camera thật là nguy hiểm từ tập mẫu này.

## 6. Đường chạy tối thiểu và bàn giao

Giai đoạn 2 sử dụng [scripts/stage2_smoke_test.py](scripts/stage2_smoke_test.py) với một clip thật S01 clean, 8 frame, đúng preprocessing và checkpoint. Chạy:

```powershell
python scripts/stage2_smoke_test.py
```

Script kiểm tra commit/hash, import đúng source, độ dài video, output hợp lệ và sai lệch mean8 với metadata nguồn dưới `1e-3`. Kết quả và log nằm ở `outputs/stage2/`. Các thư mục source/data cache nằm trong `.lab_cache/`, không đưa vào Git; checkpoint có sẵn ở `drive-c-dataset/checkpoints/`.

Giai đoạn 3 dùng [test-drivec.ipynb](test-drivec.ipynb) để chạy đầy đủ 24 clip sau khi smoke test đạt. Nếu chuyển Kaggle/Colab, ghi lại môi trường và hardware của phiên đó, giữ nguyên frame/model/metric. File [configs/benchmark.json](configs/benchmark.json) hiện là đặc tả đối chiếu, chưa được notebook tự đọc.

**Mẫu câu Method:** “Nhóm sử dụng PerceptionHealthNet checkpoint phát hành cùng DRIVE-C để dự đoán health trên một tập con các clip sạch và corruption có đối chứng. Phương pháp GSHI được tham khảo từ bài camera reliability; triển khai và công thức nhãn được đối chiếu với phiên bản source cố định. Nhóm đo health cùng ba metric ảnh, chưa tái hiện thí nghiệm detector-coupled early warning.”
