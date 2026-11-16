# Guideline gán nhãn — v1.1 (calibrated) — nhóm NoName

- Phiên bản: **v1.1** (sau calibration Pha 5; thay đổi **semantic**, áp dụng cả lô)
- Ngày: 2026-11-16
- Người viết: 052, 053, 345 · Người chốt: cả nhóm (họp Pha 2 và Pha 5)
- Taxonomy đi kèm: `submission/taxonomy_v1.1.json` (`version: v1.1`)
- Nguồn: v1.0 (`guideline_v1.0_agreed.md`, hợp nhất các bản cá nhân 052, 053, 345; bất đồng ở **mục 6**) + quyết định calibration (`submission/qc/calibration_decisions.csv`, tóm tắt ở **mục 7**).
- **Thay đổi so với v1.0** được đánh dấu **[v1.1]**.

**Phép thử cho mọi quyết định:** *"Một người gán khác, chỉ đọc guideline này và nhìn ảnh, có ra cùng số box, cùng lớp và cùng thuộc tính không?"* Mô hình cần học được điều gì thì nhãn phải nói đúng điều đó, không bắt mô hình đoán.

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình **phát hiện người và phương tiện trên ảnh 2D** cho camera giao thông đô thị (đường phố Đông Nam Á là chủ yếu).

| Loại sai | Mức nguy hiểm | Hệ quả |
|---|---|---|
| Bỏ sót `person` hoặc `motorcycle` | **Cao nhất** | Mô hình không thấy người và xe máy, hai loại đối tượng dày đặc nhất |
| Box trên tượng, mô hình, hình in, phản chiếu | Cao | Mô hình báo động giả |
| Sai lớp giữa `car`/`van`/`truck` | Trung bình | Thống kê phương tiện lệch |
| Box lỏng, sai thuộc tính | Thấp hơn | Giảm độ chính xác định vị |

**Phạm vi:** chỉ gán **vật thật, nhìn thấy trực tiếp** (không qua gương, kính phản chiếu hay hình in), thuộc 7 lớp dưới đây. **[v1.1]** thêm `bus`, `bicycle`.

## 2. Lớp và thuộc tính

