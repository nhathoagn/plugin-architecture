---
description: Resolve a merge conflict without dropping prior source or duplicating items.
alwaysApply: true
---

If the task resolves a merge conflict, a rebase conflict, or conflict markers, read both sides before you edit.

Keep each change that exists on only one side. A line that both sides already share stays once. Do not take one side and delete the other. Do not resolve the file with `--ours` or `--theirs` unless the other side has no unique change.

Do not paste both conflict blocks into the file. Pasting both blocks duplicates an import, a list item, an object key, a route, or a dependency. Merge a list by identity. The same import path, object key, or id appears once. If both sides changed the same item, combine the fields. Do not emit two copies.

Do not rewrite a line outside the conflict. The prior source stays. Before you finish, search the file for conflict markers and for a repeated item. If both sides change the same line and both meanings cannot stay, stop and ask.
