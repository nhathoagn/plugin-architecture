# React Performance Checks

Apply in priority order. Fix higher-impact issues before lower ones.

## 1. Eliminating Waterfalls (CRITICAL)

- Check cheap sync conditions before awaiting flags or remote values.
- Move `await` into the branch where the value is actually used.
- Use `Promise.all` (or the equivalent) for independent operations.
- Start promises early. Await them late.
- Hoist fetches to the highest common owner. Avoid sequential child fetches.
- Use Suspense boundaries to stream content when the stack supports it.

## 2. Bundle Size (CRITICAL)

- Import directly. Avoid barrel files that pull unused code.
- Prefer statically analyzable import paths.
- Use dynamic import or `next/dynamic` (or the equivalent) for heavy components.
- Defer non-critical third-party libraries (analytics, logging) until after hydration or the first interaction.
- Load modules only when the feature is activated.
- Do not create new `index.ts` barrels that re-export everything for convenience.

## 3. Data Fetching

- Prefer the project's existing query or cache pattern (React Query, SWR, server components, or the equivalent).
- Avoid duplicate fetches of the same data.
- Keep server and client boundaries clear. Minimize data serialized to the client.
- Do not copy query or server data into `useState` just to render it.
- Deduplicate global event listeners. Use passive listeners for scroll where appropriate.

## 4. Re-render Optimization (MEDIUM)

- Do not subscribe to state that is only used in callbacks.
- Extract expensive work into a memoized component only when that cuts a real cost or enables an early return.
- Hoist default non-primitive props so they do not create a new reference every render.
- Use primitive dependencies in effects when possible.
- Derive values during render. Do not sync derived state in `useEffect`.
- Use functional `setState` when it removes unstable dependencies.
- Pass a function to `useState` for an expensive initial value.
- Do not define a component inside another component.
- Use `startTransition` or `useDeferredValue` for a non-urgent update that should not block input.
- Do not add `memo`, `useMemo`, or `useCallback` by default.

## 5. Rendering Performance (MEDIUM)

- Virtualize a long list, or use `content-visibility`, when appropriate.
- Extract static JSX outside the component when it does not depend on props or state.
- Use stable list keys. Do not use `key={index}` when items can reorder, filter, or be inserted.
- Prefer a ternary over `&&` for conditional render when the false case can be a falsy number or string.
- Animate a wrapper element rather than an SVG element directly.

## Concrete Anti-Patterns to Reject

- A default object or array prop that creates a new reference every render.
- A `useEffect` that only syncs derived state.
- A fetch in a child when the parent already has the data, or can have it.
- An import from a barrel file that pulls unused code.
- A new convenience barrel.
- Memoization without a measured or clear cost reason.
- An unstable list key (`key={index}` on a dynamic list).
- Query or server data copied into `useState` just to render it.
- A component defined inside another component.

## Rules

- Do not add memoization by default. Add it only when it cuts a real cost or enables a clearer boundary.
- Prefer deriving a value during render over syncing it with `useEffect`.
- Keep an effect small, and use it only for a true side effect or an integration boundary.
- Report remaining performance risk, and whether that risk is acceptable for this change.
