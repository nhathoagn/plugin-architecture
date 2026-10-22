# fe-architecture-reuse-perf

One plugin directory. Claude Code and omp both load it.

The skill `fe-architecture-reuse-perf` runs before non-trivial frontend work. Order is Architecture Ownership, then Reuse-first, then Performance Check. Do not write implementation code before those two decisions are filled.

`SKILL.md` is the workflow. `references/` holds the detail. Read one reference per step.

## Install on Claude Code

Load this directory for one session:

```bash
claude --plugin-dir /Users/nhathoang/Documents/plugin-architecture
```

Install it from the catalog in this directory:

```text
/plugin marketplace add /Users/nhathoang/Documents/plugin-architecture
/plugin install fe-architecture-reuse-perf@fe-architecture
```

The skill command is `/fe-architecture-reuse-perf:fe-architecture-reuse-perf`. A session-start hook injects the same gate. Claude Code does not load `rules/`.

## Install on omp

Link this directory:

```bash
omp plugin link /Users/nhathoang/Documents/plugin-architecture
```

Or install from the catalog. Run this from the plugin directory. `omp plugin marketplace add .` is rejected. Use `./.` or the absolute path.

```bash
omp plugin marketplace add ./.
omp plugin install fe-architecture-reuse-perf@fe-architecture
```

Invoke the skill with `/skill:fe-architecture-reuse-perf`. omp injects `rules/fe-implementation.md`. omp does not run `hooks/hooks.json`.

## Layout

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
skills/fe-architecture-reuse-perf/SKILL.md
skills/fe-architecture-reuse-perf/references/
skills/fe-architecture-reuse-perf/evals/
rules/fe-implementation.md
hooks/hooks.json
```