### 2.1. Lớp

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Xe 4 bánh chở người, **mui liền từ kính trước tới đuôi**, không có thùng hàng tách rời cabin: sedan, hatchback, SUV, wagon, taxi. **[v1.1]** Kể cả **xe 3 bánh có động cơ chở người** (tuk-tuk, xe lam / auto rickshaw). | img_023 Civic đen; img_031 SUV trắng; img_040 taxi xanh; img_024 Pacer wagon; **[v1.1]** tuk-tuk img_004, 016, 040; xe lam img_035 | Pickup → `truck` (R-03); xe 16 chỗ → `van`; xích lô → `bicycle`; vỏ xe, mô hình → không gán (R-05) |
| `truck` | Xe ≥ 4 bánh có **khoang chở hàng tách rời cabin** (thấy khe hoặc bậc giữa cabin và thùng): **pickup** (kể cả có nắp thùng), xe tải thùng hở, thùng kín, mui bạt, đầu kéo. | img_001, 007, 012, 016, 028, 037 pickup; img_007 Isuzu; img_036 Veryca; img_002 đầu kéo | **[v1.1]** Xe buýt → `bus`; van thân liền → `van` |
| `van` | Xe 4 bánh **thân liền một khối, nóc cao**, đầu xe ngắn (mũi xe ≤ 1/4 chiều dài thân): minivan, xe 16 chỗ, HiAce. | img_005 xe 16 chỗ bạc và xe trắng góc trên trái; img_016 HiAce trắng | SUV mũi dài → `car`; pickup có nắp (img_037) → `truck`; **[v1.1]** xe buýt mini (img_009) → `bus` |
| **[v1.1]** `bus` | Xe chở khách cỡ lớn hoặc vừa, **thân dài liền khối, nhiều hàng cửa sổ**: xe buýt, xe buýt mini (Coaster), xe khách, songthaew. | img_009 Coaster; img_037 xe buýt GO; img_031, img_040 xe buýt; img_008 xe khách phía xa | Xe 16 chỗ (1 hàng cửa sổ ngắn) → `van` |
| `motorcycle` | Xe **2 bánh có động cơ**: xe số, xe tay ga, xe máy điện, mô tô; **kể cả xe có thùng bên (sidecar)**. | img_006, 010, 026; img_029 xe điện; img_022 sidecar | **[v1.1]** Xe đạp, xích lô → `bicycle`; tuk-tuk, xe lam → `car` |
| **[v1.1]** `bicycle` | Xe **không động cơ do người đạp**: xe đạp 2 bánh và **xe 3 bánh thô sơ** (xích lô, xe ba gác đạp). Box chỉ ôm phần xe; người đạp gán `person` riêng (như R-01). | img_006, 029, 039 xe đạp; img_023, 039 xích lô; img_003 xe đạp dựng | Xe đạp điện có động cơ → `motorcycle` |
| `person` | Người thật nhìn thấy trực tiếp, **thấy ít nhất đầu hoặc thân**; mọi tư thế (đi, đứng, ngồi, lái xe hở), kể cả người hóa trang. | img_014 hai người đi bộ; người lái ở img_006; tài xế tuk-tuk img_004 | Tượng (img_017), ma-nơ-canh (img_033), người in trên biển (img_018), **[v1.1]** nhân vật in trên poster (img_008 mép trái), hành khách sau kính xe kín (R-14); chỉ thấy tay hoặc chân |
| `ignore_region` | **Vùng** không gán từng vật; bỏ sót bên trong không tính lỗi. Dùng **chỉ** theo R-02, R-06, R-08, R-09, R-10. | Phía xa img_021; bãi xe img_030 | Không dùng để "né" một vật đơn lẻ đã đủ rõ |

**Vật không thuộc lớp nào**: xem R-02.

### 2.2. Thuộc tính

`occluded_level`, mức che, tính trên **diện tích ước lượng của vật nếu không bị che** (chia 4 bậc đều để dễ ước lượng bằng mắt):

| Mức | Bị che | Ví dụ |
|---|---|---|
| `0` | < 25% | Người đi bộ img_034 |
| `1` | 25% đến < 50% | SUV đỏ sau pickup img_028 |
| `2` | 50% đến < 75% | Tài xế trong tuk-tuk img_004 |
| `3` | ≥ 75% | Người trong thùng sidecar img_022 |

- Phần bị **mép ảnh** cắt **không** tính vào `occluded_level`, mà tính vào `truncated`.
- Hàng rào song mảnh (img_018): tính diện tích thật bị song che, thường < 25%, tức mức `0`.

`truncated`, cắt mép:

| Giá trị | Điều kiện |
|---|---|
| `yes` | **Bất kỳ cạnh nào** của box cách mép ảnh ≤ 3 px. |
| `no` | Không cạnh nào chạm mép. |

Quy tắc này chỉ dựa trên vị trí box nên script kiểm được, và hai người gán không thể hiểu khác nhau.

`can_review`, cần xem lại: tick khi **không chắc** một trong các điểm sau:
1. lớp của vật;
2. vật có thuộc diện gán không (thật hay giả, ngoài taxonomy hay không);
3. biên box có thể lệch > 10% (ảnh tối hoặc nhòe).

Không tick chỉ vì vật bị che nhiều; mức che đã ghi bằng `occluded_level`.

## 3. Quy tắc vẽ box

