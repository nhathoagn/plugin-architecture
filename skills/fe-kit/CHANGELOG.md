# Changelog

## 1.11.0

Two skills that lived as personal skills join the plugin, so every install gets them.

- `skills/ui-image-check`: compare one UI image with the code, item by item, with `file:line`, then with a screenshot of the running screen. It does not edit code.
- `skills/ut-report`: write the developer UT report of one screen (old system against new system) to `.xlsx`. `scripts/build_report.py` builds the file from YAML. The script output is the same as the personal copy: a compare of every cell on a real case file found no difference.
- Project names, internal links, a tester name, and screen IDs in the examples are now placeholders, because the repository is public.
- The UT script path is now `scripts/build_report.py` in the skill directory, not a path under `~/.claude/skills`.
- `ut-report` gains "Case bắt buộc từ lỗi đã lọt qua UT": seven case kinds taken from defects that UT missed and integration test found. They are load defaults with their condition, the text of a code label, a check on raw typed text, a derived field when its input is cleared, a switch of scope or record, the form of a message (alert or inline), and an old branch that tells data shapes apart. A bug the tester reported is a case too, with `NG -> OK` after a re-run.

## 1.10.5

A rewritten screen ported an old check: `length === 2 ? lookup : show as stored`. The old field held a code or its label, so the check told them apart. The new field holds only the code, so the check had nothing to tell apart. Review did not catch it, because the comment named the old line but not why the old system needs it. A run of both systems showed the same status text with and without the check.

Integration test of the same rewritten screen found seven more defects. Each one is a rule the authoring steps did not state:

- A check on the first typed character never failed, because the shared field rule trimmed the text first. The old screen tested the raw value.
- Two boxes stayed blank after the first save, because two load defaults of the old screen were not ported. The first fix set them on every load. A second fix added the old condition.
- A status showed its name only. The old master loader builds code, separator, and name.
- A derived checkbox stayed on after the user cleared its input. The rule returned `null` for a blank input, and the caller skipped the update. The CR named only the filled cases.
- Leaving the all-records view for one record kept the all-records defaults. A guard compared only the record key.
- A one-time completion alert became a block that stayed on screen, because the project rule sends every result to that block.

Changes:

- `code-quality.md` Design and behavior: port the behavior of the old screen, not the way it stored data. Write why the old system needs a branch before you port it. Port each load default with its condition. Take a code label from the old loader. Run a check on the raw typed text before any normalizer. Keep a one-time alert as a dialog, and name a conflict with a project rule.
- `code-quality.md` Field updates: a derived field updates for a cleared input too. A switch of record or scope resets the values and defaults of the old scope, and a "same key" guard also compares the mode.
- `review-checks.md` F18 covers behavior ported from the old system. F19 covers a derived field and a switch of record or scope. `README.md` and `evals.json` now say F1 through F19.

## 1.10.4

The gate denied an edit after the agent wrote `Runtime owner:` and `Decision:` in the reply text, just before the edit call. The same text passed 31 seconds later with no new line. Claude Code can write the current reply text to the transcript after the PreToolUse hook reads it.

- Before a deny, the gate reads the transcript again, up to 10 times, 0.3 seconds apart. An allowed edit has no wait. A deny takes about 3 seconds more.
- A label can be bold or italic with the colon outside, as in `**Decision**: extend` or `_Runtime owner_: OrderForm`. Before, only `**Decision:**` counted.
- Labels and decision words ignore case: `Runtime Owner:`, `Reuse decision:`, `Decision: N/A`, `Decision: Extend`, and `actual:` count. The template lines in SKILL.md (an empty value, or decisions joined by `|`) still do not count.

A second session denied 8 edits during a `git stash apply` conflict. The agent wrote its plan only in thinking, which the terminal shows as a summary line, so it believed it had replied. The user wrote `đang lỗi`, so the gate also asked for `Trigger:`, `Expected:`, and `Actual:`.

