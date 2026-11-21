# UT nested if

Plan này chấm ba mục về `if` lồng nhau: N2 trong `references/REVIEW_CHECKLIST.md` cho diff review, T1 trong `references/tidy-checklist.md` và F4a trong `references/fowler-checklist.md` cho refactor. Không chấm mục khác, trừ khi case nêu.

Một case pass chỉ khi mọi điều kiện Pass đúng và không điều kiện Fail nào đúng.

## Cách chạy

Mỗi case là một repo tạm ở `/tmp/ut-nested-if`. Xóa repo cũ trước case sau. Không dùng repo plugin.

1. Viết file đúng số dòng trong phần fixture, rồi áp delta của case.
2. Diff review cần hai commit. `BASE` là commit trước thay đổi. `HEAD` là commit của thay đổi.
3. Mở context mới. Không đưa ghi chú của người viết fixture.
4. Diff review chỉ đưa `BASE`, `HEAD`, và `skill://fe-kit/playbooks/review-diff.md`. Working directory là repo tạm.
5. Refactor chỉ đưa prompt của case và `skill://fe-kit/playbooks/refactor-ui.md`.
6. Sau refactor, chạy `node --experimental-strip-types check.ts`. Exit 0 là hành vi giữ nguyên.

Fail chung cho diff review:

- In `PASS`, `FAIL`, `N/A`, `N2`, `T1`, hoặc `F4a`.
- Câu đầu không phải tiếng Việt.
- Sửa file trong repo tạm.

Fail chung cho refactor:

- `check.ts` exit khác 0.
- Một chỗ lồng được kể hai lần, một lần dưới T1 và một lần dưới F4a.

## Fixture gốc

`src/checkout/submit-order.ts`, lồng 5 tầng ở dòng 4 đến dòng 8.

```ts
export type Order = { items: number[]; address: string; paid: boolean; coupon?: string };

export function submitOrder(order: Order | null): string {
  if (order) {
    if (order.items.length > 0) {
      if (order.address.trim() !== '') {
        if (order.paid) {
          if (order.coupon) {
            return `sent with ${order.coupon}`;
          }
          return 'sent';
        } else {
          return 'unpaid';
        }
      } else {
        return 'no address';
      }
    } else {
      return 'empty';
    }
  } else {
    return 'no order';
  }
}
```

`src/checkout/submit-order-flat.ts`, cùng hành vi, viết bằng guard clause.

```ts
import type { Order } from './submit-order.ts';

export function submitOrderFlat(order: Order | null): string {
  if (!order) return 'no order';
  if (order.items.length === 0) return 'empty';
  if (order.address.trim() === '') return 'no address';
  if (!order.paid) return 'unpaid';
  return order.coupon ? `sent with ${order.coupon}` : 'sent';
}
```

`check.ts`

```ts
import { submitOrder } from './src/checkout/submit-order.ts';

const base = { items: [1], address: 'Hà Nội', paid: true };
const cases: [Parameters<typeof submitOrder>[0], string][] = [
  [null, 'no order'],
  [{ ...base, items: [] }, 'empty'],
  [{ ...base, address: '   ' }, 'no address'],
  [{ ...base, paid: false }, 'unpaid'],
  [base, 'sent'],
  [{ ...base, coupon: 'SALE' }, 'sent with SALE'],
  [{ ...base, items: [], paid: false }, 'empty'],
];
for (const [input, want] of cases) {
  const got = submitOrder(input);
  if (got !== want) {
    console.error(JSON.stringify(input), got, '!==', want);
    process.exit(1);
  }
}
```

`check.ts` phải exit 0 trên fixture gốc trước khi chạy case.

## A. Diff review: N2

Diff gốc của nhóm A: `BASE` chỉ có `check.ts`, `HEAD` thêm file của case.

### A01. Lồng 5 tầng là finding
`HEAD` thêm `src/checkout/submit-order.ts`.
Pass: có một đoạn nêu `submitOrder` lồng sâu, trích `src/checkout/submit-order.ts` ở một dòng từ 4 đến 8, khuyên đưa trường hợp đặc biệt lên đầu và return sớm.
Fail: không có đoạn nào về độ lồng.

### A02. Mức của đoạn lồng
Giống A01.
Pass: đoạn lồng mang `có thể để sau`. Câu đầu là `Đưa được`.
Fail: đoạn lồng mang `nên sửa trước`, hoặc câu đầu là `Không đưa lên`.

### A03. Lồng 4 tầng không là finding
Giống A01, nhưng dòng 8 đến 11 thay bằng `return order.coupon ? \`sent with ${order.coupon}\` : 'sent';`.
Pass: không có đoạn về độ lồng. Câu đầu là `Đưa được`.
Fail: có đoạn về độ lồng.

### A04. Guard clause không là finding
`HEAD` thêm `src/checkout/submit-order-flat.ts`.
Pass: không có đoạn về độ lồng hay guard clause.
Fail: có đoạn khuyên đổi cách viết các `if`.

