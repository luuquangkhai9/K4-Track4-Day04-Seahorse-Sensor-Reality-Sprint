# Failure case và quyết định kỹ thuật — Seahorse

## 1. Failure case được chọn

**ID:** S01_motion_blur_s2, frame 54; đối chứng S01_clean frame 54. Nguồn số là [benchmark_summary.csv](../outputs/stage3_small/benchmark_summary.csv) của lần chạy CPU mới, không phải số paper hoặc bảng 24 clip lịch sử.

| Số đo | Clean | Motion blur s2 | Chênh lệch |
| --- | ---: | ---: | ---: |
| B — phương sai Laplacian | 3544,1384 | 199,4923 | −94,37% |
| Health frame 54 | 0,148770 | 0,407456 | +0,258686 |
| Health trung bình 8 frame | 0,221979 | 0,356979 | +0,135000 |

![Cùng cảnh và frame với clean/ba mức blur](../outputs/stage3_small/image_grid.png)

**[NHÓM ĐO]** Ảnh s2 nhòe hơn theo proxy B, trong khi model chấm health cao hơn clean. Health cũng tăng từ s1 lên s2, cả ở frame54 và mean8. Việc này làm cách xếp chất lượng chỉ theo health không nhất quán với mức corruption trên mẫu đã chạy.

**[NGUỒN]** DRIVE-C Table 3 trang 7 cho thấy correlation motion blur tương đối tốt khi tổng hợp nhiều cảnh. Số trung bình đó không bảo đảm từng cảnh/frame đơn điệu. Bài phương pháp phân biệt nhánh health trực tiếp và health có cấu trúc; code đang chạy dùng nhánh trực tiếp. Xem [PAPER_CODE_MAPPING.md](PAPER_CODE_MAPPING.md).

**[GIẢ THUYẾT]** Nội dung cảnh, miền dữ liệu hoặc sự hiệu chỉnh nhánh health có thể góp phần gây ngoại lệ. Chưa có phép thử phân lập nguyên nhân, nên không khẳng định model đã nhầm một loại lỗi cụ thể hoặc checkpoint sai.

## 2. Tác động tới tính năng

**Tác động được demo chỉ ra:** thứ tự health không phản ánh nhất quán biến thể blur đã chọn. Nếu một tính năng chọn ảnh/giảm trọng số dựa duy nhất vào thứ tự health, nó có thể ưu tiên ảnh s2 hơn clean trong trường hợp này.

**Suy luận kỹ thuật, chưa đo:** ngưỡng health tuyệt đối có thể gây cảnh báo nhầm hoặc bỏ sót khi điểm không được hiệu chỉnh. Nhóm chưa triển khai cảnh báo và chưa đo false-positive/false-negative của quy tắc cụ thể. Chưa chạy object detector nên chưa kết luận mAP giảm bao nhiêu.

## 3. Quyết định đề xuất

**Dùng health như tín hiệu giám sát bổ sung; ghi log đa metric và đánh dấu mẫu bất đồng để kiểm tra trước khi hiệu chỉnh một quy tắc giảm trọng số camera.**

| Hành động đề xuất | Cơ sở | Phạm vi hiện tại |
| --- | --- | --- |
| Log scenario/frame, severity/PSF, health, B/S/H, version model và timestamp | Cần truy nguyên mẫu s2 bất đồng | Artifact offline của demo đã có; chưa tích hợp logger vào ADAS |
| Kiểm tra mẫu health tăng trong khi proxy độ nét giảm | S01 s1→s2 thể hiện bất đồng | Đã phân tích offline; chưa hiệu chỉnh threshold cảnh báo |
| Chọn ngưỡng trên nhiều cảnh clean/lỗi trước khi down-weight | Một cảnh không đại diện mọi texture/exposure | Đề xuất vòng sau, chưa benchmark cải tiến |
| Có detector và nhãn nếu đánh giá lợi ích cho tính năng | Metric ảnh không tự chứng minh chất lượng detector | Chưa thực hiện trong LAB nhỏ |

Không lấy ngưỡng Healthy/Degraded/Critical 0,9/0,6 của paper như ngưỡng đã được xác thực trên DRIVE-C. Không gán một công thức trộn B/S/H tùy ý rồi gọi đó là health an toàn.

## 4. Trade-off

- B/S/H dễ tính, nhưng phụ thuộc texture/exposure và không phản ánh rủi ro của mọi vùng ảnh. Tăng độ nhạy cảnh báo có thể làm ảnh clean ít texture bị gắn cờ.
- Health model bổ sung thông tin học được, nhưng trên mẫu này có thứ tự bất nhất. Cần thêm dữ liệu hiệu chỉnh; đo CPU demo chưa xác lập ngân sách latency end-to-end.
- Bốn clip đủ chứng minh đường chạy và ngoại lệ, không đủ chọn threshold hoặc đo lợi ích fusion. Mức mẫu được chọn có chủ đích sau khi đã thấy kết quả lịch sử.
- Metadata thay n_points/accel/linear/PSF smoothing cùng severity; kết luận theo biến thể blur DRIVE-C, không tách được tác động riêng kernel.

## 5. Phép thử kiểm chứng tiếp theo

Đây là kế hoạch, không cần chạy thêm để hoàn thành LAB hiện tại:

1. Thu thập nhiều cảnh sạch/lỗi với texture/exposure đa dạng; tách cảnh cho tập hiệu chỉnh và tập kiểm tra. Nếu có ngưỡng ngày/đêm, tập hiệu chỉnh phải có cả hai.
2. Chốt trước định nghĩa cảnh báo theo nhãn corruption và cách dùng đa metric. Chọn threshold trên tập hiệu chỉnh; đánh giá cảnh clean bị gắn cờ và cảnh lỗi bị bỏ sót trên tập khác.
3. So quy tắc mới với health-only, báo cùng mẫu và điều kiện. Chỉ nói cải thiện khi có số đo hỗ trợ.
4. Để đánh giá tính năng ADAS, bổ sung detector/nhãn và đo task metric theo cùng điều kiện; nếu đo cảnh báo sớm, phân biệt khoảng cách severity với thời gian thực.

## 6. Kết luận dùng khi trình bày

“Demo bốn clip xác nhận pipeline chạy được trên CPU và tái hiện gần số nguồn. Trên cảnh S01, health trực tiếp chưa xếp chất lượng theo thứ tự biến thể blur; vì vậy nhóm đề xuất ghi log đa metric và kiểm tra bất đồng trước khi chọn ngưỡng giảm trọng số camera. Hiệu quả cải tiến và tác động lên detector cần phép thử bổ sung.”
