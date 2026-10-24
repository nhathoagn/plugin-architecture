# Code Quality

Make the code readable to the next developer without a walkthrough. Each rule below came from a review where the first version was rejected.

Project rules win. When the repo has its own conventions file, follow it and treat this file as the fallback.

## Sweep

Do this pass once. Do not stop after the first findings. Do not ask the user to run the skill again for the rest.

Scope is the files the user named. If the user named a screen or a feature, scope is the UI files in that folder. Do not scan the repo.

List those files before the table. Open each file before you write a row for it. A search of that file also counts.

Write one row for each heading from Names through Design and behavior. Copy the heading text. A missing row means the pass is not done.

| Rule | Search | Verdict |
|---|---|---|
| Names | what you searched | `clean`, or `file:line` and the broken rule |

A `clean` row names the search. A row with no search is not a verdict.

`Design and behavior` may be `n/a` when the task has no design and no old screen. Say why.

Record every finding in scope. Fix a dirty row when the task is to clean up or shorten. Also fix a dirty row when you wrote that violation in this turn. Otherwise list the row and do not fix it.

After a fix, check those rows again. Stop when the rows you had to fix are `clean`.

Do not leave an unlisted in-scope finding for the next run.

## Names

- A name says what the thing holds or does. A reader knows it without opening the file.
- Keep it short. Cut words that add nothing (`order-layout-builders.ts` → `order-builders.ts`).
- Reject generic names: `model`, `view`, `sheet`, `data`, `utils`, `helper`, `common`, `New`, `2`.
- Reject a name that collides with a library primitive (`Sheet` when the UI kit has a `Sheet` drawer).
- One term per thing. If the code says "table", the comments do not say "sheet".

## Helpers

- Do not add a helper that is called once or that wraps one line. Write it inline at its one use, and keep the comment that explains the rule.
- Keep a helper when it is called many times, or when it names a business rule (a rounding rule, a legacy format).
- Before you write a formatter or a reader, search the repo for one. Check its contract before you reuse it: a form-bound field needs a form context; a grid cell formatter may change dates.
- A helper moves to `shared/` only when a second consumer needs the same semantics. Two call sites that look alike but differ (`??` against `||`, a different key naming) are not the same semantics. Refactor them in a separate change, after you check the data source.
- When you do move it, move the pure function. A wrapper typed to one feature's record stays in that feature.

## Arguments and values

- No bare positional numbers or booleans at a call site. `cell('Size', 'size', { span: 2 })`, not `cell('Size', 'size', 2)`.
- No magic sentinel values. Use `null`, not `''` or `-1`, for "nothing".
- Tag a union with a `kind` field. Do not tell variants apart with `'field' in value`.

## Types and schemas

- Declare every field of an API record with its own type. Reject a loose record (`z.record(...)`, `Record<string, unknown>`) and a shared alias for every field (`Cell`) when the shape is known.
- Take the field list from the source that produces it (the SQL, the API resource, the generated client). Then compare it with a real response: no missing key, no extra key.
- Take each type from real data, not from the database column type. Many drivers return numbers and dates as strings.
- A key that the server sets only when it has a value is `.optional()`.
- Export `keyof` of the record and use it wherever code names a field. A typo then fails type-check instead of rendering a blank cell.

## Files

- One file answers one question:
  - builders: types and the functions that describe the UI ("write it with what"),
  - layout or config: data only ("what is in it"),
  - component: rendering, class names, props types, loading / error / empty states ("how it looks").
- A data file holds no JSX and no class names. A component file holds no field list.
- Props types and class constants sit next to the component that uses them. Do not split them into `types.ts` or `constants.ts` for one consumer.
- Keep the folder flat while it is small. Do not add a sub-folder for three files.
- Imports go one way (component → layout → builders). No cycle.

## Make it shorter

Count before you shorten. Name the repeated call and how many times it repeats.

- Shorten: a wrapper call repeated dozens of times (make a string mean "read this field"); a wrapper array around every item; two identical handlers.
- Do not shorten:
  - by building identifiers from a prefix (`` `${prefix}_name` ``): a search for the real name no longer finds it, and a typo is not a type error;
  - by merging named components: the name and its comment are lost;
  - by positional arguments in place of named ones when the formatter still breaks the line.
- When the file is long because the content is long (150 fields = 150 lines), stop and say so.

## Design and behavior

- Layout comes from the design; the field set, labels, and order come from the spec. When they differ, ask. Do not pick one.
- Measure the design. For an SVG, render it and read the cell boxes per row. Do not estimate widths by eye.
- In a rewrite, a difference from the old system is a change request, not a fix. Record it where the project records changes, and say which ones wait for sign-off.
- Before you choose a data flow, read how the old screen gets its data: does it receive an object, or only a key and fetch again?

## Verify

- Run the project's format, type-check, lint, and structure checks after each change.
- Run the UI for real. For a refactor that must not change output, capture the screen before and after, and compare the image and the text byte for byte. A difference blocks "done" until you explain it.
- Prove the comparison can fail: compare two states that differ, and expect a difference.
- When test data lacks a case, force it in the response with request interception.
- When a new type should catch mistakes, add a throwaway file with a mistake, confirm type-check fails, then delete the file.
- Stop any dev server you started. Report each command and its exit code.

## Working in a shared tree

- Someone may edit or commit the same files while you work. Read a file again before you edit it. Keep their change.
- An editor diagnostic shown between two edits can be stale. Trust the type-check command.
