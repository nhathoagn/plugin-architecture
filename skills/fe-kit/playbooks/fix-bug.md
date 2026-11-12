# Fix a bug

Use this when the task reports wrong behavior: a wrong value, a broken flow, a blank screen, lost input, or a symptom with no verb (`Tổng sai khi có discount` is a bug fix).

Do not patch the symptom. Follow these steps in order.

1. Reproduce first. Write three lines, each with a value, before any edit: `Trigger:`, `Expected:`, `Actual:`. Add the evidence: a failing test, a command, or a screen state you saw. If you cannot reproduce it, say the fix is unverified and name what is missing. Do not guess a patch.
2. Find the root cause at its owner. Trace the wrong value or rule from where it is produced to where it is shown. Read `references/ownership.md`. Record the five ownership fields: the fix lands where the wrong value or rule is produced, not in a consumer that only displays it, unless that consumer is the owner.
3. Read `references/reuse.md` and `rules/reuse-duplication.md`. Before any new state, prop, variable, validator, or handler, name the one that already holds that value or does that job, and the search you ran. Fix the existing holder.
4. Make the smallest fix that removes the root cause. Only the lines the root cause needs. No refactor, cleanup, rename, new behavior, or new flag in the same change: name those and leave them for a separate change. No fallback, guard, or default that turns the wrong case into a silent pass. No second holder, second validation path, or copy of a nearby block.
5. Write the unit test in the file the project already uses for that owner. If that owner has no test file, add one beside it, named and imported the same way as the nearest test in the repo. Do not add a test folder, a runner, or a screen snapshot for one bug.

The test calls the owner, not a copy of the logic. It asserts the result the user sees: the value, the message, or the error. A test that only checks a mock was called does not count. Include the `Actual:` case that failed before the fix and the `Expected:` case that must pass. For a text check, also include `undefined`, `null`, `""`, a leading space, and a trailing space. The `Actual:` case must fail on the old code. If you cannot show that, the test does not lock the bug.

Skip the file only when the repo has no test runner. Say that, and re-run the reproduction instead. "No time" is not a reason.
6. Verify. Run the project's type-check, lint, and the new or updated test. Report each command and its exit code. Re-run the reproduction from step 1 and state the result. A fix with no re-run reproduction is not done.

Do not create or edit a `.tsx`, `.jsx`, `.vue`, or `.svelte` file until the reply contains `Runtime owner:` with a named owner, a `Reuse Decision` with one decision, and `Trigger:`, `Expected:`, and `Actual:` each with a value. Write each line in the reply text, before the edit call. The hook cannot read thinking or a table row. A behavior-defined one-line fix (see `rules/fe-implementation.md`) skips this gate. Editing an existing file does not.
