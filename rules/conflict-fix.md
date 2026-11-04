---
description: Resolve a merge conflict without dropping a real change or duplicating an item.
alwaysApply: true
---

If the task resolves a merge conflict, a rebase conflict, or conflict markers, read base, ours, and theirs before you edit. Use `git show :1:path`, `:2:path`, and `:3:path`. A change is a difference from base. An add and a deletion are both changes.

Keep each change that exists on only one side. A line that both sides already share stays once. Do not take one side and delete the other. Do not resolve the file with `--ours` or `--theirs` unless the other side has no unique change.

If one side deletes an item or a file, and the other side does not change it from base, keep the deletion. If one side deletes it and the other side changes it from base, stop and ask. If both sides rename it to different paths or names, stop and ask. If only one side renames it, keep the rename. If the other side also edits that item or file, apply that edit on the new path or name.

Do not paste both conflict blocks into the file. Merge a list by identity. The same import path, object key, or id appears once. If both sides bind one import path to different names, stop and ask.

If both sides change different fields of the same item, combine those fields. If both sides set the same field to different values, stop and ask. Do not combine a version or a scalar.

Do not merge a lockfile, a generated file, or a snapshot by hand. `package-lock.json` is a lockfile. Resolve the source file, then regenerate.

Do not rewrite a line outside the conflict unless the merged file is invalid without that edit. Name each such edit.

Before you resolve, record every unmerged path with `git diff --name-only --diff-filter=U`. Before you finish, search each recorded file for a conflict marker and for a repeated item. A text search misses two exports with the same name, and one import path bound two ways. Read for those. Then run the build, type-check, and test commands this project already uses. Skip a check it does not have.

If two meanings cannot both stay, stop and ask.
