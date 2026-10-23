---
name: fe-arch
description: "Architecture-first ownership, reuse-first authoring, and React performance checks before frontend implementation. Use before implementing or refactoring non-trivial UI, components, hooks, forms, data fetching, or feature state. Also use for Vietnamese requests such as implement UI, refactor component, viết frontend, or viết component. Do not use for a one-line fix, a pure styling tweak, or non-frontend work."
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

Produce:

- Names
- Helpers and reuse
- Arguments and values
- Types and schemas
- File split
- Verification plan

### 5. Verify

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
- Note any departure, feasibility constraint, and remaining maintenance cost.
- Mention unrelated problems instead of silently expanding the change.
- For a change that must not alter output, compare the screen before and after, byte for byte.

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
- Names:
- Helpers and reuse:
- Arguments and values:
- Types and schemas:
- File split:
- Verification plan:

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
- Do not type a known API record as a loose map. Declare each field.

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
