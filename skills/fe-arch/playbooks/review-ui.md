# Review UI

Use this when the task is to check, review, clean up, or shorten frontend code that already exists, and no behavior should change.

1. Read `references/ownership.md`. Record the five ownership fields. Say where the current placement is wrong, if it is.
2. Read `references/reuse.md`. For each helper, formatter, and component, say whether an existing one already covers it. Record the reuse decision.
3. Read `references/code-quality.md`. Record the Code Quality section of the output template in `SKILL.md`. For each finding, give the file, the line, and the rule it breaks.
4. Read `references/performance.md` only if the code fetches, lists, or streams. Otherwise write `n/a` and say why.

Report findings first. Change code only after the user picks what to change, unless the user already asked for the change.

When you change code, capture the screen before the first edit and after the last one, and compare them as `references/code-quality.md` describes. A refactor that changes the output is not done.
