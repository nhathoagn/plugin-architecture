# fe-kit

One plugin directory. Claude Code and omp both load it.

The hooks are a POSIX `sh` script plus `python3`. The script finds `python3` even when the PATH is minimal, and on Windows it needs Git Bash. With no `python3` the hooks do nothing.

The skill `fe-kit` runs before non-trivial frontend work. Order is Architecture Ownership, then Reuse-first, then Performance Check. Do not write implementation code before those two decisions are filled.

`SKILL.md` is the workflow. It routes to one file in `playbooks/`: new UI, bug fix, refactor, performance, or review. `references/` holds the detail: ownership, reuse, performance, code quality, the senior audit (reuse, architecture, operational flow, error handling, load, extension), and when to open an external skill. The playbook names the references to read. External skills, including a Matt Pocock skill matched in `references/external.md`, run as a subroutine of the playbook step and fold into fe-kit's own output; fe-kit's files win on a conflict.

Two more skills check a screen after it is built. Neither one edits code.

- `ui-image-check` compares one UI image (mockup, screenshot, design export) with the code. It lists each item in the image, finds it in the code with `file:line`, and then compares a screenshot of the running screen. On Claude Code the command is `/fe-kit:ui-image-check`.
- `ut-report` writes the developer UT report of one screen to an `.xlsx` file. Each row compares the old system with the new one and records a real run. `scripts/build_report.py` builds the file from a YAML case file and needs `pyyaml` and `openpyxl`. On Claude Code the command is `/fe-kit:ut-report`.

## Install on Claude Code

In a session:

```text
/plugin marketplace add nhathoagn/plugin-architecture
/plugin install fe-kit@fe-kit
```

`/plugin install` opens the panel so you can pick a scope. It does not install until you pick one. The skill command is `/fe-kit:fe-kit`.

From a shell:

```bash
claude plugin marketplace add nhathoagn/plugin-architecture
claude plugin install fe-kit@fe-kit
```

An always-on omp rule tells the agent to read `skill://fe-kit` before non-trivial frontend code. Claude Code does not load that rule. Its hook injects the same line when the prompt names frontend work, or when a write touches `.tsx`, `.jsx`, `.vue`, or `.svelte`. The hook injects `rules/reuse-duplication.md` when the prompt adds or changes code, names reuse or duplication, names a fix, or when an edit touches source. That rule reuses an existing implementation, rejects the same statements written twice, and keeps one implementation when only the data changes. A bug fix does not add a second state, prop, or variable for a value that already exists. Only a behaviorless one-line wording fix or a pure style tweak skips the search: a change that alters runtime behavior is a bug fix however few lines it touches, and follows `playbooks/fix-bug.md` (reproduce, root cause at its owner, smallest fix, regression check, verify). A symptom report with no fix verb (`Tổng sai khi có discount`) also injects the reuse rule. `rules/modules.md` is injected with it: a different job is a new file in the owning feature with one call left in the old file, and file length alone does not split one. The hook also injects `rules/conflict-fix.md` when the prompt names a conflict or a marker, and when an edit touches a file whose line starts with a git conflict marker. A mention of that marker in prose does not inject the rule. A rebase onto another branch does not inject that rule unless the prompt also names a conflict or a marker. Creating or editing a `.tsx`, `.jsx`, `.vue`, or `.svelte` file is denied until the transcript contains `Runtime owner:` with a named owner and a Reuse Decision with one decision (`reuse`, `extend`, `feature-local`, `shared`, or `n/a` with a reason). Empty headings do not count, and a missing transcript denies instead of passing. Only a behaviorless one-line wording or style change is exempt. The hook reads only text the user typed or the agent wrote: reply text, and the thinking summary the transcript keeps. Lines count from the latest request on. A request asks for new work or reports a bug. `ok`, `làm đi`, an interrupt, and a compact summary do not start a new one. Under a `Reuse Decision` heading, any label can carry the decision, as in `- FE side: **reuse**`. A conflict resolution that only keeps or merges lines from the conflict block is exempt and is never a bug fix. A one-line edit is exempt only when the code outside strings, JSX text, and comments does not change. A deny names the missing lines. Run `python scripts/test_fe_gate.py` after a gate change. A value can start with a backquote, as in `` Runtime owner: `OrderForm` ``. The full-width colon `：` also counts. In text the user typed, a value can be on the next line, and `Step:` counts as `Trigger:`. The latest request decides bug mode: a request for new work ends an earlier bug report. Tool output, system reminders, and the hook's own deny message do not mark a bug fix and do not fill a line.

