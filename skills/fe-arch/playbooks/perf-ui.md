# Perf UI

Use this when the task is a waterfall, a bundle, a rerender, or list jank.

1. Read `references/performance.md`. Record the performance section of the output template in `SKILL.md`.
2. Read `references/ownership.md` only if the fix moves code into another folder. Otherwise write `n/a` for the ownership fields and say why.
3. Do not read `references/reuse.md` unless step 2 moves code. Otherwise write `n/a` for the reuse decision and say why.
4. Do not read `references/code-quality.md` unless the fix adds a file, a helper, or a type. Otherwise write `n/a` for the Code Quality section and say why. When you do read it, fill the sweep table before you stop.
5. Read `references/external.md`. For a match, read the installed skill file. Do not fetch a URL. If none match, write `n/a` under Departures / Notes and name the skip.

A performance fix that only edits an existing file does not wait for the reuse decision. A fix that creates a new `.vue` or `.tsx` file does.
