# Review a diff

Use this when the task is to review a frontend diff, or before a non-trivial frontend edit is called done. The author of the diff does not fill this report.

You are not the author. You do not have the writing session. Do not praise. Do not edit, commit, checkout, or spawn another reviewer.

1. Get the diff. If the task names `BASE` and `HEAD`, use `git diff --stat BASE..HEAD` and `git diff BASE..HEAD`, and note the commits with `git log --oneline BASE..HEAD`. Otherwise use `git diff` and `git diff --cached`. Read a file only to judge a hunk.
2. Find the spec file. Stop at the first hit. Do not fetch an issue tracker. Do not run `setup-matt-pocock-skills`. Do not open `code-review`. Do not spawn a reviewer. Search three sources in order: (a) a path or an issue reference (`#45`, `Closes #45`, `Fixes #45`, a bare `#45`) in the subject or body of a commit inside the range, (b) a spec path the task names, (c) a file whose whole stem equals the branch name or the feature the diff adds. A hit is a file under `docs/`, `specs/`, or `.scratch/` that exists at HEAD with that exact spelling: a missing path, another case, a root or `src/` file, and a directory are not hits — a file path given beside such a directory still counts. An issue number must be a whole token in the file name: `45-address.md`, `checkout-45.md`, and `issue-45-address.md` match `#45`; `145-address.md`, `450-address.md`, `4.ts`, and `5.ts` do not. When source (a) hits, do not read (b) or (c) even when a later file disagrees. A branch hit needs the stem equal to the whole branch name; the part after a slash never matches. Read only the hit file. When the hit exists but is empty, or holds only a heading, it gives no requirement: stop there — do not fall to another source, do not take a task requirement, and do not build one from the code. When no source hits, say that in one line under Kết luận; a file that merely exists in the repo is not a hit. Then judge the stated task, or the checklist alone when the task states none.
3. Read `references/REVIEW_CHECKLIST.md` and `references/review-checks.md`. Walk every item. F20 uses the file from step 2. F21 reads `GLOSSARY.md` or `CONTEXT.md` at the repo root when one exists. If only `GLOSSARY-MAP.md` exists, read the one file it names for this feature. Do not create a glossary. Do not write an ADR. Do not apply the Architecture smell list in `references/audit.md`. Do not print a code, `PASS`, `FAIL`, or `N/A`. If the diff adds or changes a check (`?? ''`, `startsWith`, `trim`, `min`, `safeParse`, or a filter/map over fields), apply `undefined`, `null`, `""`, `" ABC"`, and `"ABC "` to that check before the verdict. A value that produces no error is a finding, with `file:line`. Do not write "Đưa được" if you did not apply them. The same five values go through every guard the diff adds or changes over a parameter (`if (!discount)`, `x || …`, `x ?? …`): a value that returns through with no error is a finding like any other. When all five values produce an error, the check satisfies that requirement: write no finding against it, and do not demand an enforcement the spec does not name (a disabled button, a submit guard).

The judgement list in `references/audit.md` is not scored here. Do not write a paragraph from it in any framing — not as a smell, and not as runtime safety: fields travelling together, replacing a string or number with an existing type, a repeated switch or if, a chain like `a.b().c()`, a forward-only component, inheritance that drops props, or a brand-new file that holds two jobs of its own. The checklist has no item for them on a diff.
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