| Mã | Quy tắc |
|---|---|
| **R-01** | **Người trên xe máy.** Mỗi người (người lái, người ngồi sau, trẻ em đứng hoặc ngồi trước) **1 box `person`** ôm toàn bộ phần người thấy được (mũ, tay, chân). Mỗi xe **1 box `motorcycle`** ôm **phần xe** thấy được (bánh, thân, tay lái, gương). Box xe **không** cố ý bao thân người nhưng được phép chồng lấn. Chỉ gán `motorcycle` khi thấy **≥ 25%** xe; thấy ít hơn (ví dụ chỉ thấy gương, img_040) thì không gán xe. |
| **R-02** | **[v1.1]** Xe buýt → `bus`; tuk-tuk, xe lam → `car`; xe đạp, xích lô → `bicycle`. **Phương tiện còn lại ngoài taxonomy** (xe đẩy, quang gánh, xe kéo tay, tàu…): **không gán lớp.** Nếu box của vật đó cao **≥ 50 px**, phủ **1 `ignore_region`** ôm vật, để mô hình không bị phạt khi phát hiện nhầm thành một lớp khác. Vật cao < 50 px thì bỏ qua. **Người** ngồi hoặc lái các xe này vẫn gán `person`, và phần người được phép nằm trong `ignore_region`. |
| **R-03** | **Pickup luôn là `truck`**, kể cả có nắp thùng kín (img_037) hay chở đồ cá nhân (img_012). |
| **R-04** | **Box ôm sát phần nhìn thấy** (modal), không đoán phần bị che. Không bao bóng đổ hay phản chiếu trên mặt đường ướt. Sai lệch cho phép ≤ 2 px mỗi cạnh (vật cao ≥ 50 px). |
| **R-05** | **Vật không thật thì không gán và không phủ `ignore_region`**: tượng, mô hình, đồ chơi, **[v1.1]** quà lưu niệm, **vỏ xe / thân xe trưng bày** (không kính, không nội thất, ví dụ xe vàng trên nóc img_024), ma-nơ-canh, người hoặc xe in trên biển, poster, tranh tường; ảnh trong gương hay phản chiếu trên kính. **Ngoại lệ:** (a) xe cỡ thật, có người lái, có biển số, đang chạy trên đường (xe diễu hành img_019) → gán theo hình dạng + `can_review`; (b) người hóa trang → `person` + `can_review`. |
| **R-06** | **Xe chở xe / xe trên nóc xe**: xe được chở là xe thật thì gán **từng xe thấy ≥ 25%** theo lớp của nó, kèm `occluded_level`. Các xe được chở thấy < 25% → phủ chung 1 `ignore_region`. Box của xe chở **không** bao các xe được chở nhô lên trên. |
| **R-07** | **Hàng hóa**: box xe **không** bao hàng nhô ra ngoài thân xe (ống dài img_029, bao hàng chất cao img_035). Hàng nằm gọn trong thùng thì tự nhiên nằm trong box. Box người không bao vật người đó cầm hay gánh. |
| **R-08** | **Vật nhỏ**: box cao **< 20 px** → không gán từng vật. Vùng có **≥ 3** vật nhỏ sát nhau → phủ 1 `ignore_region` cho cả cụm. |
| **R-09** | **Đám đông**: một vùng có **≥ 10 vật cùng lớp** và **≥ một nửa** số đó bị che ≥ 50% → gán riêng các vật có `occluded_level` `0` hoặc `1`, phần còn lại phủ `ignore_region` (có thể dùng nhiều vùng). Dưới ngưỡng này thì gán từng vật. |
| **R-10** | **Nhòe chuyển động**: nhận ra lớp → gán, biên box theo **lõi đậm** của vật (không theo vệt nhòe) + `can_review`. Không nhận ra lớp → `ignore_region`. |
| **R-11** | **Xe chủ (ego)** và mọi phần xe của người chụp (khung gương img_020, khung kính img_018): không gán. |
| **R-12** | **Ảnh không có vật hợp lệ** vẫn phải có trong file COCO (không có annotation). |
| **R-13** | **Xe có thùng bên (sidecar)**: 1 box `motorcycle` bao **cả xe và thùng bên**. Người ngồi trong thùng là `person`. |
| **R-14** | **[v1.1]** **Người trong xe kín** (sau kính xe buýt, ô tô, van) **không gán**: box xe đã bao phủ họ và biên người qua kính không ổn định. Người trên **xe hở** (xe máy, tuk-tuk, xe lam, xích lô, xe đạp) vẫn gán `person`. Ví dụ: hành khách xe buýt img_009 không gán. |

