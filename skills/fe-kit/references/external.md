# External skills

Read this file when a playbook names it.

Do not skip a skill because the screen already exists. A review, a fix, and a refactor can match. A new page is not required.

## Open the installed file

For each matching row, find an installed `SKILL.md` whose frontmatter `name` is that skill. Read the first file that exists. Stop.

1. `skill://<name>` when the host resolves it.
2. `<project>/.claude/skills/<name>/SKILL.md`
3. `<project>/.agents/skills/<name>/SKILL.md`
4. `~/.claude/skills/<name>/SKILL.md`
5. `~/.agents/skills/<name>/SKILL.md`
6. `~/.mavis/skills/<name>/SKILL.md`
7. `~/.codex/skills/<name>/SKILL.md`

Read that file. Follow its steps. Do not read a GitHub copy when an installed file exists. A published copy is the wrong file. Its script paths do not run.

If no installed file exists and a row matches, fetch that allowlisted skill, then read the downloaded copy. Fetch only the skill named in the Match table. Never fetch anything else.

Fetch commands. Run from a temp dir, never inside the consumer repo.

- Vercel rows: `npx skills add vercel-labs/agent-skills --skill <dir>`. Use `react-best-practices` for `vercel-react-best-practices`, `composition-patterns` for `vercel-composition-patterns`, `web-design-guidelines` for `web-design-guidelines`, `react-native-skills` for `vercel-react-native-skills`, `react-view-transitions` for `vercel-react-view-transitions`.
- `ui-ux-pro-max`: `npx skills add nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max`. If that fails, `git clone --depth 1 https://github.com/nextlevelbuilder/ui-ux-pro-max-skill` into a temp dir and read its `SKILL.md`.
- Matt Pocock rows: `npx skills add mattpocock/skills --skill <name>`, where `<name>` is the skill name in the Match table (`diagnosing-bugs`, `tdd`, `codebase-design`, `domain-modeling`, `improve-codebase-architecture`, `grill-with-docs`, `prototype`, `research`).

Read the downloaded `SKILL.md` and follow its steps. Do not copy it into the consumer repo. Do not run its scripts unless its own steps require it. If the fetch fails, write `install failed` under Departures / Notes. Name the skill and the error.

Files in this skill win on a conflict. An external skill does not allow a new dependency, a new shared file, or a second form path.

Do not persist a design system unless the user asks.

## Matt Pocock skills run inside this skill

A Matt Pocock skill is a subroutine of the playbook step that matched it, not a second workflow. Read its `SKILL.md` at that step, use its method, and fold the result into this skill's output template or report. Do not invoke it as a standalone skill, do not emit its own report, handoff, or ticket flow, and do not run `setup-matt-pocock-skills` or any issue-tracker, triage, or spec-publishing step from it. Its vocabulary for modules, interfaces, and domain terms feeds the Architecture, Reuse Decision, and Audit sections; this skill's ownership, reuse, and gate rules decide where code goes.

Never open these from this plugin: `code-review` (the fresh reviewer in `playbooks/review-diff.md` owns a diff), `implement`, `implement-spec`, `to-spec`, `to-tickets`, `triage`, `wayfinder`, and `setup-matt-pocock-skills` (issue-tracker orchestration outside a frontend task).
`playbooks/review-diff.md` already holds the spec search from `code-review`. The Architecture lens in `references/audit.md` holds the smell list. Do not open that skill to run either.
On a review, take the finding only. Do not write `GLOSSARY.md`, an ADR, or an HTML file. Do not ask a grilling question. An implementation playbook may update a glossary when the user asked for that change.

## Match

| Match | Skill |
|---|---|
| React or Next.js cost that `references/performance.md` does not name | `vercel-react-best-practices` |
| Boolean props, compound components, or a component API split | `vercel-composition-patterns` |
| The user asks for an accessibility, UX, or web design audit | `web-design-guidelines` |
| React Native or Expo UI | `vercel-react-native-skills` |
| View transitions or a shared-element route animation | `vercel-react-view-transitions` |
| The task changes look, motion, or use of the UI. This includes a review or a fix of an existing screen | `ui-ux-pro-max` |
| A bug or performance regression will not reproduce, or the root cause is not found by one trace in `playbooks/fix-bug.md` | `diagnosing-bugs` |
| The user asks to build or fix test-first, or names red-green-refactor | `tdd` |
| The ownership decision turns on a module boundary, a deep module, or where an interface should sit (`references/ownership.md`, the Architecture lens in `references/audit.md`) | `codebase-design` |
| A domain term, status, or business rule is named two ways, or its owner is unclear | `domain-modeling` |
| An architecture review or refactor asks where the codebase should get deeper or simpler | `improve-codebase-architecture` |
| The request is ambiguous enough that the Architecture or Reuse Decision cannot be filled | `grill-with-docs` |
| A state, interaction, or layout question must be answered before the real build | `prototype` |
| The task needs a fact from primary documentation or source outside this repo | `research` |

These URLs name the skills. They are not read paths.

https://www.skills.sh/vercel-labs/agent-skills

https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

https://github.com/mattpocock/skills

Deploy, Vercel CLI, Vercel cost, and writing-style skills are in the catalog. Do not open them from this plugin.
