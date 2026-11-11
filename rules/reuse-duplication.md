---
description: Reuse an existing implementation. Do not write the same code twice. When only the data changes, keep one implementation.
alwaysApply: true
---

If the task adds or changes a function, component, hook, type, constant, validation, fetch, handler, state, prop, or variable, search before you write it. A one-line wording fix or a pure style tweak does not need this search, as defined in `rules/fe-implementation.md`. Any fix that changes behavior does, however few lines it touches.

Search by what the code does and by a literal it would own. A matching name is a lead. Open the candidate and one caller. Reuse it when the contract matches: who owns the data, what it validates, and what it returns. Extend it when the new behavior fits that responsibility. A small difference is an argument, not a new file.

On a bug fix, do not add a second holder. Before `useState`, a prop, or a variable, name the state, prop, or variable that already holds that value. Read it or write into it. A second holder is a finding: the next fix updates one and the screen still reads the other. A value that does not exist yet can be a new holder. Name the one you checked and the literal or behavior you searched for.

Write new code only when nothing owns that job, or the contract does not match. Name each candidate and the mismatch. Do not paste a nearby block and change one line. A shared abstraction needs two real consumers now. Name them. One consumer stays feature-local.

Duplicated code means the same statements written again. After the edit, compare the lines you added with the files you touched and the modules they import. Call the existing block. If the copies must differ, name the lines that differ. A copy you did not write is listed with both locations and left, unless the task is to remove it.

When those repeated calls differ only by data, describe the data once and keep one implementation: a typed record and a field list (`key: keyof TheRecord`, `as const satisfies`). Read `value[field.key]`. Write `{ ...value, [field.key]: next }`. Render once. Two calls are not enough. A call with a different component, children, or handler stays outside the list. A review proposes this and waits. Adding or changing that parent writes it.

A repeated value or a repeated request is not this check.

Before you finish, name the search and the decision: `reuse`, `extend`, `feature-local`, or `shared`. A `feature-local` or `shared` decision with no search is not done. Name both locations of any duplicated code you found.
