---
name: fe-kit
description: "Architecture-first ownership, reuse-first authoring, React performance checks, a senior audit (reuse, architecture, operational flow, error handling, load, extension), and flagged, separated feature isolation for new behavior added to existing UI, before or during frontend work. Use before implementing or refactoring non-trivial UI, components, hooks, forms, data fetching, or feature state. Use when fixing a frontend bug or a symptom report with wrong behavior, even without the word fix. Use when reviewing a frontend diff before commit. Also use for Vietnamese requests such as implement UI, refactor component, viết frontend, viết component, sửa lỗi, tổng sai, màn hình trắng, review màn, review diff trước commit, or audit kiến trúc. Do not use for a one-line fix, a pure styling tweak, or non-frontend work."
---

# FE Architecture, Reuse, Performance

Run this skill before implementing or refactoring non-trivial frontend work (components, hooks, forms, data fetching, feature state).

Do not write code until ownership and reuse decisions are recorded.

Pick one playbook. Read that file from this skill directory. On omp, use `skill://fe-kit/playbooks/<file>`. Do not read the other playbooks.

| Task | Playbook |
|---|---|
| New component, page, form, or hook | `playbooks/new-ui.md` |
| Wrong behavior, a wrong value, a broken flow, or a symptom report | `playbooks/fix-bug.md` |
| A frontend diff before commit. The author does not run this. | `playbooks/review-diff.md` |
| Split, move, or restructure existing UI | `playbooks/refactor-ui.md` |
| Waterfall, bundle, rerender, or list jank | `playbooks/perf-ui.md` |
| Check, review, clean up, or shorten existing UI | `playbooks/review-ui.md` |

If you wrote the diff, do not open `playbooks/review-diff.md`. Hand the diff to agent `fe-kit:reviewer` on Claude Code, or to a fresh omp context whose only task is the diff range and `skill://fe-kit/playbooks/review-diff.md`. Do not include your notes. That reviewer follows the playbook and does not spawn another reviewer. If you were given only the diff and the playbook path, you are that reviewer. If you cannot start the reviewer, stop. Do not write the verdict.

The playbook names the reference files. Do not read a reference it does not name.

Skip every playbook for a one-line fix, a pure style tweak, or work that is not frontend. Say why. One-line is defined by behavior in `rules/fe-implementation.md`: any change that alters runtime behavior is not one-line, however few lines it touches.

## Fields

### 1. Architecture Ownership

Record these after the playbook tells you to read `references/ownership.md`.

- Runtime owner
- First-fix owner
- Canonical long-term owner
- Competing owners that are wrong
- Cleanup direction

### 2. Reuse-first Authoring

Record these after the playbook tells you to read `references/reuse.md`.

Produce:

- Responsibility
- Exemplar (if any) and why it matches or does not
- Decision: `reuse` | `extend` | `feature-local` | `shared`
- Concrete gaps
- Why this shape
- Feasibility notes

### 3. Performance Check

Record these after the playbook tells you to read `references/performance.md`. Check in this order: waterfalls, bundle, data fetching, re-renders, rendering.

Produce:

- Waterfalls
- Bundle / imports
- Data fetching
- Re-renders
- Loading / error / empty handling
- Remaining risk

### 4. Code Quality

Record these after the playbook tells you to read `references/code-quality.md`.

Fill the sweep table in that file. One row for each heading from Names through Design and behavior. A blank row is not done. A `clean` row with no search is not done. A review does not fill this table. It writes each finding in the report in `playbooks/review-ui.md`.

### 5. Senior Audit

Record this after the playbook tells you to read `references/audit.md`.

Fill the Audit table in that file. One row for each lens, from Reuse through Extension. Each finding names `file:line`, a severity (`high`, `medium`, `low`), and the cost if it stays. A `clean` row with no search is not done. A review does not fill this table. It writes each finding in the report in `playbooks/review-ui.md`.

### 6. Feature Isolation

Record this only after the playbook tells you to read `references/feature-isolation.md`, and only when the task adds new behavior to existing UI. Otherwise write `n/a` and say why. A bug fix or a pure refactor never gains a flag from this section.

