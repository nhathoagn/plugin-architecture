# Changelog

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
