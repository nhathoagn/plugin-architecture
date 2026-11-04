import json
import os
import re
import sys

raw = sys.stdin.read().strip()
if not raw:
    sys.exit(0)
try:
    event = json.loads(raw)
except json.JSONDecodeError:
    sys.exit(0)

name = event.get("hook_event_name") or ""
prompt = event.get("prompt") or ""
tool_name = event.get("tool_name") or ""
tool_input = event.get("tool_input") or {}
path = ""
if isinstance(tool_input, dict):
    path = tool_input.get("file_path") or tool_input.get("path") or ""

cwd = event.get("cwd") or ""
full_path = path
if path and not os.path.isabs(path) and cwd:
    full_path = os.path.join(cwd, path)

prompt_hit = re.search(
    r"frontend|front-end|\breact\b|\bvue\b|\bsvelte\b|\.tsx\b|\.jsx\b|\.vue\b|\.svelte\b|\btsx\b|\bjsx\b|\bcomponents?\b|\bUI\b|giao diện|viết\s+(ui|frontend|component)",
    prompt,
    re.I,
)
conflict_hit = re.search(
    r"conflict|<<<<<<<|rebase|xung đột|duplicate items?|trùng(?: item| lặp)?",
    prompt,
    re.I,
)
path_hit = re.search(r"\.(tsx|jsx|vue|svelte)$", path, re.I)
new_view = tool_name == "Write" and re.search(r"\.(tsx|vue)$", path, re.I) and full_path and not os.path.exists(full_path)

def decisions_present():
    transcript = event.get("transcript_path") or ""
    if not transcript or not os.path.isfile(transcript):
        return None
    found_owner = False
    found_reuse = False
    with open(transcript, encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if "Runtime owner:" in line:
                found_owner = True
            if "Reuse Decision" in line:
                found_reuse = True
            if found_owner and found_reuse:
                return True
    return False

if name == "PreToolUse" and new_view and decisions_present() is False:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Fill Runtime owner and Reuse Decision from skill fe-arch before creating this file. Editing an existing file is allowed.",
        }
    }))
    sys.exit(0)

def load_rule(filename):
    root = os.environ.get("FE_ARCH_ROOT") or os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    path = os.path.join(root, "rules", filename)
    text = open(path, encoding="utf-8").read()
    return re.sub(r"^---\n.*?\n---\n*", "", text, count=1, flags=re.S).strip()

bodies = []
if name == "UserPromptSubmit":
    if prompt_hit:
        bodies.append(load_rule("fe-implementation.md"))
    if conflict_hit:
        bodies.append(load_rule("conflict-fix.md"))
elif name == "PreToolUse" and path_hit:
    bodies.append(load_rule("fe-implementation.md"))
if not bodies:
    sys.exit(0)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": name,
        "additionalContext": "\n\n".join(bodies),
    }
}))
