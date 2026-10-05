# Giai đoạn 4 — Failure, quyết định kỹ thuật và hồ sơ trình bày

**Trạng thái:** Đã chuẩn bị nội dung và bốn bản báo cáo cá nhân ở workspace, dựa trên demo mới bốn clip. Chưa tự xác nhận người trong nhóm đã rà/đóng góp, tập pitch, chia sẻ file lên GitHub hoặc nộp VLearn.

## Đầu ra đã tạo

- [ENGINEERING_DECISION.md](../reports/ENGINEERING_DECISION.md): failure S01 s2, quan sát/nguồn/giả thuyết, tác động đo được/suy luận, trade-off và phép thử cải tiến.
- [Báo cáo Khải](../reports/2A202602599_LuuQuangKhai.md).
- [Báo cáo Hưng](../reports/LeHung.md), MSSV chờ bổ sung.
- [Báo cáo Đoàn](../reports/DangDinhDoan.md), MSSV chờ bổ sung.
- [Báo cáo Nam](../reports/2A202602788_NguyenHoNam.md).
- [PITCH.md](../reports/PITCH.md): năm lượt nói cho bốn người, phân bổ 4 phút 15 giây, Q&A và hình cần mở.
- [SUBMISSION_CHECKLIST.md](../reports/SUBMISSION_CHECKLIST.md): bản đúng người, nguồn/bằng chứng chung và quy trình kiểm tra lượt nộp.

Các báo cáo đều đủ **Problem → Method → Benchmark → Failure case → Engineering decision**, có bảng số/ảnh/plot, hai nguồn, source commit/checkpoint, cách chạy và giới hạn. Mỗi bản có góc rà soát theo vai trò riêng; chỗ đóng góp thực tế cần thành viên xác nhận.

## Kết luận đã chốt để trình bày

**[NHÓM ĐO]** Bốn clip/32 output trên CPU chạy được, sai lệch mean8 với nguồn dưới 0,001. S01 s2 có B giảm 94,37% nhưng health f54 tăng 0,258686 và mean8 tăng 0,135000. Đây là ngoại lệ về xếp hạng health trên mẫu đã thử.

**[GIẢ THUYẾT]** Nguyên nhân liên quan cảnh/miền/calibration chưa được kiểm chứng. Mức blur thay nhiều tham số PSF nên không kết luận riêng tác động kernel. Chưa đo detector/mAP, early warning hoặc fusion.

**Engineering decision:** Log health và B/S/H, kiểm tra mẫu bất đồng trước khi hiệu chỉnh ngưỡng down-weight. Thử nhiều cảnh với tập hiệu chỉnh/kiểm tra riêng nếu muốn chứng minh cải tiến. Đề xuất chưa được triển khai thành bộ điều khiển hoặc benchmark thành quả tốt hơn.

## Việc còn lại trước khi hoàn tất toàn LAB

1. Bổ sung hai MSSV và đóng góp thực tế của từng người.
2. Cả nhóm đọc/rà bản riêng, tự tập pitch và bấm giờ.
3. Chia sẻ các artifact mới trong repository người chấm truy cập được; kiểm tra định dạng VLearn.
4. Bốn người tự nộp bốn bản và cùng URL repo, mở lại để kiểm tra.

Không cần chạy thêm bộ 24 clip để đáp ứng phạm vi demo nhỏ đã thống nhất.
