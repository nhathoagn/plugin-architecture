---
name: ut-report
description: Viết báo cáo UT (unit test do dev tự test) của một màn (hệ cũ ↔ hệ mới) ra file Excel theo template chuẩn của team — dòng đầu Branch / Redmine, cột Case (#, Nhóm, Trường hợp mã 1.1), Mong đợi (Hệ cũ, Hệ mới), Ngày test, Kết quả (dropdown OK/NG/NA/NT/NG -> OK), Tester (Dev), Note/Lý do; nhóm Layout / Quyền truy cập / Mở màn / Validation / Nghiệp vụ / Database / Message / CR. Dùng khi được yêu cầu "viết report UT", "UT report", "báo cáo UT", "báo cáo unit test", "điền sheet UT", hoặc xuất kết quả UT một màn ra xlsx.
---

# ut-report — báo cáo UT theo template

Kết quả là **một file `.xlsx`** đúng template của team. Một dòng là một case. Mỗi case so
"Hệ cũ làm gì" với "Hệ mới làm gì", rồi ghi kết quả UT do dev chạy thật.

Sheet chuẩn để viết theo: file UT mẫu mà dự án chỉ định (hỏi người dùng nếu rule dự án không ghi).
Đọc lại khi cần mẫu. Ba kiểu sheet mẫu thường gặp:

| Kiểu sheet mẫu | Lấy gì |
|---|---|
| Màn danh sách + batch con, 1 file nhiều sheet | Bố cục, style, cách đánh số case, nhóm Nghiệp vụ / CR |
| Màn nhập liệu | Cách viết nội dung case, chú thích tiếng Nhật, Note, nhóm màn nhập liệu |
| Màn + batch trong 1 sheet (Phần A / Phần B) | `NG -> OK`, nhóm batch nhập CSV |

## 0. Trước khi làm

1. Đọc rule của dự án (`AGENTS.md` / `CLAUDE.md`). **Rule dự án thắng skill này.**
   Dự án viết lại thường có luật: đổi kiến trúc, không đổi hành vi. Điểm khác hệ cũ phải có CR.
2. Xác định mã màn `{SID}`, link MR (Branch) và link Redmine. Thiếu → hỏi người dùng, không đoán.
3. Đọc nguồn nghiệp vụ của màn, theo thứ tự ưu tiên:
   - `works/screens/{SID}.yaml` (spec màn).
   - Code hệ cũ (rule, validator, SQL) — nguồn đúng cho cột **Hệ cũ**.
   - Code hệ mới FE/BE — nguồn cho cột **Hệ mới**.
   - CR / Figma / design người dùng đưa (nếu có).
4. Có kết quả parity sẵn (`legacy-parity-validation`) hoặc so ảnh (`ui-image-check`) → dùng lại,
   không chạy lại.

## 1. Template — không đổi

Bố cục một sheet (theo `UT-AB1010.xlsx`):

| Dòng | Nội dung |
|---|---|
| 1–5 | Ô trắng có viền, cột A–I. `B2` = `Branch`, `C2` = link MR. `B3` = `Redmine`, `C3` = link issue. |
| 5 | `B5` chữ đỏ đậm: `※ OK khi đồng nhất giữa hệ mới và hệ cũ, nếu trường hợp khác thì note lý do` |
| 6–7 | Header 2 tầng, nền `1F4E78`, chữ trắng đậm. |
| 8+ | Dữ liệu. Font Times New Roman 10. Ô `#` và `Nhóm` chữ đậm, nền `DDEBF7`, gộp theo nhóm. |

| Khối | Cột | Ghi gì |
|---|---|---|
| Case | `#` | Số thứ tự **nhóm** (1, 2, 3…). Gộp ô theo nhóm. |
| Case | `Nhóm` | Tên nhóm. Gộp ô theo nhóm. Có thể thêm dòng chú thích: `Layout` + `(Bố cục)`. |
| Case | `Trường hợp` | `{nhóm}.{số}  ` + điều kiện / thao tác test. Script tự thêm mã. |
| Mong đợi | `Hệ cũ` | Hành vi hệ cũ thật. Không áp dụng → `-`. |
| Mong đợi | `Hệ mới` | Hành vi hệ mới. Giống hệ cũ → `Như hệ cũ`. |
| | `Ngày test` | Ngày chạy thật, dạng `d/m/yyyy`. Chưa chạy → để trống. |
| | `Kết quả` | Dropdown: `OK` / `NG` / `NA` / `NT` / `NG -> OK`. Không tô màu. |
| | `Tester (Dev)` | Người chạy test. Mặc định `tester` trong YAML, không có thì `git config user.name`. |
| | `Note/Lý do` | Lý do khác hệ cũ, lý do NA/NG, link CR, nguồn kiểm chứng (`file:line`). |

Độ rộng cột: A 6, B 26, C 48, D 42, E 42, F 17.15, G 16.57, H 20, I 40.

Một màn có màn con hoặc batch:
- Mỗi mã một sheet trong cùng file (vd. `UT-AB1010.xlsx` có sheet `AB1010` và batch `AB1012`).
- Hoặc một sheet chia phần (vd. `CD2011`): dòng tiêu đề nền vàng `FFFF00`, chữ đậm,
  vd. `Phần A — CD2010 (màn hình)`, `Phần B — CD2011 (batch, chạy từ CD2010)`.
  Mỗi phần có header riêng. Số nhóm bắt đầu lại từ 1.

### Nhóm

Giữ thứ tự dưới, bỏ nhóm không áp dụng. Thêm nhóm riêng của màn ở chỗ hợp lý.

**Màn hình:**

1. **Layout** — case đầu luôn là `Theo figma`. Hệ cũ `-`. Hệ mới:
   `Đã đúng với figma, nội dung CR đã được phản ánh.` + danh sách `- Giao diện` / `- Message` /
   `- Dialog/Loading` / `- Responsive`. Note: `Theo figma, hệ cũ đã không còn phù hợp.`
   Thêm case so phần không theo figma: đủ ô, đúng thứ tự, nội dung từng combobox.
2. **Quyền truy cập** — có quyền trực tiếp, có quyền qua nhóm quyền, nhóm đã xoá, không có quyền (gõ thẳng URL),
   chưa đăng nhập, mục trên menu.
3. **Mở màn** (`初期表示`) — mở không kèm tham số, tham số không có trong master, dữ liệu đã có / chưa có.
4. Nhóm riêng của màn, vd. `Giá trị tự điền (khi ô đang trống)`, `Combo / Check box`, `Ô nhập / ô chỉ xem`,
   `Nghiệp vụ – Popup`.
5. **Validation** — chia theo nút nếu cần: `Validation — kiểm phía màn (確定登録 (Đăng ký xác nhận))`,
   `Validation — luật nhập (確定登録 (Đăng ký xác nhận))`. Mỗi rule một case: rỗng, độ dài, ký tự,
   toàn góc / khoảng trắng, liên ô, thứ tự check, nhiều lỗi cùng lúc.
6. **Nghiệp vụ – {action} ({mã xử lý})** hoặc **Action trên màn hình + Database ({nút})** — một nhóm cho mỗi nút / xử lý,
   vd. `Nghiệp vụ – 検索 (AB101001)`, `Nghiệp vụ – CSV出力 (AB101002)`, `Action trên màn hình + Database (再読込 (Tải lại))`.
   Gồm: hộp xác nhận, Huỷ, thành công, bấm liên tục, kết quả 0 dòng / quá giới hạn, thứ tự, định dạng số.
7. **Action trên màn hình + Database (cập nhật đồng thời)** — 2 user cùng sửa, lưu gần như cùng lúc.
8. **Xử lý Database** — bảng đọc / ghi, điều kiện lọc (`FLG_DELETE`, JOIN), so SQL hệ cũ, bảng không đổi khi chỉ đọc.
9. **Message / Dialog** — hộp xác nhận, message thành công, khung lỗi, cuộn tới lỗi, loading.
10. **CR** (hoặc `CR / chức năng không có`) — mỗi điểm khác hệ cũ có CR là một case.

**Batch / file CSV:** `Layout file CSV (Bố cục file)` (tên file, encoding, xuống dòng, header) /
`Dòng 2 (mã cột) / cấu trúc file` / `Validate (Kiểm tra đầu vào)` / `Đọc ô dữ liệu` / `Rule nhập liệu` /
`Nghiệp vụ – chạy batch` / `Nghiệp vụ – nội dung từng cột` / `Kết quả kiểm cả file` / `Ghi DB` /
`Tiến độ / kết quả` / `Trạng thái ở 処理状況 (tình trạng xử lý)` / `CR`.

## 2. Quy tắc điền Kết quả

- **Mọi case phải mở UI thật của cả hai hệ để test** (trình duyệt, gõ vào ô, bấm nút, đọc màn hình).
  Không thay UI bằng gọi API/HTTP trực tiếp, không kết luận theo code. API/code chỉ ghi thêm vào Note làm bằng chứng.
  Trạng thái khó tạo (đang gửi, hết phiên) cũng làm trên UI: giữ request trong trình duyệt, đăng xuất ở tab khác.
- `OK` — đã chạy thật, hệ mới giống hệ cũ.
  Hệ mới khác hệ cũ có lý do được chấp nhận → vẫn `OK`, Note **bắt buộc** ghi lý do (xem bảng dưới).
- `NG` — đã chạy thật, sai. Note ghi hành vi thật + `file:line` chỗ sai.
- `NG -> OK` — lần đầu NG, đã sửa, chạy lại OK. Note: `NG : {lỗi} -> Đã fix`, vd. `NG : Sai message -> Đã fix`.
- `NA` — không áp dụng / không so được. Note **bắt buộc** ghi lý do.
- `NT` (Not Tested) hoặc để trống — chưa chạy.
- **Không ghi `OK`/`NG` khi chưa chạy thật.** Đọc code thôi → `NT`, Note ghi `Theo code (chưa chạy)`.
- Không chạy case đổi dữ liệu thật khó hoàn tác (xoá, đổi MK thành công, gửi mail). Ghi `NT` + lý do.
- Hệ cũ chưa kiểm được → cột Hệ cũ ghi `(Chưa xác nhận – kiểm trên hệ cũ rồi ghi vào đây.)`, Kết quả `NT`.
- Hệ mới khác hệ cũ mà không có lý do được chấp nhận → `NG`, Note `Khác hệ cũ, cần CR nếu giữ`.

Note cho case `OK` mà hệ mới khác hệ cũ (dùng đúng chữ):

| Note | Khi nào |
|---|---|
| `Theo CR` | Có CR được duyệt. Thêm mã / link CR nếu có. |
| `Theo figma` / `Theo design` / `Theo CR và figma` | Giao diện theo figma / design mới. |
| `Theo hệ mới` | Hành vi chung của hệ mới (trang 403, `/sign-in?redirect=`, khoá nút khi xử lý). |
| `Chuẩn chung hệ mới` | Dialog, khung message, loading, cuộn tới lỗi dùng chung mọi màn. |
| `Thông báo lỗi theo rule mới` | Cùng message, khác cách hiện (khung lỗi, dòng header `入力内容に誤りがあります。`). |

Note thêm khi cần: nguồn cấu hình (vd. `config/app.php upload_rate_limit_per_minute = 3`),
tham chiếu case khác (`xem case CR 8.12`, `Xem sheet AB1012, case 6.1`), cách kiểm (`So số dòng và DATE_UPDATE trước và sau`).

## 3. Viết case

- Một câu một ý. Viết tiếng Việt, giữ nguyên message/identifier gốc (tiếng Nhật, mã lỗi, tên bảng/cột).
- **Thuật ngữ tiếng Nhật kèm chú thích tiếng Việt** trong ngoặc: `品番 (mã hàng)`, `確定登録 (Đăng ký xác nhận)`,
  `再読込 (Tải lại)`. Message tiếng Nhật kèm bản dịch trong ngoặc sau message.
- Cột Trường hợp ghi **điều kiện dữ liệu và giá trị cụ thể**: `外径 (đường kính ngoài): 7 ký tự / 8 ký tự (vd 1234.56 / 12345.67)`,
  `受注日 (từ) nhập ngày không có thật: 2026/02/30. Bấm 検索.` Không viết chung chung.
- Một case có thể gộp cặp biên: `12345 / 123456`. Case lặp cho nhiều ô: `Lặp lại case 2.6 – 2.10 cho 納入先 và 需要家.`
- Cột Hệ cũ ghi đủ: điều kiện dữ liệu (bảng, cột, giá trị), message nguyên văn, giá trị lưu DB, trạng thái nút.
  Liệt kê nhiều ý bằng dòng bắt đầu `- `.
- Cách mô tả message (dùng đúng chữ):
  - `Popup: {message}` — alert của trình duyệt.
  - `Hỏi: {message}` — hộp xác nhận.
  - `Message không có dòng tiêu đề: {message}` — message hiện trên trang, không có dòng header.
  - `Khung lỗi dưới tiêu đề màn: 入力内容に誤りがあります。 + {message}` — khung lỗi hệ mới.
  - Có mã message → ghi kèm: `M00005 「検索条件は、１つ以上指定して下さい！」`.
- Case có message lỗi theo ô: cột Hệ cũ và Hệ mới viết **đủ** dòng header và từng message, theo thứ tự trên màn hình:

```text
Báo lỗi:
入力内容に誤りがあります。
形状に誤りがあります。文字数を範囲内（～35）にして下さい。
```

- Cột Hệ cũ lấy từ code/chạy hệ cũ, không lấy từ tài liệu. Hành vi lạ của hệ cũ thì ghi lý do,
  vd. `(SQL Server bỏ qua khoảng trắng cuối khi so =)`, `Message hệ cũ ghi nhầm tên ngày`.
- **Thứ tự check** nằm trong nhóm Validation, sau các case đơn. Lấy thứ tự từ code hệ cũ, ghi chuỗi
  `không có cặp ngày nào → 変更日 thiếu một đầu → …`, rồi thêm case nhập nhiều lỗi cùng lúc: `Chỉ báo lỗi đầu tiên (…)`.
- **Case CR**: đầu cột Trường hợp ghi mã CR trong ngoặc vuông, vd. `[CR-AB1010-banner] Không nhập gì, bấm 検索 (M00005).`
  Hệ cũ ghi hành vi cũ (vd. `Có`), Hệ mới ghi hành vi mới (vd. `Không có`). Case ở nhóm khác bị CR ảnh hưởng →
  Note `xem case CR 8.12`.

### Số thập phân và làm tròn — bắt buộc khi màn có số

Màn có số tiền, đơn giá, tỷ giá, thuế, số lượng hoặc tỷ lệ phải có case cho phần này. Đặt các case trong nhóm
tự tính hoặc nhóm hiển thị của màn. Một số hiển thị sai sẽ dẫn tới lưu sai, vì lần lưu sau ghi lại chữ đang hiện.

1. **Liệt kê mọi số trên màn:** khi mở màn, sau khi màn tự tính, trong danh sách, và khi mở lại sau khi lưu.
   Với mỗi số, đọc code hệ cũ để biết:
   - số chữ số lẻ, và nguồn của số đó (cố định, hay theo master, vd. mã tiền tệ),
   - cách làm tròn, đọc ở cả 3 nơi:
     - Java `DecimalFormat`/`BigDecimal`: HALF_EVEN, HALF_UP hay cắt,
     - JS phía trình duyệt: `Math.round` làm tròn nửa lên về phía +∞, nên `-2.5` → `-2`; `toFixed`; hàm tự viết cắt chữ số,
     - SQL: SQL Server `CONVERT(int)` **cắt**, còn PostgreSQL `CAST(... AS INTEGER)` **làm tròn**,
   - dấu phẩy hàng nghìn. Hàm JS hệ cũ có thể chèn dấu phẩy cả vào phần lẻ, vd. `1.2345` → `1.2,345`.
2. **Mỗi số một case**, cột Trường hợp ghi giá trị cụ thể. Bắt buộc có các giá trị sau:
   - **Đúng mốc làm tròn:** `2.5`, `-2.5`, `0.125` (2 số lẻ), `2.675`, `8.345`, `1.015`.
     Java `DecimalFormat` (JDK 8 trở lên) làm tròn trên giá trị nhị phân thật của số:
     `2.675` là `2.67499…` nên → `2.67`, `8.345` là `8.34500…06` nên → `8.35`.
     Kiểm giá trị thật bằng `node -e "console.log((2.675).toFixed(40))"`.
   - **Số lẻ nhiều hơn số chữ số hiển thị**, cả dữ liệu lưu sẵn trong DB (vd. 受注数 lưu `2.5`).
   - **Số lớn:** `≥ 1000` (dấu phẩy), số tối đa của ô, số âm.
   - **Phần lẻ dài:** `1234.5678`, xem có chèn dấu phẩy vào phần lẻ không.
   - **Phép tính dây chuyền:** tỷ giá × đơn giá → làm tròn → × số lượng. Ghi từng bước của hệ cũ.
   - **Trống / không phải số / ô khác đang sai:** ví dụ 受注数 trống thì 単価 còn được định dạng không.
3. **Cột Hệ cũ** ghi input → output của từng giá trị, kèm `file:line` của hàm làm tròn.
4. **Không có dữ liệu để chạy:** khi DB thiếu giá trị đúng mốc, ghi `NT`, Note `Theo code (chưa chạy)`, và ghi
   cách đã kiểm thay thế, vd. script so hàm hệ mới với cách hệ cũ trên lưới số.
5. **Kết quả phụ thuộc phiên bản Java** của hệ cũ (JDK 7 và JDK 8+ làm tròn khác nhau ở mốc nửa): ghi rõ phiên bản
   đã giả định trong Note. Phiên bản chưa xác nhận thì ghi `chưa xác nhận bản JDK`.

### Case bắt buộc từ lỗi đã lọt qua UT

Mỗi mục dưới là một loại lỗi đã lọt qua UT của một màn viết lại, rồi bị tester bắt ở Integration Test.
Màn có tình huống tương ứng thì phải có case. Màn không có tình huống đó thì bỏ mục, không cần dòng `NA`.

1. **Giá trị tự điền khi mở màn và sau khi lưu.** Đọc nhánh khởi tạo / tải dữ liệu của hệ cũ. Liệt kê mọi ô
   hệ cũ tự điền, kèm điều kiện: chế độ (新規 / 変更), lần tải đầu hay mọi lần, một bản ghi hay tất cả bản ghi.
   Mỗi ô có hai case:
   - điều kiện đúng → ô có đúng giá trị hệ cũ (vd. 完納区分 = `00 未完`, 年月 = `yyMM` của ngày hiện tại),
   - điều kiện sai → ô để trống như hệ cũ. Hệ mới hay điền mặc định ở mọi lần tải.
2. **Chữ hiển thị của mã master.** Mỗi ô hiển thị mã có một case. Cột Hệ cũ ghi đúng chữ: chỉ mã, chỉ tên,
   hay mã + khoảng trắng + tên (vd. `10　新規_編集`). Thêm case mã đã xoá khỏi master, và mã không có trong master.
3. **Check trên chữ người dùng gõ.** Ô mà hệ cũ kiểm ký tự đầu / cuối có các case: dấu cách nửa góc ở đầu (`␣9`),
   dấu cách ở cuối, dấu cách toàn góc. Hệ mới có thể trim trước khi check, nên check không bao giờ báo lỗi.
4. **Ô tự tính từ ô khác.** Mỗi ô tự tính có ba case: ô nguồn có giá trị, ô nguồn đổi sang giá trị khác,
   và **xoá trống** ô nguồn (vd. xoá 納入先 thì 自社出荷伝票 phải bỏ tick). CR chỉ nói case có giá trị thì hỏi
   case trống, ghi câu trả lời vào Note.
5. **Đổi phạm vi hoặc bản ghi.** Có case cho mỗi lần đổi: từ "tất cả" sang một bản ghi, từ bản ghi này sang
   bản ghi khác, và quay lại cùng bản ghi sau khi xem "tất cả". Kiểm mọi ô có giá trị mặc định của phạm vi cũ:
   ô phải được xoá hoặc tải lại (vd. 販売部門, 担当者, 受注数 sau khi chọn một 製番 từ (全製番)).
6. **Cách hiện thông báo.** Mỗi message thành công và mỗi message lỗi có một case. Cột Hệ cũ ghi đúng hình thức:
   `Popup:` (alert, bấm OK là đóng) hay message trên trang. Hệ mới phải hiện cùng hình thức. Message dạng popup
   không được nằm lại trên màn sau khi đóng. Làm case cho mọi nút ghi, kể cả nút lưu tạm (一時保存).
7. **Nhánh hệ cũ phân biệt dạng dữ liệu** (vd. `length() == 2` để biết ô đang chứa mã hay nhãn). Đọc DB thật để
   biết những dạng giá trị nào có tồn tại (mã 2 ký tự, rỗng, NULL). Mỗi dạng có một case, kèm điều kiện liên quan
   (vd. 履歴 = 0 hoặc > 0). Dạng không tồn tại trong DB → ghi `NA`, Note ghi câu truy vấn và số dòng.

Mỗi bug tester đã báo cho màn này cũng là một case: ghi số bug trong Note, Kết quả `NG -> OK` sau khi đã chạy lại.

## 4. Sinh file

1. Viết file dữ liệu YAML (giữ lại để sửa và sinh lại):
   `works/ut-report/{SID}-UT-report.yaml`. Dự án không có thư mục `works/` → hỏi nơi lưu.
   **Không dùng dấu `"` và không viết `\n`.** Mọi trường chữ (`name`, `title`, `case`, `legacy`, `new`, `note`)
   viết dạng block `|-`, mỗi dòng trong ô Excel là một dòng YAML.

```yaml
tester: DevName
branch: |-
  https://gitlab.example.com/group/project/-/merge_requests/1
redmine: |-
  https://redmine.example.com/issues/1
sheets:
  - name: AB1010
    groups:
      - name: |-
          Layout
          (Bố cục)
        cases:
          - case: |-
              Theo figma
            legacy: |-
              -
            new: |-
              Đã đúng với figma, nội dung CR đã được phản ánh.
              - Giao diện
              - Message
              - Dialog/Loading
              - Responsive
            date: 2026-10-23
            result: OK
            note: |-
              Theo figma, hệ cũ đã không còn phù hợp.
      - name: |-
          Validation — luật nhập (検索)
        cases:
          - case: |-
              得意先 (khách hàng) nhập 13 ký tự: ABCDEFGHIJKLM. Bấm 検索.
            legacy: |-
              Báo lỗi:
              操作に誤りがあります。
              得意先に誤りがあります。文字数を範囲内（～12）にして下さい。
            new: |-
              Báo lỗi:
              入力内容に誤りがあります。
              得意先に誤りがあります。文字数を範囲内（～12）にして下さい。
            date: 2026-10-23
            result: OK
            note: |-
              Thông báo lỗi theo rule mới
      - name: |-
          CR
        cases:
          - case: |-
              [CR-AB1010-no-sort] Bấm tiêu đề một cột (vd. 製番 (số chế tạo)).
            legacy: |-
              Xếp theo cột đó.
            new: |-
              Không xếp lại.
            result: NT
            note: |-
              Theo CR
  - name: AB1012
    groups:
      - name: |-
          Layout file CSV
          (Bố cục file)
        cases:
          - case: |-
              Xuất CSV xong, xem tên file tải về.
            legacy: |-
              TCA00001_yyyyMMddHHmmss.csv
            new: |-
              Như hệ cũ
```

   - `tester`, `branch`, `redmine` đặt ở gốc. Một sheet có thể ghi đè `branch` / `redmine`.
   - Một sheet: bỏ `sheets`, đặt `groups` (và `sheet: {SID}` cho tên sheet) ở gốc.
   - Màn + batch trong một sheet: thay `groups` bằng `sections`, mỗi phần có `title` (dòng vàng) và `groups`.
   - Không gõ mã `1.1` vào `case`. Script tự thêm. File YAML cũ đã tự gõ mã (vd. `V01.`) → đặt `numbering: false`.
   - Luôn dùng `|-` cho trường chữ, kể cả một dòng. Viết thường (`key: giá trị`) dễ bị YAML hiểu sai
     khi giá trị có `: `, `#`, hoặc bắt đầu bằng `-`.
   - `date`: `YYYY-MM-DD` hoặc bỏ trống. `result`: `OK` / `NG` / `NA` / `NT` / `NG -> OK` hoặc bỏ trống.
     YAML cũ ghi `Pending` → script đổi thành `NT`.
   - `tester` của case bỏ trống → lấy `tester` gốc khi case đã có `date`.
   - `layer: FE|BE|FE+BE` (tuỳ chọn) → thêm cột J `Lỗi ở (FE/BE)` cho case NG.
   - Nhóm chưa có case → `cases: []`, script sinh một dòng trống. `note` cấp nhóm ghi vào dòng trống đó.
   - `- {}` trong `cases` → một dòng trống có dropdown trong nhóm (không tính là case).
   - `extra_rows: n` → thêm n dòng trống có dropdown cuối mỗi bảng (mặc định 0).
   - Kiểm tra: `grep -c '"' file.yaml` phải ra `0`.

2. Chạy script `scripts/build_report.py` trong thư mục của skill này. Claude Code in đường dẫn đó
   ở dòng `Base directory for this skill` khi nạp skill. Script cần `pyyaml` và `openpyxl`.

```bash
python {thư mục skill}/scripts/build_report.py \
  works/ut-report/{SID}-UT-report.yaml works/ut-report/{SID}-UT-report.xlsx
```

   Script kẻ dòng 1–5, header 2 tầng, gộp ô `#` / `Nhóm`, thêm mã case, bọc chữ, gắn dropdown,
   freeze ở `D8` (sheet một bảng).

3. Kiểm chứng: script in số case và số theo từng kết quả của mỗi sheet. Exit code ≠ 0 → sửa YAML rồi chạy lại.

## 5. Trả lời người dùng

- Đường dẫn file `.xlsx` và `.yaml`.
- Bảng tóm tắt: số case theo `OK` / `NG` / `NG -> OK` / `NA` / `NT`.
- Danh sách case `NG` (mã case + trường hợp + `file:line`).
- Case chưa chạy và lý do.
