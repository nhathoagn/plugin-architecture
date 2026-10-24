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

If no installed file exists, write `not installed` under Departures / Notes. Name the skill. Do not fetch a URL. Do not install the skill.

Files in this skill win on a conflict. An external skill does not allow a new dependency, a new shared file, or a second form path.

Do not persist a design system unless the user asks.

## Match

| Match | Skill |
|---|---|
| React or Next.js cost that `references/performance.md` does not name | `vercel-react-best-practices` |
| Boolean props, compound components, or a component API split | `vercel-composition-patterns` |
| The user asks for an accessibility, UX, or web design audit | `web-design-guidelines` |
| React Native or Expo UI | `vercel-react-native-skills` |
| View transitions or a shared-element route animation | `vercel-react-view-transitions` |
| The task changes look, motion, or use of the UI. This includes a review or a fix of an existing screen | `ui-ux-pro-max` |

These URLs name the skills. They are not read paths.

https://www.skills.sh/vercel-labs/agent-skills

https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

Deploy, Vercel CLI, Vercel cost, and writing-style skills are in the catalog. Do not open them from this plugin.
