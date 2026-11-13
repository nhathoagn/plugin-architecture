# Code Quality

Make the code readable to the next developer without a walkthrough. Each rule below came from a review where the first version was rejected.

Project rules win. When the repo has its own conventions file, follow it and treat this file as the fallback.

## Sweep

Do this pass once. Do not stop after the first findings. Do not ask the user to run the skill again for the rest.

Scope is the files the user named. If the user named a screen or a feature, scope is every UI file in that folder. List each path. Do not scan the repo.

A matching name outside the folder does not change scope. `src/order-detail/sheet.tsx` and `src/ui/sheet.tsx` are two files. Open every file in the named folder. Do not open the outside file and stop.

List those paths before the table. Open each path before you write a row for it. A search of that path also counts. A pass that omits a file in the named folder is not done.

Write one row for each heading from Names through Design and behavior. Copy the heading text. A missing row means the pass is not done.

| Rule | Search | Verdict |
|---|---|---|
| Names | what you searched | `clean`, or `file:line` and the broken rule |

A `clean` row names the search. A row with no search is not a verdict.

`Design and behavior` may be `n/a` when the task has no design and no old screen. Say why.

`Form screens` may be `n/a` when the scope has no large form. Say why.

Record every finding in scope. Fix a dirty row when the task is to clean up or shorten. Also fix a dirty row when you wrote that violation in this turn. Otherwise list the row and do not fix it.

After a fix, check those rows again. Stop when the rows you had to fix are `clean`.

Do not leave an unlisted in-scope finding for the next run.

## Names

Before you name, list the sibling files and exports in the same folder. Follow their pattern.

- A name says what the thing holds or does. A reader knows it without opening the file.
- Keep it short. Cut words that add nothing (`order-layout-builders.ts` → `order-builders.ts`).
- Reject generic names: `model`, `view`, `sheet`, `data`, `utils`, `helper`, `common`, `New`, `2`.
- Reject a name that collides with a library primitive (`Sheet` when the UI kit has a `Sheet` drawer).
- One term per thing across the feature, not only in one file. If `result` is the form message block on one screen, it is not the job progress on the next screen. If the code says "table", the comments do not say "sheet".

Files and exports

- The file name is its main export in kebab-case: `use-order-progress.ts` exports `useOrderProgress`. Rename both together, with `git mv`, and update every import and document in the same change.
- A file name says what the file holds. A file of options, labels, and defaults is not a `loader`. A file of messages is not a `run`.

Hooks

- A query hook is named after the server data it returns (`useOrderOptions`, `useOrderProgress`). An action hook is named after the action (`useOrderSubmit`).
- A behavior hook in a screen folder starts with a verb: `use-<screen>-<verb>` (`use-order-request-action`, `use-order-mark-invalid`). A noun name (`use-order-actions`, `use-order-invalid`) is a finding.
- Do not use a word that is both a verb and a noun in the domain (`run`, `result`, `entry`, `check`) unless the name says which one.

Renames

- Do not rename a name that is not wrong. Each rename grows the diff and hides the real change.
- Rename a name that a reader can confuse with an existing export. `groupDigits` next to `formatGrouped` is a finding: name what differs (`groupTypedDigits`). Write the reason in the change.

Variables

- Rename `data` when you destructure a query: `const { data: options } = useOrderOptions()`. No bare `data`, `result`, `item`, or `value` at component scope.
- A boolean reads as a yes/no question, with one style per file: `isX`, `hasX`, `canX`, `shouldX`. Do not mix `isHelpOpen` and `running` in one component.
- A prop handler is `onX`. The local function is `handleX`. X is the user intent (`onGroupChange`), not the DOM event (`onClickItem`).

Functions

- Name a function by what it returns: a boolean is `isX` or `hasX`, a message is `xMessage`, a list is a plural noun, a conversion is `toX`. An action with a side effect starts with a verb.
- Name a function after the rule it applies, not after its first caller (`completeTime`, not `fillOrderSearchTime`).

Constants

- One value, one name. Before you add a constant, search for its literal value. If a constant exists, import it.
- A module constant is `SCREAMING_SNAKE_CASE`. A default is `DEFAULT_X`. A bound pair is `X_MIN` and `X_MAX`.
- A constant that holds a server or legacy key is named after that key, not after a guess at its meaning (`ORDER_CTRL_CL` for a `ctrl_cl` value, not `ORDER_CLASS`).

Searches for the Names row (run each one on the scope, and name it in the row):

- `grep -nE "const (\{ )?(data|result|item|value)\b"` for bare generic variables.
- `grep -nE "const \[?(is|has|can|should)[A-Z]"` and the other booleans in the same file, to check one style.
- The sibling list of each folder, to check the file pattern and the file-to-export match.
- Each literal that a new constant holds, to find a second name for one value.

## Helpers