### A05. Lồng có lời giải thích thì không fail
Giống A01, thêm trên dòng 3 comment `// Thứ tự kiểm tra khớp thứ tự lỗi hiển thị trong docs/checkout.md; xem #45.` và thêm `docs/checkout.md` có thứ tự đó.
Pass: không có đoạn về độ lồng.
Fail: có đoạn về độ lồng.

### A06. Lồng ngoài diff không tính
`BASE` đã có `src/checkout/submit-order.ts`. `HEAD` chỉ đổi chuỗi `'sent'` ở dòng 11 thành `'đã gửi'`, và sửa `check.ts` cho khớp.
Pass: không có đoạn về độ lồng.
Fail: có đoạn về độ lồng.

### A07. Diff làm lồng sâu hơn thì tính
`BASE` có bản lồng 4 tầng của A03. `HEAD` đổi về fixture gốc 5 tầng.
Pass: có đoạn về độ lồng, trích một dòng từ 4 đến 8.
Fail: bỏ qua vì hàm đã có sẵn trước diff.

### A08. Một hàm, một đoạn
Giống A01.
Pass: đúng một đoạn về độ lồng của `submitOrder`.
Fail: tách thành nhiều đoạn, mỗi tầng một đoạn.

### A09. `if` lặp ở hai file không là finding
`HEAD` thêm cả `submit-order.ts` bản A03 và `submit-order-flat.ts`. Hai file cùng kiểm `order.paid`.
Pass: không có đoạn về `if` lặp.
Fail: có đoạn về `if` hay điều kiện lặp ở hai file.

### A10. Guard mới vẫn qua phép thử năm giá trị
Giống A01. Dòng 6 là check `trim`.
Pass: báo cáo không nói `address` `undefined` hay `null` trả về an toàn khi chưa thử. Nếu nêu lỗi `undefined` hay `null` ở dòng 6, đoạn đó trích dòng 6.
Fail: viết `Đưa được` mà không nêu kết quả của `undefined`, `null`, và `""` cho dòng 6.

## B. Refactor: T1 và F4a

Repo tạm có fixture gốc và `check.ts`, đã commit.

### B01. Refactor làm phẳng
Prompt `Refactor src/checkout/submit-order.ts so it is easier to read. Do not change behavior.`
Pass: sau refactor, `submitOrder` không lồng quá 2 tầng. Trường hợp `no order`, `empty`, `no address`, `unpaid` return sớm. `check.ts` exit 0.
Fail: vẫn lồng từ 3 tầng trở lên.

### B02. T1 và F4a đếm một lần
Giống B01.
Pass: output nêu chỗ lồng của `submitOrder` đúng một lần.
Fail: nêu dưới T1 rồi nêu lại dưới F4a như hai việc.

### B03. Không đổi hành vi
Giống B01.
Pass: sáu chuỗi trả về giữ nguyên. Không thêm `throw`, log, hay nhánh mới.
Fail: đổi chuỗi, thêm nhánh, hoặc đổi thứ tự kiểm tra làm case cuối của `check.ts` không còn ra `empty`.

### B04. Tidy tách khỏi behavior
Prompt `Flatten submitOrder, then return 'no items' instead of 'empty'.` Sửa `check.ts` cho khớp chuỗi mới.
Pass: hai commit. Commit đầu chỉ làm phẳng, `check.ts` gốc exit 0 ở commit đó. Commit sau chỉ đổi chuỗi.
Fail: một commit làm cả hai.

### B05. Hàm đã phẳng thì không refactor
Repo chỉ có `submit-order-flat.ts`. Prompt `Refactor src/checkout/submit-order-flat.ts so it is easier to read. Do not change behavior.`
Pass: không có việc về guard clause hay độ lồng. `git diff` của file đó rỗng, hoặc chỉ đổi thứ không liên quan tới `if`.
Fail: đề xuất hay viết lại các `if` của hàm.

### B06. Ba nhánh phẳng thì không fail F4a
Thay thân `submitOrder` bằng `if (!order) return 'no order'; if (order.paid) return 'sent'; return 'unpaid';`, sửa `check.ts` cho khớp. Prompt giống B01.
Pass: không có việc về guard clause.
Fail: có việc về guard clause.

### B07. Không thêm pattern cho bốn điều kiện
Giống B01.
Pass: không thêm lookup table, Strategy, hay Chain of Responsibility cho bốn điều kiện.
Fail: thay các `if` bằng một pattern, hoặc đề xuất pattern mà không trích cột `Đừng áp khi` của `references/patterns.md`.

## Bảng kết quả

Điền `pass` hoặc `fail`. Mẫu số là 17.

| Case | Kết quả | Câu làm fail |
|---|---|---|
| A01 | | |
| A02 | | |
| A03 | | |
| A04 | | |
| A05 | | |
| A06 | | |
| A07 | | |
| A08 | | |
| A09 | | |
| A10 | | |
| B01 | | |
| B02 | | |
| B03 | | |
| B04 | | |
| B05 | | |
| B06 | | |
| B07 | | |

Pass cả 17 thì ba mục về `if` lồng nhau đúng.
