# Perf UI

Use this when the task is a waterfall, a bundle, a rerender, or list jank.

1. Read `references/performance.md`. Record the performance section of the output template in `SKILL.md`.
2. Read `references/ownership.md` only if the fix moves code into another folder. Otherwise write `n/a` for the ownership fields and say why.
3. Do not read `references/reuse.md` unless step 2 moves code. Otherwise write `n/a` for the reuse decision and say why.

A performance fix that only edits an existing file does not wait for the reuse decision. A fix that creates a new `.vue` or `.tsx` file does.