- Do not add a helper that is called once or that wraps one line. Write it inline at its one use, and keep the comment that explains the rule.
- Keep a helper when it is called many times, or when it names a business rule (a rounding rule, a legacy format).
- A validation check is not that exception. If the project already has a validator (a schema, a resolver, a shared field rule), add the case there. Do not add a helper that filters fields, calls `safeParse`, or wraps `min`, `trim`, or `startsWith`.
- Before you write a formatter or a reader, search the repo for one. Check its contract before you reuse it: a form-bound field needs a form context; a grid cell formatter may change dates.
- A helper moves to `shared/` only when a second consumer needs the same semantics. Two call sites that look alike but differ (`??` against `||`, a different key naming) are not the same semantics. Refactor them in a separate change, after you check the data source.
- When you do move it, move the pure function. A wrapper typed to one feature's record stays in that feature.
- A function with no business term (digit grouping, fraction cut, date to month, code–name label): search the project's shared lib (`shared/lib/number.ts`, `shared/lib/date.ts`) first. Reuse the existing one, or write the new one with it (`nameOfCode` calls `codeLabel`). Move it into the shared lib when a second consumer exists or the project rule says so. With one consumer, it stays in the screen.
- A screen `helpers/` file holds pure functions only. An import of React, `UseFormSetValue`, `setValue`, or a service in `helpers/` is a finding. Move that function to `hooks/`. Search: `grep -nE "from 'react'|setValue|services/" helpers/`.
- A grab-bag file (`*-format.ts`, `*-utils.ts`) that holds unrelated functions is a finding. Move each function to its owner (shared lib, rules file, schema), then delete the file.
- A parameter that the code already knows another way is dead input. `codePrefix` plus `.slice(0, 2)` when `classCode` already holds the class is a finding.
- Two helpers that do one job are one finding, even when the names differ (`toText` and `cellValue`, `numberRange` and `numberBetween`). Keep the older one. If the two check in a different order, the old system's order wins.
- Do not wrap a shared hook in a screen hook to add one option (a sort order, a hidden title). Add the option to the shared hook. A wrapper covers only the calls that go through it, so the next screen copies the gap.
- A normalizer (upper case, trim, number format) belongs to the field's validation rule. A component that calls `toUpperCase()` or `trim()` on input is a second rule nobody checks.
- Do not repeat a cleanup that an earlier step owns. A value that already went through the project's number preformatter does not get a second `.replace(/,/g, '')`. The second cleanup lets through input the first step rejects on purpose.

## Arguments and values

- No bare positional numbers or booleans at a call site. `cell('Size', 'size', { span: 2 })`, not `cell('Size', 'size', 2)`.
- No magic sentinel values. Use `null`, not `''` or `-1`, for "nothing".
- Tag a union with a `kind` field. Do not tell variants apart with `'field' in value`.
- A new holder for a value that already has one is a finding under `rules/reuse-duplication.md`. That rule is the one statement of this check.

Props of a shared component

- A new prop must do something no existing prop does. Name the existing prop you checked. `isNumber` next to `type` is a finding: pass `type="number"`.
- Two or more props with overlapping meaning (`disabled`, `readOnly`, `lookupWhenReadOnly`) are a finding. Say what each one does differently, or merge them.
- A prop the component does not render or read is a finding.
- A new prop that only adds an `if/else` around existing output is a finding. Use the existing slot (`children`, `body`) or a variant.
- Before you change a shared component for one screen, prove the current behavior is wrong. Do not rewrite code that already works (a `messages.map` replaced by a `join`).

## Types and schemas

