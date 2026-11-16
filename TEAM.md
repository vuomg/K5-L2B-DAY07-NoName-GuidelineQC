# Thông tin nhóm

- Tên nhóm: NoName
- Mã thành viên (ba chữ số): 052, 053, 345
- Người điều phối: 052 (đồng thời sửa nhãn calibration trong CVAT)
- Người review bản cuối: 053 (kiểm lại calibration và review QC vòng 1); 345 viết báo cáo QC
- Commit chốt bài (điền ở kênh nộp sau khi commit):

## Kết quả tóm tắt (điền cuối bài)

- Lượt gán hoàn tất / được giao: 80/80 (052: 26, 053: 27, 345: 27 ảnh; 2 người/ảnh)
- IAA trước calibration (kèm mẫu số): IoU TB 0.994, đồng thuận lớp 99.0% trên 291 cặp box ghép. **Không dùng được để đánh giá đồng thuận**: 85–96% box trùng tọa độ tuyệt đối giữa các cặp người gán (`submission/qc/independence_check.md`), và cả 627 box để mặc định `occluded_level=0`, `truncated=no`.
- Số ảnh phải calibration: 21 / 40 ảnh bị cờ (60 ca); phạm vi sửa 40 / 40 vì v1.1 là thay đổi semantic
- Vòng QC và số ảnh đã duyệt / cả lô: <<chờ vòng 1>>
- Tỉ lệ lỗi: <<…% theo ảnh (…/…), …% theo đối tượng (…/…)>>
- **Quyết định** (Release / Hold / Rework) và lý do một dòng: <<chờ qc_report.py vòng 1>>