## Install on omp

```bash
omp plugin marketplace add nhathoagn/plugin-architecture
omp plugin install fe-kit@fe-kit
```

In the TUI, the same steps are `/marketplace add nhathoagn/plugin-architecture` and `/marketplace install fe-kit@fe-kit`. Invoke the skill with `/skill:fe-kit`. `rules/fe-implementation.md` is always applied. It defines a one-line fix by behavior, not by line count. The procedure is `skills/fe-kit/SKILL.md`. `rules/reuse-duplication.md` is always applied. Reuse an existing implementation, do not write the same code twice, and keep one implementation when only the data changes. A bug fix does not add a second state, prop, or variable for a value that already exists. `rules/modules.md` is always applied. A different job goes in a new file in the owning feature, and file length alone does not split a file. `rules/conflict-fix.md` is always applied. It tells the agent how to resolve a conflict without dropping prior source or duplicating an item. `rules/review-diff.md` is always applied. It says the author does not grade a frontend diff. omp does not run `hooks/hooks.json`.

## Load a local checkout

Use this only while you edit the plugin on disk.

```bash
claude --plugin-dir .
omp plugin link .
```

Run both from this directory.

## Layout

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
skills/fe-kit/SKILL.md
skills/ui-image-check/SKILL.md
skills/ut-report/SKILL.md
skills/ut-report/scripts/build_report.py
skills/fe-kit/playbooks/
skills/fe-kit/references/
skills/fe-kit/evals/
rules/fe-implementation.md
rules/reuse-duplication.md
rules/modules.md
rules/conflict-fix.md
hooks/hooks.json
skills/fe-kit/references/codemap-host-report.md
agents/reviewer.md
rules/review-diff.md
skills/fe-kit/playbooks/review-diff.md
skills/fe-kit/references/review-checks.md
skills/fe-kit/references/REVIEW_CHECKLIST.md
skills/fe-kit/references/review-output.md
```

## Test

Proves the host loads the plugin and fires hooks. It fails at the model call, which is fine.

```bash
cd /tmp && mkdir -p hookcheck && cd hookcheck
claude --plugin-dir /path/to/plugin-architecture --debug -p "review the diff before I commit"
grep -E "Read hooks.json for plugin fe-kit|Loading hooks from plugin: fe-kit|Hook UserPromptSubmit" ~/.claude/debug/latest
```

## Diff review

The author does not grade a frontend diff. On Claude Code, agent `fe-kit:reviewer` reads `playbooks/review-diff.md`. That playbook finds a local spec file, walks every item in `references/REVIEW_CHECKLIST.md`, then F1 through F22. A spec miss is a sentence in that same report. A name that conflicts with an existing glossary file is a sentence in that same report. A second job written into an edited file is a sentence in that same report, per `rules/modules.md`. It does not fetch an issue tracker, and it does not apply the Architecture smell list. On omp, a fresh context reads `skill://fe-kit/playbooks/review-diff.md`. A one-line fix or a pure style tweak skips this. A screen review still uses `playbooks/review-ui.md`. A smell there is "có thể để sau". A review does not write a glossary, an ADR, or an HTML file.

After compact, the Claude hook puts `rules/fe-implementation.md` and `rules/review-diff.md` back when the transcript shows frontend work. `PreCompact` tells the summary to keep those rules. After an edit, the hook exits 2 if conflict markers remain, and if `<repo>/.claude/rules.sh` is executable and fails. omp does not run these hooks. `rules/review-diff.md` is always applied there.