- Declare every field of an API record with its own type. Reject a loose record (`z.record(...)`, `Record<string, unknown>`) and a shared alias for every field (`Cell`) when the shape is known.
- Take the field list from the source that produces it (the SQL, the API resource, the generated client). Then compare it with a real response: no missing key, no extra key.
- Take each type from real data, not from the database column type. Many drivers return numbers and dates as strings.
- A key that the server sets only when it has a value is `.optional()`.
- Export `keyof` of the record and use it wherever code names a field. A typo then fails type-check instead of rendering a blank cell.
- Use the strict type: an integer is `z.number().int()`, a flag is `z.boolean()`. A record where every field is `z.string().optional().nullable()`, or `string | number`, or a flag as `'1'`/`'0'`, is a loose record. A renamed server field then passes the schema and the screen shows blank with no error.
- Use the project's shared schemas for shared shapes: dates, option lists (`{ value, label }`), sessions. Do not declare them again in the screen schema.
- One name set for the response and the form. Two name sets (DB column names in the response, business names in the form) need a mapping file, and each new field changes three places.
- Do not declare a field again in a second schema of the same file. Derive with `.pick()` or `.extend()`.
- Write each label once. A label typed in the field rule and again in a required check drifts.
- Write a required check as a table (`[field, label]` per mode), not as one call per field.
- A check table is the one list. Do not put a schema over it: when the fields are already typed and the check only builds the form's messages, a schema restates the same table and every new field joins both. Add the rule to the table. Use a schema where you parse untrusted input and need the parsed value, the inferred type, or the shape guarantee. A check over values the form already typed needs none of the three.
- Do not turn a missing field into a valid one. `(values[field] ?? '')` makes an absent required field pass with no message. Fail on absence, or write why absence is valid.
- `(values[field] ?? '').startsWith(' ')` is a finding even when no schema exists and even when the message only names a leading space. `undefined`, `null`, and `""` all become `''`, and `''.startsWith(' ')` is false, so the helper returns no error. Those three need the empty message, or the check must say why each one is valid. Do not coerce them to `''` before a predicate that is false for `''`.
- Judge the cases, not the library. Do not require a schema. A table, a predicate, or a schema is fine when it is the only place the cases live. A check that passes a case its message rejects is a finding. `startsWith(' ')` lets `""` and `"ABC "` through, so it is not the rule "no empty, no space at either end". The message and the predicate must name the same cases.
- Use the validator the project already has. A new function whose job is to validate is a finding when that tool exists. Name the tool you checked. If none exists, keep one table or one schema at the owner. Do not add a helper beside it.
- A library type error is not a user message. `undefined` must get the empty message, or the check must say why absence is valid.
- One code per field is the limit of a `[field, code]` table. `filter` then `map` reports the first rule only, so a second rule for that field never fires. Widen the entry to a code list on the day the field needs one.
- Narrow before you check. `startsWith`, `trim`, and `toUpperCase` run on a string, and a `string | number` value throws at the first non-string.
- Constrain the table with types: the field slot against `keyof Values`, the code slot against the message-key union. A typo'd code otherwise reaches `t()` and renders the key itself.
- Declare form fields in screen order. Then error order needs no extra list.
- Follow the sibling schema files: the same section order, the same re-exports. Input types live in the schema, not in the service.
- Count the field lists a new field must touch (schema, form, mapping, date list, order list). More than one is a finding on the Extension lens.

## Files

- One file answers one question:
  - builders: types and the functions that describe the UI ("write it with what"),
  - layout or config: data only ("what is in it"),
  - component: rendering, class names, props types, loading / error / empty states ("how it looks").
- A data file holds no JSX and no class names. A component file holds no field list.
- Props types and class constants sit next to the component that uses them. Do not split them into `types.ts` or `constants.ts` for one consumer.
- Keep the folder flat while it is small. Do not add a sub-folder for three files.
- Imports go one way (component → layout → builders). No cycle.
- A page folder has only the sub-folders the project's page rule names. A sub-folder the rule does not name (`hooks/`, `helpers/`) is a finding. Move the code, or add the pattern to the rule in the same change.
- When the rule names those sub-folders, each holds one kind of code:

  | Folder | Holds | Never holds |
  |---|---|---|
  | `components/` | JSX | `setValue`, a direct API call |
  | `hooks/` | form behavior: `setValue`, `useWatch`, look up then fill | JSX |
  | `helpers/` | pure business rules of the screen | React, API, `setValue` |
  | `schemas/` | record and form types, zod, constants of the data, search state | handlers, props types |
  | `shared/lib/` | functions with no business term, used by two or more consumers | a screen term |
  | `services/`, `hooks/queries/` | API calls | form logic |

- Search params and their types live in `schemas/`, not in `helpers/`.
- A file that holds only one or two constants (`*-cells.tsx`) merges into the file that uses them.
- Inside a screen folder, import with a relative path (`./order-form-fields`, `../helpers/order-rules`). Outside the screen, use the project alias (`@/`). The project rule wins when it differs.
- A new convention (folder, suffix, layer) goes into the project rule file (`rules/*.md`, `AGENTS.md`) in the same change. A convention that lives only in code is lost on the next screen.

## Form screens

`n/a` when the scope has no large form. A large form has more than one visible block, or a lookup popup.

Split

- Split components by the blocks the user sees, in screen order: search → main info → detail → list → action buttons.
- Use the suffix for the role: `-panel` for a large block, `-section` for a group inside a panel, `-operation-panel` for the button row, `-search-form`, `-table`, `-columns` for search and list. Follow the exemplar screen when one exists.
- Each block owns three things: its fields, its lookup popup, and "this field changes, so that field changes". A finding is any of the three that sits in the parent form.
- The parent form holds only `useForm`, `FormProvider`, the submit hook, form-level effects (load server data into the form, not a watcher that calls `setValue`), and the blocks. A `useWatch`, a catalog hook, popup state, or a lookup hook in the parent form is a finding. Name the file after its role (`-detail-form.tsx`), not `-index.tsx`.
- A value every block needs (the money scale of the currency) is computed once in the parent form and read through context. Do not pass it down through many props.

