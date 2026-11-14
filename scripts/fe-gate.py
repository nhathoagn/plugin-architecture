import json
import os
import re
import sys
import subprocess

# The hook payload is UTF-8. Windows Python decodes stdin as cp1252 by default, which breaks Vietnamese prompts.
raw = sys.stdin.buffer.read().decode("utf-8", errors="replace").strip()
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
    r"\bbug\b|lỗi|sai khi|(?:tổng|tong|tính|tinh|hiển thị|hien thi|bị|bi) sai\b|không (?:đúng|hiển thị|hien thi|trừ|tru|chạy|chay|mở|mo)\b|màn hình trắng|man hinh trang|mất dữ liệu|mat du lieu|does not work|not working|\bbroken\b|wrong (?:total|value|result|behavior|behaviour)",
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

DENY_REASON = "Fill Runtime owner and a Reuse Decision (reuse, extend, feature-local, shared, or n/a with a reason) from skill fe-kit before editing this file. Write each one in the reply text, on its own line, after the latest request and before the edit call: `Runtime owner:` and a name, `Decision:` and one decision. Thinking is not always saved, so write the lines in the reply text. A table row does not count. Only a behaviorless one-line wording or style change is exempt."
DENY_BUG_REASON = "A bug fix also needs Trigger:, Expected:, and Actual:, each with a value, from playbooks/fix-bug.md."
REMINDER_RE = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
# A Japanese IME types the full-width colon.
COLON = "[:：]"
# A label can be bold or italic, as in **Decision**: or _Decision_:.
LABEL_END = "[*_]*" + COLON
# A value starts after the colon. A comma, or a backquote right after the colon, is prose that names the field.
VALUE = r"(?:[ \t]+`?[^\s,`]|[^\s,`])"
REPRODUCE_LABELS = {"Trigger": "Trigger|Steps?", "Expected": "Expected", "Actual": "Actual"}
# A person can end a line with the label and put the value on the next line.
NEXT_LINE_VALUE = r"[ \t]*\n\s*(?!`|\||(?:Trigger|Steps?|Expected|Actual)\b)\S"
# A request for new work ends an earlier bug report. A short reply such as "do it" does not.
NEW_WORK_RE = re.compile(
    r"\b(add|implement|write|create|extract|refactor|introduce)\b|viết|viet |thêm |them |tách |tach ",
    re.I,
)

def entry_texts(entry):
    message = entry.get("message")
    if not isinstance(message, dict):
        return []
    content = message.get("content")
    if isinstance(content, str):
        return [content]
    if not isinstance(content, list):
        return []
    # The transcript keeps the thinking text that the user sees as a summary, so it counts as authored too.
    texts = []
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "text":
            texts.append(block.get("text") or "")
        elif block.get("type") == "thinking":
            texts.append(block.get("thinking") or "")
    return texts

def authored_entries(path, roles):
    # Only text a person typed or Claude wrote, as (role, text) in transcript order.
    # Tool output, reminders, and hook notes are not authored.
    entries = []
    for line in transcript_lines(path):
        try:
            entry = json.loads(line)
        except ValueError:
            entries.append(("", line))
            continue
        if not isinstance(entry, dict) or entry.get("type") not in roles or entry.get("isMeta"):
            continue
        # A compact summary is a user entry that no person typed. Its text counts, but it is not a request.
        role = "summary" if entry.get("isCompactSummary") else entry.get("type")
        for text in entry_texts(entry):
            text = REMINDER_RE.sub("", text).replace(DENY_REASON, "").replace(DENY_BUG_REASON, "")
            if text.strip():
                entries.append((role, text))
    return entries

def authored_texts(path, roles):
    return [text for _, text in authored_entries(path, roles)]

def is_request(text):
    # A request for new work or a bug report starts a new task. "ok", "làm đi", and an interrupt do not.
    if text.lstrip().startswith("[Request interrupted"):
        return False
    return bool(BUG_RE.search(text) or NEW_WORK_RE.search(text))

def request_scope(path):
    # Labels count from the latest request on, so labels for an earlier task do not open a later one.
    entries = authored_entries(path, ("user", "assistant"))
    for index in range(len(entries) - 1, -1, -1):
        role, text = entries[index]
        if role == "user" and is_request(text):
            return entries[index:]
    return entries

