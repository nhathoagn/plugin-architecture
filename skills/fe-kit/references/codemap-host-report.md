# Codemap host report

This note records the host APIs codemap uses, which checks ran in a host, and the limits. The source is `/Users/nhathoang/Documents/codemap`. It is not part of the fe-kit workflow. Do not read it before a frontend edit.

## APIs

omp 18.18.0. The extension default-exports a function of `ExtensionAPI` from `@oh-my-pi/pi-coding-agent`. The published types in the local 18.14 cache match the calls below. The extension does not import that package, because a typecheck without the package installed fails. The local type covers the same calls.

- `pi.registerCommand("cm-scan" | "cm-impact" | "cm-context" | "cm-review" | "cm-fix" | "cm-flow")`. The handler receives the argument string and `ctx.ui.notify`.
- `pi.registerTool` for `cm_scan`, `cm_impact`, `cm_context`, `cm_review`, `cm_fix`, `cm_flow`. Parameters use `pi.zod`. `execute` returns `{ content: [{ type: "text", text }], details: {} }`.
- `package.json` field `omp.extensions` points at `./src/index.ts`.
- MCP merge writes `~/.omp/agent/mcp.json` only when that file already exists and `mcpServers["codebase-memory-mcp"].command` is absent. The shape is `{ command, args, type: "stdio" }`.

Claude Code. Checked against the plugin manifest reference and `claude plugin validate`.

- `.claude-plugin/plugin.json` name `codemap`.
- `.claude-plugin/marketplace.json` at the repo root, source `./packages/claude-code`, and a copy inside the plugin directory.
- `commands/cm-*.md` with `description`, `argument-hint`, and `$ARGUMENTS`.
- `.mcp.json` registers `codebase-memory-mcp` as a stdio server.
- `skills/codemap/SKILL.md`.
- `hooks/hooks.json` `PreToolUse` and `PostToolUse` on `Edit|Write`, `timeout` 2. The script reads stdin JSON and may print `hookSpecificOutput.additionalContext`. It never sets `permissionDecision`.

codebase-memory-mcp 0.12.1. Core calls `cli <tool> --format json`. Tools used: `index_repository`, `index_status`, `list_projects`, `trace_path`, `search_graph`, `get_code_snippet`, `get_file_outline`, `detect_changes`. Watcher toggle is `config set auto_watch true`, not an MCP tool.

## Checks

| Check | Where | Result |
|---|---|---|
| `node --test` pure and outline tests | test runner only | pass, 7 tests |
| integration on `ecommerce-cho-viet` (`/Users/nhathoang/Documents/ecommerce-marketplace`) | CLI, not inside omp or Claude | pass. `validCoupon` impact includes `OrdersService.checkout` and `orders.controller.ts`. Context on `OrdersService.checkout` includes that controller. Staged review of a line inside `validCoupon` maps to `validCoupon`. The edit was reverted. |
| core CLI vs `packages/claude-code/bin/codemap.mjs` impact JSON | both spawn the same CLI | byte match |
| `claude plugin validate --strict` on the repo marketplace and on `plugin.json` | Claude CLI, not a session | pass |
| hook script with empty or slow input | script only | exit 0, no block |
| omp session load | host | did not run. Print mode exited with no xai-oauth API key. |
| Claude `/help`, `/mcp`, hook fire | host | did not run. Print mode exited with an expired OAuth session. |

## Session note


An omp print session with `--extension packages/omp/src/index.ts` and `/cm-impact validCoupon` did not run the command. The process logged `No API key found for xai-oauth` and exited. A Claude print session with `--plugin-dir packages/claude-code` failed with `OAuth session expired`. Those two host checks did not run.

What did run on the host CLIs: `claude plugin validate --strict` passed for the marketplace and for `plugin.json`. A Node load of the omp factory registered `cm-scan`, `cm-impact`, `cm-context`, `cm-review`, `cm-fix`, `cm-flow` and the six `cm_*` tools. That load is not an omp session.
## Limits

- `detect_changes` and a staged outline can name the containing class. The text says possibly affected.
- Understand Anything is not reimplemented. `/cm-flow` prints the missing install and the missing model host when neither Claude's plugin nor `~/.understand-anything/repo` is present. Static extraction skips `.vue`.
- Decorator and test filtering uses the label, an `@` name, and `.spec` or `.test` in the path or qualified name. A decorator recorded as a normal call can remain.
- Hooks fail open. A warm `trace_path` often takes longer than 2 seconds, so the hook exits with no summary instead of blocking the edit.
- Binary install checks sha256 against the release `checksums.txt` before extract. That path was not executed here because the binary was already on `PATH`.
- Scan does not create a new `.mcp.json` in the repo. It only merges an existing one, and it only appends `.git/info/exclude`.

## Báo cáo ngắn

omp dùng `registerCommand`, `registerTool`, và `omp.extensions`. Claude dùng `plugin.json`, `commands/cm-*.md`, `.mcp.json`, skill, và hook `PreToolUse`/`PostToolUse`. Kiểm tra trên repo NestJS chạy bằng CLI, không chạy trong phiên omp hay Claude, và đã qua. `claude plugin validate --strict` đã qua. Hai host in cùng JSON vì cùng gọi một CLI. Hook không chặn sửa. Diff có thể nêu cả class. Sơ đồ `.ua` cần host có model.
