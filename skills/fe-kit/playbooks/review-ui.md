# Review UI

Use this when the task is to check, review, clean up, or shorten frontend code that already exists, and no behavior should change.

The user sees only the report under Kết quả review. Do not print a line for each file you open. Read once, then write. If a file changes while you read, add one line under Kết luận and stop. Do not read the tree again to rewrite the report.

1. Read `references/ownership.md`. A wrong placement is one finding under Việc nên làm. A right placement is not reported.
2. Read `references/reuse.md` and `rules/reuse-duplication.md`. The decision goes under Dùng lại, in the voice of Cách viết. The same statements in two files go under Viết hai lần. Three or more calls that differ only by data go under Chỉ khác dữ liệu.
3. Read `references/code-quality.md`. Search every heading from Names through Design and behavior. Each finding goes under Việc nên làm, in the voice of Cách viết. Do not emit the sweep table. A pass that stops after the first finding is not done. A name that also exists outside the folder does not change scope. Open every file in the named folder.
4. Read `references/performance.md` only if the code fetches, lists, or streams. A finding goes under Việc nên làm. When it polls, say the worst-case rate in that finding. If it does not fetch, list, or stream, do not mention performance.
5. Read `references/audit.md`. Trace each lens from Reuse through Extension. Each finding goes under Việc nên làm and says what it costs if it stays. Do not emit the Audit table. A lens with nothing wrong is omitted.
6. Read `references/feature-isolation.md` only when the code under review adds new behavior to existing UI. Unflagged or interleaved new behavior is one finding under Việc nên làm, in the voice of Cách viết. Otherwise do not mention it.
7. Read `references/external.md`. For a match, read the installed skill file, or fetch it per that file. A finding from that skill goes under Việc nên làm, in the voice of Cách viết. If none match, say nothing.

Each finding is written once. A duplicate block is only under Viết hai lần. A data-only repetition is only under Chỉ khác dữ liệu. Việc nên làm is everything else.

Report findings first. Change code only after the user picks what to change, unless the user already asked for the change.
When the user asked for the change, fix every finding you can in this turn, then check those lines again. Capture the screen before the first edit and after the last one. A refactor that changes the output is not done. Kết luận names the commands, their exit codes, and whether the screen matched.

## Kết quả review

Đây là output duy nhất. Tiếng Việt. Viết xong thì dừng.

### Cách viết

Viết như đang giải thích cho người trong team. Câu đọc lên là hiểu. Không viết cụt thành ghi chú.

- Kết luận đi trước. Một hoặc hai câu: việc đáng làm nhất, hoặc là không còn gì phải sửa.
- Mỗi việc khoảng hai câu. Câu đầu nói cái gì đang bị, tên đúng trong code, và `file:dòng`. Câu sau nói nên làm gì, và chuyện gì xảy ra nếu để vậy.
- Câu "chuyện gì xảy ra" nói người dùng mất gì, không chỉ nói code xấu: màn hiện rỗng mà không báo lỗi, mất phần đã nhập, lỗi hiện khác màn khác.
- Khi có màn mẫu hay file rule cho việc đó, nói tên màn hay `file:dòng` của rule để người sửa đối chiếu.
- Mức nói bằng lời, nằm trong câu khuyên: "nên sửa trước", "nên sửa trong lượt này", "có thể để sau". Không gắn `Mức vừa` ở cuối câu.
- Tiếng Việt thường. Tên function, component, và file giữ nguyên như trong code. Trong câu người đọc, không dùng `duplicate`, `codebase`, `reuse`, `extend`, `feature-local`, `shared`, hay `field list`.
- Nói thẳng việc. Không mở đầu bằng "em thấy", "có vẻ", hay "hình như".
- Không kể file đã mở. Không kể chỗ đã tìm mà không có việc.
- Bỏ mục không có việc. Kết luận và Dùng lại luôn có.
- Không dùng bảng checklist. Chỉ dùng bảng khi một mục có từ ba việc. Mỗi ô vẫn là câu nói được.

Đúng: `applyDiscount` đang có hai bản giống hệt, ở `pricing/total.ts:12` và `cart/summary.ts:12`. Nên giữ một hàm rồi gọi sang, kẻo sửa giảm giá một nơi thì nơi kia vẫn tính kiểu cũ. Nên sửa trong lượt này.

Sai: `applyDiscount` nằm ở `pricing/total.ts:12` và `cart/summary.ts:12`. Gọi một hàm. Mức vừa.

Sai: Logic tính giảm giá có vẻ đang bị duplicate ở nhiều nơi trong codebase.

### Kết luận

Một hoặc hai câu theo Cách viết.

### Viết hai lần

Đoạn lệnh viết lại y hệt ở hai file. Nói tên đoạn, hai vị trí, nên gọi một chỗ hay để nguyên, và vì sao.

### Chỉ khác dữ liệu

Một component được gọi từ ba lần trở lên, mỗi lần chỉ đổi dữ liệu đưa vào. Nói số lần, file, và gom thành một danh sách trường rồi vẽ một lần. Lượt review chỉ đề xuất, không sửa. Hai lần gọi thì chưa đủ. Lần gọi dùng component khác, phần bên trong khác, hoặc hàm xử lý khác thì không gom.

### Việc nên làm

Những việc còn lại, mỗi việc theo Cách viết: tên khó hiểu, helper chỉ dùng một lần, kiểu lỏng, file lẫn việc, luồng dễ kẹt, lỗi bị nuốt, tải, đặt nhầm chỗ, khó mở rộng.

### Dùng lại

Một hoặc hai câu. Nói đã tìm theo việc gì, chỗ nào đang làm việc đó, và chọn một trong bốn hướng, bằng tiếng Việt: dùng lại chỗ đang có, thêm vào chỗ đang có, viết trong feature này, đưa ra chỗ dùng chung. Nói lý do. Không thấy chỗ nào thì nói không thấy.

### Không đụng tới

Thứ cố ý để yên, và vì sao để yên.
