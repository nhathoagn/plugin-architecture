# Changelog

## 1.9.0

Rules were prose, so a long refactor forgot them after compact, and the author graded the diff just written.

- `rules/review-diff.md` is always applied. The author does not grade a frontend diff. Claude Code hands it to agent `fe-kit:reviewer`. omp uses a fresh context and `skill://fe-kit/playbooks/review-diff.md`.
- `playbooks/review-diff.md` and `references/review-checks.md` are that review. Each item is `PASS`, `FAIL`, or `N/A`. A `FAIL` has `path:line`. The author does not write the verdict.
- A screen review still uses `playbooks/review-ui.md`. A diff written in this session does not.
- After compact, the Claude hook re-injects `rules/fe-implementation.md` and the review rule when the transcript shows frontend work. `PreCompact` tells the summary to keep those rules.
- After an edit, the hook exits 2 when conflict markers remain, and when the repo's executable `.claude/rules.sh` fails. A repo with no `rules.sh` is unchanged.
- A consumer `REVIEW_CHECKLIST.md` with filled "Lỗi riêng của repo" rows is walked by the diff reviewer. Empty template rows are not items.
- `references/REVIEW_CHECKLIST.md` is in the skill. A diff review walks every S, C, D, N, E, SEC, P, T, TY, R, and DOC item there. It is not a link to an outside repo, and it is not optional.
- Checklist vẫn đi từng mã khi review, nhưng mã chỉ ở trong đầu. Bản người đọc không copy mã ra.
- Báo cáo người đọc theo `references/review-output.md`: kết luận trước, mỗi lỗi hai câu có `file:dòng` và người dùng mất gì, không có mã checklist.

## 1.8.0

Lessons from a real merge request review where working code was rejected.

- `code-quality.md`: a new prop must do what no existing prop does; overlapping props, unread props, and if/else props are findings; do not rewrite working shared code for one screen. Two helpers for one job, a screen hook that wraps a shared hook, a normalizer outside the field rule, and a second cleanup after the preformatter are findings.
- `code-quality.md` Types and schemas: strict types, shared schemas for dates and options, one name set for response and form, no field declared twice, each label once, required checks as a table, fields in screen order, sibling section order.
- `code-quality.md` Files: page sub-folders follow the page rule, export only what is imported, rules files grouped by data, dead rules and message keys deleted, empty comments deleted. Design and behavior: events in `onChange`, not in effects; no dependence on child order.
- `audit.md`: compare with the exemplar screen; a layout rebuilt in the page; lock and session queries not reused from cache; one error classifier; the form block title is not hidden; each hand-kept field list is an Extension finding.
- `review-ui.md`: the cost sentence says what the user loses, and names the exemplar screen or rule file.
- SKILL.md gains matching Hard Rules and Common Mistakes rows.

## 1.7.7

- The plugin and the skill are named `fe-kit`. Read `skill://fe-kit`. The skill folder is `skills/fe-kit/`.

## 1.7.6

- Review findings are spoken Vietnamese: what is wrong, where, what to do, and what it costs if it stays. Priority is said in words. The report does not end a line with `Mức vừa`, and it does not use `reuse` or `field list` in the sentence the reader sees.

## 1.7.5

- A review report leads with Kết luận, then one sentence per finding. Duplicated statements and data-only repetition keep their own sections. Other findings go under Việc nên làm. Empty sections are omitted. The English sweep table and Audit table are not part of a review.

## 1.7.4

- The review template has Cách viết. Each finding is one short Vietnamese sentence, names `file:dòng` and the code's own name, and says the next step: reuse, collapse the data, or leave it.

## 1.7.3

- A review ends with the Vietnamese template in `playbooks/review-ui.md`: phạm vi, dùng lại, code viết hai lần, chỉ khác dữ liệu, chất lượng, kiểm tra, không đụng tới, kết luận. That template is the review output. Filling it ends the pass.

## 1.7.2

- `rules/reuse-duplication.md` is one check again. Reuse an existing implementation, do not write the same statements twice, and when repeated calls differ only by data keep one implementation over a typed field list. The address form is that idea. It is not a sample pasted into the rule. `fe-implementation.md` and `conflict-fix.md` stay as they are.

## 1.7.1

- The same component rendered three or more times, differing only by data, is repeated code. `rules/reuse-duplication.md` proposes one typed field list and a single `.map`. A review proposes it and waits. Adding or changing that parent writes the shape. Two calls, or a call with a different component or handler, stay as they are.

## 1.7.0

- New `rules/reuse-duplication.md`. It is always applied. Before adding a function, component, hook, type, constant, validation, fetch, or handler, search for an existing implementation and open one caller. Reuse or extend when the contract matches. After the edit, compare the new lines with existing code and remove a block that is written twice. A repeated value or a repeated request is not this check. A one-line wording fix or a pure style tweak skips the search.
- The Claude hook injects that rule when the prompt adds or changes code, or names reuse or duplicated code, and when an edit touches source. omp loads the rule file and does not run the hook.
- `tests/test_fe_gate.py` checks that injection, and that the rule treats duplicated code as the same lines written again.

## 1.6.2

- The hook injects the conflict rule only when a line starts with a git conflict marker. A doc that mentions the marker text does not inject it.
- `rules/conflict-fix.md` keeps a one-sided rename and applies the other side's edit on the new path. Two different rename targets stop and ask.

## 1.6.1

