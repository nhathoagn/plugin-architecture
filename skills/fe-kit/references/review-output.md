# Kết quả review

Đây là bản người đọc. Tiếng Việt. Viết xong thì dừng.

Không ghi mã checklist. Không ghi PASS, FAIL, N/A, blocker, major, minor, SHIP. Không kể file đã mở mà không có việc.

## Cách viết

Kết luận đi trước. Một hoặc hai câu. Nói có đưa lên được không, và nêu tên các việc phải sửa trước.

Mỗi việc sau đó là một đoạn, khoảng hai câu. Câu đầu nói cái gì đang bị, tên đúng trong code, và `file:dòng`. Câu sau nói sửa thế nào, và người dùng mất gì nếu để vậy. Mức nằm trong câu khuyên: "nên sửa trước", "nên sửa trong lượt này", "có thể để sau".
Nếu diff có check validate, không viết "Đưa được" khi chưa nêu kết quả của `undefined`, `null`, và `""`.
Có file yêu cầu thì việc thiếu, việc làm thừa, và việc làm sai nằm trong Việc cần sửa. Trích đúng dòng file đó. Không thêm mục riêng.
Trích `file:dòng` phải đúng: đếm dòng thật trong file, kể cả dòng heading, rồi quote nguyên văn đúng dòng đó. Số dòng không được ước lượng và không được lệch một dòng.
Một đoạn finding dựa trên dòng nào của file yêu cầu thì tự trích dòng đó — kể cả khi đoạn tìm ra bằng phép thử năm giá trị: lỗi thuộc phạm vi dòng nào thì trích dòng đó, và một lỗi guard (`if (!x)`, `??`, `||`) nằm trong code mà dòng đó quản lý cũng vi phạm dòng đó nên đoạn của nó phải trích dòng đó. Một dòng nêu hai việc thì đúng một đoạn trích dòng đó, nêu cả hai việc; không tách hai việc thành hai đoạn và không đổi căn cứ sang dòng riêng lẻ khác. Hai lỗi khác nhau cùng rơi vào một dòng thì hoặc gom một đoạn với dòng đó, hoặc mỗi đoạn đều trích dòng đó. Ưu tiên gom mọi lỗi của cùng một dòng vào một đoạn với dòng đó.
Không có file yêu cầu thì Kết luận nói một câu là không có file yêu cầu. Không bịa việc từ code. Đã nói câu đó thì cả báo cáo không được trích một dòng file spec nào, kể cả khi file có trong repo. Nhánh có dấu `/` không tự khớp file nào: phần sau dấu slash không bao giờ là hit, kể cả khi file đúng phần đó tồn tại — khi đó câu trả lời là không có file yêu cầu.
Không viết đoạn về độ sâu chuỗi truy cập (`a.b().c()`), cụm field gộp vào type có sẵn, switch lặp, file gộp hai việc, component chỉ chuyển tiếp, hay kế thừa bỏ prop — checklist không có mục đó cho một diff, kể cả khi viết như lỗi chạy hay lỗi an toàn.
Tên trong diff lệch file glossary thì cũng nằm trong Việc cần sửa. Trích đúng dòng file đó. Không thêm mục riêng. Không có file glossary thì không bịa một tên chuẩn.
Xung đột thuật ngữ luôn trích dòng glossary, không trích dòng spec, kể cả khi spec cũng nói về nhãn hay tên đó. Một tên khác với thuật ngữ là finding, không kể thứ tự tên file hay tên export: `Order` cho `order` thì cùng thuật ngữ, còn `purchase`, `donHang` thì không. Một khái niệm hai tên là một đoạn, trích dòng glossary đó. Comment không phải tên mới trong code: không viết finding glossary (hay finding nào) cho một comment — trừ TODO không có owner theo mục TODO.

Một lỗi một đoạn. Không viết lại cùng một chỗ dưới hai tên, kể cả khi checklist, file yêu cầu, và glossary cùng chỉ một chỗ.

Mỗi đoạn finding ghi đúng một trong ba mức trong câu khuyên; đoạn thiếu mức là đoạn hỏng. Import ngược, bản sao viết lại, wrapper hook, và secret không bao giờ là `có thể để sau`.
Checklist xong mà mọi dòng diff chạm vào đều đúng và không finding nào khác: câu đầu là `Đưa được`, và không viết finding cho dòng N/A.
Để yên một thứ mà nguồn yêu cầu có vẻ đòi (nguồn trúng nói nó không cần) thì trích đúng dòng nguồn đó làm lý do; không trích dòng chỉ để kể.

Tên function, component, và file giữ nguyên. Trong câu người đọc, không dùng `duplicate`, `codebase`, `reuse`, `shared`, `field list`.

Nói thẳng. Không mở đầu bằng "em thấy", "có vẻ", hay "hình như".

Đúng: `applyDiscount` đang có hai bản giống hệt, ở `price.ts:1` và `cartPrice.ts:1`. Nên giữ một hàm rồi gọi sang, kẻo sửa giảm giá một nơi thì nơi kia vẫn tính kiểu cũ. Nên sửa trong lượt này.

Sai: `F4 the same statements written twice — FAIL — price.ts:1`.

Sai: Logic tính giảm giá có vẻ đang bị duplicate.

Đúng: `docs/checkout.md:4` yêu cầu ô địa chỉ bắt buộc. `AddressForm.tsx` không có ô đó, nên người dùng gửi đơn mà không có địa chỉ. Nên sửa trong lượt này.

Sai: thêm một mục Spec rồi ghi missing address.

## Kết luận

Không đưa lên. Hai việc phải sửa trước: key thẻ nằm trong `SecretForm.tsx:1`, và `Conflicted.tsx:2` còn dấu conflict nên file không chạy.

Hoặc: Đưa được. Không còn việc phải sửa.

## Việc cần sửa

`SecretForm.tsx:1` đang ghi key `sk_live_` trong file, rồi đưa vào ô thẻ ở dòng 4. Xóa key khỏi source và để ô trống, kẻo key đi theo bản build và ai mở trang cũng thấy. Nên sửa trước.

## Để yên

Chỉ ghi thứ cố ý không sửa, và vì sao. Bỏ mục này nếu không có.

## Tóm tắt

Việc chặn đưa lên: 1. Việc nên sửa trong lượt này: 0. Việc có thể để sau: 0.
