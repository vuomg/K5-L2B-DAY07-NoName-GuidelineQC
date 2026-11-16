# Báo cáo QC — NoName

> Bản bàn giao vòng 1. Nhóm quyết định dùng kết quả hiện tại làm bản cuối, không sửa thêm nhãn.

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Thực hành đặc tả và QC nhãn bbox 2D (người và phương tiện) cho camera giao thông đô thị. 40 ảnh được tuyển chọn để luyện ca biên (tượng, phản chiếu, tuk-tuk, đám đông), không đại diện cho dữ liệu vận hành; không dùng để huấn luyện mô hình thật.
- Nguồn và phép sử dụng dữ liệu: 40 ảnh Wikimedia Commons, giấy phép CC BY / CC BY-SA / CC0 / public domain theo `data/ATTRIBUTION.csv`; chia sẻ lại phải giữ ghi công, ảnh CC BY-SA phải chia sẻ tương tự. Không sửa hoặc đổi tên ảnh.
- Manifest và checksum nhãn cuối: `submission/qc/batch_manifest.json`; `labels_calibrated.json` (40 ảnh, 309 annotation) SHA-256 `e5dc5770687292b5d07c011270d254c353c44b65796e36a6cdf1ed3c12a6280a`
- Guideline và taxonomy khi gán / khi bàn giao: Gán theo `guideline_v1.0_agreed.md` + `taxonomy.json` v1.0 (5 lớp + `ignore_region`). Bàn giao theo `guideline_v1.1_calibrated.md` + `taxonomy_v1.1.json` v1.1: thay đổi **semantic** (`guideline_change.json`), thêm `bus`, `bicycle`; tuk-tuk/xe lam → `car`; xích lô → `bicycle`; vỏ xe, đồ lưu niệm không gán; thêm R-14. Mục `rules` (ngưỡng) không đổi.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 80/80 (`assignment.csv`, 2 người/ảnh; 052: 26, 053: 27, 345: 27 ảnh). `validate_labels.py --all` sạch, có 2 cảnh báo vật nhỏ ở img_031 (053 #142, 345 #135).
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 291 cặp box ghép (IoU ≥ 0.5, ghép 1-1) trên 40 ảnh; IoU TB 0.994; cùng lớp 99.0% (288/291); cùng `occluded_level` 100%, cùng `truncated` 100% (`iaa_summary.md`). Theo cặp: 052–053: 113 cặp, IoU 0.995; 052–345: 114 cặp, IoU 0.999; 053–345: 64 cặp, IoU 0.982.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 45 box chưa ghép (10/35 theo A/B); 0 box loại do ignore vì không ai dùng `ignore_region`, kể cả ở đám đông img_019, 021, 030 (trái R-09).
- **Độ tin cậy của IAA**: **IAA trên không phản ánh đồng thuận độc lập.** `scripts/check_independence.py` (`independence_check.md`) cho thấy 90% (052–053), 96% (052–345) và 85% (053–345) box trên ảnh chung **trùng tọa độ tuyệt đối**. Cả 627 box đều để mặc định `occluded_level=0`, `truncated=no`, nên 100% đồng thuận thuộc tính là do không gán chứ không phải do thống nhất. Nguyên nhân chưa được nhóm xác minh khi nộp; dấu hiệu (tọa độ trùng tới 0.1 px) cho thấy nhãn được sao chép từ một nguồn chung chứ không vẽ độc lập.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: img_007, pickup Toyota Hilux: cả 052 và 053 gán `car`, trái R-03 (pickup luôn là `truck`). IAA không phát hiện vì hai người cùng lớp; chỉ lộ ra nhờ cờ `can_review` của 053 (C019). Cách kiểm: đối chiếu từng box `car` với định nghĩa lớp trong guideline. Tương tự: không ai đặt thuộc tính cắt mép ở img_015, nơi hai xe bị cắt rõ ở mép trái và mép phải.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: 60 ca IAA (C001–C060) + 6 quyết định cả lô (L01–L06) trong `calibration_decisions.csv`; mỗi dòng có quyết định, rule ID, phiếu sửa, người chốt và người kiểm lại. Theo loại: 45 bỏ sót/thừa, 4 IoU thấp, 3 sai lớp, 8 cờ `can_review`. Tóm tắt nhóm ca ở mục 7 của guideline v1.1. Kiểm lại: **chưa thực hiện**. Cột `kiem_lai` trong `calibration_decisions.csv` vẫn ghi "chưa kiểm".
- Tác động v1.1 lên nhãn và ảnh: Phạm vi cả lô 40/40 ảnh. Mapping: `ignore_region`/`van`/`truck` trên xe buýt → `bus`; `ignore_region`/`motorcycle` trên tuk-tuk, xe lam → `car`; xe đạp, xích lô (chưa gán) → `bicycle`; vỏ xe (img_024), tượng xe (img_027) → xóa; hành khách sau kính (img_009) → xóa; rà lại `occluded_level`/`truncated` mọi box. Nhãn đồng thuận v1.0 được đổi sang danh mục v1.1 (`work/calib/consensus_v1.0_as_v1.1.json`) rồi sửa trong CVAT. COCO sau sửa: `submission/qc/labels_calibrated_1fbb16530508497a.json` (export CVAT Task 18). Bước tự động (`work/apply_decisions.py`) áp dụng các thao tác đã ghi của C001–C060 và bỏ 20 box trùng. Sửa tay trong CVAT: thêm 7 box (`bicycle` ở img_003, 006, 039; `bus` ở img_021, 037, 040; `car` tuk-tuk ở img_016). **Chưa làm** khi bàn giao vòng 1: thuộc tính `occluded_level`/`truncated` cho phần lớn box (292/309 vẫn `0/no`), `bicycle` ở img_023, 029, `bus` ở img_031, `ignore_region` đám đông ở img_019, 021, 030, 032 (vùng ở img_019 bị mất sau import).
- Tham chiếu bằng chứng khi Rework: Không mở vòng 2. Vòng 1 là vòng cuối (quyết định Hold).

## 4. Kết quả duyệt

- Vòng QC: 1
- Người review và ngày: 052, 2026-11-16. Phiếu là **bản nháp AI** (Claude Code) gồm kiểm tự động `truncated` theo tọa độ, kiểm box < 20 px, và AI xem 40 ảnh overlay. 052 chấp nhận bản nháp, **không đối chiếu lại từng ảnh**. 052 cũng là người sửa nhãn calibration, nên người duyệt không độc lập với người sửa.
- Đã duyệt / cả lô: 40/40 (duyệt toàn lô, `qc_sample.py --round 1`)
- Ảnh lỗi / ảnh đã duyệt: 31/40 = 77.5% (ngưỡng ≤ 2%)
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 56/309 = 18.1%; thêm 19 vật bỏ sót ghi riêng
- Vật bỏ sót, ảnh và vùng: 19 vật/vùng bỏ sót. Thiếu `bicycle`: img_006 (2), 010, 023, 029 (2), 034. Thiếu `bus`: img_031, 040. Thiếu `person`: img_009 (ban công), img_022 (người trong sidecar). Thiếu `ignore_region` đám đông: img_019, 021, 030, 032 (R-09). Xe máy nhòe ở img_014 chưa gán và chưa phủ vùng (R-10). Predator và xe máy độ ở img_011 chưa gán theo R-05. Vùng cụ thể ghi ở cột `region` của `qc_review.csv`.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: Ca khó (ảnh bị cờ IAA): 18/21 ảnh có lỗi (85.7%). Phần còn lại: 13/19 (68.4%). **Lỗi lặp** chính: `sai_thuoc_tinh` (55 lỗi), phần lớn là box chạm mép ảnh nhưng `truncated=no` (ví dụ img_015 #119, #120), vì người gán để mặc định thuộc tính (L05 chưa thực hiện). Ngoài ra có 1 `thua` (img_031 #228 cao 19 px, R-08). Chi tiết: `submission/qc/reviews/round-01/qc_review.csv`.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Máy chặn được: box cao < 20 px (cảnh báo img_031 của `validate_labels.py`) và lượt gán thiếu (`qc_compare.py` dừng khi chưa đủ 80/80). Cần người đọc ảnh: pickup img_007 bị hai người cùng gán `car`, tức cùng sai nên IAA không thấy; poster nhân vật ở img_008 bị gán `person`; tượng pickup img_027 bị gán `truck`. Script không biết vật nào là thật.

## 5. Quyết định bàn giao

- Quyết định: Hold
- Lý do, người nhận và phạm vi sử dụng: `qc_report.py --round 1` ra HOLD vì nhãn cuối còn box `can_review` (img_005 #47, ca C018). Ngoài ra tỉ lệ lỗi theo ảnh 77.5%, vượt xa ngưỡng 2%, và có lỗi lặp. IAA trước calibration không hợp lệ (mục 2), phiếu QC chưa được người độc lập đối chiếu, và calibration chưa được kiểm lại. Người nhận: coach lớp. Phạm vi: **chỉ làm bằng chứng thực hành Day 07, không dùng huấn luyện mô hình**.
- Nếu còn việc: (1) Gán lại `occluded_level`/`truncated` cho cả lô theo mục 2.2 (L05). (2) Thêm 19 vật bỏ sót ở trên. (3) Chốt C018 và bỏ `can_review`. (4) Người khác 052 (đề xuất 053) kiểm lại calibration và duyệt vòng 2 độc lập. (5) Nhóm xác minh nguồn của các box trùng tọa độ. Người xử lý: 052 sửa nhãn, 053 duyệt. Bằng chứng: `labels_calibrated_<hash>.json` mới, `reviews/round-02/`.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: Ca C019: `calibration_decisions.csv` (C019, pickup gán `car`) → `data/images/img_007.jpg` → R-03 (pickup luôn `truck`) → box #63 lớp `truck` trong `labels_calibrated.json` → phiếu QC vòng 1 không ghi lỗi cho #63. Kết quả: khớp. Do 052 tự kiểm; **chưa có người ngoài nhóm kiểm ngược**.
