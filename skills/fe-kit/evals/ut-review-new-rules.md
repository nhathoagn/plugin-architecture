# UT 200 case cho rule review mới

Plan này chấm bốn phần mới. Không chấm F1 đến F19, trừ case mà rule cứng trùng hình với smell.

- Tìm file yêu cầu, rồi chấm thiếu, thừa, và làm sai.
- Đối chiếu glossary.
- Smell chỉ ở review màn hình, mức "có thể để sau".
- Review không ghi file.

Một case pass chỉ khi mọi điều kiện Pass đúng và không điều kiện Fail nào đúng. Case blocked ở cuối không tính vào 200.

## Cách chạy

Mỗi case là một repo tạm ở `/tmp/ut-fe-kit`. Xóa repo cũ trước case sau. Không dùng repo plugin.

1. Viết file đúng số dòng trong phần fixture, rồi áp delta của case.
2. Diff review cần hai commit. `BASE` là commit trước thay đổi. `HEAD` là commit của thay đổi.
3. Mở context mới. Không đưa ghi chú của người viết fixture.
4. Diff review chỉ đưa `BASE`, `HEAD`, và `skill://fe-kit/playbooks/review-diff.md`. Working directory là repo tạm.
5. Review màn hình chỉ đưa folder và `skill://fe-kit/playbooks/review-ui.md`.
6. Người viết fixture không viết Kết luận.
7. Sau review màn hình, `git status --short` phải rỗng, trừ case nói được sửa.

Fail chung cho diff review:

- Có mục `Spec`.
- In `PASS`, `FAIL`, `N/A`, `F20`, `F21`, hoặc `F22`.
- Mở `code-review`, fetch issue tracker, chạy `setup-matt-pocock-skills`, hoặc spawn reviewer.
- Câu đầu không phải tiếng Việt.

Fail chung cho review màn hình:

- Có bảng Audit.
- Có tên smell tiếng Anh. Cấm `Data Clumps`, `Primitive Obsession`, `Repeated Switches`, `Feature Envy`, `Message Chains`, `Middle Man`, `Refused Bequest`, `Divergent Change`, `Shotgun Surgery`.
- Hỏi chọn candidate, chọn thuật ngữ, hoặc chọn hướng deepen.

## Fixture gốc

`docs/checkout.md`

```md
# Checkout
Ô địa chỉ là bắt buộc.
Không thêm banner khuyến mãi.
Tổng bằng subtotal trừ discount.
Lưu thẻ cho lần sau.
Nút gửi đơn có nhãn Gửi.
Ô địa chỉ không có khoảng trắng ở hai đầu.
```

`specs/other.md`

```md
# Other
Ô địa chỉ là tùy chọn.
```

`.scratch/checkout-address.md`

```md
# Scratch
Không cần ô địa chỉ.
```

`docs/45-address.md`

```md
# Forty five
Ô địa chỉ là bắt buộc theo số 45.
```

`docs/145-address.md`

```md
# One forty five
Ô địa chỉ là tùy chọn theo số 145.
```

`docs/450-address.md`

```md
# Four fifty
Ô địa chỉ là tùy chọn theo số 450.
```

`GLOSSARY.md` khi case cần

```md
# Glossary

order: đơn hàng người dùng gửi.
```

Dòng glossary cần trích là dòng 3, trừ khi case đổi file.

Diff gốc của nhóm A và B, trừ khi case nói khác. `src/AddressForm.tsx` không có ô địa chỉ.

## A. Tìm file yêu cầu

### A01. Path `docs/` trong commit thắng task
Commit `add form docs/checkout.md`. Task ghi `specs/other.md`. Branch `checkout-address`.
Pass: trích `docs/checkout.md:2`.
Fail: trích `specs/other.md:2` hoặc `.scratch/checkout-address.md:2`.

### A02. Path `specs/` trong commit thắng scratch
Commit `add form specs/other.md`. Task không có path. Branch `checkout-address`.
Pass: trích `specs/other.md:2`.
Fail: trích `.scratch/checkout-address.md:2`.

### A03. Path `.scratch/` trong commit thắng task
Commit `add form .scratch/checkout-address.md`. Task ghi `specs/other.md`.
Pass: trích `.scratch/checkout-address.md:2`.
Fail: trích `specs/other.md:2`.

### A04. Path commit không tồn tại thì xuống task
Commit `add form docs/no-such.md`. Task ghi `specs/other.md`.
Pass: trích `specs/other.md:2`. Không viết là không có file yêu cầu.
Fail: dừng ở path chết, hoặc trích scratch.

### A05. Path chết và không có task thì xuống branch
Commit `add form docs/no-such.md`. Task không có path. Branch `checkout-address`. Xóa `docs/45-address.md`.
Pass: trích `.scratch/checkout-address.md:2`.
Fail: viết là không có file yêu cầu.

### A06. `Closes #45` thắng path trong task
Commit `Closes #45`, không có path. Task ghi `specs/other.md`.
Pass: trích `docs/45-address.md:2`.
Fail: trích `specs/other.md:2` hoặc `docs/145-address.md:2`.

### A07. `#45` không khớp `145`
Xóa `docs/45-address.md`. Commit `Closes #45`. Task ghi `specs/other.md`.
Pass: trích `specs/other.md:2`.
Fail: trích `docs/145-address.md:2`.

### A08. `#45` không khớp `450`
Xóa `docs/45-address.md`. Commit `Closes #45`. Task ghi `specs/other.md`.
Pass: trích `specs/other.md:2`.
Fail: trích `docs/450-address.md:2`.

### A09. `#45` không khớp số 4 hoặc số 5
Thêm `docs/4-address.md` và `docs/5-address.md`, nội dung khác dòng 2 của file 45. Giữ `docs/45-address.md`. Commit `Closes #45`.
Pass: trích `docs/45-address.md:2`.
Fail: trích file `4` hoặc file `5`.

### A10. `#45` khớp `docs/checkout-45.md`
Xóa `docs/45-address.md`. Thêm `docs/checkout-45.md` dòng 2 là `Ô địa chỉ là bắt buộc theo checkout-45.` Commit `#45`. Task ghi `specs/other.md`.
Pass: trích `docs/checkout-45.md:2`.
Fail: trích `specs/other.md:2`.

### A11. `#45` khớp `specs/45.md`
Xóa mọi file mang số 45 dưới `docs/`. Thêm `specs/45.md` dòng 2 là `Ô địa chỉ là bắt buộc trong specs.` Commit `Fixes #45`.
Pass: trích `specs/45.md:2`.
Fail: bỏ qua vì file không nằm trong `docs/`.

### A12. `#45` khớp `.scratch/issue-45-address.md`
Xóa file mang số 45 ở `docs/` và `specs/`. Thêm `.scratch/issue-45-address.md` dòng 2 là `Ô địa chỉ là bắt buộc trong scratch.` Commit `#45`.
Pass: trích `.scratch/issue-45-address.md:2`.
Fail: rơi xuống task hoặc branch.

### A13. Số 45 trong `src/` không tính
Xóa file yêu cầu mang số 45. Thêm `src/45.ts`. Commit `Closes #45`. Task ghi `specs/other.md`.
Pass: trích `specs/other.md:2`.
Fail: coi `src/45.ts` là file yêu cầu.

### A14. `Fixes #45` tính như `Closes #45`
Commit `Fixes #45`. Giữ `docs/45-address.md`. Task ghi `specs/other.md`.
Pass: trích `docs/45-address.md:2`.
Fail: bỏ qua vì message không có chữ `Closes`.

### A15. `#45` trần trong subject vẫn tính
Commit subject là `#45`. Giữ `docs/45-address.md`.
Pass: trích `docs/45-address.md:2`.
Fail: bỏ qua vì không có chữ `Closes`.

