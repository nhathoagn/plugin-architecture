# REVIEW_CHECKLIST.md

Checklist review cho AI subagent. Language-agnostic. Mỗi mục chỉ trả lời **PASS** / **FAIL** / **N/A**.

File này nằm trong skill. Reviewer đi từng mục ở đây. Không thay file này bằng link ra repo ngoài.

Nguồn đã tổng hợp vào các mục bên dưới: Google eng-practices, Anthropic code-review + pr-review-toolkit, obra/superpowers requesting-code-review, awesome-skills/code-review-skill, VoltAgent code-reviewer, OWASP Top 10 / Code Review Guide.

---

## Hướng dẫn cho reviewer

1. Chạy trong **context mới**. Không dùng lịch sử phiên vừa viết code.
2. Chỉ đọc **`git diff`** và file cần để hiểu hunk. Không sửa code.
3. Đi từng mục trong đầu. Báo cáo người đọc không ghi mã, không ghi PASS, FAIL, hay N/A. Chỉ viết câu cho chỗ sai, kèm `file:dòng`.
4. Mỗi `FAIL` bắt buộc có **bằng chứng** `path:line` (hoặc hunk diff), mô tả sai gì, vì sao quan trọng, cách sửa gợi ý 1 dòng.
5. **Không khen.** Không tóm tắt thay đổi thay cho findings. Không nói "looks good" khi chưa check hết.
6. Severity:
   - **blocker** — bug, mất data, lỗ hổng bảo mật, phá API/contract, test đỏ / flaky mới
   - **major** — thiếu error handling, thiếu test cho logic mới, lệch kiến trúc repo, race/perf rõ
   - **minor** — naming, comment, docs nhỏ, nit không chặn merge
7. Kết luận dùng chữ trong `playbooks/review-diff.md`, không dùng `SHIP`, `SHIP_WITH_FIXES`, hay `NO_SHIP`. Có **blocker** → "Không đưa lên". Chỉ **major** → "Sửa rồi hãy đưa". Chỉ **minor** → "Đưa được".

---

## Output

Bản người đọc là `references/review-output.md`. Không đưa mã checklist vào báo cáo đó.

---

## 1. Scope & diff hygiene

