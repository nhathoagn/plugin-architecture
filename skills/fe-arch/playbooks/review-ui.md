# Review UI

Use this when the task is to check, review, clean up, or shorten frontend code that already exists, and no behavior should change.

1. Read `references/ownership.md`. Record the five ownership fields. Say where the current placement is wrong, if it is.
2. Read `references/reuse.md`. For each helper, formatter, and component, say whether an existing one already covers it. Record the reuse decision.
3. Read `references/code-quality.md`. Fill the sweep table. One row for each heading from Names through Design and behavior. Each finding names the file, the line, and the broken rule. A pass that stops after the first findings is not done.
4. Read `references/performance.md` only if the code fetches, lists, or streams. Otherwise write `n/a` and say why.

Report findings first. Change code only after the user picks what to change, unless the user already asked for the change.
When the user asked for the change, fix every dirty row in this turn. Then check those rows again.

When you change code, capture the screen before the first edit and after the last one, and compare them as `references/code-quality.md` describes. A refactor that changes the output is not done.