def user_is_bug(path):
    # The latest request decides, so an old bug report does not gate later work.
    for role, text in reversed(authored_entries(path, ("user",))):
        if role != "user" or text.lstrip().startswith("[Request interrupted"):
            continue
        if BUG_RE.search(text):
            return True
        if NEW_WORK_RE.search(text):
            return False
    return False

def has_label_value(labels, text, next_line):
    if re.search("(?:" + labels + ")" + LABEL_END + VALUE, text, re.I):
        return True
    return next_line and bool(re.search("(?:" + labels + ")[*_]*" + COLON + "?" + NEXT_LINE_VALUE, text, re.I))

def reproduce_found():
    found = {key: False for key in REPRODUCE_LABELS}
    for role, text in scoped_entries():
        for key, labels in REPRODUCE_LABELS.items():
            if has_label_value(labels, text, next_line=role == "user"):
                found[key] = True
    return found

def reproduce_present(path):
    return all(reproduce_found().values())

def subagent_transcript():
    # Inside a subagent, transcript_path is the main session. The subagent writes its own text to
    # <session>/subagents/agent-<id>.jsonl, so read that file too when the payload names the agent.
    explicit = event.get("agent_transcript_path") or ""
    if explicit and os.path.isfile(explicit):
        return explicit
    agent_id = event.get("agent_id") or ""
    main = event.get("transcript_path") or ""
    if not agent_id or not main:
        return ""
    session_dir = os.path.splitext(main)[0]
    candidate = os.path.join(session_dir, "subagents", "agent-%s.jsonl" % agent_id)
    return candidate if os.path.isfile(candidate) else ""

def scoped_entries():
    entries = []
    for transcript in (event.get("transcript_path") or "", subagent_transcript()):
        if transcript and os.path.isfile(transcript):
            entries.extend(request_scope(transcript))
    return entries

DECISION_WORD = r"\b(reuse|extend|feature-local|shared|n/a)\b"
REUSE_HEADING_RE = re.compile(r"^\s*(?:#{1,6}\s*|[*_]{2})?\s*Reuse Decision\b", re.I)
HEADING_RE = re.compile(r"^\s*#{1,6}\s")
# Under a Reuse Decision heading, any label can carry the decision, as in "- FE side: **reuse**".
SECTION_DECISION_RE = re.compile(r"[:：]\s*[*_`]*\s*" + DECISION_WORD, re.I)

def decisions_found():
    # Returns (owner found, decision found) for the current request.
    transcript = event.get("transcript_path") or ""
    if not transcript or not os.path.isfile(transcript):
        return False, False
    found_owner = False
    found_reuse = False
    for _, text in scoped_entries():
        in_reuse_section = False
        for line in text.splitlines():
            if REUSE_HEADING_RE.match(line):
                in_reuse_section = True
            elif HEADING_RE.match(line):
                in_reuse_section = False
            if re.search("Runtime owner" + LABEL_END + VALUE, line, re.I):
                found_owner = True
            if "|" in line:
                continue
            if re.search("Decision" + LABEL_END + r"(?!`)[^\n]*?" + DECISION_WORD, line, re.I):
                found_reuse = True
            elif in_reuse_section and SECTION_DECISION_RE.search(line):
                found_reuse = True
        if found_owner and found_reuse:
            break
    return found_owner, found_reuse

def decisions_present():
    return all(decisions_found())

def missing_note(bug_edit):
    # Name what the gate did not find, so the agent does not retry the same edit.
    owner, reuse = decisions_found()
    missing = []
    if not owner:
        missing.append("`Runtime owner:` with a name")
    if not reuse:
        missing.append("`Decision:` with reuse, extend, feature-local, shared, or n/a")
    if bug_edit:
        found = reproduce_found()
        missing += ["`%s:` with a value" % key for key, ok in found.items() if not ok]
    if not missing:
        return "The lines were not in the transcript when the hook read it. Write them again in the reply text, then retry."
    return (
        "Not found after the latest request: " + "; ".join(missing) + ". Retrying the same edit without these lines fails again. "
        "Reply text written earlier in this turn is saved and counts. Write the missing lines now and retry the edit in this turn. "
        "Do not end the turn to ask the user to continue."
    )

