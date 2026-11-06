# Feature Isolation: Flagged, Separated, Reversible

Read this file only when a playbook names it and the task adds **new behavior** to a screen, feature, or shared component that already works.

Project rules win. When the repo has its own flag or rollout rules, follow them and treat this file as the fallback.

Three guarantees, all three, not one of them:

1. **Toggleable.** The new behavior sits behind one flag. Off restores the old behavior exactly.
2. **Non-invasive.** Code that already exists does not change its behavior, props, payload, or render when the flag is off.
3. **Separated.** New logic lives in its own files under the owning feature. Removing it is a delete, not an excavation.

## When this applies

- A new section, action, variant, flow, or data source added to an existing screen or feature.
- New optional behavior added to a shared component that existing callers already use.
- An experiment, a gradual rollout, or a replacement that must be comparable against the old path.

## When it does not apply — write `n/a` and say why

- A bug fix that restores the documented behavior. Never gate a correctness, security, or data-loss fix behind a default-off flag.
- A pure refactor, rename, move, or style tweak with no behavior change. The before/after comparison in `references/code-quality.md` is the guard there, not a flag.
- A brand-new standalone screen with no existing caller and no old path to preserve. There is nothing to toggle against. Still keep it separated (guarantee 3).
- A one-line fix. It is out of scope for this skill at all.

If unsure whether behavior changes, it changes. Apply this file.

## The flag

- **Reuse the project's flag system.** Search for it first (`flag`, `featureFlag`, `toggle`, `rollout`, the project's flag client). Never add a second flag library, a new config endpoint, or a hard-coded user/email/id check as a substitute.
- **No flag system exists:** do not build one for one feature. Use the smallest existing toggle the project already reads (its config or env seam), record that departure under Departures / Notes, and name building real flag infra as separate work.
- **One flag, one feature.** Name it after the feature in the project's convention (`checkout.promo-banner`, `enablePromoBanner`). Not `new-ui`, not `v2`, not one flag shared by unrelated features.
- **Default is the old behavior** (off) until the new path is verified on. A default that changes existing users' behavior on deploy fails guarantee 2.
- **Read the flag once**, at the feature's entry owner (the screen or feature root that owns the data/action). Pass a plain boolean or variant down as a prop. Leaf and shared components do not re-read the flag client: a flag read scattered across files cannot be removed cleanly and tests must mock it everywhere.
- **Record an owner and a removal date or ticket** where the project records flags. A flag with no expiry is permanent branching. On full rollout, delete the flag and the dead path in the same follow-up change.

## Separation

- New logic goes in its own files, colocated inside the owning feature, following `references/reuse.md` placement. One entry point (one component or one hook) that the old code calls. Not `shared/` until a second real consumer exists.
- New files hold the new hook, the new component, and their types. Existing files do not gain new functions, branches, or state for the new behavior beyond the seam below.
- **The seam in existing code is minimal and listed:** ideally one flag check that renders or invokes the new entry point, at one call site. Every existing file touched is named in the output table with what changed in it. A seam that edits logic inside an existing function body fails this rule — wrap or compose instead.
- **Deletion test:** deleting the new files plus the seam restores the old code path with no leftover imports, types, state fields, or payload fields. If deletion needs edits inside five files, the separation failed; restructure before continuing.
- New state is owned by the new files. Do not add fields to an existing store, context, or form schema for the new behavior unless the flag-on path is the only writer and the flag-off path reads the old shape unchanged.

## Non-interference (flag off = old code)

- Do not change an existing component's default props, rendered output, or event behavior. Extend shared code only with an opt-in prop whose default reproduces the old behavior, per the Architecture lens in `references/audit.md`.
- Do not change the request payload, query key, route, or validation rules on the off path. New validation applies only inside the flag-on path; it must never block the old flow.
- **Hooks rule:** never call a hook conditionally on the flag (`if (flag) useX()`). Either mount the new component only when the flag is on and let it call its hooks unconditionally inside itself, or pass `enabled: flag` through the project's query/hook options.
- On the off path the new code must not run at all: no fetch, no polling, no subscription, no timer, no new side effect. Mounting nothing is the cheapest guarantee; a mounted-but-hidden new component that still fetches fails.
- Do not interleave flag branches through an existing file (`flag ? new : old` repeated per line). One branch at the seam, whole old path or whole new entry point below it.

## Record before writing code

Fill this in the output template. One row per item; a blank row is not done.

| Item | Value |
|---|---|
| Flag name and source (system searched) | |
| Default (must be old behavior) and why | |
| Flag read at (one entry owner) | |
| New files (all under the owning feature) | |
| Existing files touched (the seam, one line each) | |
| Off-path guarantee (no fetch / render / payload change) | |
| Deletion test (what delete + seam removal restores) | |
| Flag owner and removal date or ticket | |

## Verify both states

- **Flag off:** compare the screen before and after the change as `references/code-quality.md` describes (image and text). Exercise the old flow once. Confirm no new request fires (network log or query trace).
- **Flag on:** exercise the new flow, including its loading, error, and empty states.
- **Toggle:** switching the flag needs no data migration and no reload-only state; both paths render from the same underlying data.
- Run the project's checks for both states where its test setup allows; name the commands and exit codes.
- Grep the diff for flag reads: exactly the one entry owner reads the flag. Every other hit is a finding.
