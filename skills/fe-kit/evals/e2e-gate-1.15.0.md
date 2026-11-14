# E2E gate 1.15.0 — test rule text (2026-11-15)

Mục tiêu: kiểm chứng 2 rule mới chạy thật, không chỉ trong test script.

## Phương pháp

1. **Smoke deny/allow trên artifact đang cài** (`~/.claude/plugins/cache/fe-arch/fe-kit/1.15.0`):
   - Payload PreToolUse sửa `.tsx` không có label → `permissionDecision: deny`.
   - Payload với transcript có `Runtime owner:` + `Decision: reuse` → cho phép, `additionalContext` chứa đủ `name the convention it follows`, `running list is incomplete`, `A file does one job`.
2. **Test hành vi**: fresh agent nhận đúng text rule mà hook bơm (trích từ cache 1.15.0), task thật trong repo mẫu `/tmp/gate-e2e` (3 file kebab trong `src/checkout/`): tạo hook mới + sửa `order-list.tsx` + sửa `total.ts` (multi-file, file mới khác pattern).

## Kết quả

| Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|
| List file+job trước các edit còn lại | pass | message "Files sẽ tạo/sửa (list trước edit)" trước 2 lệnh edit |
| File mới nêu convention + anh-em | pass | "kebab-case, export useOrderRefresh, khớp sibling order-list.tsx xuất OrderList (file = main export) … feature sở hữu src/checkout" |
| Job mỗi file trước khi xong | pass | "Tóm tắt thay đổi" nêu job cả 3 file |
| Rule cũ vẫn tuân | pass | search + `Decision: feature-local` kèm consumer; `Trigger/Expected/Actual`; repro `node` trước/sau fix; `esbuild` bundle |
| Artifact trên đĩa | pass | 1 file mới + 2 sửa; `git diff --stat` khớp |

`scripts/test_fe_gate.py`: 94/94 pass (logic gate, không đổi script hôm nay).

## Giới hạn

- 1 case hành vi, không phải suite.
- Cuộc test thật bị giao rules trễ (race do cách thử) — production bơm ở UserPromptSubmit trước mọi tool call, thứ tự thật tốt hơn; agent tự bổ sung convention+anh-em sau khi đọc rule nên vẫn pass.
- Vòng deny → retry → allow đầy đủ chưa chạy được bằng `claude -p` (OAuth CLI hết hạn — lỗi auth, không phải plugin); 2 nhánh deny/allow đã cover bằng smoke.