- `rules/conflict-fix.md` reads base, ours, and theirs. A deletion the other side did not edit stays deleted. Combine fields only when they do not overlap. Regenerate a lockfile, a generated file, or a snapshot. Do not merge those files by hand. After the merge, check every previously unmerged file, then run the project checks.
- The Claude hook injects that rule when the prompt names a conflict or a marker, and when the edited file contains `<<<<<<<`. A rebase onto another branch does not inject the rule unless the prompt also names a conflict or a marker.

## 1.6.0

- New `rules/conflict-fix.md`. It is always applied. When the task resolves a merge conflict, keep each unique change from both sides once. Do not take one side and delete the other. Do not paste both blocks into one list.
- The Claude hook injects that rule when the prompt names a conflict. omp loads the rule file and does not run the hook.
- New `references/feature-isolation.md`: new behavior added to existing UI must be (1) behind one flag whose default is the old behavior, read once at the entry owner, reusing the project's flag system; (2) non-invasive — flag off means no new fetch, render, payload, or validation change, and no hook called conditionally on the flag; (3) separated — new logic in its own files under the owning feature, existing files touched only at a listed seam, proven by a deletion test.
- Bug fixes, security fixes, and pure refactors never gain a flag. A brand-new standalone screen records `n/a` and keeps only the separation guarantee.
- `new-ui.md` reads it when adding to existing UI; `refactor-ui.md` and `review-ui.md` read it only when behavior is added; `perf-ui.md` is unchanged. The output template gains a Feature Isolation section. The Architecture lens in `audit.md` greps for scattered flag reads.
- Nothing existing changes for tasks that add no behavior. The gate's deny rule for new `.vue`/`.tsx` files is unchanged.
- `rules/conflict-fix.md` is tighter: read the base (`:1`) as well as ours and theirs; a deletion is a change, so a delete-versus-edit stops and asks; combine only non-overlapping fields of an item both sides changed; regenerate generated files and lockfiles instead of merging them by hand; verify every conflicted file for markers and run the project's checks. The gate also injects the rule when the edited file contains conflict markers or the repo is mid-merge/rebase, and no longer treats a bare `rebase` prompt as a conflict.

## 1.5.0

- New `references/audit.md`: a senior audit with six lenses (Reuse, Architecture, Operational flow, Error handling, Performance and load, Extension). Each finding has `file:line`, a severity, and the cost if it stays.
- `review-ui.md` and `refactor-ui.md` fill the Audit table. `new-ui.md` fills it when the UI owns data or an action. `perf-ui.md` reads the Performance and load lens when the code polls.
- The output template has an Audit section. Hard Rules and Common Mistakes gained the matching lines.
- Names in `code-quality.md` is stricter: file name matches the main export, query hooks are named after their data, no bare `data` or `result`, one boolean style per file, one value one name. The Names row lists the searches to run.

## 1.4.5

- A matching row with no installed file now fetches that allowlisted skill and reads the downloaded copy. Fetch runs outside the consumer repo. A failed fetch is recorded, not retried silently.

## 1.4.4

- A match does not require a new page. The agent reads the installed skill file. It does not fetch a GitHub copy, and it does not install the skill.

## 1.4.3

- Playbooks read `references/external.md` and open a matching skill from vercel-labs/agent-skills or ui-ux-pro-max. Local rules still win. The agent does not install those skills.

## 1.4.2

- A matching file name outside the named folder does not change scope. The pass opens every file in that folder. It does not follow the outside file and stop.

## 1.4.1

- A code-quality pass fills one row per rule, from Names through Design and behavior. A blank row, or a `clean` row with no search, is not done.
- The pass lists every in-scope finding in that same turn. It does not leave the rest for another run.
- Cleanup, and violations written in this turn, are fixed before the agent stops. Other findings are listed and left.

## 1.4.0

- New `references/code-quality.md`: names, single-use helpers, bare positional values, explicit schemas from the server source, one file per responsibility, when to shorten and when to stop, before/after screen comparison.
- New `playbooks/review-ui.md` for checking, reviewing, cleaning up, or shortening existing UI.
- `new-ui.md` and `refactor-ui.md` read `code-quality.md`. `perf-ui.md` reads it only when the fix adds a file, a helper, or a type.
- The output template has a Code Quality section. Hard Rules and Common Mistakes gained the matching lines.

## 1.3.0

- The skill routes to `playbooks/new-ui.md`, `playbooks/refactor-ui.md`, or `playbooks/perf-ui.md`. Each playbook names the references to read.
- `rules/fe-implementation.md` is always applied. It tells the agent to read `skill://fe-arch` before non-trivial frontend code.
- A new `.vue` or `.tsx` file is denied until the transcript contains `Runtime owner:` and `Reuse Decision`. An edit of an existing file is allowed.

## 1.2.0

- The gate no longer runs on every session start. It runs when the prompt names frontend work, or when a write touches `.tsx`, `.jsx`, `.vue`, or `.svelte`.
- `rules/fe-implementation.md` is a pointer to `skills/fe-arch/SKILL.md`. The procedure stays in the skill.

## 1.1.0

- Renamed the plugin and the skill from `fe-architecture-reuse-perf` to `fe-arch`. The workflow is unchanged.

## 1.0.0
- Packaged the rewritten skill as one plugin for Claude Code and omp.
- `SKILL.md` keeps the workflow, the output template, and the hard rules. Detail stays in `references/`.
- Removed the loose root copies (`SKILL (1).md`, `ownership.md`, `reuse.md`, `performance.md`).
- No external doc links. The reference text is the local rewrite.
