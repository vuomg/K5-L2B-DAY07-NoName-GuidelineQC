# Báo cáo QC — NoName

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Thực hành đặc tả và QC nhãn bbox 2D (người, phương tiện) trên 40 ảnh đường phố tuyển chọn. Không đại diện dữ liệu vận hành, không dùng để huấn luyện mô hình.
- Nguồn và phép sử dụng dữ liệu: Wikimedia Commons (CC BY / CC BY-SA / CC0 / public domain), ghi công trong `data/ATTRIBUTION.csv`.
- Manifest và checksum nhãn cuối: `batch_manifest.json`; `labels_calibrated.json` (40 ảnh, 309 box), SHA-256 `e5dc5770687292b5d07c011270d254c353c44b65796e36a6cdf1ed3c12a6280a`
- Guideline và taxonomy khi gán / khi bàn giao: Gán theo v1.0 (5 lớp + `ignore_region`). Bàn giao theo v1.1 (thay đổi semantic): thêm `bus`, `bicycle`; tuk-tuk/xe lam → `car`; vỏ xe, đồ lưu niệm không gán. Ngưỡng `rules` giữ nguyên.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 80/80 (2 người/ảnh; 052: 26, 053: 27, 345: 27 ảnh)
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 291 cặp; IoU TB 0.994; cùng lớp 288/291 (99.0%)
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 45 box chưa ghép; không ai dùng `ignore_region`
- Độ tin cậy của IAA: **Không hợp lệ.** 85–96% box trùng tọa độ tuyệt đối giữa các người gán (`independence_check.md`), nên nhãn không được vẽ độc lập. Mọi box để mặc định `occluded_level=0`, `truncated=no`.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: img_007, cả 052 và 053 gán pickup là `car` (trái R-03), IAA không phát hiện được (C019).

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: 60 ca IAA + 6 quyết định cả lô trong `calibration_decisions.csv`; người chốt 052. **Chưa có người kiểm lại.**
- Tác động v1.1 lên nhãn và ảnh: Phạm vi cả lô 40/40. Nhãn sau sửa: `labels_calibrated_1fbb16530508497a.json` (CVAT Task 18). Chưa làm xong: thuộc tính cho phần lớn box, một số `bicycle`/`bus`, `ignore_region` đám đông.
- Tham chiếu bằng chứng khi Rework: Không mở vòng 2.

## 4. Kết quả duyệt

- Vòng QC: 1
- Người review và ngày: 052, 2026-11-16. Phiếu là bản nháp AI (kiểm tự động + AI xem ảnh), 052 chấp nhận, không đối chiếu từng ảnh.
- Đã duyệt / cả lô: 40/40
- Ảnh lỗi / ảnh đã duyệt: 31/40 (77.5%), ngưỡng ≤ 2%
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 56/309 (18.1%)
- Vật bỏ sót, ảnh và vùng: 19, gồm thiếu `bicycle` (img_006, 010, 023, 029, 034), `bus` (img_031, 040), `person` (img_009, 022), `ignore_region` đám đông (img_019, 021, 030, 032). Chi tiết ở `reviews/round-01/qc_review.csv`.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: Ca khó 18/21 ảnh lỗi, phần còn lại 13/19. Lỗi lặp: `truncated` sai (55 lỗi, ví dụ img_015 #119, #120).
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Máy: box cao < 20 px (img_031 #228). Người: pickup img_007 bị gán `car` bởi cả hai người.

## 5. Quyết định bàn giao

- Quyết định: Hold
- Lý do, người nhận và phạm vi sử dụng: `qc_report.py` ra HOLD (còn box `can_review` ở img_005 #47); lỗi ảnh 77.5% vượt ngưỡng 2%; IAA không hợp lệ. Người nhận: coach lớp. Chỉ dùng làm bằng chứng thực hành.
- Nếu còn việc: gán lại thuộc tính cả lô, bổ sung 19 vật bỏ sót, bỏ `can_review`, có người khác 052 kiểm lại và duyệt vòng 2.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: C019 → img_007 → R-03 → box #63 là `truck` trong `labels_calibrated.json`: khớp. Do 052 tự kiểm.