- An Edit whose old text has conflict markers is exempt when every non-blank line of the new text is already in the conflict block (indentation ignored) and the new text has no marker. Such an edit only keeps, drops, or reorders lines. A line that is not in the block, such as a new wrapper call, is still gated.
- An Edit whose old text has conflict markers does not need `Trigger:`, `Expected:`, and `Actual:`. A merge is not a bug fix.
- The gate also reads the thinking text that the transcript keeps. The 1.10.3 note said the transcript keeps no thinking text. That is wrong: it keeps the summary the user sees. Empty or redacted thinking still does not count, so the playbooks still say to write the lines in the reply text.
- A conflict Edit that writes one line not copied from either side is exempt only when every word and every risky token in that line is already in the conflict block. A merged class string passes. A new call such as `toHalf(2)`, or a new `??`, is gated.
- A one-line Edit outside a conflict is exempt only when the code outside strings, JSX text, and comments does not change. A class or wording change passes. A new call, a new handler, or a changed value such as `limit={10}` to `limit={20}` is gated. Also exempt: an import or export list, a comment line, and a line inside a class string that spans lines (`h-14.5 min-h-14.5`, `px-3 text-primary">`). An object key with a flag or number (`open: true,`) is not a class line and stays gated.
- Labels count from the latest request on. A request is a user message that asks for new work or reports a bug. `ok`, `làm đi`, and an interrupt do not start a new request, so labels written before them still count. Before, labels written once opened every later edit in the session.
- A compact summary is not a request and does not turn on bug mode. The text before the summary stays in the same transcript, so labels written before `/compact` still count.
- Inside a subagent, the hook payload names the main transcript. A test showed that a subagent edit passed on labels written only in the main session. When the payload has `agent_id` or `agent_transcript_path`, the gate also reads `<session>/subagents/agent-<id>.jsonl`, so labels the subagent writes count. Whether the payload has `agent_id` is not verified.
- Under a `Reuse Decision` heading, any label can carry the decision, as in `- FE side: **reuse**`. An agent wrote its owner and decision that way and was denied 7 times. A decision word under another heading, or the template line with `|`, still does not count.
- The deny message names what is missing after the latest request, for example `` `Decision:` with reuse, extend, feature-local, shared, or n/a ``. It also says that reply text written earlier in the turn counts, and that the agent should write the lines and retry in the same turn. An agent believed that text written mid-turn is not saved, ended the turn, and asked the user to type "tiếp tục".
- `scripts/test_fe_gate.py` runs 94 cases: label formats, bug mode, request scope, compact, one-line edits, conflicts, file types, a subagent, a late transcript write, and a Vietnamese prompt. Run `python scripts/test_fe_gate.py`. The exit code is the number of failures.
- A replay of 1,338 view-file edits from local transcripts compared this gate with 1.10.2. 138 edits that 1.10.2 denied now pass: 124 had real labels in a format 1.10.2 missed, and 14 are conflict resolutions. 60 edits that 1.10.2 passed as one-line now need labels. 58 of them change a call, a condition, a prop, or a value. 2 are class-only lines that the check cannot read: a class list cut after `hover:`, and `marker:content-['…']` with quotes inside the class.
- `tổng sai`, `tính sai`, `hiển thị sai`, and `bị sai` now mark a bug report. `sai` alone does not, so `sai chính tả` stays a wording fix.
- On Windows, Python read the hook payload as cp1252, so a Vietnamese prompt such as `đang lỗi màn hình trắng` or `thêm cột` matched no rule and injected nothing. The gate now decodes stdin as UTF-8.
- A conflict resolution that replaces a marker block (`<<<<<<<`, `=======`, `>>>>>>>`, `|||||||`) with one line counts as a one-line edit. It is exempt when the new line adds no risky token (`??`, `||`, `&&`, `if (`, `=>`, a hook, `await`, `fetch`, `catch`) that the two sides did not already have. Marker lines do not count as code in that check. A resolution with two or more lines, or a line that keeps a marker, is still gated.