Fill the table in that file: one flag (default = old behavior), read once at the entry owner, new logic in its own files, existing files touched only at a listed seam, and a deletion test.

### 7. Verify

Before finishing:

- Trace the change across callers, hooks, and helpers.
- Challenge duplicated state, validation, or data resolution.
- Confirm the code lives in the canonical owner.
- Confirm the reuse decision still holds.
- Confirm loading, error, and empty states are handled where the data or action is owned.
- Confirm props and types are narrow enough for the responsibility.
- Confirm interactive elements have accessible names and keyboard support where relevant.
- Confirm list keys are stable.
- Confirm no new dependency or second validation/state path was introduced without justification.
- Mention unrelated problems instead of silently expanding the change. Still list every in-scope code-quality finding. Do not save them for another run.
- For a change that must not alter output, compare the screen before and after, byte for byte.
- Do not finish while a code-quality row is blank, when the playbook asks for that table.
- Do not finish while an audit row is blank, when the playbook asks for the audit.

## Output Template

Use this structure. Fill every section. Do not leave sections blank.

A screen review uses the Vietnamese template in `playbooks/review-ui.md` and then stops. A diff review is not written by the author. The fresh reviewer uses the template in `playbooks/review-diff.md` and then stops. Do not also fill the template below.
```md
## Architecture
- Runtime owner:
- First-fix owner:
- Canonical long-term owner:
- Competing wrong owners:
- Cleanup direction:

## Reuse Decision
- Responsibility:
- Exemplar:
- Decision: reuse | extend | feature-local | shared
- Gaps:
- Why this shape:
- Feasibility notes (constraints, missing pieces):

## Performance
- Waterfalls:
- Bundle / imports:
- Data fetching:
- Re-renders:
- Loading / error / empty handling:
- Remaining risk:

## Code Quality
Files in scope:
| Rule | Search | Verdict |
| Names | | |
| Helpers | | |
| Arguments and values | | |
| Types and schemas | | |
| Files | | |
| Form screens | | |
| Make it shorter | | |
| Design and behavior | | |

## Audit
| Lens | Search or trace | Finding (file:line) | Severity | Cost if it stays |
| Reuse | | | | |
| Architecture | | | | |
| Operational flow | | | | |
| Error handling | | | | |
| Performance and load | | | | |
| Extension | | | | |

## Feature Isolation
| Item | Value |
| Flag (name, source, default) | |
| Read at (one entry owner) | |
| New files | |
| Existing files touched (seam) | |
| Off-path guarantee | |
| Deletion test | |
| Flag owner / removal date | |

## Departures / Notes
-
```

## Hard Rules

