# Refactor UI

Use this when the task splits, moves, or restructures UI that already exists.

1. Read `references/ownership.md`. Record the five ownership fields in the output template in `SKILL.md`.
2. Read `references/reuse.md`. Record the reuse decision. Prefer `reuse` or `extend` over a new shared file.
3. Do not read `references/performance.md` unless the refactor is about render or fetch cost. Otherwise write `n/a` and say why.
4. Read `references/code-quality.md`. Fill the sweep table. Capture the screen before the first edit so you can compare it after the last one. Follow the fix rule in Sweep.
5. Read `references/audit.md`. Fill the Audit table for the code you move or restructure. A refactor that adds a second path for one rule is not done.
6. Do not read `references/feature-isolation.md` for a pure refactor: no behavior changes, so no flag. Write `n/a` and say why. Read it only if the refactor also adds new behavior or changes a shared component's behavior for existing callers; then that new behavior follows it, and the refactor itself stays unflagged.
7. Read `references/external.md`. For a match, read the installed skill file, or fetch it per that file. If none match, write `n/a` under Departures / Notes and name the skip.

Do not create or edit a `.tsx`, `.jsx`, `.vue`, or `.svelte` file until the reply contains `Runtime owner:` with a named owner and a Reuse Decision with one decision. Write each line in the reply text, before the edit call. Thinking is not always saved, and the hook does not read a table row. Only a behaviorless one-line wording or style change (see `rules/fe-implementation.md`) is exempt.
