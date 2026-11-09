import json
import os
import re
import sys
import subprocess

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
    r"conflict|<<<<<<<|merge markers?|rebase conflict|conflict.{0,30}rebase|rebase.{0,30}conflict|xung đột|xung dot|hợp nhất|hop nhat|duplicate items?|trùng(?: item| lặp)?",
    prompt,
    re.I,
)
reuse_hit = re.search(
    r"reuse|re-use|duplicat|dùng lại|dung lai|tái sử|tai su|trùng|trung|lặp|lap lai|song song|existing (?:code|component|hook|helper|implementation)|copy (?:a |the )?(?:component|hook|helper|function)",
    prompt,
    re.I,
)
author_hit = re.search(
    r"\b(add|implement|write|create|extract|refactor|introduce)\b|viết|viet |thêm |them |tách |tach ",
    prompt,
    re.I,
)
review_hit = re.search(
    r"review(?: the)? diff|git diff|trước commit|truoc commit|before commit|code review|soi diff",
    prompt,
    re.I,
)
path_hit = re.search(r"\.(tsx|jsx|vue|svelte)$", path, re.I)
source_hit = re.search(
    r"\.(tsx?|jsx?|vue|svelte|py|go|rs|java|kt|kts|rb|php|cs|swift)$",
    path,
    re.I,
)
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
            "permissionDecisionReason": "Fill Runtime owner and Reuse Decision from skill fe-kit before creating this file. Editing an existing file is allowed.",
        }
    }))
    sys.exit(0)

def find_git_dir(start):
    current = os.path.abspath(start) if start else ""
    while current and os.path.isdir(current):
        candidate = os.path.join(current, ".git")
        if os.path.isdir(candidate):
            return candidate
        if os.path.isfile(candidate):
            try:
                with open(candidate, encoding="utf-8", errors="ignore") as handle:
                    first = handle.readline().strip()
                if first.startswith("gitdir:"):
                    target = first.split(":", 1)[1].strip()
                    return target if os.path.isabs(target) else os.path.join(current, target)
            except OSError:
                return None
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent
    return None

def repo_in_conflict(start):
    git_dir = find_git_dir(start)
    if not git_dir:
        return False
    return any(
        os.path.exists(os.path.join(git_dir, marker))
        for marker in ("MERGE_HEAD", "rebase-merge", "rebase-apply")
    )

def file_has_markers(target):
    if not target or not os.path.isfile(target):
        return False
    try:
        with open(target, encoding="utf-8", errors="ignore") as handle:
            saw_open = False
            saw_close = False
            for line in handle:
                if line.startswith("<<<<<<<"):
                    saw_open = True
                elif line.startswith(">>>>>>>"):
                    saw_close = True
                if saw_open and saw_close:
                    return True
    except OSError:
        return False
    return False

def plugin_root():
    return os.environ.get("FE_ARCH_ROOT") or os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def load_rule(filename):
    path = os.path.join(plugin_root(), "rules", filename)
    text = open(path, encoding="utf-8").read()
    return re.sub(r"^---\n.*?\n---\n*", "", text, count=1, flags=re.S).strip()

def review_context():
    playbook = os.path.join(plugin_root(), "skills", "fe-kit", "playbooks", "review-diff.md")
    return load_rule("review-diff.md") + "\n\nPlaybook path: " + playbook

def text_has_frontend(text):
    if not text:
        return False
    if re.search(r"skill://fe-kit|Runtime owner:|Reuse Decision", text):
        return True
    return bool(re.search(
        r"frontend|front-end|\breact\b|\bvue\b|\bsvelte\b|\.tsx\b|\.jsx\b|\.vue\b|\.svelte\b|\btsx\b|\bjsx\b|\bcomponents?\b|\bUI\b|giao diện|viết\s+(ui|frontend|component)",
        text,
        re.I,
    ))

def transcript_has_frontend(event):
    if text_has_frontend(event.get("compact_summary") or ""):
        return True
    transcript = event.get("transcript_path") or ""
    if not transcript or not os.path.isfile(transcript):
        return False
    try:
        with open(transcript, encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                if text_has_frontend(line):
                    return True
    except OSError:
        return False
    return False

def project_root(start):
    env_root = os.environ.get("CLAUDE_PROJECT_DIR") or ""
    if env_root and os.path.isdir(env_root):
        return env_root
    current = os.path.abspath(start) if start else ""
    while current and os.path.isdir(current):
        if os.path.exists(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return start or ""

def run_repo_rules(start, target):
    root = project_root(start)
    script = os.path.join(root, ".claude", "rules.sh")
    if not (os.path.isfile(script) and os.access(script, os.X_OK)):
        return ""
    try:
        result = subprocess.run(
            [script, target or ""],
            cwd=root or None,
            capture_output=True,
            text=True,
            timeout=150,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ".claude/rules.sh failed: %s" % exc
    if result.returncode == 0:
        return ""
    lines = ((result.stdout or "") + (result.stderr or "")).splitlines()[:40]
    return "VI PHẠM RULE / LỖI CHECK. Sửa ngay trước khi làm tiếp:\n" + "\n".join(lines)

def emit(event_name, bodies):
    if not bodies:
        sys.exit(0)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": "\n\n".join(bodies),
        }
    }))

def fail(message):
    sys.stderr.write(message.rstrip() + "\n")
    sys.exit(2)

if name == "PreCompact":
    if transcript_has_frontend(event):
        sys.stdout.write(
            "Keep these rules in the summary. Read skill://fe-kit before a non-trivial frontend edit. "
            "Do not grade a frontend diff you wrote. A fresh reviewer reads the fe-kit review-diff playbook. "
            "Keep any Architecture ownership and Reuse Decision already recorded.\n"
        )
    sys.exit(0)

if name == "PostToolUse":
    errors = []
    if file_has_markers(full_path):
        errors.append(
            "Conflict markers remain in %s. Finish the resolution before the next edit." % full_path
        )
    rule_error = run_repo_rules(cwd, full_path) if full_path else ""
    if rule_error:
        errors.append(rule_error)
    if errors:
        fail("\n".join(errors))
    sys.exit(0)

bodies = []
if name == "SessionStart" and event.get("source") == "compact" and transcript_has_frontend(event):
    bodies.append(load_rule("fe-implementation.md"))
    bodies.append(review_context())
elif name == "UserPromptSubmit":
    if prompt_hit:
        bodies.append(load_rule("fe-implementation.md"))
    if prompt_hit or reuse_hit or author_hit:
        bodies.append(load_rule("reuse-duplication.md"))
    if prompt_hit or review_hit:
        bodies.append(review_context())
    if conflict_hit or repo_in_conflict(cwd):
        bodies.append(load_rule("conflict-fix.md"))
elif name == "PreToolUse":
    if path_hit:
        bodies.append(load_rule("fe-implementation.md"))
    if source_hit:
        bodies.append(load_rule("reuse-duplication.md"))
    if file_has_markers(full_path) or repo_in_conflict(cwd):
        bodies.append(load_rule("conflict-fix.md"))

emit(name, bodies)