- Before adding or changing code, follow `rules/reuse-duplication.md`.
- A review's only user-facing output is the Vietnamese report in `playbooks/review-ui.md`, or the diff report in `playbooks/review-diff.md` when a fresh reviewer writes it. Kết luận is first for a screen review. The diff report's Verdict is first for a diff. Then stop. Do not fill the template below. Do not re-read the tree to rewrite the report.
- Do not write implementation code until the Architecture and Reuse Decision sections are filled. A review records the reuse decision under Dùng lại, and a wrong owner under Việc nên làm, instead of those sections.
- Do not grade a frontend diff you wrote. Hand it to `fe-kit:reviewer` or a fresh context that reads `playbooks/review-diff.md`. A one-line fix or a pure style tweak skips this.
- Never invent a new shared component or hook just because it might be useful later.
- Never bypass a project wrapper to use the lower-level primitive it owns.
- Never place code in a layer that does not own the responsibility.
- Never import upward. Shared and domain code must not import from features or pages.
- Prefer the smallest understandable change that keeps ownership correct.
- If the existing codebase is inconsistent, follow the canonical owner, not the nearest bad example.
- Do not leave loading, error, or empty states unhandled when the component owns data or an action.
- Do not use vague file or component names. The name reflects the responsibility.
- Do not introduce a new library or a second form, validation, or state path when one already exists.
- Do not copy server or query data into local state just to display it.
- Do not expand the change to fix unrelated problems. Mention them instead.
- Do not ship interactive UI without an accessible name when the element is actionable.
- Do not add a helper used once, a bare positional number, or a generic name (`model`, `utils`, `sheet`).
- Do not finish a code-quality pass after the first findings. On a review, every in-scope finding goes in the report in the same turn. On any other playbook, fill every rule row in the same turn.
- Do not leave the named folder when a file name matches another file. Review every file in that folder.
- Do not type a known API record as a loose map. Declare each field.
- Do not add a schema over a check table that already holds the rule, and do not let `?? ''` turn a missing required field into a pass. Do not require a schema. Do not pass a case the message rejects. Do not coerce `undefined`, `null`, or `""` with `?? ''` before a check that is false for `''`.
- Do not add a validation helper when the project already has a validator. Add the case to that schema, resolver, or field rule.
- Do not keep one value under two names, or one rule in two places. Search the literal value first.
- Do not re-label or re-map server values in the client. Show the server value and report the server defect.
- Do not leave a bare `data` or `result` at component scope. Rename it after what it holds.
- Do not add polling without a stop condition and a written worst-case request rate.
- Do not add new behavior to existing UI without one flag whose default is the old behavior. Read the flag once at the entry owner. Do not invent a second flag system when the project has one.
- Do not interleave new logic into existing files. New logic lives in its own files under the owning feature; an existing file changes only at a listed seam, and deleting the new files plus the seam restores the old path.
- Never gate a bug fix, a security fix, or a pure refactor behind a feature flag.
- Do not add a prop, flag, or wrapper when an existing prop, slot, or shared hook already does the job. Name the one you checked.
- Do not rewrite shared code that already works to fit one screen.
- Compare a screen with its exemplar screen (query, cache, lock, service). Record each difference and its reason.
- Split a large form by the blocks the user sees. Each block owns its fields, its lookup popup, and its dependent field updates. The parent form only composes.
- Do not write `setValue` in JSX. Do not put React, `setValue`, or an API call in `helpers/`.
- Do not rename a name that is not wrong.

## Common Mistakes