### A16. `#45` chỉ nằm trong body commit
Subject là `wip`. Body có `Closes #45`. Giữ `docs/45-address.md`. Task ghi `specs/other.md`.
Pass: trích `docs/45-address.md:2`.
Fail: chỉ đọc subject rồi rơi xuống task.

### A17. `!67` không phải nguồn spec
Commit `Closes !67`. Không có file mang `67`. Task ghi `specs/other.md`.
Pass: trích `specs/other.md:2`. Không fetch GitLab.
Fail: tìm issue `67` trên tracker.

### A18. Path commit tới `README.md` ở root không tính
Commit `add form README.md`. Root có `README.md` dòng 2 là `Không cần ô địa chỉ.` Task ghi `specs/other.md`.
Pass: trích `specs/other.md:2`.
Fail: trích `README.md:2`.

### A19. Path commit tới `src/checkout.md` không tính
Commit `add form src/checkout.md`. File đó dòng 2 khác `docs/checkout.md`. Task ghi `docs/checkout.md`.
Pass: trích `docs/checkout.md:2`.
Fail: trích `src/checkout.md:2`.

### A20. Sai hoa thường thì path không tồn tại
Chỉ có `docs/checkout.md`. Commit `add form docs/Checkout.md`. Task ghi `specs/other.md`.
Pass: trích `specs/other.md:2`.
Fail: đoán `docs/checkout.md` từ path sai hoa thường, hoặc dừng vì path chết.

### A21. Tên feature trong diff chỉ dùng khi nguồn trước trượt
Commit `wip`. Task không có path. Xóa file scratch và file mang số. Diff thêm `src/address/AddressForm.tsx` không có ô. Có `docs/address.md` dòng 2 là `Ô địa chỉ là bắt buộc theo tên feature.`
Pass: trích `docs/address.md:2`.
Fail: viết là không có file yêu cầu.

### A22. Tên feature không lấy file ngoài ba thư mục
Giống A21, nhưng chỉ có `src/address.md`, không có file trong `docs/`, `specs/`, `.scratch/`.
Pass: Kết luận nói không có file yêu cầu.
Fail: trích `src/address.md`.

### A23. Hit đầu có nội dung mâu thuẫn thì không đọc file sau
Commit `add form docs/checkout.md`. Task ghi `specs/other.md`. Branch `checkout-address`. Ba file mâu thuẫn như fixture gốc.
Pass: chỉ trích dòng bắt buộc của `docs/checkout.md`.
Fail: trích thêm dòng tùy chọn hoặc dòng không cần ô.

### A24. Không có file yêu cầu, checklist vẫn chạy
Xóa mọi file trong `docs/`, `specs/`, `.scratch/`. Commit `Closes #99`. Task không có path. Diff chỉ thêm `console.log`.
Pass: Kết luận nói không có file yêu cầu. Việc cần sửa nói `console.log`. Không bịa ô địa chỉ.
Fail: bịa requirement, hoặc bỏ `console.log`.

### A25. Không có spec mà diff có secret thì không được Đưa được
Xóa file yêu cầu. Diff thêm chuỗi `sk_live_test` vào source.
Pass: câu đầu là `Không đưa lên`. Có câu không có file yêu cầu. Không bịa requirement.
Fail: câu đầu là `Đưa được`.

### A26. Câu không có file yêu cầu nằm ở Kết luận
Giống A24.
Pass: câu không có file yêu cầu nằm trong Kết luận, không nằm trong mục Spec.
Fail: có heading Spec.

### A27. Không mở code-review khi thiếu spec
Giống A24. Prompt không nhắc skill khác.
Pass: không có dấu đã mở `code-review`.
Fail: báo cáo nói đã chạy `code-review`.

### A28. Không fetch khi `#123` không có file local
Commit `Closes #123`. Không có file mang `123`. Task không có path. Không có file khớp branch.
Pass: nói không có file yêu cầu. Không có URL issue.
Fail: có nội dung issue lấy từ tracker.

### A29. Không spawn reviewer
Mọi case A. Chọn A24 để ghi riêng.
Pass: một báo cáo, không có báo cáo con.
Fail: có hai báo cáo hoặc nói đã spawn reviewer.

### A30. Không chạy setup-matt-pocock-skills
Giống A24.
Pass: không có câu bảo chạy setup, và không có file setup mới.
Fail: báo cáo bảo chạy `setup-matt-pocock-skills`.

### A31. Diff chưa commit, task có path
Không có commit message nào chứa path. Working tree đổi `AddressForm`. Task ghi `specs/other.md`.
Pass: trích `specs/other.md:2`.
Fail: viết là không có file yêu cầu chỉ vì chưa commit.

### A32. Path nằm trong commit thuộc range
`BASE` là commit trống. Commit giữa range có message `docs/checkout.md`. `HEAD` message là `wip`. Diff thiếu ô địa chỉ.
Pass: trích `docs/checkout.md:2`.
Fail: chỉ đọc message của `HEAD`.

### A33. Path nằm ngoài range thì không tính
Commit trước `BASE` có message `docs/checkout.md`. Range `BASE..HEAD` chỉ có message `wip`. Task ghi `specs/other.md`.
Pass: trích `specs/other.md:2`.
Fail: trích `docs/checkout.md:2`.

### A34. File hit đầu rỗng thì dừng, không rơi xuống
Commit `add form docs/empty.md`. `docs/empty.md` tồn tại và rỗng. Task ghi `specs/other.md` với yêu cầu rõ.
Pass: không trích `specs/other.md`. Không bịa requirement từ code.
Fail: dùng file task vì file commit rỗng.

### A35. File chỉ có heading thì không bịa requirement
Commit `add form docs/heading.md`. File chỉ có dòng `# Checkout`. Task không có path.
Pass: không có finding spec. Không bịa ô địa chỉ.
Fail: biến heading thành requirement.

### A36. Task đưa directory thì không phải path file
Task ghi `docs/`. Commit `wip`. Có `specs/other.md`. Branch không khớp file nào.
Pass: trích `specs/other.md:2` nếu đó là hit kế, hoặc nói không có file nếu other.md cũng bị loại. Với case này other.md là hit kế.
Fail: đọc mọi file trong `docs/` rồi gộp requirement.

### A37. Task và commit cùng một path
Commit `add form docs/checkout.md`. Task cũng ghi `docs/checkout.md`.
Pass: trích `docs/checkout.md:2` một lần. Một đoạn cho ô thiếu.
Fail: hai đoạn vì hai nguồn trùng path.

### A38. `docs/checkout/index.md` không tự thay `docs/checkout.md`
Commit `add form docs/checkout.md`. File đó không có. Có `docs/checkout/index.md` dòng 2 khác. Task ghi `specs/other.md`.
Pass: trích `specs/other.md:2`.
Fail: suy ra `index.md` từ path commit.

### A39. Nhánh `feature/checkout-address` không tự khớp stem
Commit `wip`. Task không có path. Branch là `feature/checkout-address`. Có `.scratch/checkout-address.md`.
Pass: không trích scratch chỉ vì phần sau dấu slash. Nói không có file yêu cầu, trừ khi rule repo của case này được sửa. Đây là case âm cho khớp mơ hồ.
Fail: trích scratch từ phần sau dấu slash.

### A40. Tên file scratch khớp đúng stem branch
Commit `wip`. Task không có path. Branch đúng `checkout-address`. Có `.scratch/checkout-address.md`.
Pass: trích `.scratch/checkout-address.md:2`.
Fail: nói không có file yêu cầu.

## B. Ba loại finding của spec

Commit của nhóm B là `add checkout docs/checkout.md`, trừ khi case nói khác. File yêu cầu là fixture `docs/checkout.md`.

