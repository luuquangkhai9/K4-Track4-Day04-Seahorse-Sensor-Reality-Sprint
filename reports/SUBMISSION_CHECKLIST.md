# Hồ sơ trình bày và nộp LAB — Seahorse

## Bốn bản riêng

| Người nộp | MSSV | Báo cáo Markdown | Cần bổ sung |
| --- | --- | --- | --- |
| Lưu Quang Khải | 2A202602599 | [Bản của Khải](reports/2A202602599_LuuQuangKhai.md) | Đóng góp thực tế, rà nội dung |
| Lê Hưng | Chờ bổ sung | [Bản của Hưng](reports/LeHung.md) | MSSV, đóng góp thực tế, rà nội dung |
| Đặng ĐỈnh Đoàn | Chờ bổ sung | [Bản của Đoàn](reports/DangDinhDoan.md) | MSSV, đóng góp thực tế, rà nội dung |
| Nguyễn Hồ Nam | 2A202602788 | [Bản của Nam](reports/2A202602788_NguyenHoNam.md) | Đóng góp thực tế, rà nội dung |

Các bản đã có đủ năm mục và bằng chứng benchmark. Nội dung chung được soạn từ kết quả nhóm; mỗi người cần ghi phần thực sự đã làm, không tự nhận toàn bộ công việc hỗ trợ. MSSV còn thiếu không được tự tạo.

## URL và bằng chứng chung

- URL repository dùng cho cả bốn người: <https://github.com/luuquangkhai9/K4-Track4-Day04-Seahorse-Sensor-Reality-Sprint>.
- [TEAMMATES.md](TEAMMATES.md): đủ bốn tên, chấp thuận nhóm 4 người; thiếu hai MSSV.
- [STAGE3_REPORT.md](STAGE3_REPORT.md): kết quả chính của demo mới bốn clip.
- [ENGINEERING_DECISION.md](ENGINEERING_DECISION.md): failure, tác động, giới hạn và đề xuất.
- [PITCH.md](PITCH.md): kịch bản phân vai 3–5 phút và Q&A.
- [CSV](outputs/stage3_small/benchmark_summary.csv), [log](outputs/stage3_small/run.log), [manifest](outputs/stage3_small/run_manifest.json), [plot](outputs/stage3_small/metric_curves.png), [ảnh](outputs/stage3_small/image_grid.png).

## Trước khi nộp

- [x] Đã kiểm tra số liệu/ảnh/bảng báo cáo và liên kết cục bộ; xem [nghiệm thu](STAGE5_REPORT.md) và [kết quả kiểm tra](outputs/submission_check/verification.json).
- [x] Đã bổ sung hướng dẫn CPU cho checkout mới, setup và cấu hình submodule đúng nguồn.
- [ ] Bổ sung MSSV của Hưng/Đoàn vào TEAMMATES, file công việc và bản riêng tương ứng.
- [ ] Mỗi người rà bản riêng và ghi đóng góp thực tế có file/commit hỗ trợ.
- [ ] Tập pitch và bấm giờ đạt 3–5 phút; chuẩn bị mở ảnh/CSV/log khi được hỏi.
- [ ] Các file mới đã được chia sẻ lên repository người chấm truy cập được. Việc tạo file cục bộ chưa có nghĩa chúng đã xuất hiện trên GitHub.
- [ ] Mở URL repo và bản riêng trong một phiên không đăng nhập để kiểm tra quyền truy cập nếu repo dùng công khai; nếu repo riêng, đảm bảo người chấm có quyền.
- [ ] Xác nhận định dạng tệp VLearn chấp nhận. Nếu cần DOCX/PDF/PPTX thì xuất từ nội dung Markdown đã rà, giữ bảng/ảnh và nguồn.
- [ ] Mỗi người nộp đúng bản của mình và cùng URL repo; ghi rõ đường dẫn `reports/...` tương ứng.
- [ ] Mở lại tệp/link sau nộp; kiểm tra metric, failure case, engineering decision và ảnh/log vẫn tìm được.

Liên kết ảnh/file trong Markdown là tương đối theo cấu trúc repo. Nếu nộp một file Markdown tách khỏi repo, link có thể không resolve; dùng bản trong repository hoặc định dạng xuất có ảnh đi kèm để người chấm đọc được.

Sau khi bổ sung thông tin cá nhân, chạy `python scripts/verify_submission.py --require-personal-details`. Trước khi dùng URL GitHub để nộp, người dùng cần commit/push các file mới rồi mở lại bốn đường dẫn báo cáo trên GitHub. Cache dữ liệu/model và bản render tạm không cần đưa vào repository nhóm; submodule lưu tham chiếu source đúng commit.

## Đối chiếu rubric bằng artifact

| Tiêu chí | Tỷ trọng | Bằng chứng đã chuẩn bị |
| --- | ---: | --- |
| Demo/benchmark chạy được | 40% | Script, bốn clip/32 health-frame, CSV/ảnh/log/manifest, hash và kiểm tra sai lệch |
| Hiểu failure thực tế | 25% | S01 blur s2: B giảm 94,37%, health tăng cả f54/mean8; ảnh cùng cảnh/frame; phạm vi suy luận |
| Giải thích thuật toán | 20% | Hai paper đúng vai trò; nhánh health trực tiếp, công thức nhãn, input/output và khác biệt code |
| Trade-off | 15% | Giới hạn một cảnh/PSF, texture/exposure, log đa metric, tập hiệu chỉnh/kiểm tra vòng sau |

Bảng này là tự đối chiếu nội dung, không phải điểm chấm hoặc cam kết đạt tỷ trọng tối đa.