### Thứ tự quyết định khi gặp một vật

1. Vật có **thật** và thấy **trực tiếp** không? Không → R-05, R-11.
2. Box cao **≥ 20 px** không? Không → R-08.
3. Có nằm trong **đám đông** thỏa R-09 không? Có → R-09.
4. Thuộc **lớp nào**? Không thuộc lớp nào → R-02. Pickup → R-03. Người trên xe → R-01.
5. Vẽ box theo R-04 và R-07, rồi gán `occluded_level`, `truncated`, `can_review`.

## 4. Ca khó (đã chốt)

| Ảnh | Tình huống | Rule ID | Quyết định |
|---|---|---|---|
| img_001 | Pickup Suzuki chở ống sắt, cắt mép phải, có người đứng che | R-03, R-07 | `truck`, `truncated=yes`, `occluded_level=0`; ống trong thùng không tách box; cô gái `person`; người ngồi trong quán gán từng người (< 10 người, R-09 không áp dụng) |
| img_002 | Đầu kéo chở khoảng 9 ô tô | R-06 | 1 `truck` (đầu kéo + rơ-moóc); từng ô tô thấy ≥ 25% → `car` kèm `occluded_level`; xe tầng dưới thấy < 25% → 1 `ignore_region`; người đứng sau xe `person` |
| img_003 | Gánh hàng, xe đạp, xe máy dựng | R-02, R-07, R-08 | Xe đạp ≥ 50 px → `ignore_region`; người gánh `person` (không bao quang gánh); xe máy dựng `motorcycle` |
| img_004 | 2 tuk-tuk có tài xế | R-02, R-14 | **[v1.1]** Mỗi tuk-tuk 1 `car`; tài xế (xe hở) `person`, `occluded_level=2` |
| img_005 | Người đi xe máy cận cảnh, xe bị che gần hết | R-01 | Từng người `person`; xe thấy ≥ 25% → `motorcycle`; xe 16 chỗ `van`, `occluded_level=2` |
| img_006 | **Ảnh chuẩn R-01**: xe chở 2 người, xe đạp, taxi | R-01, R-02 | Xe 75S1-7182: 2 `person` + 1 `motorcycle`; xe đạp → `ignore_region`, người đạp `person`; taxi `car`, `truncated=yes` |
| img_009 | Xe buýt mini | R-02, R-14 | **[v1.1]** `bus`; hành khách sau kính không gán; người và xe máy theo R-01, R-08 |
| img_011 | Người hóa trang Predator, xe máy độ trưng bày | R-05 | Predator: `person` + `can_review`, `truncated=yes`; xe máy độ có bánh, yên, tay lái → `motorcycle` + `can_review`; người ở xa < 20 px → R-08 |
| img_014 | Xe máy nhòe chuyển động | R-10 | Người đi bộ rõ → `person`; xe máy nhòe nhận ra được → `motorcycle` + người, theo lõi đậm + `can_review` |
| img_015 | 2 xe cắt mép, xe nhòe | R-04, R-10 | Xe đỏ, xe bạc `car`, `truncated=yes`; xe nhòe `car` + `can_review`; không bao phản chiếu mặt đường |
| img_016 | Tuk-tuk, Vespa, HiAce, pickup | R-01, R-02, R-03 | **[v1.1]** Tuk-tuk → `car`; Vespa `motorcycle` + `person`; HiAce `van`; pickup `truck`; người phụ nữ góc phải `person`, `truncated=yes` |
| img_017 | Tượng người cưỡi ngựa | R-05, R-12 | **Không có box** |
| img_018 | Người in trên biển; xe sau hàng rào | R-05, R-11 | Biển không gán; xe `car`/`truck`, `occluded_level=0` (song rào < 25%); xe bị biển treo che thì tính mức theo phần bị che |
| img_019 | Xe diễu hành Dangermouse, đám đông | R-05(a), R-09 | Xe `car` + `can_review`; tài xế `person`; mô hình chuột không gán; đám đông sau rào thỏa R-09 → hàng đầu gán riêng, còn lại `ignore_region` |
| img_020 | Ô tô trong gương chiếu hậu | R-05, R-11 | **Không có box** |
| img_021 | Đám đông xe máy giờ cao điểm | R-01, R-08, R-09 | Gán riêng người và xe có mức che `0`–`1`; phần dày phía sau phủ `ignore_region`; xe buýt xa → R-02 |
| img_022 | Sidecar | R-13 | 1 `motorcycle` bao cả thùng bên; người trong thùng `person`, `occluded_level=3` |
| img_023 | Xích lô | R-02 | **[v1.1]** Xích lô `bicycle`; người đạp `person` |
| img_024 | Xe vàng trên nóc xe đen, bảo tàng | R-05 | Xe đen `car`; **[v1.1]** xe vàng là vỏ xe trưng bày → **không gán**; các xe trưng bày khác `car`; xe cam góc trái `truncated=yes` |
| img_026 | 2 người trên 1 xe, phía sau là tranh tường | R-01, R-05 | 2 `person` + 1 `motorcycle`; tranh tường không gán |
| img_027 | Tượng pickup ở nghĩa trang | R-05 | **Không có box** |
| img_028 | Pickup thật chở tượng ngựa | R-03, R-05 | `truck`; ngựa không gán, không nằm trong box xe (nhô ra trên thùng, R-07); SUV đỏ `car`, `occluded_level=1` |
| img_029 | Ống dài trên xe máy và xe đạp | R-07, R-02 | `motorcycle` + `person`, không bao ống; **[v1.1]** xe đạp `bicycle`, người đạp `person` |
| img_030 | Bãi giữ xe máy dày | R-09 | Xe có mức che `0`–`1` gán riêng; còn lại `ignore_region`; nhân viên `person` |
| img_032 | Đám đông chờ xe buýt | R-09 | Theo R-09; ô tô xanh `car`, `truncated=yes`; nón giao thông không gán |
| img_033 | Ma-nơ-canh, người in, xe phản chiếu | R-05 | **Không có box** |
| img_035 | Xe lam chở hàng | R-02, R-07 | **[v1.1]** Mỗi xe lam `car`, box **không** bao bao hàng chất trên nóc; tài xế `person`; mô tô `motorcycle` + `person`; ô tô `car` |
| img_036 | Xe tải nhỏ mui bạt | R-03 | `truck`; xe máy đỗ dày theo R-09 nếu thỏa ngưỡng |
| img_037 | Pickup có nắp thùng, xe buýt | R-03, R-02 | Pickup `truck`; **[v1.1]** 2 xe buýt `bus` (xe phải `occluded_level=2`); người đi bộ `person` |
| img_038 | Tủ kính bày mô hình xe | R-05 | **Không có box** |
| img_040 | Người đội mũ cận cảnh, chỉ thấy gương xe | R-01, R-02 | `person`, `truncated=yes`; không gán `motorcycle` (< 25%); taxi `car` (box bao cả biển TAXI-METER), `truncated=yes`; SUV đen `car`; **[v1.1]** tuk-tuk `car`, xe buýt `bus` |

