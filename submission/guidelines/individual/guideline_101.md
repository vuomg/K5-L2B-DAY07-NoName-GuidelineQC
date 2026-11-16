# Guideline gán nhãn — v0.1-101 — thành viên 101

- Phiên bản: v0.1-101 (bản cá nhân, Pha 1)
- Ngày: 2026-11-16
- Người viết / duyệt: 101 / chưa duyệt
- Hướng tiếp cận: **chặt, chỉ gán vật thật tham gia giao thông**; cái gì không chắc thì che bằng `ignore_region` để mô hình không bị phạt sai.

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình **phát hiện người và phương tiện trên ảnh 2D** cho camera giao thông đô thị (Việt Nam, Thái Lan và tương tự).

- Sai nguy hiểm nhất: **bỏ sót người** (mô hình không thấy người đi bộ, người đi xe máy) và **bỏ sót xe máy**, vì đây là đối tượng dày đặc nhất ở đô thị châu Á.
- Sai ít nguy hiểm hơn nhưng làm bẩn dữ liệu: box trên **tượng, mô hình, hình in, phản chiếu**. Mô hình học những box đó sẽ báo động giả.
- Nguyên tắc chung: **chỉ gán vật thật, có thể di chuyển trên đường, nhìn thấy trực tiếp** (không qua gương hay hình in).

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe 4 bánh chở người, ≤ 9 chỗ, không có thùng hàng tách khỏi cabin (sedan, SUV, hatchback, wagon, taxi). | img_023 Civic đen; img_031 SUV trắng; img_040 taxi xanh; img_024 Pacer wagon | Pickup → `truck` (R-03); xe 16 chỗ → `van` |
| `truck` | Xe có **thùng hàng tách khỏi cabin** (thùng hở, thùng kín, mui bạt), kể cả **pickup** và đầu kéo. | img_002 đầu kéo chở xe; img_007 Isuzu ELF; img_036 Veryca mui bạt; img_001, 012, 028, 037 pickup | Xe buýt → không gán (R-02); van kín liền cabin → `van` |
| `van` | Xe 4 bánh **thân liền một khối** (cabin và khoang sau chung mái), dùng chở người hoặc hàng, cao hơn sedan. | img_005 xe 16 chỗ bạc; img_016 HiAce trắng | Pickup có nắp thùng (img_037) → vẫn `truck` vì cabin và thùng là hai khối |
| `motorcycle` | Xe 2 bánh có động cơ (xe máy, xe tay ga, xe điện, mô tô), kể cả loại **có thùng bên** (sidecar). | img_006, img_010, img_026, img_029 xe điện, img_022 sidecar | Xe đạp → không gán; tuk-tuk 3 bánh → không gán (R-02) |
| `person` | Con người thật, nhìn thấy trực tiếp, **đứng, đi, ngồi hoặc đang điều khiển xe**. | img_014 hai người đi bộ; người lái xe máy ở img_006 | Tượng (img_017), ma-nơ-canh (img_033), người in trên biển (img_018) → không gán |
| `ignore_region` | Vùng **không gán từng vật**; bỏ sót trong vùng này không tính lỗi. | Đám đông img_021 phía xa; bãi xe img_030 phía sau | Không dùng để "đỡ" một vật đơn lẻ đã đủ rõ |

**Vật không thuộc lớp nào** (xe buýt, tuk-tuk, xe lam, xích lô, xe đạp, quang gánh): **không gán lớp**. Nếu vật đó cao ≥ 50 px thì vẽ một `ignore_region` ôm nó, để mô hình không bị phạt khi phát hiện nhầm thành `car`/`truck`/`motorcycle`. **Người đang ngồi hoặc lái** các xe này vẫn gán `person`.

### Thuộc tính

| Thuộc tính | Mức | Ngưỡng cụ thể |
|---|---|---|
| `occluded_level` | `0` | Thấy ≥ 90% diện tích ước lượng của vật (bị che < 10%). |
| | `1` | Bị che 10% đến < 40%. |
| | `2` | Bị che 40% đến < 80%. |
| | `3` | Bị che ≥ 80%, **hoặc** không đoán được phần bị che lớn cỡ nào. |
| `truncated` | `yes` | Box chạm mép ảnh (cách mép ≤ 2 px) **và** vật rõ ràng còn tiếp tục ra ngoài khung. |
| | `no` | Các trường hợp còn lại. |
| `can_review` | tick | Không chắc về lớp, về việc có gán hay không, hoặc biên box sai lệch > 10% do ảnh mờ/tối. |

