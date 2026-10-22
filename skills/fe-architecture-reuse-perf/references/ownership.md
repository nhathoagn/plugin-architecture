# Architecture Ownership

Determine where a responsibility belongs before writing or copying code.

Focus on the long-term canonical owner, not only the place where the current behavior appears.

## Required Discovery

Before deciding ownership:

- Read repo docs, AGENTS.md, or ADRs that define architecture, boundaries, or responsibilities.
- Inspect the top-level project structure.
- Map the repo's concrete folders and modules onto the layers below.

When docs are incomplete:

- Infer the current layer model from the codebase.
- State the assumption explicitly.
- Keep the recommendation aligned to one canonical owner.

## Required Output

Explicitly separate. Do not collapse into a single answer.

- Runtime owner. Where the behavior currently appears.
- First-fix owner. Where to patch first if the product is wrong now.
- Canonical long-term owner. Where it should live.
- Competing owners that are wrong.
- Cleanup direction. Required when current placement is wrong.

## Decision Order

1. Identify the runtime concern:
   - visible UI state
   - feature workflow or form state
   - domain or application policy
   - pure shared logic
   - adapter or integration behavior
   - page or route composition
2. Name the layer where the wrong behavior currently happens.
3. Decide whether that layer is only the first-fix owner or also the canonical long-term owner.
4. If the behavior is reusable product or business policy, move the long-term owner out of UI or page layers.
5. Remove duplicate policy or dual paths once the canonical owner is clear.

## Layer Map

Translate these into the repo's real folder and module names before recommending.

- **UI / presentation.** Owns visible UI state, navigation, rendering, presentation-oriented derived state, and view composition.
- **Feature.** Owns feature-specific workflow, form state, local orchestration, and feature-local actions.
- **Domain / application.** Owns canonical product workflow, business rules, reusable application services, and cross-interface behavior.
- **Shared core.** Owns shared types, enums, validation, normalization, capability logic, and pure logic used by multiple features.
- **Adapter / data.** Owns concrete protocol, provider, vendor, transport, query hooks, or API integration behavior. Does not own cross-provider product policy.
- **Page / route.** Owns routing and thin page composition. Should stay thin.

## Hard-Cut Rules

- Do not leave reusable domain policy in UI or page layers just because the wrong behavior currently appears there.
- Do not put UI state, layout state, or user-facing presentation ownership in data or adapter layers.
- Do not put adapter or vendor-specific concerns in the domain layer.
- Do not put pure validation, normalization, or capability logic in feature orchestration when it can live in shared core or a narrow domain module.
- Do not create shared code for a single consumer.
- Keep imports unidirectional. Page imports feature. Feature imports shared, UI, or domain. Shared and domain must not import from features or pages.
- Colocate code that changes together inside the feature folder. Do not dump feature-specific components into a global `components/` folder.
- Prefer a simple feature layout (`components/`, `hooks/`, `types.ts`, or colocated files) when the feature grows. Keep it flat while small.
- Do not introduce a new state library, form library, or data-fetching library if the project already has one.
- If existing implementations are wrong, do not treat them as the target. Name the correct canonical owner instead.

## Common Judgments

- "Who should decide this for all future interfaces?" Usually the domain or application layer, a narrow domain module, or shared core. Not UI or page.
- "Where do I patch this bug first so the product stops doing the wrong thing?" That may still be the current runtime layer (first-fix owner).
- "Who owns the wire shape or payload type?" Usually shared core or generated types, not the feature UI.
- "Who owns vendor-specific behavior?" The relevant adapter, but only for adapter behavior, not canonical product policy.