| **[v1.1]** img_007 | Pickup Hilux trước xe tải | R-03 | `truck` (cả 052 và 053 gán `car` ở v1.0, tức cùng sai) |
| **[v1.1]** img_008 | Poster nhân vật, xe khách xa | R-05, R-02 | Nhân vật in trên poster mép trái không gán; xe khách phía xa `bus` |
| **[v1.1]** img_030 | Bãi xe máy | R-09 | 2 xe phía trước (che < 50%) gán riêng; các xe phía sau phủ `ignore_region`; nhân viên `person` |

Các ảnh còn lại (010, 012, 013, 025, 031, 034, 039) áp dụng trực tiếp R-01 đến R-04 và R-08. **[v1.1]** Xe đạp và xích lô ở img_003, 006, 039 gán `bicycle`; xe buýt ở img_021, 031 gán `bus`.

## 5. QC và phiên bản

- Ngưỡng theo `taxonomy.json` mục `rules` (**không đổi**): box cao ≥ 20 px; IoU ≥ 0.85 (vật ≥ 50 px) hoặc ≥ 0.7 (vật nhỏ hơn); IAA: IoU trung bình ≥ 0.85 và đồng thuận lớp ≥ 95%; lỗi theo ảnh ≤ 2%.
- **Khóa v1.0** trong suốt Pha 3. Không sửa guideline khi đang gán; ca chưa chắc thì tick `can_review` hoặc ghi lại (ảnh, vùng, lý do) để đưa vào `image_issues.csv` sau khi khóa nhãn.
- Ca mơ hồ do **cả nhóm** chốt ở Pha 5. Mỗi ca một dòng trong `calibration_decisions.csv`, dẫn mã `R-xx`.
- Đổi cách chọn vật, lớp, box hay thuộc tính → `semantic`, tăng phiên bản và kiểm lại cả lô. Chỉ sửa câu chữ → `editorial`.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên | — |
| v0.1-101/102/103 | Bản cá nhân (Pha 1) | Xem `individual/` |
| v1.0 | Hợp nhất 3 bản cá nhân: định nghĩa lớp theo dấu hiệu hình dạng; `occluded_level` 4 bậc 25%; `truncated` theo vị trí box; R-01 đến R-13; ca khó đã chốt | Bất đồng ở mục 6 |
| **v1.1** | **Semantic**: thêm `bus`, `bicycle`; tuk-tuk/xe lam → `car`; xích lô → `bicycle`; vỏ xe/đồ lưu niệm không gán (R-05); thêm R-14; bổ sung ca khó | 60 ca IAA (C001–C060) và 6 quyết định cả lô (L01–L06), xem mục 7 |

