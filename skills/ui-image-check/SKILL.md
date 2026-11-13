---
name: ui-image-check
description: Đối chiếu một ảnh giao diện (mockup SVG/PNG/JPG, ảnh chụp màn hình, ảnh Figma export) với code FE/BE thật — liệt kê từng item trong ảnh rồi kiểm item đó có trong code không, chữ/thứ tự/trạng thái/kích thước có khớp không, kèm file:line. Dùng khi được đưa một ảnh và yêu cầu "check lại trong code", "so ảnh với code", "màn này đã đúng mockup chưa", "liệt kê item trong ảnh".
---

# ui-image-check — so một ảnh giao diện với code

Áp dụng khi người dùng đưa **một ảnh** (đường dẫn hoặc dán vào chat) và muốn biết code hiện tại
đã có đủ, đúng những gì trong ảnh chưa. Kết quả là **báo cáo chênh lệch**, không phải bản sửa.

## 0. Trước khi làm

1. Đọc rule của dự án (`AGENTS.md` / `CLAUDE.md` ở gốc repo và ở thư mục FE/BE). **Rule dự án thắng skill này**
   — kể cả nơi lưu báo cáo, cổng dev server, cách dựng màn.
2. Từ rule dự án, xác định và ghi lại:
   - Thư mục mã FE (page, components, file i18n/locales) và BE (route, controller, service).
   - Spec màn hình nếu dự án có (vd file yaml/markdown theo mã màn). Spec là nghiệp vụ; ảnh chỉ là bản vẽ.
   - Dự án có phải bản **viết lại** hệ cũ với luật "không đổi hành vi nếu không có CR" không (ảnh hưởng §5).

## 1. Đầu vào và đầu ra

- Đầu vào: một file ảnh (`.svg`, `.png`, `.jpg`) hoặc ảnh dán trong chat. Tuỳ chọn: mã màn hoặc route.
- Thiếu mã màn/route → tự suy từ ảnh (tiêu đề màn, menu đang chọn) rồi `grep` tiêu đề trong thư mục FE.
  Ra nhiều hơn một màn → hỏi người dùng, không đoán.
- Đầu ra mặc định: báo cáo trong chat theo §5. Người dùng yêu cầu lưu → theo nơi rule dự án quy định;
  không có quy định thì hỏi (gợi ý `reports/ui-image-check-{slug}.md`).
- **Không sửa code** trong skill này. Sửa là việc riêng, chỉ làm khi được yêu cầu, theo rule dự án.

## 2. Đọc được ảnh

| Loại ảnh | Cách đọc |
| --- | --- |
| PNG / JPG / ảnh dán | Mở thẳng bằng Read. |
| SVG có `<text>` | `grep -o '<text[^>]*>[^<]*' file.svg` lấy chữ, vẫn render (dòng dưới) để thấy bố cục. |
| SVG chữ đã outline (`grep -c '<text'` = 0, thường gặp với Figma export) | Render ra PNG rồi Read. Chữ nhỏ → render lại phóng to từng vùng để chép chữ. |

Render ra file trong **scratchpad**, không ghi vào repo. Kích thước lấy từ `width`/`height` của thẻ `<svg>`
(`head -c 300 file.svg`). Một trong hai cách:

```bash
# Chrome headless (Windows: "/c/Program Files/Google/Chrome/Application/chrome.exe";
# macOS: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; Linux: google-chrome)
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size={W},{H} \
  --force-device-scale-factor=1 --screenshot="{scratchpad}/{name}.png" "file:///{đường dẫn tuyệt đối}.svg"
```

```js
// Playwright: viewport = kích thước SVG; chụp từng vùng với deviceScaleFactor: 2 khi cần đọc chữ nhỏ
await page.goto('file:///{đường dẫn tuyệt đối}.svg');
await page.screenshot({ path, clip: { x, y, width, height } });
```

## 3. Liệt kê item trong ảnh

Đi theo vùng, từ trên xuống, trái sang phải. Mỗi item ghi: **vùng · loại · chữ nguyên văn · trạng thái**.