CONFLICT_MARKER_RE = re.compile(r"^(?:<{7}|={7}|>{7}|\|{7})(?:\s|$)", re.M)

def behaviorless_one_line():
    if tool_name != "Edit" or not isinstance(tool_input, dict):
        return False
    old = tool_input.get("old_string") or ""
    new = tool_input.get("new_string") or ""
    if not old or not new or old == new:
        return False
    if len(new.splitlines()) != 1 or CONFLICT_MARKER_RE.search(new):
        return False
    # A conflict resolution can replace the marker block with one line. It counts as one line.
    if len(old.splitlines()) != 1 and not CONFLICT_MARKER_RE.search(old):
        return False
    if CONFLICT_MARKER_RE.search(old):
        # A merged line is behaviorless when every word and risky token in it comes from the conflict block.
        old_code = "\n".join(line for line in old.splitlines() if not CONFLICT_MARKER_RE.match(line))
        return (
            set(WORD_RE.findall(new)) <= set(WORD_RE.findall(old_code))
            and set(RISKY_RE.findall(new)) <= set(RISKY_RE.findall(old_code))
        )
    if RISKY_RE.search(new) and not RISKY_RE.search(old):
        return False
    # An import line alone changes no behavior. The edit that uses the name is gated on its own.
    if IMPORT_RE.match(old) and IMPORT_RE.match(new):
        return True
    # A line inside a multi-line class string has no quotes, so check it as a class list.
    if class_list_line(old) and class_list_line(new):
        return True
    old_tail, new_tail = string_tail_skeleton(old), string_tail_skeleton(new)
    if old_tail is not None or new_tail is not None:
        # The quote closes a class string, so only the code after it decides.
        return old_tail == new_tail
    # Wording and style live in strings, JSX text, and comments. Any other change is code: a call, a handler, or a value.
    return code_skeleton(new) == code_skeleton(old)

RISKY_RE = re.compile(r"useState|useEffect|useMemo|useCallback|\?\?|\|\||&&|\bif\s*\(|\bcatch\b|=>|\bawait\b|\bfetch\b")
WORD_RE = re.compile(r"[\w$]+")
STRING_RE = re.compile(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`")
JSX_TEXT_RE = re.compile(r">[^<>{}]*<")

# An import or export list, also the first line of one that spans lines, as in import { a, b, or } from.
IMPORT_RE = re.compile(r"\s*import\s[^;]*\sfrom(?:\s+['\"][^'\"]+['\"])?;?\s*$|\s*(?:import|export)\s+(?:type\s+)?\{[^}]*\}?;?\s*$")
COMMENT_RE = re.compile(r"\{\s*/\*.*?\*/\s*\}|/\*.*?\*/|\{\s*/\*.*$|/\*.*$|^\s*\*.*$|(?<![:\w])//.*$")
# The end of a comment that began on an earlier line, as in "link. */" or "link. */}".
COMMENT_TAIL_RE = re.compile(r"^[^/]*?\*/\s*\}?")
# A quote left open after the closed strings are removed starts a string that ends on a later line.
OPEN_STRING_RE = re.compile(r"[\"'`].*$")
# The first or last line of a multi-line class string carries its quote, as in h-14" or `px-3.
# Upper case appears in arbitrary values such as bg-[#FFFFFF33].
CLASS_TOKEN_RE = re.compile(r"[!\-\"'`]?[A-Za-z0-9\[\]()&>:._/%#+*,=~@-]+[\"'`]?,?$")
JS_WORD_RE = re.compile(r"\b(?:return|const|let|var|if|else|await|import|export|function|new|throw|typeof)\b")

def class_list_line(line):
    tokens = line.split()
    if not tokens or JS_WORD_RE.search(line) or ";" in line:
        return False
    # A class list token has a dash, colon, bracket, slash, or dot, as in h-14.5 or md:w-59. Plain words do not prove it.
    if not any(re.search(r"[-:\[/.]", token) for token in tokens):
        return False
    # A bare operator such as - or + is arithmetic, not a class.
    if not all(CLASS_TOKEN_RE.match(token) and re.search(r"[A-Za-z0-9]", token) for token in tokens):
        return False
    # An object key (open:) or a literal value (true, 12) is code. A class variant always has a utility after the colon.
    return not any(
        re.search(r"[:：]$", token) or re.fullmatch(r"(?:true|false|null|undefined|-?\d+(?:\.\d+)?),?", token)
        for token in tokens
    )

