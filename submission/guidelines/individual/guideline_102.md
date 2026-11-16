# Guideline gán nhãn — v0.1-102 — thành viên 102

- Phiên bản: v0.1-102 (bản cá nhân, Pha 1)
- Ngày: 2026-11-16
- Người viết / duyệt: 102 / chưa duyệt
- Hướng tiếp cận: **rộng, ưu tiên độ phủ**: gom phương tiện lạ vào lớp gần nhất theo chức năng, gán càng nhiều vật thật càng tốt, hạn chế dùng `ignore_region`.

## 1. Mục tiêu

Nhãn dùng cho mô hình phát hiện **người và phương tiện** trên camera giao thông ở Đông Nam Á, nơi có nhiều phương tiện không chuẩn (tuk-tuk, xe lam, xích lô).

- Mô hình **phải phát hiện mọi phương tiện có thể va chạm**, kể cả loại lạ. Một tuk-tuk bị bỏ qua nghĩa là một vật cản không được thấy.
- Sai nguy hiểm nhất là **bỏ sót**. Phát hiện thừa trên tượng hay mô hình ít nguy hiểm hơn, nhưng vẫn không gán chúng.
- Vì thế: phương tiện lạ được **xếp vào lớp gần nhất theo kích thước và số bánh**, thay vì bỏ qua.

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe ≥ 4 bánh chở người, thân thấp, **kể cả pickup dùng làm xe cá nhân** (cabin kép, thùng hở trống hoặc chở đồ nhẹ). | img_023 Civic; img_040 taxi; img_012, 028 pickup | Pickup có nắp thùng kín cao hơn nóc cabin (img_037) → `van` |
| `truck` | Xe chở hàng có **cabin riêng và thùng hàng cố định cao hơn hoặc bằng nóc cabin**, hoặc xe tải thương mại (biển hiệu, thùng kín, mui bạt), **kể cả xe buýt** (xe lớn, ≥ 6 bánh hoặc dài > 2 lần chiều cao). | img_002, img_007 Isuzu, img_036 Veryca, img_009 xe buýt mini, img_037 xe buýt | Pickup cá nhân → `car` |
| `van` | Xe thân liền một khối, nóc cao (minivan, xe 16 chỗ), hoặc pickup có nắp thùng kín cao. | img_005, img_016 HiAce, img_037 pickup có nắp | Xe buýt → `truck` |
| `motorcycle` | Mọi xe **có động cơ, 2 hoặc 3 bánh, lái bằng ghi-đông**: xe máy, xe điện, sidecar, **tuk-tuk, xe lam (auto rickshaw)**. | img_006, img_022, img_004 tuk-tuk, img_035 xe lam | Xe đạp, xích lô (không động cơ) → không gán |
| `person` | Người thật, nhìn thấy trực tiếp, mọi tư thế, kể cả người hóa trang. | img_014; người lái tuk-tuk img_004 | Tượng, ma-nơ-canh, hình in, ảnh phản chiếu |
| `ignore_region` | Chỉ dùng cho vật **< 20 px** hoặc **nhòe không nhận ra lớp**. | Người rất nhỏ ở xa img_025 | Không dùng cho đám đông có vật ≥ 20 px |

**Vật không thuộc lớp nào** (xe đạp, xích lô, quang gánh, xe đẩy): **không gán, không phủ `ignore_region`**. Người trên xe đạp hoặc xích lô vẫn gán `person`.

### Thuộc tính

| Thuộc tính | Mức | Ngưỡng cụ thể |
|---|---|---|
| `occluded_level` | `0` | Không bị che (0%). |
| | `1` | Bị che > 0% đến < 35%. |
| | `2` | Bị che 35% đến < 70%. |
| | `3` | Bị che ≥ 70%. |
| `truncated` | `yes` | Phần vật bị mép ảnh cắt mất ≥ 10% (ước lượng). Cắt < 10% → `no`. |
| | `no` | Còn lại. |
| `can_review` | tick | Chỉ tick khi **không chắc lớp**. Không tick vì box khó vẽ. |

"% bị che" tính trên **chiều cao** của vật: ví dụ người bị xe che từ hông xuống là khoảng 50% → mức `2`.

## 3. Quy tắc vẽ box

