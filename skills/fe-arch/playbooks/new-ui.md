# New UI

Use this when the task adds a component, page, form, or hook.

1. Read `references/ownership.md`. Record the five ownership fields in the output template in `SKILL.md`.
2. Read `references/reuse.md`. Record the reuse decision in that same template.
3. Read `references/performance.md` only if the new UI fetches, lists, or streams. Otherwise write `n/a` in the performance section and say why.
4. Read `references/code-quality.md`. Record the Code Quality section before you name files, helpers, and types. After the last edit, fill the sweep table for each file you created or edited. Follow the fix rule in Sweep.
5. Read `references/audit.md` when the new UI owns data or an action. Fill the Operational flow, Error handling, and Extension rows before you write the code, and every row after the last edit. Otherwise write `n/a` for the Audit section and say why.
6. Read `references/external.md`. For a match, read the installed skill file, or fetch it per that file. If none match, write `n/a` under Departures / Notes and name the skip.

Do not create a new `.vue` or `.tsx` file until the reply contains `Runtime owner:` and `Reuse Decision`. Editing a file that already exists is allowed before that.