def code_skeleton(line):
    line = COMMENT_TAIL_RE.sub("", line)
    line = COMMENT_RE.sub("", line)
    # The placeholder has no quote, so OPEN_STRING_RE sees only a quote that is really left open.
    line = STRING_RE.sub("STR", line)
    line = OPEN_STRING_RE.sub("STR", line)
    line = JSX_TEXT_RE.sub("><", line)
    return re.sub(r"\s+", "", line)

def string_tail_skeleton(line):
    # A line that starts inside a class string that began on an earlier line, as in px-3 text-primary">.
    match = re.match(r"([^\"'`]*)([\"'`])(.*)$", line)
    if not match or not class_list_line(match.group(1)):
        return None
    # An even count of that quote means the line opens and closes its own strings, as in variant: 'primary'.
    if line.count(match.group(2)) % 2 == 0:
        return None
    return "tail:" + code_skeleton(match.group(3))

def conflict_edit():
    if tool_name != "Edit" or not isinstance(tool_input, dict):
        return False
    return bool(CONFLICT_MARKER_RE.search(tool_input.get("old_string") or ""))

def conflict_lines_only():
    # A resolution that only keeps or reorders lines from the conflict block writes no new code.
    if not conflict_edit():
        return False
    old = tool_input.get("old_string") or ""
    new = tool_input.get("new_string") or ""
    if CONFLICT_MARKER_RE.search(new):
        return False
    old_lines = {line.strip() for line in old.splitlines() if not CONFLICT_MARKER_RE.match(line)}
    return all(line.strip() in old_lines for line in new.splitlines() if line.strip())

gated_view = (
    tool_name in ("Write", "Edit", "MultiEdit")
    and re.search(r"\.(tsx|jsx|vue|svelte)$", path, re.I)
    and not behaviorless_one_line()
    and not conflict_lines_only()
)

def gate_open(bug_edit):
    return decisions_present() and not (bug_edit and not reproduce_present(event.get("transcript_path") or ""))

def gate_open_after_flush(bug_edit):
    # Claude Code can write the reply text of the current turn after this hook reads the transcript.
    # Read again for a short time before a deny, so lines written just before the edit call count.
    import time
    if gate_open(bug_edit):
        return True
    for _ in range(FLUSH_RETRIES):
        time.sleep(FLUSH_WAIT_SECONDS)
        if gate_open(bug_edit):
            return True
    return False

FLUSH_RETRIES = 10
FLUSH_WAIT_SECONDS = 0.3

# A conflict resolution is a merge, not a bug fix, even when the user said the merge failed.
bug_edit = gated_view and not conflict_edit() and user_is_bug(event.get("transcript_path") or "")
if name == "PreToolUse" and gated_view and not gate_open_after_flush(bug_edit):
    reason = DENY_REASON
    if bug_edit:
        reason += " " + DENY_BUG_REASON
    reason += " " + missing_note(bug_edit)
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

def rule_bundle():
    return load_rule("reuse-duplication.md") + "\n\n" + load_rule("modules.md")

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
            "A different job goes in a new file, per rules/modules.md. "
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
    bodies.append(rule_bundle())
    bodies.append(review_context())
elif name == "UserPromptSubmit":
    if prompt_hit or bug_hit:
        bodies.append(load_rule("fe-implementation.md"))
    if (prompt_hit or reuse_hit or author_hit or bug_hit) and not (wording_hit and not bug_hit):
        bodies.append(rule_bundle())
    if prompt_hit or review_hit:
        bodies.append(review_context())
    if conflict_hit or repo_in_conflict(cwd):
        bodies.append(load_rule("conflict-fix.md"))
elif name == "PreToolUse":
    if path_hit:
        bodies.append(load_rule("fe-implementation.md"))
    if source_hit:
        bodies.append(rule_bundle())
    if file_has_markers(full_path) or repo_in_conflict(cwd):
        bodies.append(load_rule("conflict-fix.md"))

emit(name, bodies)
