# Báo cáo QC — NoName

> Bản nháp. Mục 1–3 điền từ số liệu đã có. Mọi chỗ `<<...>>` chờ nhãn sau calibration và vòng QC 1; `check_submission.py` sẽ báo lỗi cho tới khi điền xong.

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Thực hành đặc tả và QC nhãn bbox 2D (người và phương tiện) cho camera giao thông đô thị. 40 ảnh được tuyển chọn để luyện ca biên (tượng, phản chiếu, tuk-tuk, đám đông), không đại diện cho dữ liệu vận hành; không dùng để huấn luyện mô hình thật.
- Nguồn và phép sử dụng dữ liệu: 40 ảnh Wikimedia Commons, giấy phép CC BY / CC BY-SA / CC0 / public domain theo `data/ATTRIBUTION.csv`; chia sẻ lại phải giữ ghi công, ảnh CC BY-SA phải chia sẻ tương tự. Không sửa hoặc đổi tên ảnh.
- Manifest và checksum nhãn cuối: <<submission/qc/batch_manifest.json, SHA-256 của labels_calibrated.json>>
- Guideline và taxonomy khi gán / khi bàn giao: Gán theo `guideline_v1.0_agreed.md` + `taxonomy.json` v1.0 (5 lớp + `ignore_region`). Bàn giao theo `guideline_v1.1_calibrated.md` + `taxonomy_v1.1.json` v1.1: thay đổi **semantic** (`guideline_change.json`), thêm `bus`, `bicycle`; tuk-tuk/xe lam → `car`; xích lô → `bicycle`; vỏ xe, đồ lưu niệm không gán; thêm R-14. Mục `rules` (ngưỡng) không đổi.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 80/80 (`assignment.csv`, 2 người/ảnh; 052: 26, 053: 27, 345: 27 ảnh). `validate_labels.py --all` sạch, có 2 cảnh báo vật nhỏ ở img_031 (053 #142, 345 #135).
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 291 cặp box ghép (IoU ≥ 0.5, ghép 1-1) trên 40 ảnh; IoU TB 0.994; cùng lớp 99.0% (288/291); cùng `occluded_level` 100%, cùng `truncated` 100% (`iaa_summary.md`). Theo cặp: 052–053: 113 cặp, IoU 0.995; 052–345: 114 cặp, IoU 0.999; 053–345: 64 cặp, IoU 0.982.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 45 box chưa ghép (10/35 theo A/B); 0 box loại do ignore vì không ai dùng `ignore_region`, kể cả ở đám đông img_019, 021, 030 (trái R-09).
- **Độ tin cậy của IAA**: **IAA trên không phản ánh đồng thuận độc lập.** `scripts/check_independence.py` (`independence_check.md`) cho thấy 90% (052–053), 96% (052–345) và 85% (053–345) box trên ảnh chung **trùng tọa độ tuyệt đối**. Cả 627 box đều để mặc định `occluded_level=0`, `truncated=no`, nên 100% đồng thuận thuộc tính là do không gán chứ không phải do thống nhất. Nguyên nhân: <<nhóm xác nhận nguồn chung: cùng Task CVAT, import chung file, ...>>.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: img_007, pickup Toyota Hilux: cả 052 và 053 gán `car`, trái R-03 (pickup luôn là `truck`). IAA không phát hiện vì hai người cùng lớp; chỉ lộ ra nhờ cờ `can_review` của 053 (C019). Cách kiểm: đối chiếu từng box `car` với định nghĩa lớp trong guideline. Tương tự: không ai đặt thuộc tính cắt mép ở img_015, nơi hai xe bị cắt rõ ở mép trái và mép phải.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: 60 ca IAA (C001–C060) + 6 quyết định cả lô (L01–L06) trong `calibration_decisions.csv`; mỗi dòng có quyết định, rule ID, phiếu sửa, người chốt và người kiểm lại. Theo loại: 45 bỏ sót/thừa, 4 IoU thấp, 3 sai lớp, 8 cờ `can_review`. Tóm tắt nhóm ca ở mục 7 của guideline v1.1. Người kiểm lại: <<053, kết quả>>.
- Tác động v1.1 lên nhãn và ảnh: Phạm vi cả lô 40/40 ảnh. Mapping: `ignore_region`/`van`/`truck` trên xe buýt → `bus`; `ignore_region`/`motorcycle` trên tuk-tuk, xe lam → `car`; xe đạp, xích lô (chưa gán) → `bicycle`; vỏ xe (img_024), tượng xe (img_027) → xóa; hành khách sau kính (img_009) → xóa; rà lại `occluded_level`/`truncated` mọi box. Nhãn đồng thuận v1.0 được đổi sang danh mục v1.1 (`work/calib/consensus_v1.0_as_v1.1.json`) rồi sửa trong CVAT. COCO sau sửa: <<submission/qc/labels_calibrated_<hash>.json>>.
- Tham chiếu bằng chứng khi Rework: <<không áp dụng nếu vòng 1 không Rework; nếu có: vòng cũ, vùng sửa, vòng mới>>

## 4. Kết quả duyệt

- Vòng QC: <<1>>
- Người review và ngày: <<mã, ngày>>
- Đã duyệt / cả lô: <<40/40>>
- Ảnh lỗi / ảnh đã duyệt: <<…/40 (…%)>>
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: <<…/… (…%)>>
- Vật bỏ sót, ảnh và vùng: <<từ qc_review.csv, error_type=bo_sot>>
- Ca khó / phần còn lại, lỗi lặp và ví dụ: <<dẫn submission/qc/reviews/round-01/qc_review.csv>>
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Máy chặn được: box cao < 20 px (cảnh báo img_031 của `validate_labels.py`) và lượt gán thiếu (`qc_compare.py` dừng khi chưa đủ 80/80). Cần người đọc ảnh: pickup img_007 bị hai người cùng gán `car`, tức cùng sai nên IAA không thấy; poster nhân vật ở img_008 bị gán `person`; tượng pickup img_027 bị gán `truck`. Script không biết vật nào là thật.

## 5. Quyết định bàn giao

- Quyết định: <<Release hoặc Hold hoặc Rework, khớp qc_report.py vòng 1>>
- Lý do, người nhận và phạm vi sử dụng: <<lý do; người nhận: coach lớp; phạm vi: chỉ dùng cho thực hành Day 07. Lưu ý: IAA trước calibration không hợp lệ do nhãn không độc lập (mục 2)>>
- Nếu còn việc: <<việc, người xử lý, bằng chứng cần kiểm lại>>
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: <<ví dụ C019: calibration_decisions.csv → img_007 → R-03 → box truck trong labels_calibrated.json; người kiểm ngoài nhóm, kết quả>>
