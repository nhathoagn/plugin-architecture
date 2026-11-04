---
description: Resolve a merge conflict without dropping a real change or duplicating an item.
alwaysApply: true
---

If the task resolves a merge conflict, a rebase conflict, or conflict markers, read all three sides before you edit: the base (`:1`), ours (`:2`), and theirs (`:3`) — `git show :<n>:<path>`. In a rebase, ours is the branch you rebase onto and theirs is the work being replayed. Do not judge a change from the two sides alone.

Keep each change that exists on only one side. A line that both sides already share stays once. A deletion is a change too: an item removed on one side and untouched on the other stays removed. One side deleted an item and the other side changed it — stop and ask; do not resurrect or silently drop it. If only one side renames a file, keep the rename. If the other side edits that file, apply the edit on the new path. If both sides rename it to different paths, stop and ask. Do not resolve the file with `--ours` or `--theirs` unless you have checked against the base that the other side has no unique change.

Do not paste both conflict blocks into the file. Pasting both blocks duplicates an import, a list item, an object key, a route, or a dependency. Merge a list by identity. The same import path, object key, or id appears once. If both sides changed the same item, combine only the fields that do not overlap. Both sides set the same field to different values — stop and ask. Do not emit two copies.

A generated file or a lockfile is not merged by hand. Resolve the source it is generated from, then regenerate it.

Do not rewrite a line outside the conflict. The prior source stays. The only exception is a change the merged result needs to be valid — merging two import statements into one, reordering what the merge brought together. Name that change when you report.

Before you finish, list every file that was in conflict (`git status`, or `git diff --name-only --diff-filter=U` before you resolve). Search each resolved file for conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`, `|||||||`) and for a repeated item. Run the project's build, type-check, or tests: text search does not catch two exports with one name or one import path with two bindings. If both sides change the same line and both meanings cannot stay, stop and ask. Name both meanings.
