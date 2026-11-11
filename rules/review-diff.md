---
description: Do not grade a frontend diff you wrote.
alwaysApply: true
---

Do not grade a frontend diff you wrote. On Claude Code, hand the diff and the playbook path to agent `fe-kit:reviewer`. On omp, a fresh context reads `skill://fe-kit/playbooks/review-diff.md`. You do not write the verdict. A one-line fix or a pure style tweak skips this, as defined in `rules/fe-implementation.md`: a change that alters runtime behavior never skips it.
