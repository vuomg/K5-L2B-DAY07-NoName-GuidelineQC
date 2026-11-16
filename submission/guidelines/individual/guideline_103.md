# Guideline gán nhãn — v0.1-103 — thành viên 103

- Phiên bản: v0.1-103 (bản cá nhân, Pha 1)
- Ngày: 2026-11-16
- Người viết / duyệt: 103 / chưa duyệt
- Hướng tiếp cận: **dễ lặp lại giữa các người gán**: quy tắc dựa trên dấu hiệu nhìn thấy được (số bánh, hình dạng thân, kích thước pixel), ít phán đoán chủ quan; dùng `ignore_region` theo ngưỡng đếm được.

## 1. Mục tiêu

Nhãn để huấn luyện mô hình phát hiện **người và phương tiện** trên ảnh đường phố 2D.

- Ưu tiên: **nhãn nhất quán** giữa các người gán (IAA cao). Một quy tắc hơi thô nhưng ai cũng áp dụng giống nhau tốt hơn một quy tắc tinh tế nhưng mỗi người hiểu một kiểu.
- Sai nguy hiểm: bỏ sót người; gán vật giả là vật thật.
- Phép thử cho mọi quyết định: *"Một người gán khác, chỉ nhìn ảnh và đọc guideline này, có ra cùng kết quả không?"*

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe 4 bánh, **nóc liền một mặt từ kính trước đến đuôi**, chiều cao thân ≤ chiều cao bánh × 3. | img_023, img_031, img_040 taxi, img_024 | Thân có thùng hở phía sau → `truck` |
| `truck` | Xe ≥ 4 bánh có **khoang chở hàng tách rời cabin** (nhìn thấy khe hoặc bậc giữa cabin và thùng): pickup, xe tải, đầu kéo. | img_001, 002, 007, 012, 028, 036, 037 | Xe buýt (thân liền, nhiều cửa sổ) → không gán |
| `van` | Xe 4 bánh **thân liền một khối, nóc cao**, đầu xe ngắn (≤ 1/4 chiều dài thân). | img_005 xe 16 chỗ; img_016 HiAce | SUV đầu dài → `car` |
| `motorcycle` | Xe **đúng 2 bánh** có động cơ (thấy ống xả, động cơ hoặc thân nhựa ốp). Sidecar: chỉ phần xe 2 bánh. | img_006, 010, 026, 029 | Tuk-tuk, xe lam (3 bánh) → không gán; xe đạp → không gán |
| `person` | Người thật, thấy trực tiếp, có ít nhất **đầu hoặc thân** trong ảnh. | img_014, img_034 | Chỉ thấy tay hoặc chân → không gán; tượng, ma-nơ-canh, hình in → không gán |
| `ignore_region` | Vùng chứa vật nhỏ hoặc vật quá dày đặc theo **ngưỡng đếm** (R-08, R-09). | img_021 phía xa, img_030 | Không dùng cho phương tiện ngoài taxonomy |

**Vật không thuộc lớp nào** (tuk-tuk, xe lam, xe buýt, xích lô, xe đạp, sidecar thùng bên, quang gánh): **không gán và không phủ `ignore_region`**. Ghi tên ảnh vào `image_issues.csv` nếu vật chiếm > 10% diện tích ảnh, để nhóm quyết định có cần thêm lớp không. Người trên các xe này vẫn gán `person`.

### Thuộc tính

| Thuộc tính | Mức | Ngưỡng cụ thể |
|---|---|---|
| `occluded_level` | `0` | Bị che < 25%. |
| | `1` | Bị che 25% đến < 50%. |
| | `2` | Bị che 50% đến < 75%. |
| | `3` | Bị che ≥ 75%. |
| `truncated` | `yes` | **Bất kỳ cạnh box nào** cách mép ảnh ≤ 3 px. |
| | `no` | Không cạnh nào chạm mép. |
| `can_review` | tick | Không chắc ở **bất kỳ** điểm nào: lớp, gán hay không, mức che, biên box. |

Vì sao chọn mức 25%: chia đều 4 bậc dễ ước lượng bằng mắt (¼, ½, ¾), giảm lệch giữa người gán. `truncated` dựa trên vị trí box nên có thể kiểm bằng script.

## 3. Quy tắc vẽ box