| Mã | Quy tắc |
|---|---|
| R-01 | **Người trên xe máy:** 1 box `person` cho **mỗi** người, ôm toàn thân thấy được. 1 box `motorcycle` ôm **cả xe và người đang ngồi trên xe** (đơn vị "xe đang lưu thông"). Box `motorcycle` vì vậy luôn chứa các box `person` của người trên xe. |
| R-02 | **Tuk-tuk, xe lam** → `motorcycle` (2–3 bánh, có động cơ, lái bằng ghi-đông). Box bao cả mui và khoang khách. **Xe buýt** → `truck`. **Xe đạp, xích lô** → không gán. |
| R-03 | **Pickup**: cabin kép hoặc thùng trống/chở đồ nhẹ → `car`; có nắp thùng kín cao hơn nóc cabin → `van`; pickup thương mại cỡ nhỏ, cabin đơn, chở hàng nặng (img_001) → `truck`. |
| R-04 | **Box ôm sát phần nhìn thấy**, không đoán phần bị che. |
| R-05 | **Vật không thật** (tượng, mô hình, đồ chơi, ma-nơ-canh, hình in, phản chiếu): **không gán**. Xe diễu hành cỡ thật có người lái (img_019) → `car`. Người hóa trang → `person`. |
| R-06 | **Xe chở xe**: chỉ gán **xe chở** (`truck`). Các xe được chở **không gán riêng**, phủ chung 1 `ignore_region`. Lý do: chúng không tự lưu thông, mô hình không cần đếm chúng là xe trên đường. |
| R-07 | **Hàng hóa gắn vào xe** (bao hàng chất trên xe lam img_035) **nằm trong box xe**. Vật dài do người cầm (ống img_029) **không** vào box. |
| R-08 | **Vật nhỏ:** cao < 20 px → `ignore_region` (từng vật hoặc cả cụm). |
| R-09 | **Đám đông:** vẫn gán **từng vật ≥ 20 px**, kể cả bị che nhiều (`occluded_level=3`). Không dùng `ignore_region` cho đám đông. |
| R-10 | **Nhòe chuyển động:** nhận ra lớp → gán bình thường; không nhận ra → `ignore_region`. |
| R-11 | **Xe chủ** và phần thân xe của người chụp: không gán. |
| R-12 | **Ảnh không có vật hợp lệ** vẫn có trong COCO. |

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_001 | Pickup Suzuki cabin đơn chở ống sắt | R-03 | `truck`, `truncated=yes`, `occluded_level=1` | Pickup thương mại chở hàng nặng |
| img_002 | Xe chở ô tô | R-06 | 1 `truck`; khối ô tô trên giàn → 1 `ignore_region` | Xe được chở không tự lưu thông |
| img_004 | 2 tuk-tuk | R-02 | 2 `motorcycle` (bao cả mui); tài xế `person` | Tuk-tuk là xe 3 bánh có động cơ |
| img_005 | Người đi xe máy cận cảnh | R-01 | Mỗi người 1 `person`; mỗi xe 1 `motorcycle` bao cả người; xe 16 chỗ `van` | R-01 |
| img_006 | Xe chở 2 người, xe đạp | R-01, R-02 | Xe 75S1-7182: `motorcycle` bao cả 2 người + 2 `person`; xe đạp không gán, người đạp `person` | Ảnh chuẩn của R-01 |
| img_009 | Xe buýt mini | R-02 | `truck` | Xe lớn chở khách |
| img_011 | Predator, xe máy độ | R-05 | Predator `person`; xe máy độ `motorcycle` | Người hóa trang vẫn là người; xe độ vẫn chạy được |
| img_012 | Pickup chở tạp hóa | R-03 | `car`, `truncated=yes` | Pickup cá nhân, chở đồ nhẹ |
| img_016 | 2 tuk-tuk, Vespa, HiAce, pickup | R-02, R-03 | Tuk-tuk `motorcycle`; Vespa `motorcycle`; HiAce `van`; pickup `car`; người cắt mép `person` `truncated=yes` | — |
| img_017 | Tượng | R-05 | Không có box | — |
| img_019 | Xe Dangermouse, đám đông | R-05, R-09 | Xe `car`; tài xế `person`; từng người xem ≥ 20 px gán `person` | Không dùng `ignore_region` cho đám đông |
| img_020 | Gương chiếu hậu | R-05, R-11 | Không có box | Phản chiếu |
| img_021 | Đám đông xe máy | R-01, R-08, R-09 | Gán từng xe và từng người ≥ 20 px; vật xa < 20 px → `ignore_region` | Độ phủ tối đa |
| img_022 | Sidecar | R-02 | 1 `motorcycle` bao xe và thùng bên; người `person` `occluded_level=3` | — |
| img_023 | Xích lô | R-02 | Xích lô không gán; người đạp `person` | Không động cơ |
| img_024 | Xe trên nóc xe | R-06 | Xe đen `car`; xe vàng `ignore_region` | Xe được chở |
| img_027 | Tượng pickup | R-05 | Không có box | — |
| img_028 | Pickup cổ chở tượng ngựa | R-03, R-05 | `car` (pickup cá nhân, thùng chở vật nhẹ); ngựa không gán | — |
| img_029 | Ống dài | R-07 | Xe máy và người không bao ống; xe đạp không gán | Ống do người cầm |
| img_030 | Bãi xe máy | R-09 | Gán từng xe ≥ 20 px (`occluded_level` 2–3) | Không dùng `ignore_region` cho đám đông |
| img_032 | Đám đông chờ xe buýt | R-09 | Gán từng người | Mỗi người ≥ 20 px |
| img_033 | Ma-nơ-canh, phản chiếu | R-05 | Không có box | — |
| img_035 | Xe lam chở hàng | R-02, R-07 | `motorcycle` bao cả đống bao hàng | Hàng gắn cố định vào xe |
| img_036 | Veryca mui bạt | R-03 | `truck` | Thùng cao bằng nóc cabin |
| img_037 | Pickup có nắp, xe buýt | R-03, R-02 | Pickup `van`; xe buýt `truck` | Nắp thùng cao hơn nóc cabin |
| img_038 | Mô hình xe | R-05 | Không có box | — |
| img_040 | Người cận cảnh, tuk-tuk, xe buýt | R-01, R-02 | `person` `truncated=yes`; xe máy chỉ thấy gương → không gán; tuk-tuk `motorcycle`; xe buýt `truck`; taxi `car` | — |

## 5. QC và phiên bản

- Ngưỡng theo `taxonomy.json` (không đổi). Quan tâm nhất: **bỏ sót** (`bo_sot`) và **sai lớp** giữa `car`/`van`/`truck`.
- Ca mơ hồ về lớp: tick `can_review`; nhóm chốt ở Pha 5.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản của giảng viên | — |
| v0.1-102 | Mở rộng `motorcycle` (gồm tuk-tuk, xe lam), `truck` gồm xe buýt, chia pickup theo công dụng, R-01 đến R-12 | img_004, 016, 035 (3 bánh); img_009, 037 (xe buýt); img_012, 028, 037 (pickup) |
