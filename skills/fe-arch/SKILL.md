---
name: fe-arch
description: "Architecture-first ownership, reuse-first authoring, React performance checks, and a senior audit (reuse, architecture, operational flow, error handling, load, extension) before or during frontend work. Use before implementing or refactoring non-trivial UI, components, hooks, forms, data fetching, or feature state. Also use for Vietnamese requests such as implement UI, refactor component, viết frontend, viết component, review màn, or audit kiến trúc. Do not use for a one-line fix, a pure styling tweak, or non-frontend work."
---

# FE Architecture, Reuse, Performance

Run this skill before implementing or refactoring non-trivial frontend work (components, hooks, forms, data fetching, feature state).

Do not write code until ownership and reuse decisions are recorded.

Pick one playbook. Read that file from this skill directory. On omp, use `skill://fe-arch/playbooks/<file>`. Do not read the other playbooks.

| Task | Playbook |
|---|---|
| New component, page, form, or hook | `playbooks/new-ui.md` |
| Split, move, or restructure existing UI | `playbooks/refactor-ui.md` |
| Waterfall, bundle, rerender, or list jank | `playbooks/perf-ui.md` |
| Check, review, clean up, or shorten existing UI | `playbooks/review-ui.md` |

The playbook names the reference files. Do not read a reference it does not name.

Skip every playbook for a one-line fix, a pure style tweak, or work that is not frontend. Say why.

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

Fill the sweep table in that file. One row for each heading from Names through Design and behavior. A blank row is not done. A `clean` row with no search is not done.

### 5. Senior Audit

Record this after the playbook tells you to read `references/audit.md`.

Fill the Audit table in that file. One row for each lens, from Reuse through Extension. Each finding names `file:line`, a severity (`high`, `medium`, `low`), and the cost if it stays. A `clean` row with no search is not done.

### 6. Verify

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
- Do not finish while a code-quality row is blank.
- Do not finish while an audit row is blank, when the playbook asks for the audit.

## Output Template

Use this structure. Fill every section. Do not leave sections blank.

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

## Departures / Notes
-
```

## Hard Rules

- Never invent a new shared component or hook just because it might be useful later.
- Never bypass a project wrapper to use the lower-level primitive it owns.
- Never place code in a layer that does not own the responsibility.
- Never import upward. Shared and domain code must not import from features or pages.
- Prefer the smallest understandable change that keeps ownership correct.
- If the existing codebase is inconsistent, follow the canonical owner, not the nearest bad example.
- Do not write implementation code until the Architecture and Reuse Decision sections are filled.
- Do not leave loading, error, or empty states unhandled when the component owns data or an action.
- Do not use vague file or component names. The name reflects the responsibility.
- Do not introduce a new library or a second form, validation, or state path when one already exists.
- Do not copy server or query data into local state just to display it.
- Do not expand the change to fix unrelated problems. Mention them instead.
- Do not ship interactive UI without an accessible name when the element is actionable.
- Do not add a helper used once, a bare positional number, or a generic name (`model`, `utils`, `sheet`).
- Do not finish a code-quality pass after the first findings. Fill every rule row in the same turn.
- Do not leave the named folder when a file name matches another file. Review every file in that folder.
- Do not type a known API record as a loose map. Declare each field.
- Do not keep one value under two names, or one rule in two places. Search the literal value first.
- Do not re-label or re-map server values in the client. Show the server value and report the server defect.
- Do not leave a bare `data` or `result` at component scope. Rename it after what it holds.
- Do not add polling without a stop condition and a written worst-case request rate.

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
| Stop after the first findings | Fill every rule row in the same pass. Name the search for each row. |
| Follow a colliding name out of the folder | Stay in the named folder. Open every path there. |
| `const { data } = useX()` at component scope | Rename it: `const { data: options } = useX()`. |
| `isHelpOpen` next to `running` in one file | One boolean style per file: `isRunning`. |
| File `x-loader.ts` that holds options and labels | Name the file after what it holds, or move it into the schema that owns it. |
| Same literal (`'23:59:59'`) under two constants | Keep one constant at its owner. Import it. |
| Client map of server labels or status names | Show the server label. Keep a fallback for an unknown value. |
| Second watcher, download path, or error block for one flow | Reuse the first one, or record why it must differ. |
| Polling every row with no rate estimate | Write rows × polls per minute. Stop polling when the run ends or fails. |
| "It works" as the review verdict | Fill the Audit table. Name the cost of each finding later. |
