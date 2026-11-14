---
description: One job per file. A different job is a new file in the owning feature, with a narrow export.
alwaysApply: true
---

A file does one job. A folder does one job. When the new code does a different job from the file you are editing, put it in a new file in the owning feature and leave one call in the old file. A small difference in the same job is an argument, not a new file (`rules/reuse-duplication.md`).

Folders follow the feature or the domain, not the kind of file. Inside one feature, UI, business rule, data access, and pure helpers stay in separate files.

Export only what a caller uses, and keep the rest private to the file. A file outside the folder imports one file in the folder. Files inside the folder import each other. Do not add an `index.ts` that re-exports the folder.

Do not grow a god file. When the file you are editing already holds two jobs, the second one goes to a new file.

File length alone is not a reason to split. A 400-line file that does one job stays one file. When a file passes 200 lines, name its job and check whether a second job crept in. Split only when you find that second job.

A bug fix does not split files, and does not touch a file the task is not about. New behavior on a screen that already works still follows `references/feature-isolation.md`. This rule only says where the file goes.

Before code, list the files you will create and the job of each. For each new file, name the convention it follows and the existing file or folder whose shape it takes: the path pattern, the file-name style, and the export style of the nearest sibling. When nothing in the project looks like it, say that on the same line and name the feature that owns it. Before you finish, name the job of each file you edited.