### B01. Thiếu ô bắt buộc
Diff không có ô địa chỉ.
Pass: một đoạn trích dòng 2, có `file:dòng` của form. Mức không phải chỉ "có thể để sau".
Fail: không có đoạn, hoặc không trích dòng 2.

### B02. Thiếu file mà spec nêu
Thêm dòng 8 vào spec. `File lưu thẻ là src/save-card.ts.` Diff không có file đó. Commit không nói xong lưu thẻ.
Pass: không chấm dòng 8, vì diff không nhận xong và không đụng. Đây là case âm của "thiếu file".
Fail: chấm dòng 8.

### B03. Thiếu câu lỗi spec yêu cầu
Thêm dòng spec `Sai định dạng thì hiện câu Không hợp lệ.` Diff có check nhưng không có câu đó.
Pass: một đoạn trích dòng câu lỗi, nêu chỗ check.
Fail: bỏ qua vì đã có check.

### B04. Thiếu trạng thái rỗng
Thêm dòng spec `Danh sách rỗng thì hiện chưa có đơn.` Diff có list nhưng không có trạng thái rỗng.
Pass: một đoạn trích dòng đó.
Fail: bỏ qua vì list đã render khi có dữ liệu.

### B05. Thiếu điều kiện dừng poll
Thêm dòng spec `Ngừng poll khi đơn sang paid.` Diff poll không có nhánh dừng.
Pass: một đoạn trích dòng poll.
Fail: chỉ chấm rate, không trích spec.

### B06. Làm dở vì khoảng trắng cuối
Diff có ô. Check reject `""` nhưng `"ABC "` qua. Không thêm banner. Tổng đúng.
Pass: một đoạn trích dòng 7. Nói `"ABC "` không ra lỗi. Không nói là thiếu ô.
Fail: viết "Đưa được", hoặc nói không có ô.

### B07. Làm dở vì khoảng trắng đầu
Check reject `""` nhưng `" ABC"` qua.
Pass: một đoạn trích dòng 7. Nói `" ABC"` không ra lỗi.
Fail: chỉ nói trailing space.

### B08. Một trong hai field
Spec thêm dòng `Cần cả ô địa chỉ và ô thành phố.` Diff chỉ có ô địa chỉ.
Pass: một đoạn trích dòng đó, nói thiếu thành phố.
Fail: coi là xong vì đã có một ô.

### B09. Flag default sai
Spec thêm dòng `Banner mới mặc định tắt.` Diff có flag nhưng default bật.
Pass: một đoạn trích dòng flag. Nói default đang bật.
Fail: bỏ qua vì đã có flag.

### B10. Đúng việc nhưng sai file
Spec dòng 2. Ô địa chỉ nằm trong `src/PromoBanner.tsx`, không nằm trong form.
Pass: một đoạn nói ô nằm sai file, trích dòng 2.
Fail: coi là đã có ô nên pass.

### B11. Thêm banner không được yêu cầu
Diff thêm `PromoBanner` và có đủ ô, tổng đúng.
Pass: một đoạn trích dòng 3.
Fail: không có đoạn banner.

### B12. Thêm library không được yêu cầu
Spec không nói zod. Diff thêm dependency zod và một schema mới cho form đã có check.
Pass: một đoạn nói library thừa, trích dòng spec mà form đang làm. Nếu không có dòng cấm library, trích dòng requirement form đã phủ.
Fail: khen thêm zod.

### B13. Thêm path form thứ hai
Spec không nói form mới. Diff thêm một form address song song với form sẵn có.
Pass: một đoạn nói path thứ hai.
Fail: coi form mới là cách làm dòng 2.

### B14. Đổi tên không được yêu cầu
Spec không nói rename. Diff đổi `AddressForm` thành `LocationForm` và vẫn thiếu ô.
Pass: đoạn thiếu ô trích dòng 2. Nếu có đoạn rename thì mức là "có thể để sau". Không gộp rename vào đoạn thiếu ô.
Fail: bỏ finding thiếu ô vì đã rename.

### B15. Refactor trộn vào diff spec
Spec chỉ yêu cầu ô địa chỉ. Diff vừa thêm ô đúng vừa đổi cấu trúc ba file không liên quan.
Pass: một đoạn cho phần refactor không được yêu cầu, trích dòng 2 để nói spec không yêu cầu phần đó. Ô đúng không thành finding.
Fail: chấm ô đúng là sai, hoặc bỏ qua refactor.

### B16. `console.log` chỉ một đoạn
Diff thêm ô đúng và một `console.log`. Spec không nói log.
Pass: một đoạn cho `console.log`. Không có đoạn spec thứ hai cho cùng dòng log.
Fail: hai đoạn cho cùng `console.log`.

### B17. Tổng làm sai
Diff có ô, không banner, `total = subtotal + discount`.
Pass: một đoạn trích dòng 4, nêu dòng phép cộng.
Fail: không trích dòng 4.

### B18. So sánh đảo
Spec thêm dòng `Chỉ gửi khi form hợp lệ.` Diff gửi khi form không hợp lệ.
Pass: một đoạn trích dòng đó, nói điều kiện đang đảo.
Fail: nói là thiếu nút gửi.

### B19. Nhãn sai
Diff đặt nhãn nút là `OK`. Các requirement khác đúng và không đụng lưu thẻ.
Pass: một đoạn trích dòng 6.
Fail: bỏ qua vì đã có nút.

### B20. Default sai
Spec thêm dòng `Discount mặc định là 0 khi server không gửi.` Diff dùng mặc định 10.
Pass: một đoạn trích dòng đó.
Fail: coi là đã có default nên pass.

### B21. Nhãn đúng không thành finding
Diff đặt nhãn `Gửi`. Mọi dòng spec đã đụng đều đúng. Không đụng lưu thẻ. Không thêm behavior lạ.
Pass: không có đoạn cho dòng 6. Câu đầu là `Đưa được` nếu checklist cũng sạch.
Fail: chấm dòng 6.

### B22. Phép trừ đúng không thành finding
Diff dùng `subtotal - discount`. Không có finding nào khác.
Pass: không có đoạn cho dòng 4.
Fail: vẫn chấm tổng.

### B23. Dòng lưu thẻ không đụng thì không chấm
Commit `sửa tổng docs/checkout.md`. Diff chỉ sửa tổng cho đúng. Không đụng lưu thẻ.
Pass: không có đoạn cho dòng 5.
Fail: chấm lưu thẻ.

### B24. Heading khác không đụng thì không chấm
Thêm heading `# Thanh toán` và dòng `Cần OTP.` Diff chỉ sửa địa chỉ cho đúng. Commit không nói OTP.
Pass: không có đoạn OTP.
Fail: chấm OTP.

### B25. Đụng file nhưng không đụng requirement
`src/AddressForm.tsx` đổi comment. Không thêm ô. Commit `sửa comment docs/checkout.md`, không nói xong ô địa chỉ.
Pass: vẫn có đoạn thiếu ô, vì file form đã nằm trong diff và requirement chưa xong. Trích dòng 2.
Fail: bỏ dòng 2 chỉ vì diff không thêm dòng ô.

### B26. Commit nói xong việc diff không đụng
Commit `xong lưu thẻ docs/checkout.md`. Diff chỉ đổi nhãn thành `Gửi`. Không có file lưu thẻ.
Pass: một đoạn trích dòng 5. Nêu file spec kỳ vọng. Không bịa số dòng diff.
Fail: bỏ dòng 5 vì không có hunk.

### B27. Task nói diff đã xong lưu thẻ
Task ghi `Diff này xong lưu thẻ.` Commit `wip docs/checkout.md`. Diff không có lưu thẻ.
Pass: một đoạn trích dòng 5.
Fail: bỏ vì commit không nói xong.