- **Vùng:** header · sidebar · tiêu đề màn · từng panel/section · thanh nút · vùng kết quả/thông báo · footer · dialog.
- **Loại:** nhãn, ô nhập, danh sách chọn, option, nút, badge (`必須`, `Required`…), icon có nghĩa, thông báo,
  link/nút tải file, bảng + cột, **đường kẻ / viền / gạch chân / vạch ngăn** (đếm số đường, ghi độ dài và vị trí).
- **Chữ:** chép **nguyên văn** kể cả dấu ngoặc toàn/nửa góc (`（）` ≠ `()`), khoảng trắng, số toàn góc (`２`).
- **Trạng thái:** đang chọn, mở/thu gọn, disabled, ẩn/hiện theo điều kiện, có thanh cuộn, dấu ✓.
- **Kích thước/màu** (chỉ khi người dùng quan tâm hoặc ảnh có ghi spec): đo bằng pixel trên ảnh render 1:1
  (chiều cao dòng, độ rộng cột, khoảng cách, màu nền/viền/chữ).
- Chữ không đọc chắc chắn được → ghi `[không rõ]`, không đoán.

Đánh dấu mỗi item một trong ba nguồn trước khi tra code — vì cách kiểm khác nhau:

| Nguồn | Ví dụ | Kiểm ở đâu |
| --- | --- | --- |
| **Tĩnh** — chữ viết cứng trên FE | tiêu đề, nhãn field, nút, option cố định | mã FE (page, components, hằng số, file i18n) |
| **Dữ liệu** — đến từ API/DB | menu sidebar, danh sách lựa chọn từ server, tên user, ngày | endpoint BE + nơi nó đọc (config, service, bảng) |
| **Mẫu** — giá trị minh hoạ của người vẽ | tên file kết quả, ngày cụ thể, tên người mẫu | chỉ kiểm **định dạng** (vd `{ID}_{YYYYMMDD}.csv`), không kiểm giá trị |

## 4. Tra từng item trong code

1. Tìm thư mục màn: `grep -rn "{tiêu đề màn}"` trong thư mục page/route của FE.
2. Đọc page và toàn bộ components của màn — **đọc file**, không chỉ grep.
   **Đọc cả component dùng chung mà màn import** (layout, breadcrumb/tiêu đề, help, section, form grid…),
   không chỉ thư mục màn. Với mỗi component, ghi class viền/nền/khoảng cách nó tự vẽ. Rồi kiểm page có bọc
   thêm lớp cùng style không (vd page bọc `<Breadcrumbs>` trong `div` có `border-b-2`, mà `Breadcrumbs` đã có
   `border-b-2` → hai đường gạch). So cách dùng với các màn khác và với comment/JSDoc của component.
   Chưa đọc component dùng chung của một vùng → item vùng đó là `❓`, không phải `✅`.
3. Item **tĩnh**: `grep -rn "{chữ nguyên văn}"` trong mã FE. Có spec màn thì đối chiếu thêm với spec.
4. Item **dữ liệu**: lần từ component → hook/store → service → URL → controller/service BE. Kiểm được giá trị
   thật chỉ khi chạy app (§6); không chạy được thì ghi "nguồn đúng, giá trị chưa kiểm runtime".
5. Kiểm **thứ tự** (option, cột, field) và **trạng thái mặc định** (option nào chọn sẵn, panel mở hay đóng,
   field nào ẩn theo điều kiện).
6. Kiểm item **có trong code mà không có trong ảnh** — cũng là chênh lệch.
7. **Kích thước:** không suy pixel từ tên class (`h-12`, `p-4`, `1rem`…). Font-size gốc của `<html>` có thể khác
   16px (CSS dự án đặt `* { font-size }`, theme người dùng…), làm mọi giá trị rem lệch. Đo bằng runtime (§6).

Mọi kết luận kèm `file:line` + đoạn code trích. Không đọc được thì ghi `unverified` và nói rõ chưa đọc gì.

## 5. Báo cáo

Bảng chính, mỗi item một dòng, theo thứ tự §3:

