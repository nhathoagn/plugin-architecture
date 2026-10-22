#!/bin/sh
cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "FE Implementation: before you implement or refactor non-trivial UI, components, hooks, forms, data fetching, or feature state, invoke skill fe-arch. Order: Architecture Ownership, then Reuse-first, then Performance Check. Do not write implementation code before you fill the Architecture and Reuse Decision sections. Skip the skill for a one-line fix, a pure styling tweak, or work that is not frontend, and say why."
  }
}
EOF