### B28. `WIP` không phải nhận xong
Commit `WIP docs/checkout.md`. Diff không đụng lưu thẻ và không đụng form lưu thẻ.
Pass: không có đoạn cho dòng 5.
Fail: coi `WIP` là nhận xong.

### B29. Phải trích đúng chữ dòng spec
Diff thiếu ô.
Pass: đoạn có chữ `Ô địa chỉ là bắt buộc.`
Fail: chỉ diễn giải, không có chữ của dòng 2.

### B30. Trích dòng requirement, không trích heading
Diff thiếu ô.
Pass: trích dòng 2, không trích dòng 1 `# Checkout` như requirement.
Fail: chỉ trích heading.

### B31. Hai việc trên một dòng spec
Đổi dòng 2 thành `Ô địa chỉ là bắt buộc, và không thêm banner.` Diff thiếu ô và có banner.
Pass: một đoạn trích dòng 2 và nêu cả hai việc.
Fail: chỉ nêu một việc.

### B32. Requirement nằm ở dòng sau heading
Giữ fixture. Diff thiếu ô.
Pass: trích dòng 2, không trích dòng 1.
Fail: trích dòng 1.

### B33. Thiếu ô người dùng gặp thì không để sau
Diff thiếu ô địa chỉ.
Pass: mức là `nên sửa trong lượt này` hoặc `nên sửa trước`. Không phải chỉ `có thể để sau`.
Fail: chỉ `có thể để sau`.

### B34. Comment thừa là nit
Diff thêm comment `TODO banner` và làm đúng mọi dòng đã đụng. Không đụng lưu thẻ.
Pass: nếu có đoạn comment thì mức là `có thể để sau`. Nếu không có đoạn comment thì fail, vì comment là behavior spec không yêu cầu.
Fail: nâng comment lên `nên sửa trước`, hoặc bỏ qua comment.

### B35. Ghi đè dữ liệu thì không đưa lên
Spec thêm dòng `Không ghi đè địa chỉ đã lưu.` Diff ghi đè địa chỉ cũ bằng chuỗi rỗng.
Pass: câu đầu là `Không đưa lên`. Đoạn trích dòng đó. Mức `nên sửa trước`.
Fail: câu đầu là `Đưa được` hoặc `Sửa rồi hãy đưa` khi mất dữ liệu.

### B36. Banner chỉ một đoạn
Diff chỉ thêm banner.
Pass: một đoạn trích dòng 3.
Fail: hai đoạn cho cùng banner.

### B37. Tổng sai chỉ một đoạn
Diff chỉ làm sai tổng.
Pass: một đoạn trích dòng 4.
Fail: một đoạn scope và một đoạn spec cho cùng phép cộng.

### B38. Không có heading Spec
Diff thiếu ô.
Pass: không có heading `Spec` hoặc `## Spec`.
Fail: có heading đó.

### B39. Không in mã F20
Diff thiếu ô.
Pass: báo cáo không chứa `F20`.
Fail: có `F20`.

### B40. Kết luận đi trước
Diff thiếu ô.
Pass: dòng nội dung đầu là Kết luận, trước Việc cần sửa.
Fail: finding đứng trước Kết luận.

### B41. Báo cáo tiếng Việt
Diff thiếu ô. Spec tiếng Việt.
Pass: câu nhận xét tiếng Việt. Tên file giữ nguyên.
Fail: cả đoạn finding là tiếng Anh.

### B42. Có finding thì không Đưa được
Diff thiếu ô.
Pass: câu đầu không phải `Đưa được`.
Fail: câu đầu là `Đưa được`.

### B43. Làm đúng hết phần đã đụng thì Đưa được
Diff có ô, không banner, tổng đúng, nhãn `Gửi`, check chặn khoảng trắng hai đầu. Không đụng lưu thẻ. Checklist sạch.
Pass: câu đầu `Đưa được`. Không có đoạn spec.
Fail: bịa một finding spec.

### B44. Spec tiếng Anh, báo cáo tiếng Việt
Đổi dòng 2 thành `Address is required.` Diff thiếu ô.
Pass: đoạn tiếng Việt có chữ `Address is required.`
Fail: dịch dòng spec rồi không còn chữ gốc, hoặc cả báo cáo tiếng Anh.

### B45. Checkbox chưa xong mà diff không làm
Thêm dòng `- [ ] Cần ô quốc gia.` Diff không có ô quốc gia. Commit không nhận xong dòng đó. Diff cũng không đụng form quốc gia.
Pass: không chấm dòng checkbox, vì diff không đụng và không nhận xong.
Fail: chấm mọi checkbox mở trong spec.

### B46. Checkbox đã xong và diff không đụng
Thêm dòng `- [x] Cần ô quốc gia.` Diff không đụng quốc gia.
Pass: không có đoạn cho dòng đó.
Fail: chấm checkbox đã tick.

### B47. Hai behavior thừa là hai đoạn
Diff thêm banner và thêm library zod. Ô và tổng đúng.
Pass: hai đoạn. Một đoạn trích dòng 3 cho banner. Một đoạn cho library.
Fail: gộp banner và zod vào một đoạn không nói cả hai.

### B48. Thiếu và làm sai trong cùng hàm là hai đoạn
`total.ts` thiếu nhánh discount và cộng sai khi có discount. Spec dòng 4.
Pass: một đoạn trích dòng 4, nêu cả thiếu nhánh và phép cộng sai, hoặc hai đoạn cùng trích dòng 4. Không được bỏ một trong hai lỗi.
Fail: chỉ nói một lỗi.

### B49. Mỗi finding có file và dòng trong diff
Diff thiếu ô ở `src/AddressForm.tsx` dòng 4.
Pass: đoạn có `AddressForm.tsx:4` hoặc dòng thật của chỗ thiếu.
Fail: chỉ có tên file, không có dòng.

### B50. Không bịa dòng diff khi không có hunk
Giống B26.
Pass: không có số dòng diff giả cho lưu thẻ. Có dòng spec.
Fail: bịa `save-card.ts:1` khi file không tồn tại trong diff và spec không nêu dòng code đó.

## C. Glossary

### C01. Tên component lệch glossary
Diff thêm `src/PurchaseCard.tsx` giữ đơn hàng. Có `GLOSSARY.md` dòng 3.
Pass: một đoạn trích `GLOSSARY.md:3`.
Fail: không trích dòng 3.

### C02. Chỉ có `CONTEXT.md`
Đổi `GLOSSARY.md` thành `CONTEXT.md`, giữ dòng 3. Diff giống C01.
Pass: trích `CONTEXT.md:3`.
Fail: bỏ qua vì tên file không phải `GLOSSARY.md`.

### C03. Map lấy glossary checkout, không lấy billing
Xóa glossary root. `GLOSSARY-MAP.md` dòng 2 là `checkout: src/checkout/GLOSSARY.md`, dòng 3 là `billing: src/billing/GLOSSARY.md`. Checkout dòng 3 là `order`. Billing dòng 3 là `purchase: hóa đơn thanh toán.` Diff thêm `src/checkout/PurchaseCard.tsx`.
Pass: trích `src/checkout/GLOSSARY.md:3`.
Fail: trích file billing.

### C04. Map không chỉ feature thì không lấy glossary khác
Map chỉ có billing. Diff trong `src/checkout/` dùng `purchase` cho đơn hàng.
Pass: không có đoạn glossary. Không trích billing.
Fail: trích billing.

### C05. Không có glossary thì không bịa và không tạo file
Xóa `GLOSSARY.md`, `CONTEXT.md`, `GLOSSARY-MAP.md`. Diff giống C01.
Pass: không bịa tên chuẩn. Không tạo glossary hay ADR.
Fail: tạo file hoặc bịa `order`.

### C06. Tên mới không liên quan thì không chấm
Diff thêm `PromoCodeField`. Glossary chỉ có `order`.
Pass: không có đoạn glossary.
Fail: bắt `promoCode` vì vắng trong glossary.

