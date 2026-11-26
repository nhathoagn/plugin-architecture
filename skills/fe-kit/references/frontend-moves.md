# frontend-moves.md

Catalog các move đặc thù frontend (React-flavored, nguyên tắc áp cho Vue/Svelte) — phần Fowler chưa đặt tên. Format giống Fowler: **tín hiệu → động tác → đừng khi**. Không phải checklist PASS/FAIL — là menu động tác khi `smells-checklist.md`/`fowler-checklist.md` FAIL trên code FE mà cure của Fowler không đủ (Fowler không biết component, hook, effect, fetch).

Mỗi move giữ hành vi — test xanh trước và sau; test vỡ mà behavior không đổi là U1 của test đó.

---

## Nhóm 1 · State ở đúng chỗ

- **FM1 Lift State Up** — *Tín hiệu*: hai component anh em cần cùng giá trị, đang sync bằng callback lên cha rồi prop xuống lòng vòng. *Động tác*: move state lên ancestor chung gần nhất của cả hai, truyền value+setter xuống. *Đừng khi*: chỉ một nhánh thật sự cần — lift lên là kéo re-render cả nhánh kia; lúc đó FM2. Liên quan SM6: đừng "lift" thẳng lên global store khi phạm vi chỉ hai component.
- **FM2 Colocate State Down** — *Tín hiệu*: state ở parent/store mà chỉ một nhánh con đọc-ghi; prop chỉ forward xuống một chỗ, setter không ai gọi ngoài nhánh. *Động tác*: move state (và logic đi kèm) xuống component con. *Đừng khi*: state chia sẻ thật — chỉ vì "hiện tại" một chỗ đọc không nghĩa là không phải shared; check cả writer lẫn reader trong tương lai gần.
- **FM3 Prop Drilling → Composition/Context** — *Tín hiệu*: prop đi xuyên 2+ tầng mà tầng giữa không đọc nó (= O6 Pass-Through Variable ở tầng props). *Động tác*: ưu tiên composition — truyền JSX/component xuống (`children`, render prop) để prop dừng lại sớm; context chỉ khi giá trị thật sự cross-cutting (theme, user, locale). *Đừng khi*: context cho state đổi nhanh — mọi consumer re-render; composition trước, context sau.
- **FM4 Effect → Derived State** — *Tín hiệu*: `useEffect` chỉ để `setX(f(props, state))` — đồng bộ state với state. Đây là derived state chạy qua effect: thêm một render, dễ stale, che mất quan hệ data thật. *Động tác*: xóa effect, tính trong render (`const x = f(a)`), `useMemo` nếu đắt thật. *Đừng khi*: effect đồng bộ với hệ ngoài (subscription, DOM, timer) — đó là chỗ đứng của effect, không phải FM4. (= React docs "You Might Not Need an Effect"; bản SM7 Mutable Data trong component.)

## Nhóm 2 · Tách component đúng trục

- **FM5 Split by Change Axis** — *Tín hiệu*: component bị sửa vì 2+ lý do độc lập — fetch + render + form + permission (SM10 ở component level, F2b). *Động tác*: tách theo *lý do thay đổi*, không theo loại code — data fetching ra một file, render nhánh đổi-nhanh ra một file; đừng tách "mọi hook vào hooks/, mọi format vào utils/" — đó là split theo kind, O4 temporal/kind decomposition. Dạng hay gặp nhất là **container / view**: component vừa fetch hoặc giữ state feature, vừa xử lý event, vừa render một khối markup lớn → container giữ data, state feature và handler (gọi hook, FM6/FM11); view chỉ nhận props và render JSX, gọi callback qua props, không fetch, không import data layer. View vẫn được giữ state UI cục bộ (mở/đóng, hover, focus) — tầng UI sở hữu state hiển thị (`references/ownership.md:49`). *Đừng khi*: chỉ một lý do đổi — file 400 dòng một việc giữ nguyên (`rules/modules.md`); component nhỏ, markup ngắn — tách container/view chỉ thêm một file và một lớp props (SM16).
- **FM6 Extract Custom Hook** — *Tín hiệu*: logic stateful trộn trong component — subscription, timer, fetch state, form bookkeeping — phần render chìm trong phần cơ chế. *Động tác*: gom chuỗi `useState`/`useEffect` liên quan thành `useX()`, component chỉ còn render; tên theo *việc* nó làm cho UI (`useOrderSearch`), không theo cơ chế (`useFetchData`). *Đừng khi*: một component duy nhất, vài dòng — hook cho một consumer chưa có nhu cầu thứ hai là abstraction suy đoán (SM17); consumer thứ hai mới là tín hiệu share.
- **FM7 Extract List Item** — *Tín hiệu*: JSX trong `.map` dài quá một màn hình, hoặc item có state/logic riêng. *Động tác*: trích item thành component con đặt tên theo item, truyền `key` ngoài map. *Đừng khi*: map 3–5 dòng JSX thuần — extract chỉ thêm indirection (SM16).
- **FM8 Effect → Event Handler** — *Tín hiệu*: `useEffect` chạy vì một hành động cụ thể của user (submit gọi API, click ghi log) — effect là chỗ cho *đồng bộ với hệ ngoài*, không phải *phản ứng với user*. *Động tác*: move logic vào handler tương ứng; effect chỉ giữ subscription/external sync. *Đừng nhầm*: effect khởi động một lần lúc mount để load data vẫn là sync — không phải FM8, xem FM11.

