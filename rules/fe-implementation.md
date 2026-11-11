---
description: Read skill fe-kit before non-trivial frontend code.
alwaysApply: true
---

If the task changes UI, a component, a hook, a form, data fetching, or feature state, and it is not a one-line fix or a pure style tweak, read `skill://fe-kit` before you write code.

One-line is defined by behavior, not by line count. A fix is one-line only when it changes wording or style on one existing line and alters no runtime behavior: no new state, prop, variable, branch, validation, handler, fallback, or default, and no changed value, condition, or call. A one-line change that alters behavior — a new condition, a `??` default, a changed constant — is a bug fix and follows `playbooks/fix-bug.md`, however few lines it touches.
