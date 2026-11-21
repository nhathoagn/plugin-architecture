# Code map

File map của plugin fe-kit. Mỗi node một trách nhiệm. Đọc từ trên xuống; nhánh = thư mục.

```text
plugin-architecture
├── .claude-plugin/
│   ├── plugin.json          manifest: tên fe-kit, version 1.15.0
│   └── marketplace.json     khai báo marketplace để /plugin install fe-kit@fe-kit
├── hooks/
│   └── hooks.json           5 event (UserPromptSubmit, PreToolUse, PostToolUse, SessionStart, PreCompact) → chạy fe-gate.sh; PreToolUse bắt Write|Edit|MultiEdit|Bash
├── scripts/
│   ├── fe-gate.sh           tìm python3, chuyển stdin JSON sang fe-gate.py; thiếu python3 thì bỏ qua (fail open)
│   ├── fe-gate.py           lõi gate: đọc transcript, chốt allow/deny, bơm rule theo intent
│   │   ├── wording_exempt() :369  Edit/MultiEdit đi qua khi token diff chỉ đổi copy/style/comment
│   │   ├── gate_open()      :405  owner + reuse decision có đủ? bug edit thì có nhãn repro?
│   │   ├── conflict_edit()  :313  edit có conflict marker? → qua gate ngay
│   │   ├── run_repo_rules() :544  gọi <repo>/.claude/rules.sh nếu có, fail → exit 2
│   │   ├── deny path :435    in JSON permissionDecision=deny + exit 0 (PostToolUse mới dùng exit 2)
│   │   └── emit()           :565  in JSON additionalContext trả cho hook
│   ├── label_store.py       nhãn khai báo bằng một lệnh `echo`/`printf`: đọc từ Bash payload, lưu theo session_id (hoặc transcript) + agent + request
│   ├── bash_target.py       Bash command → file frontend nó ghi (redirect, tee, cp/mv, sed/perl -i, script writeFileSync/write_text, đọc cả file script, theo cd); thư mục tmp/temp/scratchpad được bỏ qua
│   ├── wording.py           lexer JS/TS/JSX + token diff: JSX text, text attr, copy call/property, style, comment = wording
│   ├── project_config.py    file thay đổi → luật dự án cần đọc: .fe-kit/config.yaml (rules, always_read, presets, spec_dirs, gate, exclude, legacy) hoặc tự tìm AGENTS.md/CLAUDE.md/rules/ từ root tới thư mục của file
│   ├── yaml_subset.py       đọc tập con YAML bằng thư viện chuẩn; cú pháp ngoài tập con → YamlError kèm số dòng
│   ├── review_check.py      kiểm report review-diff: verdict, mức lỗi, file:dòng có thật, mục Nguồn và độ phủ
│   ├── review_packages.py   split: diff trên 10 file → gói tối đa 15 file, mỗi gói một reviewer; merge: gộp report các gói (verdict nặng nhất, cộng số lỗi)
│   ├── review_record.py     save: lưu report + sha vào .fe-kit/reviews/<branch>.md; last: in sha và lỗi cũ cho lần review sau
│   ├── test_wording.py      78 test lexer/token diff
│   ├── test_fe_gate.py      191 test cho hành vi fe-gate.py
│   ├── test_yaml_subset.py  52 test, so với pyyaml khi máy có
│   ├── test_project_config.py  53 test glob, fallback, config, lỗi, preset, git, thư mục con, tên non-ASCII
│   ├── test_review_check.py 25 test report
│   ├── test_review_packages.py 19 test split/merge
│   ├── test_review_record.py 15 test save/last
│   ├── test_rule_copies.py  một câu luật chỉ nằm ở một file (rules/ → skill, SKILL.md → playbook)
│   └── test_versions.py     plugin.json = package.json = marketplace.json = CHANGELOG
├── extensions/
│   ├── fe-gate.ts           omp extension (khai báo `omp.extensions` trong package.json): map edit/ast_edit/write/bash sang payload gate (nhận old_string, oldText, oldString, old_str, old, search; edits[]), chặn edit thiếu nhãn qua tool_call, kiểm conflict/rules.sh sau ghi qua tool_result — gọi cùng scripts/fe-gate.sh; ghi verdict cuối (ok/blocked/note/rules) lên status line
│   └── fe-gate.test.ts      29 case `node --test`, spawn gate thật (Windows: qua `sh`, đường dẫn dấu /)
├── rules/                   nội dung bơm vào prompt (hook nạp, không phải agent tự đọc)
│   ├── fe-implementation.md quy trình edit: quyết định trước, code sau
│   ├── reuse-duplication.md tái sử dụng implementation có sẵn, cấm viết trùng
│   ├── modules.md           một việc một file; file dài không tự nhiên là lý do chia
│   ├── comments.md          xóa comment thừa/workaround/suppression che lỗi; chỉ giữ ngoại lệ có bằng chứng; encode ràng buộc thay vì văn xuôi
│   ├── conflict-fix.md      cách xử lý conflict marker
│   └── review-diff.md       luật review diff, luôn áp trên omp
├── presets/
│   └── legacy-rewrite/      design.md (câu hỏi trước khi code), review.md (giống hệ cũ, không CR → không phải lỗi)
├── agents/
│   └── reviewer.md          agent review context mới, read-only, không khen
├── skills/
│   ├── fe-kit/
│   │   ├── SKILL.md         entry: chọn playbook theo loại việc (new-ui, fix-bug, refactor, perf, review)
│   │   ├── CHANGELOG.md     lịch sử version
│   │   ├── playbooks/       6 playbook: new-ui, fix-bug, refactor-ui, perf-ui, review-ui, review-diff — mỗi playbook gọi references/
│   │   ├── references/      chi tiết: ownership, reuse, performance, code-quality, audit, REVIEW_CHECKLIST, feature-isolation, external
│   │   └── evals/           evals.json + triggers.json + 3 report eval (e2e-gate, ut-review, ut-nested-if)
│   ├── ut-report/
│   │   ├── SKILL.md         xuất báo cáo UT 1 màn hình ra .xlsx
│   │   └── scripts/build_report.py  YAML case → xlsx (cần pyyaml, openpyxl)
│   └── ui-image-check/
│       └── SKILL.md         so sánh ảnh mockup với code, không sửa code
├── README.md                cho người dùng: tính năng, review, cài, yêu cầu, cấu trúc
└── package.json             metadata: tên, version, license + `omp.extensions` khai báo extension cho omp
```

