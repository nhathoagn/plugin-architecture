# Refactor UI

Use this when the task splits, moves, or restructures UI that already exists.

1. Read `references/ownership.md`. Record the five ownership fields in the output template in `SKILL.md`.
2. Read `references/reuse.md`. Record the reuse decision. Prefer `reuse` or `extend` over a new shared file.
3. Do not read `references/performance.md` unless the refactor is about render or fetch cost. Otherwise write `n/a` and say why.

Do not create a new `.vue` or `.tsx` file until the reply contains `Runtime owner:` and `Reuse Decision`. Editing a file that already exists is allowed.
