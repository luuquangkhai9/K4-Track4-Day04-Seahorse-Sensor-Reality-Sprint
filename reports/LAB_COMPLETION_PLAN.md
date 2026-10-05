# Kế hoạch hoàn thành LAB — trạng thái cuối

**Phạm vi thống nhất:** T1, xe ADAS, camera/motion blur; **4 clip S01 clean + s1/s2/s5**, không chạy lại 24 clip. Nhóm 4 người đã được giảng viên chấp thuận theo thông tin đội trưởng. Kế hoạch ban đầu được giữ trong [LAB_PLAN_HISTORY.md](../docs/LAB_PLAN_HISTORY.md).

## Các giai đoạn

| Giai đoạn | Trạng thái hiện tại | Bằng chứng |
| --- | --- | --- |
| 1 — Chốt bài toán và phân công | Đã có claim, baseline, metric, tên và vai trò 4 người; thiếu hai MSSV | [Thiết kế](../docs/BENCHMARK_DESIGN.md), [TEAMMATES](../TEAMMATES.md) |
| 2 — Nguồn và baseline | Đã đọc hai paper, đối chiếu code, chạy S01 clean trên CPU | [Mapping](PAPER_CODE_MAPPING.md), [báo cáo](../docs/STAGE2_REPORT.md) |
| 3 — Demo nhỏ | PASS 4 clip/32 health-frame, có CSV/log/ảnh/plot/provenance | [Báo cáo](../docs/STAGE3_REPORT.md), [manifest](../outputs/stage3_small/run_manifest.json) |
| 4 — Failure và quyết định | Đã soạn failure/decision, bốn báo cáo riêng và pitch | [Báo cáo](../docs/STAGE4_REPORT.md), [quyết định](ENGINEERING_DECISION.md), [pitch](PITCH.md) |
| 5 — Rà hồ sơ/repository | Đã kiểm tra số/ảnh/liên kết, bổ sung setup CPU/submodule và hướng dẫn chạy nhỏ; còn thông tin cá nhân | [Nghiệm thu](../docs/STAGE5_REPORT.md), [kiểm tra](../outputs/submission_check/verification.json) |
| Nộp và trình bày | Người dùng thực hiện chia sẻ repo, tập nói và các lượt nộp riêng | [Checklist](SUBMISSION_CHECKLIST.md) |

Giai đoạn 5 của nhóm hoàn thiện Bước 6–7 trong hướng dẫn. Không tự ghi nhận đã diễn tập, đẩy GitHub hoặc nộp VLearn.

## Đối chiếu nội dung bắt buộc

- [x] Nền tảng, tính năng, sensor và failure đủ hẹp để đo.
- [x] Hai nguồn, commit/checkpoint/dataset, input/output, công thức metric và limitation.
- [x] Cùng pipeline trên baseline và ba mức lỗi; 32 output health và bốn ảnh metric.
- [x] Số đo mới trên CPU, log/manifest/ảnh/plot; kiểm tra mean8 với nguồn dưới 0,001.
- [x] Failure s2: B giảm 94,37%, health tăng cả f54/mean8; quan sát tách khỏi giả thuyết.
- [x] Engineering decision dựa trên kết quả và trade-off; đề xuất chưa được benchmark cải tiến.
- [x] Bốn bản cá nhân theo Problem → Method → Benchmark → Failure case → Engineering decision.
- [x] Pitch phân vai dự kiến 4 phút 15 giây, Q&A và file minh chứng để mở.
- [x] README ưu tiên demo nhỏ; setup riêng; cấu hình submodule và quy tắc LF giữ hash.
- [x] Tái tính metric từ ảnh và kiểm tra toàn bộ liên kết Markdown ở gốc/reports.
- [ ] Bổ sung MSSV của Lê Hưng và Đặng ĐỈnh Đoàn.
- [ ] Mỗi thành viên xác nhận đóng góp thực tế/rà báo cáo.
- [ ] Nhóm tập pitch, bấm giờ 3–5 phút.
- [ ] Người dùng chia sẻ các file mới lên repo, kiểm tra truy cập.
- [ ] Bốn người tự nộp bản riêng và cùng URL repo trên VLearn, mở lại kiểm tra.

Rubric nội dung đã có bằng chứng cho benchmark 40%, failure 25%, phương pháp 20%, trade-off 15%. Đây là tự đối chiếu hồ sơ, không phải điểm đã chấm.

## Lệnh kiểm tra trước chia sẻ

```powershell
python scripts/verify_submission.py
python scripts/verify_submission.py --require-personal-details
git diff --check
git status --short
```

Lệnh đầu kiểm tra nội dung kỹ thuật và báo thông tin cá nhân còn thiếu. Lệnh có `--require-personal-details` trả mã lỗi 2 khi còn chỗ trống; không thay dữ liệu thật bằng placeholder để đạt kiểm tra. Không cần chạy thêm inference khi kết quả đã đạt.