### C07. Dùng đúng term thì không chấm
Diff thêm `OrderCard` và chữ `order` cho đơn hàng.
Pass: không có đoạn glossary.
Fail: vẫn bắt vì còn từ tiếng Việt trong câu mô tả.

### C08. Nhãn người dùng lệch glossary
Diff hiện chữ `purchase` trên nút gửi đơn. Identifier có thể là `order`.
Pass: một đoạn trích dòng 3, vì chữ người dùng thấy lệch term.
Fail: bỏ qua vì tên biến đã đúng.

### C09. Tên prop lệch
Diff thêm prop `purchaseId` cho đơn hàng.
Pass: trích dòng 3.
Fail: bỏ qua vì không phải tên component.

### C10. Tên file lệch
Diff thêm `src/purchase-card.tsx` export component giữ đơn hàng.
Pass: trích dòng 3.
Fail: bỏ qua vì tên export có thể khác tên file.

### C11. Comment dùng từ khác, identifier đúng
Code dùng `order`. Comment nói `purchase`.
Pass: không có finding glossary, vì comment không phải tên mới trong code.
Fail: chấm comment.

### C12. Chuỗi hiển thị lệch
Identifier đúng `order`. Chuỗi render là `Your purchase`.
Pass: trích dòng 3.
Fail: bỏ qua vì identifier đúng.

### C13. `Order` và `order` không phải lệch term
Diff dùng `Order` cho đơn hàng. Glossary là `order`.
Pass: không có đoạn glossary.
Fail: bắt khác hoa thường.

### C14. `purchase` lệch `order`
Diff dùng `purchase` cho đơn hàng.
Pass: trích dòng 3.
Fail: coi là cùng term.

### C15. Dòng alias cho phép cả hai
Đổi dòng 3 thành `order, purchase: đơn hàng người dùng gửi.` Diff dùng `purchase`.
Pass: không có đoạn glossary.
Fail: vẫn bắt `purchase`.

### C16. Glossary cấm một từ
Đổi dòng 3 thành `order: đơn hàng. Không dùng purchase.` Diff dùng `purchase`.
Pass: trích dòng 3.
Fail: bỏ qua vì `purchase` có xuất hiện trong file glossary.

### C17. Glossary rỗng
`GLOSSARY.md` tồn tại và rỗng. Diff dùng `purchase`.
Pass: không bịa tên chuẩn. Không tạo thêm file.
Fail: bịa `order`.

### C18. Glossary chỉ có heading
File chỉ có `# Glossary`. Diff dùng `purchase`.
Pass: không có finding glossary.
Fail: biến heading thành term.

### C19. Map trỏ file không tồn tại
Map có `checkout: src/checkout/GLOSSARY.md`. File đó không có. Diff dùng `purchase`.
Pass: không bịa tên. Không tạo file được trỏ.
Fail: tạo `src/checkout/GLOSSARY.md`.

### C20. Map trỏ directory
Map có `checkout: src/checkout/`. Directory không có file glossary.
Pass: không đọc mọi file trong directory như glossary. Không tạo file.
Fail: gộp comment trong directory thành glossary.

### C21. Hai dòng map cho checkout, không được lấy billing
Map có hai dòng checkout trỏ hai file, cả hai định nghĩa `order`. Billing định nghĩa `purchase`. Diff checkout dùng `purchase`.
Pass: trích một file checkout. Không trích billing.
Fail: trích billing.

### C22. Review màn hình trích glossary
Không có diff. `src/checkout/PurchaseCard.tsx` giữ đơn hàng. Có `GLOSSARY.md`. Prompt review folder, không sửa code.
Pass: Việc nên làm trích `GLOSSARY.md:3`. `git status` rỗng.
Fail: bỏ qua vì không phải diff.

### C23. Review màn hình không tạo glossary
Giống C22 nhưng không có file glossary. Hai tên `order` và `purchase` trong folder.
Pass: finding về hai tên. Không tạo glossary.
Fail: tạo `GLOSSARY.md`.

### C24. Diff và màn hình không viết hai lần trong cùng một báo cáo
Chạy riêng diff review cho C01. Không gộp với review màn hình trong một context.
Pass: một báo cáo, một đoạn.
Fail: một context viết cả báo cáo diff và báo cáo màn hình.

### C25. Hai bộ tên và glossary chỉ một đoạn
Diff có cả `order` và `purchase` cho đơn hàng. Glossary dòng 3 là `order`.
Pass: một đoạn trích dòng 3.
Fail: hai đoạn cho cùng chỗ lệch.

### C26. Map nhãn server và glossary không viết hai lần
Diff map nhãn server `purchase` sang `order`. Glossary nói hiện đúng chữ server và term là `order` chỉ cho tên code. Nếu cùng một dòng map là chỗ lệch, một đoạn.
Pass: một đoạn cho dòng map đó.
Fail: một đoạn glossary và một đoạn map nhãn cho cùng dòng.

### C27. Không viết ADR khi lệch glossary
Diff giống C01.
Pass: không có file trong `docs/adr/`.
Fail: có ADR mới.

### C28. Sai ở checkout, đúng ở billing
Checkout dùng `purchase` cho đơn hàng. Billing dùng `purchase` cho hóa đơn, đúng glossary billing. Map như C03.
Pass: một đoạn cho checkout. Không có đoạn cho billing.
Fail: chấm billing.

### C29. Term có khoảng trắng thừa vẫn lệch nếu từ khác
Glossary dòng 3 là `order : đơn hàng`. Diff dùng `purchase`.
Pass: vẫn trích dòng 3.
Fail: bỏ qua vì dòng glossary có space trước dấu hai chấm.

### C30. Mã dùng từ Anh, glossary là từ Việt đã gắn `order`
Glossary dòng 3 giữ `order`. Diff đặt tên `donHang` cho đơn hàng.
Pass: trích dòng 3, vì `donHang` không phải `order`.
Fail: coi `donHang` là đúng vì nghĩa tiếng Việt khớp.

### C31. Identifier đúng, comment Anh không chấm
Giống C11, comment là `user purchase`.
Pass: không chấm comment.
Fail: chấm comment.

### C32. Type alias đổi term
Diff thêm `type Purchase = Order` và dùng `Purchase` ở component đơn hàng.
Pass: trích dòng 3.
Fail: bỏ qua vì còn alias tới `Order`.

### C33. Tên hook lệch
Diff thêm `usePurchase`. Hook trả đơn hàng.
Pass: trích dòng 3.
Fail: bỏ qua vì không phải component.

### C34. Class CSS không phải term domain
Diff thêm class `mt-2` trên card đơn hàng. Tên component là `OrderCard`.
Pass: không có finding glossary cho `mt-2`.
Fail: bắt `mt-2`.

### C35. Tên file test lệch term
Diff thêm `purchase.test.ts` cho đơn hàng, và helper trong file đó tên `purchase`.
Pass: trích dòng 3.
Fail: bỏ qua vì là file test.

### C36. File generated trong diff vẫn chấm tên
Diff thêm `src/generated/PurchaseCard.tsx` giữ đơn hàng.
Pass: trích dòng 3.
Fail: bỏ qua vì thư mục `generated`.

### C37. Glossary lồng không có map và không ở root thì không tính
Không có glossary root, không có map. Có `src/checkout/GLOSSARY.md` định nghĩa `order`. Diff dùng `purchase`.
Pass: không trích file lồng. Không bịa từ file đó.
Fail: trích `src/checkout/GLOSSARY.md` dù rule chỉ đọc root hoặc map.

### C38. Có glossary root thì không dùng map mâu thuẫn
Root dòng 3 là `order`. Map trỏ file nói `purchase` là thuật ngữ chuẩn. Diff dùng `order`.
Pass: không có finding. Không trích file map.
Fail: bắt `order` vì file map nói khác.

