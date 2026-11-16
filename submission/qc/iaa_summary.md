# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 3
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 291 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 291 | 0.994 | 99.0% | 100.0% | 100.0% | 10/35 | 0 | ĐẠT |
| 052|053 | 13 | 113 | 0.995 | 99.1% | 100.0% | 100.0% | 3/5 | 0 | ĐẠT |
| 052|345 | 13 | 114 | 0.999 | 99.1% | 100.0% | 100.0% | 3/21 | 0 | ĐẠT |
| 053|345 | 14 | 64 | 0.982 | 98.4% | 100.0% | 100.0% | 4/9 | 0 | ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 60 ({'bo_sot_thua': 45, 'iou_thap': 4, 'sai_lop': 3, 'co_can_review': 8}), trên 21 ảnh cần calibration.
