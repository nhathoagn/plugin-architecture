# fe-kit

One plugin directory. Claude Code and omp both load it.

The skill `fe-kit` runs before non-trivial frontend work. Order is Architecture Ownership, then Reuse-first, then Performance Check. Do not write implementation code before those two decisions are filled.

`SKILL.md` is the workflow. It routes to one file in `playbooks/`: new UI, refactor, performance, or review. `references/` holds the detail: ownership, reuse, performance, code quality, the senior audit (reuse, architecture, operational flow, error handling, load, extension), and when to open an external skill. The playbook names the references to read.

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

An always-on omp rule tells the agent to read `skill://fe-kit` before non-trivial frontend code. Claude Code does not load that rule. Its hook injects the same line when the prompt names frontend work, or when a write touches `.tsx`, `.jsx`, `.vue`, or `.svelte`. The hook injects `rules/reuse-duplication.md` when the prompt adds or changes code, names reuse or duplication, or when an edit touches source. That rule reuses an existing implementation, rejects the same statements written twice, and keeps one implementation when only the data changes. A one-line wording fix or a pure style tweak skips the search. The hook also injects `rules/conflict-fix.md` when the prompt names a conflict or a marker, and when an edit touches a file whose line starts with a git conflict marker. A mention of that marker in prose does not inject the rule. A rebase onto another branch does not inject that rule unless the prompt also names a conflict or a marker. A new `.vue` or `.tsx` file is denied until the transcript contains `Runtime owner:` and `Reuse Decision`.

## Install on omp

```bash
omp plugin marketplace add nhathoagn/plugin-architecture
omp plugin install fe-kit@fe-kit
```

In the TUI, the same steps are `/marketplace add nhathoagn/plugin-architecture` and `/marketplace install fe-kit@fe-kit`. Invoke the skill with `/skill:fe-kit`. `rules/fe-implementation.md` is always applied. It is one line. The procedure is `skills/fe-kit/SKILL.md`. `rules/reuse-duplication.md` is always applied. Reuse an existing implementation, do not write the same code twice, and keep one implementation when only the data changes. `rules/conflict-fix.md` is always applied. It tells the agent how to resolve a conflict without dropping prior source or duplicating an item. omp does not run `hooks/hooks.json`.

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
skills/fe-kit/playbooks/
skills/fe-kit/references/
skills/fe-kit/evals/
rules/fe-implementation.md
rules/reuse-duplication.md
rules/conflict-fix.md
hooks/hooks.json
tests/test_fe_gate.py
```