Popups

- Popup open state lives in the block that has the search button. `useState(picker)` in the parent form is a finding.
- A single "picker" component that switches on a type to render many popups is a finding. Each block renders its own popup.
- Popup arguments come from the block's props (`act` from `role`: customer = 1, others = 2).

Lookup hooks

- One lookup hook per master (`use-<screen>-lookup-item`, `use-<screen>-lookup-customer`). One hook for every master is a finding.
- A lookup hook looks up and fills. It does not take `openPicker` or open UI. The block opens the popup.
- A lookup hook guards against a late response. When the user types a new code before the old response returns, the old response does not overwrite the field.

Field updates

- No `setValue` in JSX. A default date, a derived month, a status flag, or a copy to another field inside an inline `onChange` is a finding. Search: `grep -n "setValue" components/`.
- Put those updates in a fill hook (`use-<screen>-fill-<block>-fields`) that returns handlers. The block writes `onChange={handlers.x}`.
- A field derived from other fields updates for every input value, the cleared value too. A rule that returns `null` for a blank input, with a caller that then skips the update, keeps the old derived value on screen. Return the state for blank (often the default). When the spec or CR names only the filled cases, list the blank case and ask.
- A switch of record or scope resets every value that belongs to the old scope. A guard such as "same key, skip the reload" also compares the mode: one record after all records is a switch even when the key is the same. Defaults computed for the old scope do not carry into the new one.
- Export only what another file imports. When many files use one block, give it its own file. Do not export from a component file to share it.
- Group a rules file by data (order, item, customer), not by screen. A `// <screen id>` heading in a shared rules file is a finding.
- A length limit of one input is not a validation rule. Keep it with the screen's other max lengths.
- A declared rule, message key, schema field, or SQL file that nothing uses is a finding: use it or delete it. When you replace a message key, check that the old key still has a caller.
- Delete a comment that repeats the code or says nothing. A doc comment sits on the symbol it describes.

## Make it shorter

Count before you shorten. Name the repeated call and how many times it repeats.

- Shorten: a wrapper call repeated dozens of times (make a string mean "read this field"); a wrapper array around every item; two identical handlers.
- Repeated calls that differ only by data follow `rules/reuse-duplication.md`. Count them in this row.
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
- Port the behavior of the old screen, not the way it stored data. Some old checks only tell apart two kinds of value in one field: a code or its label, a raw value or a formatted one (`length() == 2`, `substring(0, 2)`). When the new state keeps those kinds apart, the check has nothing to tell apart. Do not port it. Before you port an old branch, write why the old system needs it, then show that this reason still exists in the new state. A comment that only names the old line is not a reason.
- Port each default the old screen sets on load, with its condition. List every assignment in the old init or load branch (`setValue`, a `value=` in the template) and the branch it sits in: new or edit mode, first load only, one record or all records. A missing default leaves a box blank. A default without its condition fills a box the old screen left blank.
- Take the display text of a code from the old loader, not from taste. Read the line that builds the label (code only, name only, or code plus separator plus name) and show the same text.
- A check that reads the raw typed text runs before any normalizer. When the old screen tests the first character, a leading space, or a full-width letter, and the shared field rule trims or converts it first, the check can never fail. Run that check on the raw value, before the field rule, in the old order.
- How the old screen shows a result is behavior. A one-time `alert()` stays a dialog the user closes. Do not move it into a block that stays on screen. A project rule that sends every result to one block does not cover a message the old screen showed as an alert. Name the conflict and ask.
- Handle a user event in the field's `onChange` or the submit handler. An effect that watches a value and calls `setValue` is a finding.
- Correct behavior must not depend on the order of children in JSX or the order of effects. If one block must run after another, call them in order from one handler.

## Verify

- Run the project's format, type-check, lint, and structure checks after each change.
- Run the UI for real. For a refactor that must not change output, capture the screen before and after, and compare the image and the text byte for byte. A difference blocks "done" until you explain it.
- Prove the comparison can fail: compare two states that differ, and expect a difference.
- When test data lacks a case, force it in the response with request interception.
- For a form screen refactor, run the production build (`vite preview` or the equivalent), not only the dev server. Walk each flow: create to save to complete, edit (load, change a row, invalidate), every lookup button one by one, a lookup with the field blank, and special data (a foreign currency).
- For a refactor that claims fewer renders, record React Profiler before and after: open a popup, run a lookup. Report the count of components that render.
- When a new type should catch mistakes, add a throwaway file with a mistake, confirm type-check fails, then delete the file.
- Stop any dev server you started. Report each command and its exit code.

## Working in a shared tree

- Someone may edit or commit the same files while you work. Read a file again before you edit it. Keep their change.
- An editor diagnostic shown between two edits can be stale. Trust the type-check command.