- [ ] **S1** Test diff có khớp file yêu cầu mà playbook đã tìm không. Không có file thì khớp goal đã nêu. FAIL nếu thêm việc nguồn đó không yêu cầu. Không có cả hai thì N/A.
- [ ] **S2** Test diff có trộn format hoặc rename lớn với logic không. FAIL nếu trộn mà chưa tách. Không có diff thì N/A.
- [ ] **S3** Test file generated, lockfile, artifact vô tình. FAIL nếu có mà không cần. Không có diff thì N/A.
- [ ] **S4** Test debug leftover trong diff. FAIL nếu có commented-out code, `console.log`, hoặc `debugger`. Không có diff thì N/A.
- [ ] **S5** Test secret trong diff. FAIL nếu có token, private key, hoặc `.env` thật. Không có diff thì N/A.
- [ ] **S6** Test diff lớn đã được chia chưa. FAIL nếu logic mới hơn khoảng 400 dòng mà chưa chia và chưa ghi đã review từng phần. Nhỏ hơn thì PASS.
- [ ] **C1** Test hành vi có đúng file yêu cầu đó, hoặc goal đã nêu, không. FAIL nếu kết quả chạy sai nguồn đó, hoặc một yêu cầu trong nguồn đó bị thiếu hay làm dở. Không có cả hai thì N/A. Không lấy goal của fixture đem chấm như UI sản phẩm.
- [ ] **C2** Test null, rỗng, field thiếu ở biên. FAIL nếu biên đó có trong diff mà bị bỏ. Không có field đó thì N/A.
- [ ] **C3** Test biên 0, 1, max, off-by-one, overflow. FAIL nếu diff có số hoặc thời gian mà sai biên. Không có biên số thì N/A.
- [ ] **C4** Test nhánh lỗi và happy path. FAIL nếu lỗi bị nuốt hoặc ra kết quả sai im lặng. Không có đường lỗi thì N/A.
- [ ] **C5** Test await và promise. FAIL nếu fire-and-forget không xử lý. Không có async thì N/A.
- [ ] **C6** Test race, double-submit, TOCTOU. FAIL nếu có shared state mà không xử lý. Không có shared state thì N/A.
- [ ] **C7** Test retry có ghi trùng không. FAIL nếu retry không idempotent. Không có retry, job, webhook thì N/A.
- [ ] **C8** Test invariant của module. FAIL nếu caller gần diff bị gãy. Không có caller thì N/A.
- [ ] **D1** Test file mới có đúng layer không. FAIL nếu đặt sai thư mục theo convention repo. Repo không có convention thì N/A.
- [ ] **D2** Test có dùng helper sẵn không. FAIL nếu viết song song thứ đã có. Không có helper cho việc đó thì N/A.
- [ ] **D3** Test abstraction chưa cần. FAIL nếu thêm lớp cho tương lai. Không thêm thì PASS.
- [ ] **D4** Test coupling và vòng phụ thuộc. FAIL nếu tạo cycle hoặc god-module. Không có quan hệ mới thì PASS.
- [ ] **D5** Test export thừa. FAIL nếu export thứ chỉ dùng nội bộ khi repo vốn kín. Repo không cấm thì N/A.
- [ ] **D6** Test flag có theo pattern repo không. FAIL nếu repo đang dùng flag mà diff bỏ pattern. Repo không dùng flag thì N/A.
- [ ] **D7** Test caller cũ còn chạy không. FAIL nếu đổi UI hoặc API mà caller gãy, không có migration. Không có caller thì N/A.
- [ ] **D8** Test chỗ giữ thứ hai. FAIL nếu thêm state, prop, hoặc biến cho giá trị đã có chỗ giữ, hoặc không nêu chỗ đã kiểm và literal hay behavior đã search. Rule là `rules/reuse-duplication.md`. Không thêm thì PASS. Không phải diff thì N/A.
- [ ] **D9** Test việc thứ hai trong một file. FAIL nếu diff thêm logic có trách nhiệm riêng vào file đã có việc khác, hoặc file ngoài thư mục import file bên trong không phải file entry, hoặc tách file chỉ vì dài, hoặc tách file trong lúc sửa bug. Rule là `rules/modules.md`. Không có file mới và không thêm việc thì PASS. Không phải diff thì N/A.
- [ ] **N1** Test tên trong diff. FAIL nếu tên không nói việc nó giữ. Không có tên mới thì N/A.
- [ ] **N2** Test hàm có làm một việc không. FAIL nếu nesting sâu hơn 4 mà không giải thích được. Một việc thì PASS.
- [ ] **N3** Test magic number hoặc magic string. FAIL nếu giá trị cứng lẽ ra là hằng. UI copy không tính. Secret tính ở S5.
- [ ] **N4** Test comment. FAIL nếu comment nhắc lại what, hoặc comment cũ sai sau diff. Không có comment thì PASS.
- [ ] **N5** Test block viết hai lần. FAIL nếu hai block gộp được mà không mất nghĩa. Không có bản sao thì PASS.
- [ ] **E1** Test nuốt lỗi. FAIL nếu empty `catch`, hoặc thất bại mà thoát như thành công. Không có đường lỗi thì N/A.
- [ ] **E2** Test lỗi có giữ context không. FAIL nếu map sai tầng hoặc mất stack cần thiết. Không có lỗi được ném thì N/A.
- [ ] **E3** Test fallback có che bug không. FAIL nếu fallback giấu lỗi. Không có fallback thì N/A.
- [ ] **E4** Test giới hạn I/O ngoài. FAIL nếu không có timeout, retry cap, hoặc cancel. Không có I/O ngoài thì N/A.
- [ ] **E5** Test lỗi user thấy. FAIL nếu message lộ stack, path, hoặc secret. Không có message lỗi thì N/A.
- [ ] **E6** Test cleanup. FAIL nếu file, connection, listener, hoặc lock sót ở một nhánh thoát. Không có resource thì N/A.
- [ ] **SEC1** Test credential hardcode. FAIL nếu có API key, token, hoặc password trong diff. Không có thì PASS.
- [ ] **SEC2** Test input từ user hoặc ngoài. FAIL nếu boundary không validate. Input trong UI là boundary. Không có input đó thì N/A.
- [ ] **SEC3** Test injection. FAIL nếu SQL, command, template, hoặc path ghép từ input. Không ghép thì N/A.
- [ ] **SEC4** Test XSS. FAIL nếu HTML hoặc DOM không encode. Không có output HTML thì N/A.
- [ ] **SEC5** Test auth trên action mới. FAIL nếu endpoint hoặc action mới thiếu AuthN hoặc AuthZ. Không có action đó thì N/A.
- [ ] **SEC6** Test ownership theo id. FAIL nếu lấy resource theo id mà không check chủ. Không có id resource thì N/A.
- [ ] **SEC7** Test dữ liệu nhạy trong log hoặc client bundle. FAIL nếu secret không cần mà vẫn lộ. Không có dữ liệu nhạy thì PASS.
- [ ] **SEC8** Test cookie và chỗ lưu token. FAIL nếu sai httpOnly, secure, hoặc dùng localStorage khi repo cấm. Không có cookie hoặc token storage thì N/A.
- [ ] **SEC9** Test dependency mới. FAIL nếu package mới không có lý do hoặc quyền quá rộng. Không thêm package thì N/A.
- [ ] **SEC10** Test CORS, CSRF, SSRF. FAIL nếu diff chạm network mà bỏ qua. Không chạm network thì N/A.
- [ ] **P1** Test N+1. FAIL nếu query hoặc mạng nằm trong loop. Không có loop gọi mạng thì N/A.
- [ ] **P2** Test độ phức tạp trên hot path. FAIL nếu O(n²) vô cớ với input lớn. Không có hot path thì N/A.
- [ ] **P3** Test list lớn. FAIL nếu list không có limit khi cần. Không có list thì N/A.
- [ ] **P4** Test file lớn trong memory. FAIL nếu đọc cả blob khi có stream. Không có blob thì N/A.
- [ ] **P5** Test cache. FAIL nếu sai key hoặc không xóa cache khi data đổi. Không có cache thì N/A.
- [ ] **P6** Test work nặng có block UI không. FAIL nếu chạy trên event loop hoặc UI thread. Không có work nặng thì N/A.
- [ ] **P7** Test leak listener, timer, subscription. FAIL nếu không gỡ. Không có thì N/A.
- [ ] **T1** Test logic mới có test không. FAIL nếu đổi hành vi mà không có test. Không đổi hành vi thì N/A.
- [ ] **T2** Test error path của test đã có. FAIL nếu test chỉ có happy path. Chưa có test thì N/A.
- [ ] **T3** Test assertion có kiểm tra hành vi không. FAIL nếu chỉ assert mock được gọi. Không có test thì N/A.
- [ ] **T4** Test có deterministic không. FAIL nếu phụ thuộc thứ tự, giờ thật, hoặc mạng. Không có test thì N/A.
- [ ] **T5** Test selector Playwright. FAIL nếu dùng CSS hoặc xpath dễ gãy. Không có E2E thì N/A.
- [ ] **T6** Test chờ Playwright. FAIL nếu `waitForTimeout` cố định. Không có E2E thì N/A.
- [ ] **T7** Test isolation Playwright. FAIL nếu dùng chung state bẩn. Không có E2E thì N/A.
- [ ] **T8** Test flaky UI. FAIL nếu race hoặc animation không được xử lý. Không có UI test thì N/A.
- [ ] **T9** Test có đỏ khi behavior hỏng không. FAIL nếu test vẫn xanh khi code hỏng. Không có test thì N/A.
- [ ] **T10** Test bị xóa hoặc skip. FAIL nếu xóa hoặc skip để cho xanh, không có lý do. Không xóa test thì PASS.
- [ ] **TY1** Test type có giữ invariant không. FAIL nếu `any` hoặc cast rộng khi repo cấm. Không có type trong diff thì N/A.
- [ ] **TY2** Test schema khớp implementation. FAIL nếu DTO hoặc Zod lệch code. Không có schema thì N/A.
- [ ] **TY3** Test breaking change. FAIL nếu gãy caller mà không có version hoặc migration. Không gãy contract thì N/A.
- [ ] **TY4** Test nullability giữa client, server, DB. FAIL nếu lệch. Không có field đó thì N/A.
- [ ] **TY5** Test enum hoặc error code mới. FAIL nếu consumer trong diff chưa cập nhật. Không có mã mới thì N/A.
- [ ] **TY6** Test check validate mới. FAIL nếu check viết tay lặp lại rule mà schema hoặc validator sẵn có đã giữ, hoặc coi field thiếu là hợp lệ khi field bắt buộc. Không đòi schema cho check trên field đã có type. Không có check mới thì N/A.
- [ ] **TY7** Test case mà message cấm. FAIL nếu check cho qua case đó, kể cả `""`, `undefined`, `null`, space đầu, hoặc space cuối. Không bắt thư viện. Không có check mới thì N/A.
- [ ] **TY8** Test helper validate mới. FAIL nếu thêm hàm tự filter, map, hoặc bọc `safeParse`, `trim`, hoặc `startsWith` trong khi repo đã có schema, resolver, hoặc field rule. Gọi tool đó. Không có tool sẵn thì N/A.
- [ ] **TY9** Test helper `(values[field] ?? '')` rồi check. FAIL nếu `""`, `undefined`, hoặc `null` không ra lỗi. Không cần schema sẵn. Không cần message nói tới trống. Không có kiểu helper đó thì N/A.
- [ ] **R1** Test refactor có giữ behavior không. FAIL nếu đổi output mà plan không nói. Không phải refactor thì N/A.
- [ ] **R2** Test import sau move. FAIL nếu path gãy. Không move thì N/A.
- [ ] **R3** Test caller cũ sau move. FAIL nếu chưa migrate và không có shim có hạn. Không có caller cũ thì N/A.
- [ ] **R4** Test dead code sau move. FAIL nếu file hoặc export thừa còn. Không move thì N/A.
- [ ] **R5** Test rename. FAIL nếu tên cũ còn ngoài chỗ cố ý giữ. Không rename thì N/A.
- [ ] **R6** Test registry. FAIL nếu route, DI, hoặc plugin registry trỏ module cũ. Không có registry thì N/A.
- [ ] **R7** Test path trong test và fixture. FAIL nếu vẫn trỏ path cũ. Không move thì N/A.
- [ ] **R8** Test pure move có đổi logic không. FAIL nếu sửa behavior trong lúc rename. Không phải move thì N/A.
- [ ] **DOC1** Test docs cách chạy. FAIL nếu đổi build, test, hoặc deploy mà README không cập nhật. Không đổi cách chạy thì N/A.
- [ ] **DOC2** Test ghi chú public API. FAIL nếu breaking mà không có ADR hoặc changelog. Không có quyết định đó thì N/A.
- [ ] **DOC3** Test commit message. FAIL nếu không nói why hoặc lệch diff. Không có commit thì N/A.
- [ ] **DOC4** Test TODO. FAIL nếu TODO mới không có owner, hoặc TODO đã xong còn đó. Không có TODO thì PASS.
- [ ] **DOC5** Test comment cũ. FAIL nếu comment sai sau refactor. Không có comment thì PASS.

---

## Lỗi riêng của repo (thêm từ feedback reviewer)

Bảng dưới đây trong file skill này để trống. Reviewer không đi hàng trống. Hàng đã điền nằm ở `REVIEW_CHECKLIST.md` tại root repo đang review, nếu file đó có.

| ID | Rule (viết dạng có/không) | Ví dụ sai | Ví dụ đúng | Severity |
|----|---------------------------|-----------|------------|----------|
| L1 | | | | |
| L2 | | | | |
| L3 | | | | |
