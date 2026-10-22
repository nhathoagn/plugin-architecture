# Reuse-First Authoring

Optimize for the smallest understandable change. Reuse behavior and ownership, not merely similar syntax.

## Discover Before Writing

1. Identify each responsibility the change needs: visual primitive, interaction, data access, state ownership, validation, formatting, navigation, or domain policy.
2. Read repository instructions and any project capability catalog.
3. Find the nearest compatible implementation and trace its callers. Who loads and narrows data, owns state, validates, submits, and handles failure.
4. Inspect candidate contracts and representative usage, including variants, lifecycle, accessibility, and composition.
5. Establish which ownership pattern fits and which requirement demands a departure.

Directory listings and name matches are leads, not completed discovery.

## Precedence

Use this order when responsibilities match:

1. An established project semantic component, adapter, generated client, or domain boundary.
2. An existing feature or domain implementation with the same behavior and ownership.
3. An extension to an existing local boundary when the new behavior fits its responsibility.
4. An installed library primitive when no project boundary owns that responsibility.
5. A new feature-local implementation.
6. A new shared abstraction only after real consumers (at least two independent ones) demonstrate a stable shared contract.

## Record the Decision

Before implementation, identify:

- Exemplar, if any, and why it matches or does not
- Decision: `reuse` | `extend` | `feature-local` | `shared`
- Concrete gaps
- Why not a simpler composition
- Feasibility notes (constraints, missing pieces)

For each proposed abstraction, compare direct composition and extension of the existing boundary. Extract only when the new boundary improves coherence enough to justify its indirection.

A reuse map is a hypothesis, not approval to create its listed files. If implementation exposes a simpler shape or an incompatible contract, revise the decision and record the departure and the evidence.

## Choose the Code Shape

- Keep code together when it changes together.
- Promote to shared only when consumers share semantics and ownership. Similar markup or hypothetical future reuse is not enough.
- Resolve initial data once at its owning boundary and pass the narrowed result onward.
- Keep revalidation when time, authority, or inputs can change.
- Preserve generated types through internal helpers. Narrow the actual uncertainty. A partial predicate must not claim fields it has not established.
- Validate genuinely untrusted data at its entry boundary using established validators.
- Prefer the project's existing form and validation approach. Do not invent a second validation path.
- Separate server or query state from client UI state. Do not copy server data into local state just to read it.
- State lives at the smallest cohesive owner. Lift it only when coordination is required.
- Prefer composition over prop drilling or a boolean-prop explosion.
- Prefer explicit variants or composition over adding more boolean props to one component.
- Extract a private component or hook when naming the responsibility improves readability or change isolation, even for a single use. Do not present that extraction as a shared abstraction.
- One component per file. The file name matches the component (PascalCase).
- Hooks live in `useXxx.ts`. Types are colocated or live in `types.ts`. Do not create vague names (`utils2`, `helper`, `common`, `MyComponentNew`).
- Keep props narrow. Pass only what the component needs. Avoid `any` and an overly generic config object when composition is clearer.
- Make surgical changes. Mention unrelated problems instead of expanding the change to fix them.

## Rules That Reject Bad Reuse

- Do not create a parallel implementation because markup looks similar or a legacy version is nearby.
- Do not copy a legacy exception merely because it is nearby.
- Do not bypass a project wrapper to use the lower-level primitive it owns.
- A small visual difference is normally a reason to use a supported variant or extend the canonical component, not a reason to create a parallel implementation.
- Imports and map rows are not proof of reuse.

## Verify After Implementation

1. Trace the changed behavior across callers, hooks, and helpers. Challenge duplicated resolution, validation, state, and failure handling against the exemplar.
2. Reconsider each new abstraction against simpler composition and its actual consumers.
3. Run targeted repository checks and tests for meaningful behavior and required invariants.
4. Report substantive departures and remaining maintenance cost.
