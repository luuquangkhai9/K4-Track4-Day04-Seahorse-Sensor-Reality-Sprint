# Pitch Seahorse — demo camera health trên bốn clip

**Mục tiêu:** 3–5 phút; phân bổ gợi ý **4 phút 15 giây**. Đây là thời lượng dự kiến, nhóm cần tự tập nói và bấm giờ. Không cần chạy model trực tiếp khi trình bày; mở bằng chứng đã lưu.

## Thứ tự và hình cần mở

| Người | Thời lượng | Phần | Bằng chứng |
| --- | ---: | --- | --- |
| Lưu Quang Khải | 30 giây | Problem, claim | README / thiết kế demo |
| Lê Hưng | 45 giây | Method, hai nguồn | PAPER_CODE_MAPPING |
| Đặng ĐỈnh Đoàn | 60 giây | Benchmark và tái hiện | CSV, manifest và run.log |
| Nguyễn Hồ Nam | 75 giây | Kết quả và failure | image_grid, metric_curves |
| Lưu Quang Khải | 45 giây | Decision và trade-off | ENGINEERING_DECISION |

## 1. Khải — Problem

“Nhóm Seahorse chọn T1, giám sát chất lượng camera trong bối cảnh xe ADAS. Một camera vẫn có thể gửi hình nhưng ảnh bị nhòe, khiến dữ liệu đầu vào kém đáng tin. Nhóm kiểm tra câu hỏi: khi mức motion blur tăng trên cùng cảnh, blur score và health score có giảm nhất quán không? Chúng em dùng một demo nhỏ có baseline và ba mức lỗi để xác nhận đường chạy và phân tích một ngoại lệ.”

## 2. Hưng — Method

“Nhóm dùng hai nguồn của Shiva Aher. Bài camera reliability giới thiệu GSHI và mô hình EfficientNet-B2 nhiều nhánh. Bài DRIVE-C cung cấp clip sạch và các biến thể corruption có đối chứng. Nhóm chạy checkpoint PerceptionHealthNet phát hành cùng DRIVE-C. Code thực tế lấy health từ một nhánh dự đoán trực tiếp; nhãn gshi_gt được tính từ severity. Vì vậy, công thức nhãn giảm đều không bảo đảm health dự đoán từ ảnh cũng giảm đều. Nhóm đã ghi bảng đối chiếu paper với code và phân biệt kết quả nguồn với số nhóm đo.”

## 3. Đoàn — Benchmark

“Bộ thử mới có bốn clip của cảnh S01: clean, blur s1, s2 và s5, với kernel 11, 13 và 33 pixel. Mọi clip dùng cùng model, preprocessing và sampling. Mỗi clip lấy tám frame cho health, tổng 32 output; ba metric ảnh đo tại cùng frame 54 gồm phương sai Laplacian, tỷ lệ pixel rất tối hoặc rất sáng và entropy mức xám.

Nhóm chạy trên CPU, đã xác minh source commit, hash checkpoint và dữ liệu. Chênh lệch health trung bình clip với metadata nguồn lớn nhất là khoảng 0,000323, dưới ngưỡng 0,001. Tổng forward khoảng 7,2 giây; chạy lại toàn script khi đã cache mất khoảng 13,3 giây, chưa gồm tải dữ liệu lần đầu. CSV, log và manifest có thể mở để kiểm tra.”

## 4. Nam — Kết quả và failure case

**Mở image_grid trước, rồi metric_curves.**

“Ảnh trước/sau cho thấy các biến thể blur trên cùng cảnh và frame. Blur score B giảm từ khoảng 3544 ở clean xuống 293, 199 và 14. Nhưng health frame 54 tăng từ 0,1488 lên 0,2760 rồi 0,4075, sau đó mới giảm còn 0,0766.

Failure case chính là s2: B giảm khoảng 94,37% so với clean, trong khi health tăng khoảng 0,2587. Health trung bình tám frame cũng tăng, nên ngoại lệ không chỉ nằm ở một frame đã chọn. Trên ba mức đã chạy, health không giảm đơn điệu.

Điều này cho thấy cách xếp chất lượng chỉ theo health chưa nhất quán trên mẫu này. Nhóm chưa chạy detector nên không kết luận mAP giảm. Các biến thể còn khác một số tham số PSF, không chỉ kernel; kết quả phản ánh các mức corruption DRIVE-C đã chọn. Một cảnh không đủ khái quát cho ngày/đêm hoặc toàn dataset.”

## 5. Khải — Engineering decision

“Nhóm đề xuất dùng health như một tín hiệu giám sát bổ sung, ghi log cùng B, tỷ lệ pixel và entropy, rồi đánh dấu các mẫu bất đồng để kiểm tra trước khi chọn ngưỡng giảm trọng số camera. Trade-off là metric ảnh dễ tính nhưng phụ thuộc nội dung và ánh sáng; model health có thêm tín hiệu nhưng vẫn có ngoại lệ.

Bước kiểm chứng tiếp theo là chọn ngưỡng trên nhiều cảnh hiệu chỉnh, đo cảnh báo nhầm và lỗi bỏ sót trên tập khác. Nhóm chưa chứng minh hiệu quả của quy tắc kết hợp. Demo hiện tại đã xác nhận tính khả thi, có số đo và một failure case kiểm tra được.”

## Câu hỏi có thể gặp

| Câu hỏi | Trả lời ngắn |
| --- | --- |
| Sao chỉ chạy bốn clip? | Mục tiêu là demo khả thi trong thời gian LAB; có clean và ba mức lỗi. Giới hạn một cảnh được nêu rõ. |
| Có tự tạo corruption không? | Nhóm sử dụng các biến thể DRIVE-C phát hành, đã kiểm tra hash; không thêm blur lần hai. |
| gshi_gt có phải health thật không? | Là nhãn từ công thức severity, không phải phép đo độc lập hoặc mAP detector. |
| Vì sao health tăng? | Chưa phân lập nguyên nhân. Đó là quan sát; domain shift/cảnh/calibration chỉ là giả thuyết. |
| Paper nói blur theo severity tốt, sao nhóm thấy sai? | Paper tổng hợp nhiều cảnh/clip, nhóm xem một cảnh và frame. Số trung bình không bảo đảm mọi mẫu đơn điệu. |
| Kết hợp nhiều metric có chắc tốt hơn không? | Đây là đề xuất kiểm chứng; chưa báo cải thiện khi chưa đo quy tắc mới. |
| Lead 0,47 có nghĩa 0,47 giây không? | Không, là khoảng cách trên trục severity trong thí nghiệm tác giả; demo này chưa đo lead. |
| Chạy lại thế nào? | `python scripts/stage3_small_demo.py --threads 4`, source/data tự cache; xem STAGE2_REPORT để setup. |

## Checklist tập nói

- [ ] Mỗi người đọc và hiểu phần của mình; nhóm tự bấm giờ đạt 3–5 phút.
- [ ] Mở sẵn ảnh, plot, CSV và log; biết vị trí dòng S01 s2.
- [ ] Nói “nhóm đo” / “nguồn báo cáo” / “giả thuyết” đúng chỗ.
- [ ] Không đổi các số theo trí nhớ, không gọi timing cached là thời gian tải + chạy lần đầu.
- [ ] Chuẩn bị bản riêng và link repo của từng người trước khi nộp.
