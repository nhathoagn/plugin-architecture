# Code map

File map của plugin fe-kit. Mỗi node một trách nhiệm. Đọc từ trên xuống; nhánh = thư mục.

```text
plugin-architecture
├── .claude-plugin/
│   ├── plugin.json          manifest: tên fe-kit, version 1.15.0
│   └── marketplace.json     khai báo marketplace để /plugin install fe-kit@fe-kit
├── hooks/
│   └── hooks.json           5 event (UserPromptSubmit, PreToolUse, PostToolUse, SessionStart, PreCompact) → chạy fe-gate.sh
├── scripts/
│   ├── fe-gate.sh           tìm python3, chuyển stdin JSON sang fe-gate.py; thiếu python3 thì bỏ qua (fail open)
│   ├── fe-gate.py           lõi gate (~590 dòng): đọc transcript, chốt allow/deny, bơm rule theo intent
│   │   ├── gate_open()      :369  owner + reuse decision có đủ? bug edit thì có nhãn repro?
│   │   ├── conflict_edit()  :346  edit có conflict marker? → qua gate ngay
│   │   ├── run_repo_rules() :506  gọi <repo>/.claude/rules.sh nếu có, fail → exit 2
│   │   ├── deny path :394    in JSON permissionDecision=deny + exit 0 (PostToolUse mới dùng exit 2)
│   │   └── emit()           :527  in JSON additionalContext trả cho hook
│   └── test_fe_gate.py      94 test cho hành vi fe-gate.py
├── extensions/
│   ├── fe-gate.ts           omp extension (khai báo `omp.extensions` trong package.json): chặn edit thiếu nhãn qua tool_call, kiểm conflict/rules.sh sau ghi qua tool_result — gọi cùng scripts/fe-gate.sh
│   └── fe-gate.test.ts      8 case `node --test`, spawn gate thật
├── rules/                   nội dung bơm vào prompt (hook nạp, không phải agent tự đọc)
│   ├── fe-implementation.md quy trình edit: quyết định trước, code sau
│   ├── reuse-duplication.md tái sử dụng implementation có sẵn, cấm viết trùng
│   ├── modules.md           một việc một file; file dài không tự nhiên là lý do chia
│   ├── conflict-fix.md      cách xử lý conflict marker
│   └── review-diff.md       luật review diff, luôn áp trên omp
├── agents/
│   └── reviewer.md          agent review context mới, read-only, không khen
├── skills/
│   ├── fe-kit/
│   │   ├── SKILL.md         entry: chọn playbook theo loại việc (new-ui, fix-bug, refactor, perf, review)
│   │   ├── CHANGELOG.md     lịch sử version
│   │   ├── playbooks/       6 playbook: new-ui, fix-bug, refactor-ui, perf-ui, review-ui, review-diff — mỗi playbook gọi references/
│   │   ├── references/      chi tiết: ownership, reuse, performance, code-quality, audit, REVIEW_CHECKLIST, feature-isolation, external
│   │   └── evals/           evals.json + triggers.json + 2 report eval (e2e-gate, ut-review)
│   ├── ut-report/
│   │   ├── SKILL.md         xuất báo cáo UT 1 màn hình ra .xlsx
│   │   └── scripts/build_report.py  YAML case → xlsx (cần pyyaml, openpyxl)
│   └── ui-image-check/
│       └── SKILL.md         so sánh ảnh mockup với code, không sửa code
├── README.md                install (Claude Code + omp), layout, cách test hook
└── package.json             metadata: tên, version, license + `omp.extensions` khai báo extension cho omp
```

## Flow chính

```text
prompt vào ──► UserPromptSubmit ──► fe-gate.py: nhận diện intent → bơm rule tương ứng
ghi file ────► PreToolUse       ──► fe-gate.py: conflict_edit? → qua; gate_open? → thiếu nhãn thì DENY, agent phải điền
ghi xong ────► PostToolUse      ──► fe-gate.py: conflict marker còn? rules.sh fail? → exit 2
compact      ──► SessionStart / PreCompact ──► fe-gate.py: transcript còn frontend work? → bơm lại rule
```