## 1.10.3

An agent retried a blocked edit ten times. It wrote `Runtime owner:` and `Decision:` only in thinking. The transcript keeps no thinking text, so the gate never saw the lines.

- The deny message says where to write the lines: in the reply text, one line each, before the edit call. It says that thinking and a table row do not count.
- The playbooks and SKILL.md say the same.
- A value can start with a backquote after a space, as in `` Runtime owner: `OrderForm` ``. `` Decision: `extend` `` and `Decision: **extend**` also count. A backquote right after the colon is still prose that names the field.
- `Decision:` counts when one decision word is anywhere on the line, as in `Decision: mở rộng (extend)`. A line with `|` still does not count.
- The full-width colon `：` counts the same as `:`.
- In text the user typed, a value can be on the next line, as in `Actual:` and then the value below it. `Step:` counts as `Trigger:`. `Expected` with no colon at the end of a line also counts. The agent still writes each value on the same line.
- The latest request decides bug mode. A message such as `làm đi` keeps an earlier bug report. A request for new work (`add`, `thêm`, `viết`) ends it. Before, one bug word anywhere in the session gated every later edit.

## 1.10.2

The 1.10.1 gate read text that no person wrote.

- Every session counted as a bug fix. The bug check read tool output, `<system-reminder>` text such as a global CLAUDE.md with `bug cause`, and the hook's own deny message. The check now reads only text the user typed.
- Reading `playbooks/fix-bug.md` filled the gate. Prose such as `` `Trigger:`, `Expected:` `` and the deny message `Trigger:, Expected:` matched as a value. The gate now reads only text the user typed or the agent wrote, without the deny message. A value cannot start with `,` or `` ` ``.
- The owner and decision lines follow the same source rule.

## 1.10.1

Bug-fix work that landed after 1.10.0. 1.10.0 already used F13–F15, so the new review rows are F16 and F17.

- `playbooks/fix-bug.md`: reproduce with `Trigger:`, `Expected:`, and `Actual:` before an edit. Fix at the owner. Write the unit test in the owner's existing test file. A text check includes `undefined`, `null`, `""`, a leading space, and a trailing space. The failing case must fail on the old code.
- `review-checks.md` F16: a new check that lets `undefined`, `null`, `""`, or `"ABC "` through fails. F17: a bug fix with no unit test for that case fails.
- The hook denies a view edit until owner, decision, and the three reproduce lines are filled. After the edit it names the unit test and the reviewer handoff. `trung tâm` and a typo prompt do not inject the reuse rule.

## 1.10.0

Lessons from a reviewer's plan to restructure a large form screen without a change in behavior.

- `code-quality.md` Names: a behavior hook starts with a verb. Do not rename a name that is not wrong. Rename a name a reader can confuse with an existing export.
- `code-quality.md` Helpers: search the shared lib for a function with no business term. Move it there only with a second consumer or a project rule. `helpers/` holds pure functions only. A grab-bag `*-format.ts` and a dead parameter are findings.
- `code-quality.md` Files: one kind of code per sub-folder, search params in `schemas/`, tiny constant files merged, relative imports inside a screen, new conventions written to the project rule file.
- `code-quality.md` gains a `Form screens` heading: split by visible block with `-panel`, `-section`, `-operation-panel`; each block owns its fields, popup, and dependent updates; the parent form only composes; one lookup hook per master that does not open UI and guards a late response; no `setValue` in JSX.
- `code-quality.md` Verify: walk every lookup button on a production build. Record React Profiler before and after a render claim.
- `performance.md`: state and `useWatch` in the smallest block, catalog hooks in the block that read the prefetched cache, `useCallback` on a hook function used as an effect dependency.
- `review-checks.md`: F13 large form, F14 `setValue` and layers, F15 renames and hook names.
- SKILL.md gains the `Form screens` row, and matching Hard Rules and Common Mistakes rows.
- `reuse.md` no longer says PascalCase files and `useXxx.ts`. File names follow the project rule, else kebab-case, as in `code-quality.md`. A shared `types.ts` needs two consumers.

## 1.9.9

A bug fix could finish with no unit test. Step 5 said to leave a regression check, and allowed skipping it.

- `playbooks/fix-bug.md` now says where the test file goes, what it must call, and which cases it must include. A text check includes `undefined`, `null`, `""`, a leading space, and a trailing space. The failing case must fail on the old code. Skip the file only when the repo has no test runner.
- `review-checks.md` gains the bug-fix unit test row (F17 after 1.10.0). A bug fix with no such test fails review.
- After a bug-fix edit, the hook names that test instead of only saying to re-run the reproduction.

## 1.9.8

Five holes left after the bug-fix playbook. A notification prompt injected the reuse rule, a typo prompt did too, a filled decision skipped reproduction, and the hook said nothing after the edit.

- `trung` no longer matches `trung tâm`. A wording prompt (`typo`, chính tả, button label) does not inject the reuse rule.
- A bug-fix edit of a view file is denied until the transcript has `Trigger:`, `Expected:`, and `Actual:`, each with a value, plus the existing owner and decision lines.
- After that edit, the hook says to re-run the reproduction and hand the diff to the reviewer. It does not run the project's tests.
- D8 and F7 point at `rules/reuse-duplication.md` instead of restating a second holder rule.

## 1.9.7

A bug fix had no playbook, and the hook gate only stopped a new `.tsx` or `.vue` file. A fix could edit an existing component, patch the symptom where the value is shown, add a fallback that hides the cause, and finish with no reproduction and no test. Empty `Runtime owner:` and `Reuse Decision` headings also opened the gate, and a missing transcript passed it.

- New `playbooks/fix-bug.md`, routed from `SKILL.md`: reproduce first, root cause at its owner, smallest fix with no mixed refactor and no silent fallback, a regression check, and a reported verify run. A symptom report with no fix verb (`Tổng sai khi có discount`) is a bug fix.
- `rules/fe-implementation.md` defines one-line by behavior: a change that alters runtime behavior is never one-line, however few lines it touches. `rules/reuse-duplication.md` and `rules/review-diff.md` point at that one definition.
- The second-holder rule now lives only in `rules/reuse-duplication.md`. The copies in `SKILL.md` and `references/code-quality.md` are gone or point at it. Naming the holder checked is not enough: name the literal or behavior searched.
- `scripts/fe-gate.py`: creating or editing a `.tsx`, `.jsx`, `.vue`, or `.svelte` file is denied until the transcript names a `Runtime owner:` value and a `Decision:` of `reuse`, `extend`, `feature-local`, `shared`, or `n/a`. Empty headings and the template line do not count. A missing or unreadable transcript denies. A symptom prompt with no fix verb injects the implementation and reuse rules. Only a behaviorless one-line Edit is exempt.

## 1.9.6

A review of the helper ran and wrote that it could ship. The checklist had the case, but the review never applied `undefined`, `null`, or `""` to the check. Walking items in your head is not applying them.

- `playbooks/review-diff.md`: a new or changed check must be applied to `undefined`, `null`, `""`, `" ABC"`, and `"ABC "` before the verdict. A value with no error is a finding. "Đưa được" is not allowed if those inputs were not applied.
- `review-checks.md` gains the check row (F16 after 1.10.0), on the short table the reviewer walks, not only in the long checklist.
- The reader report cannot say "Đưa được" without the result of `undefined`, `null`, and `""`.

## 1.9.5

The original helper `(values[field] ?? '').startsWith(' ')` still passed review. TY7 only failed a case the message already named, and TY8 was N/A when no schema existed. `""` and `undefined` produced no error.

- That helper is a finding even with no schema and even when the message only names a leading space. `undefined`, `null`, and `""` become `''`, and `''.startsWith(' ')` is false.
- TY7 now names `undefined` and `null`. TY9 fails the helper when those three values produce no error. It does not wait for a schema or for the message to mention empty.

## 1.9.4

A bug fix could add `useState`, a prop, or a variable for a value that already existed. The reuse rule only searched before a new function, hook, type, constant, validation, fetch, or handler.

- `rules/reuse-duplication.md` now includes state, props, and variables. A bug fix that adds one must name the holder that already has that value and read it or write into it. A second holder is a finding. A one-line wording fix still skips the search.
- `REVIEW_CHECKLIST.md` gains D8. `review-checks.md` F7 covers a new state or variable, not only a repeated prop.
- The Claude hook injects the reuse rule when the prompt says fix, sửa, or bug.

## 1.9.3

A screen that already had a validator still grew a helper that reimplemented the check.

- Use the validator the project already has: the schema, the resolver, or the shared field rule. Do not add a function that filters fields, calls `safeParse`, or wraps `min`, `trim`, or `startsWith`.
- If no validator exists, keep one table or one schema at the owner. Do not add a helper beside it. Do not require a new library.
- `REVIEW_CHECKLIST.md` gains TY8. A helper next to an existing validator fails. No existing tool is N/A.

## 1.9.2

1.9.1 said not to demand a schema. A check could still pass a case its message rejects, and the review had nothing to fail.

- `code-quality.md`: judge the cases, not the library. Do not require a schema. `startsWith(' ')` is not the rule "no empty, no space at either end", because `""` and `"ABC "` pass. The message and the predicate must name the same cases. A library type error is not the empty message.
- `REVIEW_CHECKLIST.md` TY6 no longer reads as a pass for every typed form check. TY7 fails a check that lets a forbidden case through. It does not name a library.
- SKILL.md: the hard rule and one Common Mistakes row match.

## 1.9.1

A diff review had no rule for a hand-written validation check, so it could only guess whether the change needed a schema.

- `code-quality.md` Types and schemas: a `[field, code]` check table is the one list, and a schema over it is a second list every new field must join. A schema is for parsing untrusted input: the parsed value, the inferred type, the shape guarantee. A check over values the form already typed needs none of the three.
- `(values[field] ?? '')` turns an absent required field into a pass with no message: fail on absence instead.
- One code per field is the table's limit, and `filter` then `map` reports the first rule only.
- Narrow to a string before `startsWith`, `trim`, or `toUpperCase`; type the field slot against `keyof Values` and the code slot against the message-key union.
- `REVIEW_CHECKLIST.md` gains TY6: a hand-written check that repeats a rule the schema already holds, or that counts a missing required field as valid, fails. A check on typed values that only builds form messages passes, and the reviewer does not ask for a schema.
- SKILL.md gains the matching Hard Rule and two Common Mistakes rows.
- One eval case asks the zod question about a real `[field, code]` helper.

## 1.9.0

Rules were prose, so a long refactor forgot them after compact, and the author graded the diff just written.

- `rules/review-diff.md` is always applied. The author does not grade a frontend diff. Claude Code hands it to agent `fe-kit:reviewer`. omp uses a fresh context and `skill://fe-kit/playbooks/review-diff.md`.
- `playbooks/review-diff.md` and `references/review-checks.md` are that review. Each item is `PASS`, `FAIL`, or `N/A`. A `FAIL` has `path:line`. The author does not write the verdict.
- A screen review still uses `playbooks/review-ui.md`. A diff written in this session does not.
- After compact, the Claude hook re-injects `rules/fe-implementation.md` and the review rule when the transcript shows frontend work. `PreCompact` tells the summary to keep those rules.
- After an edit, the hook exits 2 when conflict markers remain, and when the repo's executable `.claude/rules.sh` fails. A repo with no `rules.sh` is unchanged.
- `scripts/fe-gate.sh` no longer needs `dirname`, and it finds `python3` in `/opt/homebrew/bin`, `/usr/local/bin`, or `/usr/bin` when the PATH is minimal. With no `python3` it exits 0 and writes nothing.
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
