# fe-architecture-reuse-perf

One plugin directory. Claude Code and omp both load it.

The skill `fe-architecture-reuse-perf` runs before non-trivial frontend work. Order is Architecture Ownership, then Reuse-first, then Performance Check. Do not write implementation code before those two decisions are filled.

`SKILL.md` is the workflow. `references/` holds the detail. Read one reference per step.

## Install on Claude Code

In a session:

```text
/plugin marketplace add nhathoagn/plugin-architecture
/plugin install fe-architecture-reuse-perf@fe-architecture
```

`/plugin install` opens the panel so you can pick a scope. It does not install until you pick one. The skill command is `/fe-architecture-reuse-perf:fe-architecture-reuse-perf`.

From a shell:

```bash
claude plugin marketplace add nhathoagn/plugin-architecture
claude plugin install fe-architecture-reuse-perf@fe-architecture
```

A session-start hook injects the gate. Claude Code does not load `rules/`.

## Install on omp

```bash
omp plugin marketplace add nhathoagn/plugin-architecture
omp plugin install fe-architecture-reuse-perf@fe-architecture
```

In the TUI, the same steps are `/marketplace add nhathoagn/plugin-architecture` and `/marketplace install fe-architecture-reuse-perf@fe-architecture`. Invoke the skill with `/skill:fe-architecture-reuse-perf`. omp injects `rules/fe-implementation.md`. omp does not run `hooks/hooks.json`.

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
skills/fe-architecture-reuse-perf/SKILL.md
skills/fe-architecture-reuse-perf/references/
skills/fe-architecture-reuse-perf/evals/
rules/fe-implementation.md
hooks/hooks.json
```