## 6. Giải quyết bất đồng giữa các bản cá nhân

Cột 101 / 102 / 103 là mã tạm lúc viết nháp; tương ứng với thành viên **101 = 052**, **102 = 345**, **103 = 053** (`submission/guidelines/individual/`).

| # | Vấn đề | 101 | 102 | 103 | **Chốt v1.0** | Lý do |
|---|---|---|---|---|---|---|
| 1 | Box xe máy có bao người? | Không | Có | Không | **Không** (R-01) | 2/3 đồng ý. Box xe có bao người thì lệch nhiều theo tư thế người, nên IoU giữa người gán thấp. Tách riêng thì mô hình học được hình dạng xe thật. |
| 2 | Tuk-tuk, xe lam | `ignore_region` | `motorcycle` | Không gán | **`ignore_region` khi ≥ 50 px** (R-02) | Ép thành `motorcycle` làm lớp này có hình dạng rất khác nhau, mô hình phải đoán. Không gán gì thì mô hình bị phạt khi phát hiện nhầm. `ignore_region` vừa không dạy sai vừa không phạt. |
| 3 | Xe buýt | `ignore_region` | `truck` | Không gán | **`ignore_region`** (R-02) | Xe buýt không có thùng hàng tách cabin, nên gán `truck` trái định nghĩa. |
| 4 | Pickup | `truck` | Tùy công dụng | `truck` | **Luôn `truck`** (R-03) | "Công dụng" không nhìn ra từ ảnh. Khe cabin–thùng thì nhìn thấy được, nên người gán thống nhất. |
| 5 | Xe được chở (img_002, 024) | Gán từng xe | `ignore_region` | Gán xe thấy ≥ 25% | **Gán xe thấy ≥ 25%, còn lại `ignore_region`** (R-06) | Xe được chở vẫn là xe thật, mô hình cần nhận ra. Ngưỡng 25% tránh tranh cãi về xe bị khung che gần hết. |
| 6 | Đám đông | ≥ 5 vật bị che ≥ 80% | Gán hết | ≥ 10 vật, một nửa bị che ≥ 50% | **Ngưỡng của 103** (R-09) | Đếm được, áp dụng giống nhau. Gán hết như 102 thì img_021, 030 cần hàng trăm box, dễ sai. |
| 7 | Mức `occluded_level` | 10/40/80 | 0/35/70 | 25/50/75 | **25/50/75** | Bốn bậc đều (¼, ½, ¾) dễ ước lượng bằng mắt nhất, giảm lệch thuộc tính. |
| 8 | `truncated` | Chạm mép và còn tiếp | Bị cắt ≥ 10% | Chạm mép ≤ 3 px | **Chạm mép ≤ 3 px** | Chỉ dựa vào vị trí box, nên script kiểm được và không cần phán đoán. |
| 9 | Xe diễu hành img_019 | `car` + `can_review` | `car` | Không gán | **`car` + `can_review`** (R-05a) | Xe cỡ thật, có biển số, đang chạy trên đường, nên mô hình gặp ngoài đời thì cũng phải tránh. |
| 10 | Predator img_011 | `person` + `can_review` | `person` | Không gán | **`person` + `can_review`** (R-05b) | Tên ảnh gốc ghi "costumed character", tức người hóa trang. Vẫn đánh dấu để xem lại ở Pha 5. |
| 11 | Sidecar img_022 | Bao thùng | Bao thùng | Không bao thùng | **Bao thùng** (R-13) | 2/3 đồng ý; thùng bên gắn cố định vào xe. |
| 12 | Hàng chất trên xe lam img_035 | Không bao | Bao | Không bao | Không áp dụng: xe lam đã là `ignore_region` (R-02); quy tắc chung R-07 là **không bao hàng nhô ra** | 2/3 đồng ý. |
| 13 | Ngưỡng thấy xe máy để gán | 20% | Không nói | 25% | **25%** (R-01) | Thống nhất với ngưỡng 25% ở R-06 và `occluded_level`. |
| 14 | Nhòe chuyển động | Gán nếu biên lệch ≤ 10% | Gán nếu nhận ra lớp | Gán theo lõi đậm | **Gán theo lõi đậm + `can_review`** (R-10) | "Lõi đậm" cho người gán một biên cụ thể để vẽ. |

