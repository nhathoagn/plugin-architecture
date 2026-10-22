# fe-arch

One plugin directory. Claude Code and omp both load it.

The skill `fe-arch` runs before non-trivial frontend work. Order is Architecture Ownership, then Reuse-first, then Performance Check. Do not write implementation code before those two decisions are filled.

`SKILL.md` is the workflow. `references/` holds the detail. Read one reference per step.

## Install on Claude Code

In a session:

```text
/plugin marketplace add nhathoagn/plugin-architecture
/plugin install fe-arch@fe-arch
```

`/plugin install` opens the panel so you can pick a scope. It does not install until you pick one. The skill command is `/fe-arch:fe-arch`.

From a shell:

```bash
claude plugin marketplace add nhathoagn/plugin-architecture
claude plugin install fe-arch@fe-arch
```

The hook injects a pointer to `skills/fe-arch/SKILL.md` only when the prompt names frontend work, or when a write touches `.tsx`, `.jsx`, `.vue`, or `.svelte`. Claude Code does not load `rules/`.

## Install on omp

```bash
omp plugin marketplace add nhathoagn/plugin-architecture
omp plugin install fe-arch@fe-arch
```

In the TUI, the same steps are `/marketplace add nhathoagn/plugin-architecture` and `/marketplace install fe-arch@fe-arch`. Invoke the skill with `/skill:fe-arch`. `rules/fe-implementation.md` is one line that points at `skills/fe-arch/SKILL.md`. It is not always applied. omp does not run `hooks/hooks.json`.

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
skills/fe-arch/SKILL.md
skills/fe-arch/references/
skills/fe-arch/evals/
rules/fe-implementation.md
hooks/hooks.json
```
