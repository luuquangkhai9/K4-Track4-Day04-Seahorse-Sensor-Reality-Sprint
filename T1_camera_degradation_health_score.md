# Chủ đề thực hành

## T1. Camera degradation health score

### Bối cảnh thực tế
Camera ADAS thường fail khi glare, night, rain, blur, rolling shutter hoặc lens bẩn. Nếu chỉ đưa ảnh vào detector, hệ thống không biết frame nào đáng tin.

### Gợi ý tìm paper/repo
Search keywords:

- camera image quality assessment for autonomous driving
- blur detection
- lens soiling detection
- nuScenes-C image corruption
- adverse weather perception

### Benchmark tối thiểu
Tạo 3–5 mức degradation trên ảnh hoặc video:

- blur
- brightness
- rain/noise

Đo các chỉ số:

- blur score
- saturation ratio
- entropy

Và nếu có thời gian, đo:

- detector confidence
- mAP proxy

### Output cần trình bày
Một bảng trước/sau degradation, bao gồm:

- metric health score
- nhận xét khi nào nên down-weight camera

### Challenge thêm
Thử:

- adaptive threshold theo daytime/nighttime; hoặc
- so sánh với VLM/vision model confidence.