## 7. Calibration (Pha 5) — tóm tắt

Nguồn: `submission/qc/calibration_decisions.csv` (60 ca IAA + 6 quyết định cả lô). IAA trước calibration giữ nguyên trong `iaa_summary.md`.

| Nhóm ca | Ca | Kết luận | Quy tắc |
|---|---|---|---|
| Phương tiện mới | C013, C014, C022, C024, C054–C056, C058; L01–L03 | Thêm `bus`, `bicycle`; tuk-tuk/xe lam → `car` | R-02 [v1.1] |
| Pickup gán `car` | C019, C031, C033, C034 | Luôn `truck`. img_007: hai người cùng gán `car` → **cùng sai**, IAA không phát hiện được | R-03 |
| Vật không thật | C021, C041, C042; L04 | Poster, vỏ xe, tượng → không gán | R-05 [v1.1] |
| Người sau kính | C025, C026; L06 | Không gán | R-14 (mới) |
| Đám đông | C035, C044–C052 | Không dùng 1 box `person` cho cả đám đông; dùng `ignore_region` + gán riêng hàng đầu | R-09 |
| Bỏ sót do sơ suất | C001, C003–C012, C015, C016, C020, C023, C027, C029, C030, C032, C036, C039, C040, C043, C053 | Một người lệch, quy tắc rõ → **sửa nhãn, không sửa guideline** | R-01, R-04, R-08 |
| Biên box | C002, C017, C038, C059, C060 | Chọn box đúng theo R-04/R-13; xóa box trùng | R-04, R-13 |
| Thuộc tính | L05 | Cả 3 người để mặc định `occluded_level=0`, `truncated=no` → rà lại cả lô | Mục 2.2 |

**Phạm vi sửa:** cả lô 40 ảnh (có quyết định `pham_vi=lo`, taxonomy đổi lớp).