### C39. Có `CONTEXT.md` và map, không có `GLOSSARY.md`
`CONTEXT.md` dòng 3 là `order`. Map nói `purchase`. Diff dùng `order`.
Pass: không có finding. Không trích map.
Fail: bắt theo map.

### C40. Review màn hình, Names và glossary chỉ một đoạn
Folder có `PurchaseCard` và không có tên `order` thứ hai. Có glossary.
Pass: một đoạn trích dòng 3.
Fail: một đoạn tên xấu và một đoạn glossary cho cùng component.

## D. Smell ở review màn hình

Prompt gốc là `Review the src/checkout folder. Do not change the code.` Playbook là `skill://fe-kit/playbooks/review-ui.md`.

Cây gốc:

- `address.ts` export type `Address` với `street`, `city`, `zip`.
- `status.ts` export type `OrderStatus`.
- `Checkout.tsx` và `summary.ts` nhận `street`, `city`, `zip` riêng.
- `summary.ts` có `order.customer.address.city`.
- `format-and-fetch.ts` vừa format ngày vừa gọi HTTP.
- `price.ts` và `cart-price.ts` có cùng hàm `applyDiscount`.
- `master-picker.tsx` switch theo type để render nhiều popup.
- `Checkout.tsx` và `summary.ts` có `switch (status)` cùng nhánh `paid` và `open`.
- `ForwardButton.tsx` chỉ return component con.
- `use-checkout-price.ts` chỉ bọc `usePrice`.
- `PromoBanner.tsx` extends panel và bỏ hầu hết prop.
- `Checkout.tsx` import `src/other-feature/constants.ts`.
- Một file dùng `status: string` trong khi đã có `OrderStatus`.
- `note.ts` dùng `string` cho ghi chú tự do. Không có type ghi chú.

### D01. Cụm field khi đã có type
Pass: một đoạn nói dùng `Address`. Có `có thể để sau`. Không có `Data Clumps`.
Fail: mức sửa trước chỉ vì cụm field, hoặc bịa type mới.

### D02. Không bịa type cho ghi chú
Pass: không có đoạn bắt `note` thành type mới.
Fail: đề xuất type mới cho ghi chú tự do.

### D03. String đứng chỗ `OrderStatus`
Pass: một đoạn nói dùng `OrderStatus`. Mức `có thể để sau`.
Fail: bỏ qua type đã có.

### D04. Number đứng chỗ type id đã có
Thêm `OrderId` là type. Một hàm nhận `orderId: number` cho cùng khái niệm.
Pass: đoạn nói dùng `OrderId`. Mức `có thể để sau`.
Fail: bịa một type id khác.

### D05. Boolean không có enum thì không bịa
`isOpen: boolean` không có type sẵn.
Pass: không đề xuất enum mới.
Fail: đề xuất enum mới.

### D06. Switch lặp ở hai file
Pass: một đoạn cho `switch (status)` ở hai file. Mức `có thể để sau`. Không có `Repeated Switches`.
Fail: bỏ qua vì mỗi file một switch.

### D07. Switch chỉ một file thì không chấm lặp
Xóa switch ở `summary.ts`. Còn một switch.
Pass: không có đoạn switch lặp.
Fail: vẫn chấm switch một nơi.

### D08. Picker không có đoạn smell thứ hai
Pass: picker một đoạn, vì mỗi block render popup của nó. Không có đoạn smell thứ hai.
Fail: hai đoạn cho picker.

### D09. Feature envy trong cùng feature
`Checkout.tsx` có hàm chỉ đọc field của `address.ts` hơn field của chính nó. Đưa hàm sang `address.ts` vẫn trong feature.
Pass: một đoạn `có thể để sau`, nói đưa sang `address.ts`.
Fail: bảo đưa sang shared.

### D10. Không đề xuất move phá layer
Hàm ở `src/shared/format.ts` đọc field của checkout. Đưa hàm vào checkout sẽ khiến shared phụ thuộc feature.
Pass: không đề xuất move đó. Có thể nói để yên vì layer.
Fail: đề xuất move vào feature hoặc để shared import feature.

### D11. Chuỗi `a.b().c()`
Pass: một đoạn cho `order.customer.address.city`. Mức `có thể để sau`. Không có `Message Chains`.
Fail: nâng thành defect người dùng gặp trên màn.

### D12. `a.b()` không phải chuỗi dài
Chỉ có `order.customer`. Không có chuỗi ba bước.
Pass: không có đoạn chuỗi gọi.
Fail: chấm `order.customer`.

### D13. Component chỉ chuyển tiếp
Pass: một đoạn cho `ForwardButton`, `có thể để sau`, nói gọi thẳng con.
Fail: bỏ qua, hoặc mức sửa trước.

### D14. Wrapper hook chỉ một đoạn
Pass: `use-checkout-price` một đoạn. Không có đoạn smell thứ hai.
Fail: hai đoạn cho cùng hook.

### D15. Forward có thêm việc thì không phải chỉ chuyển tiếp
`ForwardButton` thêm một nhánh disabled.
Pass: không có đoạn middle man cho nút đó.
Fail: vẫn bảo xóa wrapper dù nó có nhánh riêng.

### D16. Bỏ hầu hết prop của lớp cha
Pass: một đoạn cho `PromoBanner`, nói dùng composition. Mức `có thể để sau`.
Fail: có `Refused Bequest`, hoặc bỏ qua.

### D17. Dùng prop kế thừa thì không chấm
`PromoBanner` dùng hầu hết prop của panel.
Pass: không có đoạn composition cho banner.
Fail: vẫn bắt extends.

### D18. Một file hai việc
Pass: một đoạn nói `format-and-fetch.ts` đang format và gọi HTTP. Mức `có thể để sau`.
Fail: bỏ qua vì không có diff.

### D19. Một file một việc thì không chấm
Tách sẵn format và fetch. Mỗi file một việc.
Pass: không có đoạn tách file.
Fail: vẫn bắt một trong hai file.

### D20. Hàm viết hai lần không thành smell thứ hai
Pass: `applyDiscount` chỉ dưới Viết hai lần.
Fail: thêm đoạn Việc nên làm cho cùng hai hàm.

### D21. Tên khó hiểu không thành smell
Thêm hàm `doStuff` trong checkout.
Pass: một đoạn tên, không gọi đó là smell. Không có tên smell tiếng Anh.
Fail: đoạn smell riêng cho `doStuff` bên cạnh đoạn tên.

### D22. Helper cho tương lai không thành smell thứ hai
Thêm `useFutureCheckout` không ai gọi, cho nhu cầu sau.
Pass: một đoạn rule cứng về abstraction chưa cần. Không có đoạn smell thứ hai.
Fail: hai đoạn cho cùng helper.

### D23. Danh sách field giữ tay không thành Shotgun Surgery
Một field phải vào schema, file map, và list thứ tự.
Pass: một đoạn Extension về các list đó. Không có `Shotgun Surgery`.
Fail: thêm đoạn smell tiếng Anh, hoặc đoạn thứ hai cùng các list.

### D24. Import ngược không bị hạ mức
Pass: đoạn import `other-feature/constants.ts` không dùng `có thể để sau`. Mức là `nên sửa trong lượt này` hoặc `nên sửa trước`.
Fail: import ngược chỉ `có thể để sau`.

### D25. Secret không bị hạ thành smell
Thêm `sk_live_test` vào `Checkout.tsx`.
Pass: secret là `nên sửa trước`. Không gọi đó là smell.
Fail: secret chỉ `có thể để sau`.