| Mã | Quy tắc |
|---|---|
| R-01 | **Người trên xe máy:** **mỗi người 1 box `person`**, **mỗi xe 1 box `motorcycle`** chỉ ôm phần xe (bánh, thân, tay lái). Phần người ngồi lên xe **không** đưa vào box xe; nếu chân người che thân xe thì vẫn kéo box xe tới biên thật của xe thấy được. Người ngồi sau bị che ≥ 75% vẫn gán, `occluded_level=3`. |
| R-02 | **Phương tiện ngoài taxonomy:** không gán, không phủ `ignore_region` (xem mục 2). |
| R-03 | **Pickup**: luôn `truck` (có khoang hàng tách cabin), kể cả có nắp thùng (img_037). |
| R-04 | **Box ôm sát phần nhìn thấy** (modal). Không bao bóng đổ, phản chiếu trên mặt đường. |
| R-05 | **Vật không thật** không gán, gồm tượng, mô hình, đồ chơi, ma-nơ-canh, hình in, ảnh trong gương/kính, **và cả xe hay người hóa trang trong diễu hành/lễ hội** khi không chắc là vật thật lưu thông → không gán, ghi `image_issues.csv`. Người thật ngồi trong xe diễu hành vẫn gán `person`. |
| R-06 | **Xe chở xe**: gán **mọi xe thấy ≥ 25% diện tích**, kể cả xe được chở và xe trên nóc xe, theo lớp hình dạng của nó (R-05 vẫn áp dụng nếu là mô hình). |
| R-07 | **Hàng hóa** không vào box xe hay box người, trừ khi nằm trong thùng xe. |
| R-08 | **Vật nhỏ:** box cao < 20 px → không gán từng vật. Vùng có ≥ 3 vật nhỏ → 1 `ignore_region`. |
| R-09 | **Đám đông:** khi trong một vùng có **≥ 10 vật cùng lớp** và **≥ một nửa trong số đó bị che ≥ 50%** → gán riêng các vật có `occluded_level` ≤ 1, phần còn lại phủ `ignore_region`. |
| R-10 | **Nhòe chuyển động:** gán nếu thấy rõ lớp; biên box lấy theo **lõi đậm** của vật, không lấy vệt nhòe; tick `can_review`. |
| R-11 | **Xe chủ**, thân xe người chụp, khung gương: không gán. |
| R-12 | **Ảnh không có vật hợp lệ** vẫn có trong COCO. |

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_001 | Pickup Suzuki | R-03 | `truck`, `truncated=yes` | Thùng tách cabin |
| img_002 | Xe chở ô tô | R-06 | `truck` cho xe chở; tầng trên khoảng 5 `car`; tầng dưới chỉ gán xe thấy ≥ 25% | Ngưỡng 25% đếm được |
| img_004 | 2 tuk-tuk | R-02 | Không gán tuk-tuk; tài xế `person` `occluded_level=2`; ghi `image_issues.csv` | 3 bánh, ngoài taxonomy |
| img_005 | Đám xe máy cận cảnh | R-01, R-09 | Từng người `person`; xe máy chỉ gán nếu thấy ≥ 25%; xe 16 chỗ `van` | Chưa đủ 10 vật nên R-09 chưa áp dụng |
| img_006 | Xe chở 2 người | R-01 | 2 `person` + 1 `motorcycle` (chỉ xe) | Ảnh chuẩn của R-01 |
| img_011 | Predator, xe máy độ | R-05 | Không gán Predator và xe độ; ghi `image_issues.csv`; người xem hợp lệ gán `person` | Không chắc vật thật |
| img_014 | Xe máy nhòe | R-10 | Gán theo lõi đậm + `can_review`; người đi bộ `person` | — |
| img_015 | 2 xe cắt mép, xe nhòe | R-04, R-10 | Xe đỏ, xe bạc `car` `truncated=yes`; xe nhòe phía sau `car` + `can_review` | Không lấy phản chiếu mặt đường |
| img_017 | Tượng | R-05 | Không có box | — |
| img_018 | Biển quảng cáo, xe sau rào | R-05 | Không gán người in; xe `car`, `occluded_level=0` (rào mảnh < 25%) | — |
| img_019 | Xe Dangermouse | R-05, R-09 | Xe không gán (xe giả tưởng); tài xế `person`; đám đông > 10 người che ≥ 50% → `ignore_region`, hàng đầu gán riêng | — |
| img_020 | Gương | R-05, R-11 | Không có box | — |
| img_021 | Đám đông xe máy | R-09 | Gán riêng vật `occluded_level` ≤ 1; còn lại `ignore_region` | Thỏa ngưỡng ≥ 10 vật |
| img_022 | Sidecar | R-01, R-02 | `motorcycle` chỉ phần xe 2 bánh; thùng bên không gán; người `person` `occluded_level=3` | Thùng bên ngoài taxonomy |
| img_024 | Xe vàng trên nóc | R-06 | Xe đen `car`; xe vàng `car` + `can_review` (có thể là thân xe trưng bày) | Thấy ≥ 25% |
| img_027 | Tượng pickup | R-05 | Không có box | — |
| img_028 | Pickup chở tượng ngựa | R-03, R-05 | `truck`; ngựa không gán; SUV đỏ `car` `occluded_level=1` | — |
| img_029 | Ống dài | R-07 | Không bao ống | — |
| img_030 | Bãi xe | R-09 | Xe `occluded_level` ≤ 1 gán riêng; còn lại `ignore_region`; nhân viên `person` | Thỏa ngưỡng |
| img_032 | Đám đông chờ xe buýt | R-09 | Theo R-09 | Thỏa ngưỡng ≥ 10 người |
| img_033 | Ma-nơ-canh | R-05 | Không có box | — |
| img_035 | Xe lam chở hàng | R-02 | Không gán xe lam; tài xế `person`; xe máy `motorcycle` + `person`; ô tô `car` | 3 bánh |
| img_036 | Veryca mui bạt | R-03 | `truck` | — |
| img_037 | Pickup có nắp | R-03 | `truck`; xe buýt không gán | — |
| img_038 | Mô hình xe | R-05 | Không có box | — |
| img_040 | Người cận cảnh | R-01 | `person` `truncated=yes`; không gán xe máy (thấy < 25%); tuk-tuk, xe buýt không gán; taxi `car` `truncated=yes` | — |

## 5. QC và phiên bản

- Ngưỡng theo `taxonomy.json` (không đổi).
- Câu hỏi QC đầu tiên cho mỗi ca lệch: *quy tắc có ngưỡng đo được không?* Nếu không, sửa guideline trước khi sửa người gán.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản của giảng viên | — |
| v0.1-103 | Định nghĩa lớp theo dấu hiệu hình dạng; ngưỡng che chia 4 bậc 25%; ngưỡng đám đông ≥ 10 vật; R-01 đến R-12 | img_021, 030, 032 (đám đông); img_004, 035 (3 bánh); img_011, 019 (lễ hội) |
