# Kết quả review

Đây là bản người đọc. Tiếng Việt. Viết xong thì dừng.

Không ghi mã checklist. Không ghi PASS, FAIL, N/A, blocker, major, minor, SHIP. Không kể file đã mở mà không có việc.

## Cách viết

Kết luận đi trước. Một hoặc hai câu. Nói có đưa lên được không, và nêu tên các việc phải sửa trước.

Mỗi việc sau đó là một đoạn, khoảng hai câu. Câu đầu nói cái gì đang bị, tên đúng trong code, và `file:dòng`. Câu sau nói sửa thế nào, và người dùng mất gì nếu để vậy. Mức nằm trong câu khuyên: "nên sửa trước", "nên sửa trong lượt này", "có thể để sau".
Nếu diff có check validate, không viết "Đưa được" khi chưa nêu kết quả của `undefined`, `null`, và `""`.

Một lỗi một đoạn. Không viết lại cùng một chỗ dưới hai tên.

Tên function, component, và file giữ nguyên. Trong câu người đọc, không dùng `duplicate`, `codebase`, `reuse`, `shared`, `field list`.

Nói thẳng. Không mở đầu bằng "em thấy", "có vẻ", hay "hình như".

Đúng: `applyDiscount` đang có hai bản giống hệt, ở `price.ts:1` và `cartPrice.ts:1`. Nên giữ một hàm rồi gọi sang, kẻo sửa giảm giá một nơi thì nơi kia vẫn tính kiểu cũ. Nên sửa trong lượt này.

Sai: `F4 the same statements written twice — FAIL — price.ts:1`.

Sai: Logic tính giảm giá có vẻ đang bị duplicate.

## Kết luận

Không đưa lên. Hai việc phải sửa trước: key thẻ nằm trong `SecretForm.tsx:1`, và `Conflicted.tsx:2` còn dấu conflict nên file không chạy.

Hoặc: Đưa được. Không còn việc phải sửa.

## Việc cần sửa

`SecretForm.tsx:1` đang ghi key `sk_live_` trong file, rồi đưa vào ô thẻ ở dòng 4. Xóa key khỏi source và để ô trống, kẻo key đi theo bản build và ai mở trang cũng thấy. Nên sửa trước.

## Để yên

Chỉ ghi thứ cố ý không sửa, và vì sao. Bỏ mục này nếu không có.

## Tóm tắt

Việc chặn đưa lên: 1. Việc nên sửa trong lượt này: 0. Việc có thể để sau: 0.