### D26. Smell và lỗi cứng là hai đoạn
Giữ cụm field và import ngược.
Pass: hai đoạn. Cụm field là `có thể để sau`. Import không phải mức đó.
Fail: một đoạn cho cả hai, hoặc cùng một mức.

### D27. Không có bảng Audit
Pass: không có bảng lens Reuse đến Extension.
Fail: in bảng Audit.

### D28. Ba smell không lộ tên tiếng Anh
Giữ cụm field, chuỗi gọi, và file hai việc.
Pass: ba đoạn tiếng Việt, không có tên smell tiếng Anh.
Fail: có một tên smell tiếng Anh.

### D29. Rule trong task cho phép tách field
Prompt thêm `Project rule: street, city, and zip stay separate fields.`
Pass: không bắt gom ba field. Smell khác vẫn chấm.
Fail: vẫn bắt gom.

### D30. Rule không nói gì về switch thì switch vẫn chấm
Prompt có rule field như D29. Switch lặp vẫn còn.
Pass: vẫn có đoạn switch, mức `có thể để sau`.
Fail: bỏ switch vì đã có một rule khác.

### D31. Task nói linter đã bắt `any`
Prompt thêm `The linter already reports no-explicit-any at Checkout.tsx:4.` File có `const x: any = 1`.
Pass: không có đoạn cho `any`.
Fail: có đoạn cho `any`.

### D32. Review không sửa smell
Prompt nói không sửa code.
Pass: `git status --short` rỗng.
Fail: sửa cụm field hoặc switch.

### D33. Người dùng bảo dọn màn thì được sửa smell
Prompt là `Clean up the src/checkout screen. Fix the findings.`
Pass: được sửa cụm field để dùng `Address`. Không được viện lệnh cấm review để từ chối mọi sửa.
Fail: từ chối sửa vì rule review cấm ghi file.

### D34. Diff không chấm cụm field
Đưa cụm field vào diff. Không có file yêu cầu. Prompt diff review.
Pass: không có đoạn gom `Address`.
Fail: có đoạn smell cho cụm field.

### D35. Diff không chấm chuỗi gọi
Diff chỉ thêm `order.customer.address.city`.
Pass: không có đoạn smell cho chuỗi đó.
Fail: có đoạn `có thể để sau` cho chuỗi.

### D36. Diff không chấm file hai việc
Diff thêm `format-and-fetch.ts`.
Pass: không có đoạn bảo tách file vì smell.
Fail: có đoạn smell tách file.

### D37. Diff vẫn fail hàm viết hai lần
Diff nhân đôi `applyDiscount`.
Pass: một đoạn cho hai bản hàm.
Fail: bỏ vì smell list bị cấm trên diff.

### D38. Diff vẫn fail wrapper hook
Diff thêm `use-checkout-price` chỉ bọc `usePrice`.
Pass: một đoạn cho wrapper.
Fail: bỏ vì không chấm smell trên diff.

### D39. Diff vẫn fail import ngược
Diff thêm import từ `other-feature` vào checkout.
Pass: một đoạn import, không phải mức smell.
Fail: bỏ import, hoặc gọi đó là smell được để sau.

### D40. Playbook có bảng audit thì smell là low
Prompt new-ui thêm một nút. Màn sẵn có cụm field, task không bảo sửa cụm đó.
Pass: không sửa cụm field trong diff của nút. Nếu có bảng audit và có dòng cụm field, severity là `low`.
Fail: severity `high` hoặc `medium` cho cụm field, hoặc diff nútRewrite cụm field.

## E. Biên diff và rule cứng

Không có file yêu cầu. Không có glossary, trừ khi case nói có.

### E01. Wrapper trên diff vẫn fail
Diff chỉ thêm hook bọc `usePrice`.
Pass: có đoạn wrapper.
Fail: không có đoạn.

### E02. Hai bản hàm trên diff vẫn fail
Diff nhân đôi `applyDiscount`.
Pass: có đoạn hai nơi.
Fail: không có đoạn.

### E03. Import ngược trên diff vẫn fail
Diff thêm import feature khác.
Pass: có đoạn import. Mức không phải `có thể để sau`.
Fail: không có đoạn, hoặc chỉ `có thể để sau`.

### E04. Cụm field trên diff không thành smell
Có `Address`. Diff truyền `street`, `city`, `zip` riêng.
Pass: không có đoạn gom type.
Fail: có đoạn gom type.

### E05. Chuỗi gọi trên diff không thành smell
Diff thêm `order.customer.address.city`.
Pass: không có đoạn chuỗi.
Fail: có đoạn chuỗi.

### E06. Switch lặp trên diff không thành smell
Diff thêm cùng `switch (status)` ở hai file.
Pass: không có đoạn smell switch.
Fail: có đoạn `có thể để sau` cho switch.

### E07. String thay type trên diff không thành smell
Diff dùng `status: string` dù repo có `OrderStatus`.
Pass: không có đoạn smell bảo đổi type.
Fail: có đoạn smell đổi type.

### E08. Component chỉ chuyển tiếp trên diff không thành smell
Diff thêm `ForwardButton` chỉ return con. Không thêm hook bọc.
Pass: không có đoạn smell. Không có fail wrapper, vì không có hook bọc.
Fail: fail như F7, hoặc có đoạn smell.

### E09. Banner bỏ prop trên diff không thành smell
Diff thêm `PromoBanner` bỏ hầu hết prop cha.
Pass: không có đoạn composition vì smell.
Fail: có đoạn smell composition.

### E10. File hai việc trên diff không thành smell
Diff thêm file vừa format vừa fetch.
Pass: không có đoạn smell tách file.
Fail: có đoạn smell tách file.

### E11. Secret thắng cụm field
Diff có `sk_live_test` và cụm field.
Pass: secret là `nên sửa trước`. Không có đoạn cụm field.
Fail: có đoạn cụm field, hoặc secret bị hạ mức.

### E12. `console.log` không kéo theo smell
Diff có `console.log` và chuỗi `a.b().c()`.
Pass: có đoạn `console.log`. Không có đoạn chuỗi.
Fail: có đoạn chuỗi.

### E13. Spec miss không biến thành smell
Có `docs/checkout.md`. Diff thiếu ô và có cụm field.
Pass: có đoạn trích dòng 2. Không có đoạn gom `Address`.
Fail: thay đoạn spec bằng đoạn smell.

### E14. Glossary không biến thành smell
Có glossary. Diff thêm `PurchaseCard` và cụm field.
Pass: có đoạn trích glossary. Không có đoạn gom field.
Fail: chỉ có đoạn smell, không trích glossary.

### E15. Diff không mở code-review để lấy smell
Diff có cụm field.
Pass: không nói đã chạy `code-review`. Không có đoạn smell.
Fail: nói đã mở `code-review`.

## F. Review không ghi file

### F01. Hai tên, không tạo glossary
Review folder có `order` và `purchase`. Không có glossary. Prompt không sửa code.
Pass: có finding hai tên. Không tạo `GLOSSARY.md`.
Fail: tạo glossary.

### F02. Không viết ADR
Giống F01.
Pass: không có file mới trong `docs/adr/`.
Fail: có ADR.

### F03. Không hỏi chọn thuật ngữ
Giống F01.
Pass: báo cáo nêu lệch tên, không hỏi người dùng chọn một tên trước khi kết thúc.
Fail: câu hỏi chặn, chưa có finding.

### F04. Deepen không ghi HTML
Prompt `Review the src/checkout folder. Where should it get deeper or simpler? Do not change the code.`
Pass: không có path `.html`.
Fail: có path HTML.

### F05. Deepen không hỏi chọn candidate
Giống F04.
Pass: không có câu hỏi chọn candidate.
Fail: có câu như which of these would you like to explore.

### F06. Deepen để git status sạch
Giống F04.
Pass: `git status --short` rỗng.
Fail: có file mới.

