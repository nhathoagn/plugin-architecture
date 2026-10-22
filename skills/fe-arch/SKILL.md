---
name: fe-arch
description: "Architecture-first ownership, reuse-first authoring, and React performance checks before frontend implementation. Use before implementing or refactoring non-trivial UI, components, hooks, forms, data fetching, or feature state. Also use for Vietnamese requests such as implement UI, refactor component, viết frontend, or viết component. Do not use for a one-line fix, a pure styling tweak, or non-frontend work."
---

# FE Architecture, Reuse, Performance

Run this skill before implementing or refactoring non-trivial frontend work (components, hooks, forms, data fetching, feature state).

Do not write code until ownership and reuse decisions are recorded.

Read each reference from this skill directory. On omp, use `skill://fe-arch/references/<file>`. Do not load the other reference files until their step.

## Required Order

1. Architecture Ownership. Read `references/ownership.md`.
2. Reuse-first Authoring. Read `references/reuse.md`.
3. Performance Check. Read `references/performance.md`.
4. Verify.

Skip a step only when it clearly does not apply, and state why.

## Workflow

### 1. Architecture Ownership

Read `references/ownership.md` and produce:

- Runtime owner
- First-fix owner
- Canonical long-term owner
- Competing owners that are wrong
- Cleanup direction

### 2. Reuse-first Authoring

Read `references/reuse.md`. Only after the canonical owner is known, decide how to implement inside that boundary.

Produce:

- Responsibility
- Exemplar (if any) and why it matches or does not
- Decision: `reuse` | `extend` | `feature-local` | `shared`
- Concrete gaps
- Why this shape
- Feasibility notes

### 3. Performance Check

Read `references/performance.md`. Check in priority order: waterfalls, bundle, data fetching, re-renders, rendering.

Produce:

- Waterfalls
- Bundle / imports
- Data fetching
- Re-renders
- Loading / error / empty handling
- Remaining risk

### 4. Verify

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
