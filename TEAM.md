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
- Vòng QC và số ảnh đã duyệt / cả lô: Vòng 1, 40/40 ảnh (phiếu là bản nháp AI do 052 chấp nhận)
- Tỉ lệ lỗi: 77.5% theo ảnh (31/40), 18.1% theo đối tượng (56/309), thêm 19 vật bỏ sót
- **Quyết định** (Release / Hold / Rework) và lý do một dòng: **Hold**: còn box `can_review` và tỉ lệ lỗi 77.5% > 2%; nhãn chưa đủ chất lượng bàn giao, chỉ dùng làm bằng chứng thực hành
