# Giai đoạn 5 — Hoàn thiện hồ sơ và kiểm tra repository

**Trạng thái:** Phần kỹ thuật/hồ sơ chung đã kiểm tra đạt. Chưa đủ điều kiện xác nhận bản nộp cuối vì còn hai MSSV và phần đóng góp thực tế trong báo cáo cá nhân.

## Việc hoàn thiện

- README ưu tiên đúng demo bốn clip, có problem/method/benchmark/failure/decision và hướng dẫn CPU từ checkout mới. Mô tả 24 clip cũ lưu trong [BENCHMARK_HISTORY.md](BENCHMARK_HISTORY.md), kế hoạch cũ trong [LAB_PLAN_HISTORY.md](LAB_PLAN_HISTORY.md).
- Thêm [requirements-demo.txt](requirements-demo.txt) từ môi trường thực tế và [setup_demo.py](scripts/setup_demo.py): clone source riêng, kiểm tra commit/cleanliness, lấy checkpoint thiếu từ commit đã chốt và kiểm tra hash; không chạy inference hay tải clip.
- Bổ sung `.gitmodules` cho gitlink DRIVE-C hiện có. `.gitattributes` giữ LF cho runner/config để hash còn khớp sau checkout trên Windows.
- Thêm [verify_submission.py](scripts/verify_submission.py), chạy không inference: kiểm tra provenance/config/runner hash, số mẫu/frame, mean8/f54/delta/sai lệch nguồn/đơn điệu; tái tính B/S/H từ PNG; kiểm tra bảng bốn báo cáo và các liên kết Markdown cục bộ.

## Kết quả kiểm tra thực tế

`python scripts/setup_demo.py`: PASS đúng commit và checkpoint SHA-256; không tải clip.

`python scripts/verify_submission.py`: PASS bằng chứng kỹ thuật, metric tái tính từ ảnh, bảng báo cáo và liên kết. Chi tiết: [verification.json](outputs/submission_check/verification.json).

Kiểm tra này không thay cho cài dependency trên máy mới, diễn tập thật, xác minh quyền xem GitHub hay lượt nộp VLearn. Script inference đã chạy thành công trước đó, không chạy lại chỉ để hoàn thiện tài liệu.

## Thông tin nhóm còn cần cung cấp

1. MSSV của Lê Hưng và Đặng ĐỈnh Đoàn để đồng bộ TEAMMATES/README/báo cáo/file công việc.
2. Đóng góp thực tế từng người; không tự nhận thay thành viên công việc chưa được xác nhận.

Sau khi điền, chạy `python scripts/verify_submission.py --require-personal-details`. Nhóm dùng [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) để chia sẻ và tự nộp. Chưa thực hiện commit/push thay người dùng hoặc đăng nhập/nộp VLearn.
