# Diff checklist

Walk every item. The reader report does not print the ID, `FAIL`, or `PASS`. Write a sentence only when the item fails. Name `file:line` and what the user loses.

| ID | Test | FAIL when | If absent |
|----|------|-----------|-----------|
| F1 | diff against the stated task | extra library, second form or state path, or unnamed cleanup | no stated task: N/A |
| F2 | placement and upward imports | UI sits outside the owning feature, or shared code imports a feature | no placement change: N/A |
| F3 | a pasted nearby block, or a new shared file | one consumer gets a new shared file, or a block is copied and one line changes | no new shared file and no copy: PASS |
| F4 | the same statements written twice | both copies remain | no second copy: PASS |
| F5 | three or more calls that differ only by data | they are not one typed list and one render | fewer than three, or a different component: N/A |
| F6 | new behavior added to existing UI | no flag, flag default is not the old behavior, flag read in more than one place, or new logic is woven into the old file | no new behavior: N/A. A flag on a bug fix or pure refactor: FAIL |
| F7 | a new prop or a screen hook | the prop repeats an existing prop, or the hook only wraps a shared hook | no new prop or wrapper hook: N/A |
| F8 | a known API record | loose map, two name sets, or a client map of server labels | no API record: N/A |
| F9 | a catch, or loading, error, and empty where data is owned | empty catch, or those states are missing | no data owner and no catch: N/A |
| F10 | polling | no stop, or no written worst-case rate | no polling: N/A |
| F11 | secret, console.log, conflict marker | a secret or conflict marker is a blocker. `console.log` is minor | none of the three: PASS |
| F12 | an output-preserving screen change | the before and after compare was not run | a behavior change: N/A |
| F13 | a large form: parent form, popups, lookup hooks | the parent holds `useWatch`, popup state, a catalog or lookup hook; one picker switches many popups; a lookup hook opens UI or lets a late response overwrite | no large form: N/A |
| F14 | `setValue` and layers | `setValue` in JSX; React, `setValue`, or a service in `helpers/`; a grab-bag `*-format.ts`; a function with no business term rewritten when the shared lib already has it | no form and no helper: N/A |
| F15 | renames and names in a refactor | a rename of a name that is not wrong; a new name a reader can confuse with an existing export; a behavior hook named with a noun | no rename and no new hook: N/A |

Wrong: a promo banner rendered inside `Checkout.tsx`, always on.

Right: `checkout/promo-banner.tsx`, one flag read in `Checkout.tsx`, default off. Deleting the new file and the seam restores checkout.

Wrong: `isNumber` next to `type`.

Right: `type="number"`.

Wrong: `z.record` for a known order payload, and a client map of status labels.

Right: each field declared, the server label shown, a fallback only for an unknown value.

Wrong: `useState(picker)` and `useWatch('curr_cd')` in the parent form, one `master-picker.tsx` for every popup, `onChange={(v) => { setValue('due_date', addDays(v, 7)) }}` in JSX.

Right: each block holds its popup and its `useWatch`. A fill hook returns `handlers`, and the block writes `onChange={handlers.dueDate}`.