| # | Vùng | Item (chữ trong ảnh) | Nguồn | Code | Kết quả | Bằng chứng |
| --: | --- | --- | --- | --- | --- | --- |
| 1 | Panel 処理内容 | Option `抽出（エクスポート）` (chọn sẵn) | Tĩnh | `抽出(エクスポート)`, default `export` | ⚠️ khác ngoặc | `{file}:{line}` + đoạn trích |

`Kết quả` chỉ dùng: ✅ khớp · ⚠️ khác (ghi khác gì: chữ / thứ tự / trạng thái / vị trí / kích thước / màu) ·
❌ thiếu trong code · ➕ thừa trong code · ❓ chưa kiểm (ghi lý do).

Sau bảng:

- **Tóm tắt:** số item theo từng kết quả.
- **Mâu thuẫn trong chính ảnh** (vd ngày header ≠ ngày trong tên file) — báo, không coi là lỗi code.
- **Ảnh vs spec / hệ cũ:** item ảnh khác spec màn hoặc hành vi hệ cũ → ghi rõ. Với dự án viết lại có luật
  "không đổi hành vi nếu không có CR": **ảnh không thay CR**. Không tự kết luận ảnh đúng hay code đúng;
  nêu để người phụ trách chốt.

## 6. Đối chiếu runtime (bắt buộc thử)

Code khớp chưa chắc màn hình khớp. **Phải chụp màn thật** mỗi trạng thái trong ảnh rồi đặt cạnh ảnh gốc,
so từng vùng bằng mắt: số đường kẻ, viền, khoảng cách, item thừa/thiếu. Lỗi bố cục (viền đôi, gạch chân thừa,
lệch hàng) thường chỉ thấy khi chụp. Không có browser harness (Playwright, Chrome DevTools…) hoặc không đăng
nhập được → **hỏi người dùng** chụp màn hình gửi lại hoặc cấp tài khoản, trước khi báo xong. Chưa có ảnh chụp
thật → mọi item bố cục / viền / kích thước / màu là `❓`, và báo cáo ghi rõ "chưa so với màn thật".

Trước khi kết luận "không có harness": kiểm cả cài global (`npm ls -g --depth=0`, `npm root -g` →
`require(path + '/playwright')`, `~/AppData/Local/ms-playwright` hoặc `~/.cache/ms-playwright`), không chỉ
`node_modules` của dự án. Thử đăng nhập bằng tài khoản test trong memory/ghi chú dự án trước khi hỏi người dùng.

Khi FE chạy được:

- **Xác nhận đúng app** trước khi chụp: cổng dev có thể bị app khác chiếm. Kiểm `<title>` hoặc fetch một file
  nguồn vừa đọc qua dev server (vd Vite phục vụ `/src/...`) để chắc đó là working tree này.
- Mở màn bằng browser harness, đưa về đúng trạng thái trong ảnh (chọn option, bấm nút như ảnh), chụp cùng
  kích thước viewport với ảnh gốc, đặt cạnh nhau.
- Kích thước/màu: đo bằng `getBoundingClientRect()` và `getComputedStyle()` (màu ra `rgb(...)`, so với hex trong ảnh).
- Cập nhật cột `Kết quả` cho item **dữ liệu**, trạng thái và kích thước.
- **Không có tài khoản / BE không chạy:** với kiểm tra thuần UI, giả lập API ở trình duyệt
  (Playwright `context.route()` trả response đúng schema mà FE parse — đăng nhập, profile, menu, dữ liệu màn).
  Ghi rõ trong báo cáo là "runtime với API giả lập"; giá trị item **dữ liệu** khi đó vẫn là `❓`.
  Khi giả lập theo URL, khớp chính xác (vd `/auth/me` vs `/auth/menus` — `includes('/auth/me')` bắt nhầm cả hai).
- Tài khoản test dùng chung có thể bị người khác đổi mật khẩu giữa chừng → đăng nhập thất bại không phải lỗi code;
  xem memory/ghi chú dự án, hỏi người dùng. Thao tác import/ghi dữ liệu chỉ làm khi người dùng cho phép.
- Không chạy được → giữ `❓`, ghi lý do. Không báo "khớp" chỉ dựa vào đọc code với item cần runtime.