### F07. Review không sửa glossary có sẵn
Có `GLOSSARY.md`. Review thấy tên lệch. Prompt không sửa code.
Pass: `GLOSSARY.md` không đổi.
Fail: file glossary đổi.

### F08. Diff lệch tên không tạo glossary
Diff thêm `PurchaseCard`. Không có glossary. Diff review.
Pass: không tạo glossary. Không bịa tên chuẩn thành file.
Fail: tạo `GLOSSARY.md`.

### F09. Review không chạy setup
Review folder. Prompt không nhắc setup.
Pass: không bảo chạy `setup-matt-pocock-skills`.
Fail: có câu bảo chạy setup.

### F10. Review không mở code-review
Review folder có smell và hai tên.
Pass: không nói đã mở `code-review`.
Fail: nói đã mở skill đó.

### F11. new-ui được ghi glossary khi người dùng yêu cầu
Prompt `Add the term order to GLOSSARY.md. It means the order the user submits.` Playbook `skill://fe-kit/playbooks/new-ui.md`.
Pass: ghi `order`, hoặc không ghi nhưng không viện lệnh cấm của review.
Fail: từ chối vì rule review cấm ghi glossary.

### F12. Refactor được đổi tên theo glossary khi người dùng yêu cầu
Prompt `Rename purchase to order in src/checkout. The glossary term is order.` Playbook `skill://fe-kit/playbooks/refactor-ui.md`.
Pass: được sửa tên. Không viện lệnh cấm review.
Fail: từ chối sửa vì đang review.

### F13. Review cấm sửa thì không sửa smell
Prompt review, có câu do not change the code. Folder có cụm field.
Pass: không sửa file. Có thể có đoạn `có thể để sau`.
Fail: sửa file.

### F14. Path HTML trong `/tmp` vẫn fail
Giống F04.
Pass: báo cáo không chứa `.html` và không chứa `/tmp/`.
Fail: có path dưới `/tmp/` hoặc `.html`.

### F15. Finding không phải câu hỏi chặn
Review hai tên `order` và `purchase`.
Pass: có đoạn nói chỗ lệch và hệ quả. Không kết thúc bằng câu hỏi bắt người dùng trả lời trước.
Fail: chỉ có câu hỏi, không có finding.

## Không tính vào 200

`GLOSSARY.md` và `CONTEXT.md` cùng tồn tại, hai file mâu thuẫn. Rule chưa chọn file nào thắng. Ghi báo cáo reviewer trích file nào. Không chấm pass hay fail. Không sửa rule trong lúc chạy case này.

## Bảng kết quả

Điền `pass` hoặc `fail`. Mẫu số là 200.

| Case | Kết quả | Câu làm fail |
|---|---|---|
| A01 | pass | |
| A02 | pass | |
| A03 | pass | |
| A04 | pass | |
| A05 | pass | |
| A06 | pass | |
| A07 | pass | |
| A08 | pass | |
| A09 | pass | |
| A10 | pass | |
| A11 | pass | |
| A12 | pass | |
| A13 | pass | |
| A14 | pass | |
| A15 | pass | |
| A16 | pass | |
| A17 | pass | |
| A18 | pass | |
| A19 | pass | |
| A20 | pass | |
| A21 | pass | |
| A22 | pass | |
| A23 | pass | |
| A24 | pass | |
| A25 | pass | |
| A26 | pass | |
| A27 | pass | |
| A28 | pass | |
| A29 | pass | |
| A30 | pass | |
| A31 | pass | |
| A32 | pass | |
| A33 | pass | |
| A34 | pass | |
| A35 | pass | |
| A36 | pass | |
| A37 | pass | |
| A38 | pass | |
| A39 | pass | |
| A40 | pass | |
| B01 | pass | |
| B02 | pass | |
| B03 | pass | |
| B04 | pass | |
| B05 | pass | |
| B06 | pass | |
| B07 | pass | |
| B08 | pass | |
| B09 | pass | |
| B10 | pass | |
| B11 | pass | |
| B12 | pass | |
| B13 | pass | |
| B14 | pass | |
| B15 | pass | |
| B16 | pass | |
| B17 | pass | |
| B18 | pass | |
| B19 | pass | |
| B20 | pass | |
| B21 | pass | |
| B22 | pass | |
| B23 | pass | |
| B24 | pass | |
| B25 | pass | |
| B26 | pass | |
| B27 | pass | |
| B28 | pass | |
| B29 | pass | |
| B30 | pass | |
| B31 | pass | |
| B32 | pass | |
| B33 | pass | |
| B34 | pass | |
| B35 | pass | |
| B36 | pass | |
| B37 | pass | |
| B38 | pass | |
| B39 | pass | |
| B40 | pass | |
| B41 | pass | |
| B42 | pass | |
| B43 | pass | |
| B44 | pass | |
| B45 | pass | |
| B46 | pass | |
| B47 | pass | |
| B48 | pass | |
| B49 | pass | |
| B50 | pass | |
| C01 | pass | |
| C02 | pass | |
| C03 | pass | |
| C04 | pass | |
| C05 | pass | |
| C06 | pass | |
| C07 | pass | |
| C08 | pass | |
| C09 | pass | |
| C10 | pass | |
| C11 | pass | |
| C12 | pass | |
| C13 | pass | |
| C14 | pass | |
| C15 | pass | |
| C16 | pass | |
| C17 | pass | |
| C18 | pass | |
| C19 | pass | |
| C20 | pass | |
| C21 | pass | |
| C22 | pass | |
| C23 | pass | |
| C24 | pass | |
| C25 | pass | |
| C26 | pass | |
| C27 | pass | |
| C28 | pass | |
| C29 | pass | |
| C30 | pass | |
| C31 | pass | |
| C32 | pass | |
| C33 | pass | |
| C34 | pass | |
| C35 | pass | |
| C36 | pass | |
| C37 | pass | |
| C38 | pass | |
| C39 | pass | |
| C40 | pass | |
| D01 | pass | |
| D02 | pass | |
| D03 | pass | |
| D04 | pass | |
| D05 | pass | |
| D06 | pass | |
| D07 | pass | |
| D08 | pass | |
| D09 | pass | |
| D10 | pass | |
| D11 | pass | |
| D12 | pass | |
| D13 | pass | |
| D14 | pass | |
| D15 | pass | |
| D16 | pass | |
| D17 | pass | |
| D18 | pass | |
| D19 | pass | |
| D20 | pass | |
| D21 | pass | |
| D22 | pass | |
| D23 | pass | |
| D24 | pass | |
| D25 | pass | |
| D26 | pass | |
| D27 | pass | |
| D28 | pass | |
| D29 | pass | |
| D30 | pass | |
| D31 | pass | |
| D32 | pass | |
| D33 | pass | |
| D34 | pass | |
| D35 | pass | |
| D36 | pass | |
| D37 | pass | |
| D38 | pass | |
| D39 | pass | |
| D40 | pass | |
| E01 | pass | |
| E02 | pass | |
| E03 | pass | |
| E04 | pass | |
| E05 | pass | |
| E06 | pass | |
| E07 | pass | |
| E08 | pass | |
| E09 | pass | |
| E10 | pass | |
| E11 | pass | |
| E12 | pass | |
| E13 | pass | |
| E14 | pass | |
| E15 | pass | |
| F01 | pass | |
| F02 | pass | |
| F03 | pass | |
| F04 | pass | |
| F05 | pass | |
| F06 | pass | |
| F07 | pass | |
| F08 | pass | |
| F09 | pass | |
| F10 | pass | |
| F11 | pass | |
| F12 | pass | |
| F13 | pass | |
| F14 | pass | |
| F15 | pass | |

Pass cả 200 thì bốn phần mới đúng. Một case fail là rule của case đó chưa ăn.
