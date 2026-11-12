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
    r"reuse|re-use|duplicat|dùng lại|dung lai|tái sử|tai su|trùng|trung(?!\s*t[âa]m)|lặp|lap lai|song song|existing (?:code|component|hook|helper|implementation)|copy (?:a |the )?(?:component|hook|helper|function)",
    prompt,
    re.I,
)
author_hit = re.search(
    r"\b(add|implement|write|create|extract|refactor|introduce|fix)\b|viết|viet |thêm |them |tách |tach |sửa |sua |bug",
    prompt,
    re.I,
)
BUG_RE = re.compile(
    r"\bbug\b|lỗi|sai khi|không (?:đúng|hiển thị|hien thi|trừ|tru|chạy|chay|mở|mo)\b|màn hình trắng|man hinh trang|mất dữ liệu|mat du lieu|does not work|not working|\bbroken\b|wrong (?:total|value|result|behavior|behaviour)",
    re.I,
)
bug_hit = BUG_RE.search(prompt)
wording_hit = re.search(
    r"\btypo\b|wording|chính tả|chinh ta|button label|style tweak|from blue to|đổi màu|doi mau",
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
def transcript_lines(path):
    if not path or not os.path.isfile(path):
        return []
    try:
        handle = open(path, encoding="utf-8", errors="ignore")
    except OSError:
        return []
    with handle:
        return handle.readlines()

DENY_REASON = "Fill Runtime owner and a Reuse Decision (reuse, extend, feature-local, shared, or n/a with a reason) from skill fe-kit before editing this file. Only a behaviorless one-line wording or style change is exempt."
DENY_BUG_REASON = "A bug fix also needs Trigger:, Expected:, and Actual:, each with a value, from playbooks/fix-bug.md."
REMINDER_RE = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
# A value starts after the colon. A comma or backquote there is prose that names the field.
VALUE = r"[ \t]*[^\s,`]"

def entry_texts(entry):
    message = entry.get("message")
    if not isinstance(message, dict):
        return []
    content = message.get("content")
    if isinstance(content, str):
        return [content]
    if not isinstance(content, list):
        return []
    return [block.get("text") or "" for block in content if isinstance(block, dict) and block.get("type") == "text"]

def authored_texts(path, roles):
    # Only text a person typed or Claude wrote. Tool output, reminders, and hook notes are not authored.
    texts = []
    for line in transcript_lines(path):
        try:
            entry = json.loads(line)
        except ValueError:
            texts.append(line)
            continue
        if not isinstance(entry, dict) or entry.get("type") not in roles or entry.get("isMeta"):
            continue
        for text in entry_texts(entry):
            text = REMINDER_RE.sub("", text).replace(DENY_REASON, "").replace(DENY_BUG_REASON, "")
            if text.strip():
                texts.append(text)
    return texts

def user_is_bug(path):
    return bool(BUG_RE.search("\n".join(authored_texts(path, ("user",)))))

def reproduce_present(path):
    found = {key: False for key in ("Trigger", "Expected", "Actual")}
    for text in authored_texts(path, ("user", "assistant")):
        for key in found:
            if re.search(key + ":" + VALUE, text):
                found[key] = True
    return all(found.values())

def decisions_present():
    transcript = event.get("transcript_path") or ""
    if not transcript or not os.path.isfile(transcript):
        return False
    found_owner = False
    found_reuse = False
    for text in authored_texts(transcript, ("user", "assistant")):
        for line in text.splitlines():
            if re.search("Runtime owner:" + VALUE, line):
                found_owner = True
            if "|" not in line and re.search(
                r"Decision:\s*(reuse|extend|feature-local|shared|n/a)\b", line
            ):
                found_reuse = True
        if found_owner and found_reuse:
            return True
    return False

def behaviorless_one_line():
    if tool_name != "Edit" or not isinstance(tool_input, dict):
        return False
    old = tool_input.get("old_string") or ""
    new = tool_input.get("new_string") or ""
    if not old or not new or old == new:
        return False
    if len(old.splitlines()) != 1 or len(new.splitlines()) != 1:
        return False
    risky = r"useState|useEffect|useMemo|useCallback|\?\?|\|\||&&|\bif\s*\(|\bcatch\b|=>|\bawait\b|\bfetch\b"
    return not (re.search(risky, new) and not re.search(risky, old))

gated_view = (
    tool_name in ("Write", "Edit", "MultiEdit")
    and re.search(r"\.(tsx|jsx|vue|svelte)$", path, re.I)
    and not behaviorless_one_line()
)

bug_edit = gated_view and user_is_bug(event.get("transcript_path") or "")
if name == "PreToolUse" and gated_view and (not decisions_present() or (bug_edit and not reproduce_present(event.get("transcript_path") or ""))):
    reason = DENY_REASON
    if bug_edit:
        reason += " " + DENY_BUG_REASON
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
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
    if path_hit and user_is_bug(event.get("transcript_path") or ""):
        emit(name, [
            "Write or update the unit test beside the owner. It must fail on Actual and pass on Expected. For a text check, include undefined, null, empty, leading space, and trailing space. Then re-run that test and the reproduction. Hand this diff to fe-kit:reviewer or a fresh context that reads skill://fe-kit/playbooks/review-diff.md. Do not write the verdict."
        ])
    sys.exit(0)

bodies = []
if name == "SessionStart" and event.get("source") == "compact" and transcript_has_frontend(event):
    bodies.append(load_rule("fe-implementation.md"))
    bodies.append(review_context())
elif name == "UserPromptSubmit":
    if prompt_hit or bug_hit:
        bodies.append(load_rule("fe-implementation.md"))
    if (prompt_hit or reuse_hit or author_hit or bug_hit) and not (wording_hit and not bug_hit):
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