Trên omp: `hooks/hooks.json` không chạy. `extensions/fe-gate.ts` bắt event `tool_call`/`tool_result`, dựng payload (session omp → JSONL shape fe-gate.py đọc), spawn `scripts/fe-gate.sh`, đổi kết quả thành `{block, reason}` hoặc lỗi trong tool result. Rule vẫn always-on qua discovery `rules/`.

## Intent → rule nào được nạp (fe-gate.py)

Cờ regex ở `:27-67`, khớp prompt tiếng Việt lẫn tiếng Anh:

| Cờ | Dòng | Kích hoạt khi prompt có |
|---|---|---|
| `prompt_hit` | :27 | frontend, react, vue, tsx, component, UI, giao diện |
| `conflict_hit` | :34 | conflict, xung đột, hợp nhất, trùng |
| `reuse_hit` | :42 | reuse, duplicat, dùng lại, tái sử, trùng lặp |
| `author_hit` | :49 | add, implement, viết, thêm, tách, sửa |
| `bug_hit` | :54 | bug, lỗi, sai khi, màn hình trắng, broken |
| `wording_hit` | :64 | typo, chính tả, đổi màu (để BỎ QUA rule reuse) |
| `review_hit` | :67 | review diff, trước commit, git diff |

Ma trận nạp ở `:573-588`:

| Event | Điều kiện | Nạp |
|---|---|---|
| UserPromptSubmit | `prompt_hit` hoặc `bug_hit` | `rules/fe-implementation.md` |
| | `(prompt\|reuse\|author\|bug)` và không phải wording-only | `rule_bundle()` = reuse-duplication + modules |
| | `prompt_hit` hoặc `review_hit` | `review_context()` = review-diff + đường dẫn playbook |
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
│   └── đọc playbooks/review-diff.md → đi REVIEW_CHECKLIST.md + F1..F22
└── omp: context mới, duy nhất nhiệm vụ = diff range + skill://fe-kit/playbooks/review-diff.md
    └── không mang ghi chú của tác giả
Báo cáo: Verdict đứng đầu, mỗi miss là 1 câu, xong rồi dừng.
```

## Verify — chạy gì để chắc map đúng

```text
python3 scripts/test_fe_gate.py          94 test hành vi gate (deny/allow, intent, conflict)
cat skills/fe-kit/evals/triggers.json    16 query mẫu: should_trigger true/false — kiểm intent regex
sh scripts/fe-gate.sh < event.json        chạy thật 1 event với payload giả
README.md § Test                         chứng minh host nạp plugin + hook có fire
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
| wording-only edit, transcript rỗng | allow — bypass `behaviorless_one_line()`, không cần nhãn |

2 lần FAIL trong lần chạy đầu là lỗi harness (fixture sai đường `splitext(main)[0]` → `session/main/subagents/`, và pattern check yêu cầu `permissionDecision` ở case allow) — chạy lại đều pass.

Ghi chú đường subagent: `session_dir = os.path.splitext(main)[0]` nên file nằm `<main-không-ext>/subagents/agent-<id>.jsonl`, không phải `<thư-mục-chứa-main>/subagents/`.

Transcript gate đọc là JSONL, mỗi dòng 1 entry gate nhận ra (thiếu cấu trúc này thì owner/decision/repro đều coi như không có):

```json
{"type": "user",      "message": {"content": [{"type": "text", "text": "Tổng sai khi có discount..."}]}}
{"type": "assistant", "message": {"content": [{"type": "text", "text": "Runtime owner: Checkout.tsx\nDecision: reuse\nTrigger: ...\nExpected: ...\nActual: ..."}]}}
```

Nhãn phải nằm SAU dòng request mới nhất trong transcript; assistant viết cùng dòng (value sau `:`), user có thể xuống dòng.

Không thuộc plugin (bỏ qua khi đọc map): `conversation-*.txt`, `trajectory-*.json`, `Tai_lieu_*.md`, `.openidea/`, `.omp/`.
