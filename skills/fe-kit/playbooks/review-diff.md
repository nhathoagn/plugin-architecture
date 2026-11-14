# Review a diff

Use this when the task is to review a frontend diff, or before a non-trivial frontend edit is called done. The author of the diff does not fill this report.

You are not the author. You do not have the writing session. Do not praise. Do not edit, commit, checkout, or spawn another reviewer.

1. Get the diff. If the task names `BASE` and `HEAD`, use `git diff --stat BASE..HEAD` and `git diff BASE..HEAD`, and note the commits with `git log --oneline BASE..HEAD`. Otherwise use `git diff` and `git diff --cached`. Read a file only to judge a hunk.
2. Find the spec file. Stop at the first hit. Do not fetch an issue tracker. Do not run `setup-matt-pocock-skills`. Do not open `code-review`. Do not spawn a reviewer. First, look for a path under `docs/`, `specs/`, or `.scratch/` that a commit message names. An issue reference in a commit message (`#123`, `Closes #45`) counts only when that number is in a file name under those directories. Next, use a spec path the task names. Next, use a file under those directories whose name matches the branch or the feature in the diff. Read only that file. If no file exists, say that in one line under Kết luận. Then judge the stated task, or the checklist alone when the task states none.
3. Read `references/REVIEW_CHECKLIST.md` and `references/review-checks.md`. Walk every item. F20 uses the file from step 2. F21 reads `GLOSSARY.md` or `CONTEXT.md` at the repo root when one exists. If only `GLOSSARY-MAP.md` exists, read the one file it names for this feature. Do not create a glossary. Do not write an ADR. Do not apply the Architecture smell list in `references/audit.md`. Do not print a code, `PASS`, `FAIL`, or `N/A`. If the diff adds or changes a check (`?? ''`, `startsWith`, `trim`, `min`, `safeParse`, or a filter/map over fields), apply `undefined`, `null`, `""`, `" ABC"`, and `"ABC "` to that check before the verdict. A value that produces no error is a finding, with `file:line`. Do not write "Đưa được" if you did not apply them.
4. If the repo root has `REVIEW_CHECKLIST.md`, apply each filled row under "Lỗi riêng của repo". Skip an empty rule cell.
5. Ignore a hit a linter already catches, unless a repo row says otherwise. Ignore a problem outside the diff, unless the diff makes it worse.
6. Write the report by filling `references/review-output.md`. Follow Cách viết in that file. The reader sees those sentences, not checklist codes. Do not add a Spec section. Then stop.

## Verdict words

Say the verdict in the first sentence, in Vietnamese.

- A defect that loses data, ships a secret, or breaks the build: "nên sửa trước". The first sentence is "Không đưa lên".
- A defect the user will hit in this screen: "nên sửa trong lượt này". If none are "nên sửa trước", the first sentence is "Sửa rồi hãy đưa".
- A nit: "có thể để sau". If nothing else failed, the first sentence is "Đưa được".

## Report

The report is `references/review-output.md`, filled. Do not add a checklist section. Do not add a Spec section.