## Flow chính

```text
prompt vào ──► UserPromptSubmit ──► fe-gate.py: nhận diện intent → bơm rule tương ứng
ghi file ────► PreToolUse       ──► fe-gate.py: conflict_edit? → qua; gate_open? → thiếu nhãn thì DENY, mở đầu bằng lệnh `echo` mẫu; agent chạy lệnh đó; có session id thì nhãn trong reply text không được tính (Bash ghi file frontend cũng bị gate như Write)
ghi xong ────► PostToolUse      ──► fe-gate.py: conflict marker còn? rules.sh fail? → exit 2
compact      ──► SessionStart / PreCompact ──► fe-gate.py: transcript còn frontend work? → bơm lại rule
```

Trên omp: `hooks/hooks.json` không chạy. `extensions/fe-gate.ts` bắt event `tool_call`/`tool_result`, dựng payload (session omp → JSONL shape fe-gate.py đọc), spawn `scripts/fe-gate.sh`, đổi kết quả thành `{block, reason}` hoặc lỗi trong tool result. Rule vẫn always-on qua discovery `rules/`.

## Intent → rule nào được nạp (fe-gate.py)

Cờ regex ở đầu file, khớp prompt tiếng Việt lẫn tiếng Anh:

| Cờ | Dòng | Kích hoạt khi prompt có |
|---|---|---|
| `prompt_hit` | :35 | frontend, react, vue, tsx, component, UI, giao diện |
| `conflict_hit` | :40 | conflict, xung đột, hợp nhất, trùng |
| `reuse_hit` | :45 | reuse, duplicat, dùng lại, tái sử, trùng lặp |
| `author_hit` | :50 | add, implement, viết, thêm, tách, sửa |
| `bug_hit` | :90 | `bug_signal()`: bug, lỗi, sai khi, màn hình trắng, broken — trừ wording/meta |
| `wording_hit` | :59 | typo, chính tả, đổi màu, text, copy, label (bỏ rule reuse và bug mode) |
| `review_hit` | :91 | review diff, trước commit, git diff |

