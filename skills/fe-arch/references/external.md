# External skills

Read this file when a playbook names it. Open each matching row. Do not open the catalog and read every skill.

Read the published `SKILL.md`. Do not copy it into this repo. Do not install it into the consumer repo.

Files in this skill win on a conflict. An external skill does not allow a new dependency, a new shared file, or a second form path.

If no row matches, write `n/a` under Departures / Notes. Name the skip.

If a path returns 404, open the catalog and use the skill name. Do not guess a new path.

## Open these

| Match | Skill | Path |
|---|---|---|
| React or Next.js cost that `references/performance.md` does not name | `vercel-react-best-practices` | `skills/react-best-practices/SKILL.md` |
| Boolean props, compound components, or a component API split | `vercel-composition-patterns` | `skills/composition-patterns/SKILL.md` |
| The user asks for an accessibility, UX, or web design audit | `web-design-guidelines` | `skills/web-design-guidelines/SKILL.md` |
| React Native or Expo UI | `vercel-react-native-skills` | `skills/react-native-skills/SKILL.md` |
| View transitions or a shared-element route animation | `vercel-react-view-transitions` | `skills/react-view-transitions/SKILL.md` |
| A new look, and the repo has no design system to reuse | `ui-ux-pro-max` | `.claude/skills/ui-ux-pro-max/SKILL.md` |

Catalog: https://www.skills.sh/vercel-labs/agent-skills

Repo for the first five paths: https://github.com/vercel-labs/agent-skills

Repo for `ui-ux-pro-max`: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

Read `https://github.com/vercel-labs/agent-skills/blob/main/<path>` for a Vercel skill.

Read `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/<path>` for `ui-ux-pro-max`.

Deploy, Vercel CLI, Vercel cost, and writing-style skills are in the catalog. Do not open them from this plugin.

The `ui-ux-pro-max` search script runs only when that skill is already installed. If it is not installed, read the priority table in its `SKILL.md` and say the search database is absent. Do not install it. Do not persist a design system unless the user asks.