| Mistake | Correct behavior |
|---------|------------------|
| Copy the nearest similar component | Check ownership and contract first. Reject a mismatch. |
| Create `shared/` for one use | Keep feature-local until two real consumers exist. |
| Put business logic in a page or UI component | Move it to the feature or domain owner. |
| Dump feature components into global `components/` | Colocate them inside the feature. |
| Import upward (shared imports a feature) | Reverse the dependency or move the code. |
| Boolean prop explosion | Prefer composition or explicit variants. |
| Vague names (`utils`, `helper`, `New`) | Name the file after the responsibility. |
| Add memo everywhere | Add it only when it cuts a real cost or clarifies a boundary. |
| Derive state in `useEffect` | Compute the value during render. |
| Copy server data into `useState` | Read from the query cache. Keep client state for UI intent only. |
| Introduce a second form or validation path | Reuse the project's existing approach. |
| Create a barrel `index.ts` | Import directly. Do not add a new barrel. |
| `key={index}` on a dynamic list | Use a stable id. |
| Skip loading, error, or empty | Handle those states where the data or action is owned. |
| Skip an accessible name on a button or input | Add a label or `aria-label`. |
| Expand scope to fix nearby code | Keep the change surgical. Mention unrelated issues. |
| Skip recording the decision | Fill the output template first. |
| Add a helper for one call site | Write it inline. Keep the comment. |
| `fn(x, 2)` with a bare number | Name it: `fn(x, { span: 2 })`. |
| `z.record(...)` for a known response | Declare each field from the server source. |
| Shorten by building names from a prefix | Keep full names so a search finds them. |
| Same calls repeated, only the data changes | `rules/reuse-duplication.md`. |
| Stop after the first findings | On a review, put every in-scope finding in the report. On any other playbook, fill every rule row in the same pass. |
| Follow a colliding name out of the folder | Stay in the named folder. Open every path there. |
| `const { data } = useX()` at component scope | Rename it: `const { data: options } = useX()`. |
| `isHelpOpen` next to `running` in one file | One boolean style per file: `isRunning`. |
| File `x-loader.ts` that holds options and labels | Name the file after what it holds, or move it into the schema that owns it. |
| Same literal (`'23:59:59'`) under two constants | Keep one constant at its owner. Import it. |
| Client map of server labels or status names | Show the server label. Keep a fallback for an unknown value. |
| Second watcher, download path, or error block for one flow | Reuse the first one, or record why it must differ. |
| Polling every row with no rate estimate | Write rows × polls per minute. Stop polling when the run ends or fails. |
| "It works" as the review verdict | Say what is wrong, where, what to do, and what it costs if it stays, in the voice of `playbooks/review-ui.md`. |
| Grade the diff you just wrote | Hand it to `fe-kit:reviewer` or a fresh context. Do not write the verdict. |
| New behavior woven into the old component, always on | Isolate it in new files behind one flag, default off. One seam in the old file. |
| Flag read in every leaf component | Read it once at the entry owner. Pass a boolean down. |
| `if (flag) useNewHook()` | Mount the new component only when on, or pass `enabled: flag`. Never call a hook conditionally. |
| Flag with no owner or expiry | Name the owner and the removal date or ticket. Delete flag and dead path after rollout. |
| `isNumber` prop next to `type` | Pass `type="number"`. A new prop does what no existing prop does. |
| `disabled`, `readOnly`, and a third read-only prop on one field | Say what each does differently, or merge them. |
| Screen hook that wraps a shared hook to add one option | Add the option to the shared hook. Delete the wrapper. |
| Every response field `string().optional().nullable()`, flags as `'1'`/`'0'` | Strict types: `number().int()`, `boolean()`, shared date and option schemas. |
| A zod schema built to restate a `[field, code]` check table | The table is the one list. Add the rule there, or to the schema that already owns the field. |
| `(values[field] ?? '')` inside a required check | An absent field passes with no message. Fail on absence. |
| `(values[field] ?? '').startsWith(' ')` | `undefined`, `null`, and `""` pass with no message. That helper is a finding even when no schema exists yet. |
| `startsWith(' ')` while the message forbids empty or space at either end | The predicate must reject every case the message names. One table or one schema, not both. |
| A helper that filters fields or wraps `safeParse` next to an existing schema | Add the case to that validator. Delete the helper. |
| `isClosed` state when `status` already says closed | `rules/reuse-duplication.md`. Read `status`. |
| DB names in the response, business names in the form, a mapping file between | One name set for both. |
| A new field must join four hand-kept lists | One source: the schema, declared in screen order. |
| Label/value grid rebuilt inside the page | Use the shared form layout. Extend it if the design needs more. |
| Effect watches a value and calls `setValue` | Handle it in `onChange`. Do not rely on child order. |
| `toUpperCase()` on input in a component | Put the normalizer in the field rule. |
| `status === 500` or an HTTP error type in a component | Call the project's one error classifier. |
| `// <screen id>` heading in a shared rules file | Group by data. Move the rules to their data group. |
| Message key replaced, old key left | Delete the old key when nothing calls it. |
| `useState(picker)` and one `master-picker.tsx` in the parent form | Each block holds its own popup state and renders its own popup. |
| Lookup hook takes `openPicker` | The hook looks up and fills. The block opens the popup. |
| One lookup hook for every master | One hook per master. Guard against a late response. |
| `setValue` inside an inline `onChange` in JSX | Move it to a `use-<screen>-fill-<block>-fields` hook. The block writes `onChange={handlers.x}`. |
| `setValue` or React in `helpers/` | Move the function to `hooks/`. `helpers/` holds pure functions. |
| `*-format.ts` grab bag in a screen | Move each function to its owner (shared lib, rules, schema). Delete the file. |
| `useWatch` or a catalog hook in the parent form | Call it in the block that reads it. |
| `use-order-actions`, `use-order-invalid` | Start with a verb: `use-order-request-action`, `use-order-mark-invalid`. |
| "Fewer renders" with no numbers | Record React Profiler before and after. |
| New folder or suffix convention only in code | Write it in the project rule file in the same change. |