Cách ước lượng "% bị che": tưởng tượng box đầy đủ của vật nếu không bị che, rồi so phần diện tích thấy được với box đó. Bị che bởi **mép ảnh** thì tính vào `truncated`, **không** tính vào `occluded_level`.

## 3. Quy tắc vẽ box

| Mã | Quy tắc |
|---|---|
| R-01 | **Người trên xe máy:** vẽ **2 loại box tách riêng**: 1 box `person` cho **mỗi** người (lái và ngồi sau đều gán), 1 box `motorcycle` cho xe. Box `person` ôm toàn bộ phần người thấy được (mũ, tay, chân). Box `motorcycle` ôm phần xe thấy được (bánh, thân, tay lái, gương), **không** cố ý bao thân người nhưng được phép chồng lấn với box người. |
| R-02 | **Phương tiện ngoài taxonomy** (xe buýt, tuk-tuk, xe lam, xích lô, xe đạp): không gán lớp; cao ≥ 50 px thì phủ `ignore_region`. Người trên xe vẫn gán `person` (R-01 áp dụng cho phần người). |
| R-03 | **Pickup** (cabin và thùng hở hoặc có nắp) luôn là `truck`. |
| R-04 | **Box ôm sát phần nhìn thấy** (modal), không đoán phần bị che. Sai lệch cho phép ≤ 2 px mỗi cạnh với vật cao ≥ 50 px. |
| R-05 | **Vật không thật** (tượng, mô hình, đồ chơi, ma-nơ-canh, người/xe in trên biển hoặc tranh tường, ảnh trong gương hay phản chiếu trên kính): **không gán, không cần `ignore_region`**. Ngoại lệ: xe đồ chơi cỡ thật có người lái và có biển số chạy trên đường (img_019) → gán `car` + `can_review`. |
| R-06 | **Xe chở xe**: xe được chở là xe thật → gán từng xe theo lớp của nó, `occluded_level` theo phần bị khung che. Box của xe chở **không** bao các xe được chở. |
| R-07 | **Hàng hóa**: box xe **không** bao hàng nhô ra ngoài thân xe (ống dài img_029, bao hàng chất cao img_035). Hàng nằm gọn trong thùng thì tự nhiên nằm trong box xe. |
| R-08 | **Vật nhỏ:** cao < 20 px thì không gán từng vật. Nếu có ≥ 3 vật nhỏ sát nhau, phủ 1 `ignore_region`. |
| R-09 | **Đám đông:** nhóm ≥ 5 vật cùng loại mà mỗi vật bị che ≥ 80% → phủ 1 `ignore_region` cho cả nhóm. Vật ở hàng đầu (thấy ≥ 20%) vẫn gán riêng. |
| R-10 | **Nhòe chuyển động:** nếu nhận ra được lớp và đoán được biên trong sai số 10% → gán + `can_review`. Không nhận ra được → `ignore_region`. |
| R-11 | **Xe chủ (ego)** và phần xe của người chụp (img_020 khung gương, kính xe img_018): không gán. |
| R-12 | **Ảnh không có vật hợp lệ** vẫn để trong COCO (không có annotation). |

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_001 | Pickup Suzuki cỡ nhỏ chở ống sắt, cắt mép phải, có người đứng che | R-03, R-07 | `truck`, `truncated=yes`, `occluded_level=1`; người đứng gán `person` | Có thùng hàng tách cabin; cô gái che khoảng 15% thân xe |
| img_002 | Đầu kéo chở khoảng 9 ô tô | R-06, R-03 | 1 `truck` cho đầu kéo + rơ-moóc; mỗi ô tô thấy được gán `car`, tầng dưới `occluded_level=2` | Xe được chở là xe thật, mô hình cần nhận ra chúng |
| img_004 | 2 tuk-tuk có tài xế bên trong | R-02 | Mỗi tuk-tuk 1 `ignore_region`; tài xế gán `person`, `occluded_level=2` | Không có lớp 3 bánh; không ép thành `motorcycle` |
| img_005 | Người đi xe máy cận cảnh, xe gần như bị che hết | R-01, R-09 | Gán `person` cho từng người; `motorcycle` chỉ khi thấy ≥ 20% xe, còn lại không gán | Không vẽ box cho xe chỉ thấy gương |
| img_006 | Xe máy chở 2 người, xe đạp, taxi cắt mép | R-01, R-02 | Xe 75S1-7182: 2 `person` + 1 `motorcycle`; xe đạp → `ignore_region`, người đạp → `person`; taxi `car` `truncated=yes` | Ảnh chuẩn của R-01 |
| img_011 | Người hóa trang Predator, xe máy độ trưng bày | R-05 | Predator: `person` + `can_review`; xe máy độ có bánh và yên → `motorcycle` + `can_review` | Không chắc là người thật hay tượng |
| img_014 | Xe máy nhòe chuyển động mạnh | R-10 | Người đi bộ rõ: `person`; cụm xe nhòe trái và phải: `ignore_region` | Không đoán được biên trong 10% |
| img_017 | Tượng người cưỡi ngựa | R-05, R-12 | Không có box | Tượng, không phải người |
| img_018 | Người in trên biển; xe sau hàng rào | R-05, R-11 | Biển không gán; xe gán `car`, `occluded_level=1` (rào mảnh che khoảng 15–25%) | Xe thật nhìn qua hàng rào |
| img_019 | Xe Dangermouse diễu hành, đám đông | R-05, R-09 | Xe: `car` + `can_review`; tài xế `person`; đám đông sau rào: `ignore_region` | Xe chạy được, có biển số |
| img_020 | Ô tô trong gương chiếu hậu | R-05, R-11 | Không có box | Phản chiếu |
| img_021 | Đám đông xe máy giờ cao điểm | R-01, R-08, R-09 | Gán riêng khoảng 3 hàng đầu; phần sau (từ y ≈ 260 lên trên) phủ `ignore_region` | Phía sau bị che ≥ 80% hoặc nhỏ < 20 px |
| img_022 | Xe máy có thùng bên | R-01 | 1 `motorcycle` bao cả thùng bên; người trong thùng `person`, `occluded_level=3` | Sidecar là một phần của xe |
| img_024 | Xe vàng trên nóc xe đen trong bảo tàng | R-06 | Xe đen `car`; xe vàng `car` + `can_review`; các xe trưng bày khác `car` | Xe thật dù đang đỗ trong nhà |
| img_027 | Tượng pickup ở nghĩa trang | R-05 | Không có box | Tượng đá |
| img_028 | Pickup thật chở tượng ngựa | R-03, R-05 | Pickup `truck`, ngựa không gán; SUV đỏ `car`, `occluded_level=1` | Xe thật, vật chở là giả |
| img_029 | Ống dài trên xe máy | R-07 | Box xe máy và box người **không** bao ống | Ống không phải một phần của xe |
| img_030 | Bãi xe máy dày | R-09 | Khoảng 4–5 xe hàng đầu gán riêng; phần còn lại `ignore_region`; nhân viên `person` | Đa số xe bị che ≥ 80% |
| img_032 | Đám đông chờ xe buýt | R-09 | Người đứng hàng đầu thấy ≥ 20% gán riêng; khối người chồng nhau phía sau `ignore_region` | Đám đông |
| img_033 | Ma-nơ-canh, người in, xe phản chiếu | R-05 | Không có box | Cả 3 đều không thật |
| img_036 | Xe tải nhỏ mui bạt | R-03 | `truck` | Thùng tách cabin |
| img_037 | Pickup có nắp thùng kín | R-03 | `truck`; xe buýt → `ignore_region`; người đi bộ `person` | Cabin và thùng là hai khối |
| img_038 | Tủ kính bày mô hình xe | R-05 | Không có box | Đồ chơi |
| img_040 | Người đội mũ cận cảnh, xe máy chỉ thấy gương | R-01 | `person` `truncated=yes`; không gán `motorcycle`; taxi `car`; tuk-tuk, xe buýt `ignore_region` | Thấy < 20% xe máy |

## 5. QC và phiên bản

- Ngưỡng theo `taxonomy.json`: box cao ≥ 20 px; IoU ≥ 0.85 (vật ≥ 50 px), ≥ 0.7 (vật nhỏ hơn); IAA lớp ≥ 95%; lỗi theo ảnh ≤ 2%.
- Ca mơ hồ: người gán tick `can_review`; nhóm chốt tại Pha 5 và ghi mã quy tắc vào `calibration_decisions.csv`.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản của giảng viên | — |
| v0.1-101 | Thêm định nghĩa lớp, ngưỡng `occluded_level`, R-01 đến R-12, bảng ca khó | v0 không xử lý: người trên xe (img_006), tuk-tuk (img_004), pickup (img_037), tượng (img_017, 027), đám đông (img_021, 030) |