Ma trận nạp ở `:611`:

| Event | Điều kiện | Nạp |
|---|---|---|
| UserPromptSubmit | `prompt_hit` hoặc `bug_hit` | `rules/fe-implementation.md` |
| | `(prompt\|reuse\|author\|bug)` và không phải wording-only | `rule_bundle()` = reuse-duplication + modules + comments |
| | `prompt_hit` hoặc `review_hit` | `review_context()` = review-diff + đường dẫn playbook + `Project rules command:` (lệnh `project_config.py --mode review`) |
| | `prompt_hit` hoặc `bug_hit`, repo có `.fe-kit/config.yaml` | `project_config_context()` = lệnh `project_config.py --mode author` |
| | `conflict_hit` hoặc repo đang conflict | `rules/conflict-fix.md` |
| PreToolUse | file `.tsx/.jsx/.vue/.svelte` | `rules/fe-implementation.md` |
| | file source (ts, py, go…) | `rule_bundle()` |
| | file/repo còn marker conflict | `rules/conflict-fix.md` |
| PostToolUse | marker còn trong file | stderr + exit 2, chặn phiên |
| | `<repo>/.claude/rules.sh` fail | stderr + exit 2 |
| | sửa file frontend trong bug flow | lệnh bắt viết UT fail-on-Actual trước khi hand reviewer (`:562`) |
| SessionStart(compact) | transcript có frontend | nạp lại fe-implementation + bundle + review_context (`:569`) |
| PreCompact | transcript có frontend | dặn summary giữ rule, không đổi (`:544`) |

Gate deny (thiếu `Runtime owner` / `Reuse Decision` nhãn) nằm ở PreToolUse, không ở bảng này — xem `gate_open()` `:369`.

## Skill flow — từ prompt đến output

```text
skill://fe-kit  (SKILL.md)
├── chọn 1 playbook (bảng tại SKILL.md, không đọc playbook khác)
│   ├── new-ui.md       component/page/form/hook mới
│   ├── fix-bug.md      hành vi sai / symptom
│   ├── refactor-ui.md  split, move, restructure
│   ├── perf-ui.md      waterfall, bundle, rerender
│   ├── review-ui.md    soi 1 màn hình có sẵn → báo cáo tiếng Việt
│   └── review-diff.md  diff trước commit — TÁC GIẢ KHÔNG ĐẠO CÁI NÀY
├── playbook gọi reference cụ thể (không đọc file playbook không nêu)
│   ├── ownership.md          → field Architecture Ownership
│   ├── reuse.md              → field Reuse Decision (reuse|extend|feature-local|shared)
│   ├── performance.md        → field Performance (waterfalls → bundle → fetch → rerender → states)
│   ├── code-quality.md       → bảng sweep, mỗi heading 1 dòng, dòng trống = chưa xong
│   ├── audit.md              → bảng Audit, mỗi lens 1 dòng, có file:line + severity
│   └── feature-isolation.md  → chỉ khi thêm behavior mới vào UI cũ, mặc định n/a
├── Verify (SKILL.md mục 7): trace callers, chất vấn trùng lặp, loading/error/empty, keys ổn định
└── Output Template: Architecture / Reuse / Performance / Code Quality / Audit / Feature Isolation
    → điền đủ mọi mục trước khi ghi code (mục 1-2 bắt buộc trước khi viết dòng đầu tiên)
```

## Reviewer flow — ai chấm diff

```text
tác giả viết diff ──KHÔNG được chấm──► bàn giao
├── Claude Code: agent fe-kit:reviewer (agents/reviewer.md)
│   ├── read-only: Read, Grep, Glob, Bash — không sửa, không commit, không spawn reviewer khác
│   ├── task PHẢI kèm playbook path, thiếu → dừng, không tự bịa checklist
│   └── đọc playbooks/review-diff.md → chạy project_config.py → đi REVIEW_CHECKLIST.md + F1..F23 + luật dự án → grep caller → lọc lại → review_check.py
└── omp: context mới, duy nhất nhiệm vụ = diff range + skill://fe-kit/playbooks/review-diff.md
    └── không mang ghi chú của tác giả
Báo cáo: Verdict đứng đầu, mỗi miss là 1 câu, xong rồi dừng.
```