## Nhóm 3 · Async & fetch

- **FM9 `.then` chain → async/await** — *Tín hiệu*: `.then().catch()` lồng hoặc chuỗi >2 — flow đọc ngược, error path tản mát. *Động tác*: đổi thành `try { const a = await x(); const b = await y(a) } catch { ... }`, giữ nguyên điểm bắt lỗi ở boundary. *Đừng khi*: chain một `.then` đơn giản không cần dàn xếp.
- **FM10 Serial → Parallel fetch** — *Tín hiệu*: `await a(); await b()` mà `b` không cần kết quả `a` — waterfall nhân tạo. *Động tác*: `const [a, b] = await Promise.all([fa(), fb()])`; từng nhánh độc lập một promise. *Đừng khi*: `b` cần output của `a` — serial là dependency thật, không phải mùi.
- **FM11 Fetch-in-effect → data layer** — *Tín hiệu*: `useEffect` + `setLoading` + `setError` + `setData` viết tay cho fetch — boilerplate lặp ở mọi màn (SM2), cache/dedupe/refetch không có. *Động tác*: move sang data layer repo đã có (react-query/SWR/fetch hook chung của feature) — component chỉ render 3 trạng thái. *Đừng khi*: fetch một lần duy nhất không cần cache và repo không có layer đó — thêm framework cho một call là SM17; tối thiểu trích `useFetch` feature-local (FM6).
- **FM12 Unstable dependency → stable** — *Tín hiệu*: object/array literal hoặc function inline trong deps của effect/memo con → effect chạy mỗi render, `React.memo` con mất tác dụng. *Động tác*: hoist ra ngoài component nếu tĩnh; `useMemo`/`useCallback` nếu phụ thuộc props/state; hoặc chuyển thành primitive dep. *Đừng khi*: bọc `useMemo` phòng mọi thứ — memo có giá và có chi phí đọc; chỉ khi referential equality thật sự quan trọng (dep của hook, props của memoized child, context value). Memo không chứng cứ = SM17 dạng perf.

## Nhóm 4 · Data & render

- **FM13 JSX lặp → typed record + map** — *Tín hiệu*: nhiều JSX call chỉ khác data (3 field cùng `<Field>` khác `name`/`label`) — chính là check typed-record của `rules/reuse-duplication.md`. *Động tác*: mô tả data một lần — `const fields = [...] as const`, render một lần qua `.map`. *Đừng khi*: hai call — chưa đủ hai consumers cho abstraction; hoặc mỗi call khác component/handler — ở ngoài list, giữ JSX tường minh.
- **FM14 Abort/cleanup cho effect async** — *Tín hiệu*: fetch/subscription trong effect không cleanup — unmount hoặc props đổi nhanh sinh race (`setState` sau unmount, response cũ đè response mới). *Động tác*: `AbortController` cho fetch, unsubscribe cho listener, hoặc `let cancelled = false` trong cleanup — mỗi effect async một chiếc ô thoát. *Đừng khi*: effect đồng bộ thuần — không có race để mà chống.
- **FM15 Code split theo route boundary** — *Tín hiệu*: màn nặng (editor, chart, admin) import thẳng vào bundle chung — user phổ thông trả giá tải phần không dùng. *Động tác*: `lazy()` + `Suspense` tại ranh giới route/feature; giữ boundary ở tầng cao nhất có thể. *Đừng khi*: split theo component nhỏ lẻ — mỗi boundary một waterfall; split ở trục route/feature lớn, không phải mọi component.

---

## Khi nào mở catalog này

| Tình huống | Dùng |
|---|---|
| Refactor UI (`playbooks/refactor-ui.md`) | FAIL của SM/F/O ở code FE mà cure Fowler không đủ — tra move tương ứng; check "đừng khi" trước khi đề xuất |
| Review diff có component/hook | Tín hiệu của move nào xuất hiện trong diff → gợi ý move kèm tên, không phải verdict |
| Viết finding | `tín hiệu → FM# → vì sao điều kiện áp đứng` |

## Giới hạn

- Catalog cho **move đặc thù FE** — move chung ngôn ngữ vẫn tra `patterns.md` và Fowler catalog.
- "Đừng khi" thắng "động tác" khi do dự — move chỉ đáng khi tín hiệu có thật hôm nay (SM17/O7/D3).
- Severity tối đa minor; project rule cho phép shape đó thì rule thắng.
- React-đặc-thù (FM4, FM6–FM8, FM12, FM15): Vue/Svelte có cơ chế tương đương nhưng tên khác — map theo khái niệm, không theo tên.
