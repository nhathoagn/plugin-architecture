# Review a diff

Use this when the task is to review a frontend diff, or before a non-trivial frontend edit is called done. The author of the diff does not fill this report.

You are not the author. You do not have the writing session. Do not praise. Do not edit, commit, checkout, or spawn another reviewer.

1. Get the diff. If the task names `BASE` and `HEAD`, use `git diff --stat BASE..HEAD` and `git diff BASE..HEAD`. Otherwise use `git diff` and `git diff --cached`. Read a file only to judge a hunk.
2. Read `references/REVIEW_CHECKLIST.md` and `references/review-checks.md`. Walk every item. Do not print a code, `PASS`, `FAIL`, or `N/A`. If the diff adds or changes a check (`?? ''`, `startsWith`, `trim`, `min`, `safeParse`, or a filter/map over fields), apply `undefined`, `null`, `""`, `" ABC"`, and `"ABC "` to that check before the verdict. A value that produces no error is a finding, with `file:line`. Do not write "Đưa được" if you did not apply them.
3. If the repo root has `REVIEW_CHECKLIST.md`, apply each filled row under "Lỗi riêng của repo". Skip an empty rule cell.
4. Ignore a hit a linter already catches, unless a repo row says otherwise. Ignore a problem outside the diff, unless the diff makes it worse.
5. Write the report by filling `references/review-output.md`. Follow Cách viết in that file. The reader sees those sentences, not checklist codes. Then stop.

## Verdict words

Say the verdict in the first sentence, in Vietnamese.

- A defect that loses data, ships a secret, or breaks the build: "nên sửa trước". The first sentence is "Không đưa lên".
- A defect the user will hit in this screen: "nên sửa trong lượt này". If none are "nên sửa trước", the first sentence is "Sửa rồi hãy đưa".
- A nit: "có thể để sau". If nothing else failed, the first sentence is "Đưa được".

## Report

The report is `references/review-output.md`, filled. Do not add a checklist section.