## Verify — chạy gì để chắc map đúng

```text
python3 scripts/test_wording.py          78 test lexer/token diff (copy vs code)
python3 scripts/test_fe_gate.py          191 test hành vi gate (deny/allow, intent, conflict, file type, Bash ghi file, nhãn khai báo, dòng project rules)
python3 scripts/test_yaml_subset.py      52 test tập con YAML
python3 scripts/test_project_config.py   53 test luật dự án
python3 scripts/test_review_check.py     25 test kiểm report
python3 scripts/test_review_packages.py  19 test chia gói, gộp report
python3 scripts/test_review_record.py    15 test lưu, đọc review cũ
python3 scripts/test_rule_copies.py      không câu luật nào bị chép sang file khác
python3 scripts/test_versions.py         version giống nhau ở mọi manifest + CHANGELOG
node --test extensions/fe-gate.test.ts   29 test extension omp: verdict, prompt, chặn edit, wording
cat skills/fe-kit/evals/triggers.json    16 query mẫu: should_trigger true/false — kiểm intent regex
sh scripts/fe-gate.sh < event.json        chạy thật 1 event với payload giả
claude --debug -p "review the diff"      rồi grep "Loading hooks from plugin: fe-kit" ~/.claude/debug/latest
```

Đã chạy thật với payload giả (2026-11-15, fixture `/tmp/fe-gate-fixture/`):

| Payload | Kết quả |
|---|---|
| prompt frontend | inject `additionalContext`, exit 0 |
| prompt wording-only (`đổi màu nút`) | rỗng, exit 0 |
| edit `.tsx`, không transcript | deny JSON, exit 0 |
| bug + owner/decision, thiếu repro | deny + nêu `Trigger/Expected/Actual` thiếu, exit 0 |
| bug + owner/decision + đủ repro | allow + inject rule, exit 0 |
| PostToolUse + bug | sinh lệnh viết UT fail-on-Actual, exit 0 |
| SessionStart(compact) + transcript frontend | nạp lại fe-implementation + bundle + review_context |
| PreCompact + transcript frontend | in "Keep these rules in the summary" |
| PostToolUse file còn conflict marker | stderr "Conflict markers remain", exit 2 |
| PostToolUse `<repo>/.claude/rules.sh` exit 1 | stderr "VI PHẠM RULE", exit 2 |
| prompt `review diff trước commit` | inject `review_context` (rule + playbook path) |
| prompt `xung đột merge` | inject `conflict-fix.md` |
| decision nằm ở transcript subagent (`agent_id`) | allow nhờ nhánh `subagent_transcript()` |
| wording-only edit, transcript rỗng | allow — token diff `scripts/wording.py`, không cần nhãn |
| edit `fetch('/api/v1')` → `v2`, transcript rỗng | deny — string code, không phải copy |
| edit `.js` wording / `.js` behavior | allow / deny — `.js` đã vào gate |
| edit `.vue/.svelte/.astro/.mdx` wording | deny — phase 1 chưa có exemption |

2 lần FAIL trong lần chạy đầu là lỗi harness (fixture sai đường `splitext(main)[0]` → `session/main/subagents/`, và pattern check yêu cầu `permissionDecision` ở case allow) — chạy lại đều pass.

Ghi chú đường subagent: `session_dir = os.path.splitext(main)[0]` nên file nằm `<main-không-ext>/subagents/agent-<id>.jsonl`, không phải `<thư-mục-chứa-main>/subagents/`.

Transcript gate đọc là JSONL, mỗi dòng 1 entry gate nhận ra (thiếu cấu trúc này thì owner/decision/repro đều coi như không có):

```json
{"type": "user",      "message": {"content": [{"type": "text", "text": "Tổng sai khi có discount..."}]}}
{"type": "assistant", "message": {"content": [{"type": "text", "text": "Runtime owner: Checkout.tsx\nDecision: reuse\nTrigger: ...\nExpected: ...\nActual: ..."}]}}
```

Nhãn phải nằm SAU dòng request mới nhất trong transcript; assistant viết cùng dòng (value sau `:`), user có thể xuống dòng.

Không thuộc plugin (bỏ qua khi đọc map): `conversation-*.txt`, `trajectory-*.json`, `Tai_lieu_*.md`, `.openidea/`, `.omp/`.
