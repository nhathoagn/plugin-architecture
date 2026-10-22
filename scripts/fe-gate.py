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
tool_input = event.get("tool_input") or {}
path = ""
if isinstance(tool_input, dict):
    path = tool_input.get("file_path") or tool_input.get("path") or ""

prompt_hit = re.search(
    r"frontend|front-end|\breact\b|\bvue\b|\bsvelte\b|\.tsx\b|\.jsx\b|\.vue\b|\.svelte\b|\btsx\b|\bjsx\b|\bcomponents?\b|\bUI\b|giao diện|viết\s+(ui|frontend|component)",
    prompt,
    re.I,
)
path_hit = re.search(r"\.(tsx|jsx|vue|svelte)$", path, re.I)
if name == "UserPromptSubmit":
    hit = bool(prompt_hit)
elif name == "PreToolUse":
    hit = bool(path_hit)
else:
    hit = False
if not hit:
    sys.exit(0)

root = os.environ.get("FE_ARCH_ROOT") or os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
rule = os.path.join(root, "rules", "fe-implementation.md")
text = open(rule, encoding="utf-8").read()
body = re.sub(r"^---\n.*?\n---\n*", "", text, count=1, flags=re.S).strip()
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": name,
        "additionalContext": body,
    }
}))
