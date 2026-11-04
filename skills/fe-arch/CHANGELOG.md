# Changelog

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
