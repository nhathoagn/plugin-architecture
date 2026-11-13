"""Tests for scripts/fe-gate.py. Run: python scripts/test_fe_gate.py (exit code = number of failures).

Each case writes a small transcript, sends one hook payload to the gate as UTF-8 bytes, and checks
the decision: allow, deny, or deny+bug (deny that also asks for Trigger:, Expected:, Actual:).
"""
import json
import os
import subprocess
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "fe-gate.py")
ENV = dict(os.environ, FE_ARCH_ROOT=os.path.dirname(HERE))
TMP = tempfile.mkdtemp(prefix="fe-gate-test-")

def U(text, **extra):
    return dict({"type": "user", "message": {"role": "user", "content": text}}, **extra)

def A(blocks):
    return {"type": "assistant", "message": {"role": "assistant", "content": blocks}}

def T(text):
    return [{"type": "text", "text": text}]

def THINK(text):
    return [{"type": "thinking", "thinking": text}]

def write_transcript(name, entries):
    path = os.path.join(TMP, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return path

def call_gate(payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    result = subprocess.run([sys.executable, "-I", GATE], input=data, capture_output=True, env=ENV)
    return result.stdout.decode("utf-8")

def decision(output):
    if '"deny"' not in output:
        return "allow"
    return "deny+bug" if "Trigger:" in output else "deny"

def pre_tool(entries, tool=None, extra=None):
    transcript = write_transcript("main.jsonl", entries)
    name, tool_input = tool or ("Write", {"file_path": "src/B.tsx", "content": "x"})
    payload = {"hook_event_name": "PreToolUse", "tool_name": name, "tool_input": tool_input,
               "transcript_path": transcript, "cwd": TMP}
    payload.update(extra or {})
    return decision(call_gate(payload))

def E(old, new, path="src/components/confirm/confirm-dialog.tsx"):
    return ("Edit", {"file_path": path, "old_string": old, "new_string": new})

def chat(user, blocks):
    return [U(user), A(blocks)]

OK = "Runtime owner: OrderForm\nDecision: extend\n"
REPRO = "Trigger: click Save\nExpected: 10\nActual: 0\n"

STASH_USER = "đang lỗi tôi không apply stash mới nhất đc"
SUMMARY = THINK("Stash apply đang gây conflict ở `ConfirmDialog` (dòng 120–151 có marker); tôi sẽ giữ footer upstream và dùng lại `toHalfKanaNode` từ stash để gỡ conflict này.")
BLOCK = """                            {visible.confirmText ?? t('labels.button.OK')}
                        </AlertDialogAction>
                    ) : null}
=======
                <AlertDialogFooter className="gap-2 border-t border-border bg-muted px-4 py-2.5 sm:gap-2">
                        {/* @cr CR-half-width-kana: button text shows katakana in half-width. */}
                        {toHalfKanaNode(visible.confirmText ?? t('labels.button.OK'))}
                    </AlertDialogAction>
>>>>>>> Stashed changes"""
COMBINED = """                            {/* @cr CR-half-width-kana: button text shows katakana in half-width. */}
                            {toHalfKanaNode(visible.confirmText ?? t('labels.button.OK'))}
                        </AlertDialogAction>
                    ) : null}"""
WIDTH = """<<<<<<< HEAD
                    'gap-0 overflow-hidden p-0 sm:w-max sm:min-w-sm sm:max-w-2xl',
=======
                    'gap-0 overflow-hidden rounded-xl border-0 p-0 shadow-md sm:max-w-[27rem]',
>>>>>>> develop"""
WIDTH_MERGED = "                    'gap-0 overflow-hidden rounded-xl border-0 p-0 shadow-md sm:w-max sm:min-w-sm sm:max-w-[27rem]',"
M2 = "<<<<<<< HEAD\n  <A x={1} />\n=======\n  <A x={2} />\n>>>>>>> develop"
D3 = "<<<<<<< HEAD\n  <A x={1} />\n||||||| base\n  <A x={0} />\n=======\n  <A x={2} />\n>>>>>>> develop"
NEW_CODE = "                            {toHalfKanaNode(visible.confirmText ?? props.label ?? 'OK')}"

# (name, transcript entries, tool or None, expected)
CASES = [
    # Label formats.
    ("plain labels", chat("add field", T(OK)), None, "allow"),
    ("bold, colon outside", chat("add field", T("**Runtime owner**: OrderForm\n**Decision**: extend")), None, "allow"),
    ("bold, colon inside", chat("add field", T("**Runtime owner:** OrderForm\n**Decision:** extend")), None, "allow"),
    ("italic labels", chat("add field", T("_Runtime owner_: OrderForm\n_Decision_: extend")), None, "allow"),
    ("lowercase reuse decision", chat("add field", T("Runtime owner: OrderForm\nReuse decision: extend")), None, "allow"),
    ("Runtime Owner capital", chat("add field", T("Runtime Owner: OrderForm\nDecision: extend")), None, "allow"),
    ("Decision N/A upper", chat("add field", T("Runtime owner: OrderForm\nDecision: N/A, merge only")), None, "allow"),
    ("Decision Extend capital", chat("add field", T("Runtime owner: OrderForm\nDecision: Extend")), None, "allow"),
    ("full-width colon", chat("add field", T("Runtime owner： OrderForm\nDecision： extend")), None, "allow"),
    ("backquoted values", chat("add field", T("Runtime owner: `OrderForm`\nDecision: `extend`")), None, "allow"),
    ("thinking with labels", chat("add field", THINK(OK)), None, "allow"),
    ("labels written by the user", [U(OK + "thêm cột"), A(T("ok"))], None, "allow"),
    ("decision under a Reuse Decision heading", chat("làm đi sửa ở BE", T("## Architecture\n- Runtime owner: `src/pages/ca3020-seiban-header.tsx:34`.\n\n## Reuse Decision\n- Responsibility: show the label.\n- BE side: **reuse**. The labels come from labelMap.\n- FE side: **reuse** of the rej_reason_name pattern.")), None, "allow"),
    ("decision word outside the Reuse Decision section", chat("add field", T("## Reuse Decision\n- Responsibility: x\n\n## Notes\n- BE side: **reuse**\nRuntime owner: OrderForm")), None, "deny"),
    ("Reuse Decision heading with the template only", chat("add field", T("Runtime owner: OrderForm\n## Reuse Decision\n- Decision: reuse | extend | feature-local | shared")), None, "deny"),
    ("empty labels", chat("add field", T("Runtime owner:\nDecision:")), None, "deny"),
    ("SKILL.md template", chat("add field", T("- Runtime owner:\n- Decision: reuse | extend | feature-local | shared")), None, "deny"),
    ("SKILL.md backquoted template", chat("add field", T("- Runtime owner:\n- Decision: `reuse` | `extend` | `feature-local` | `shared`")), None, "deny"),
    ("table row", chat("add field", T("| Runtime owner: OrderForm | Decision: extend |")), None, "deny"),
    ("empty thinking", chat("add field", THINK("")), None, "deny"),
    ("prose names the fields", chat("add field", T("Write Runtime owner, then Decision, then edit.")), None, "deny"),
    ("no decision word", chat("add field", T("Runtime owner: OrderForm\nDecision: maybe later")), None, "deny"),
    ("labels only in a tool result", [U("thêm cột"), {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": OK}]}}], None, "deny"),
    ("labels only in a meta entry", [U("thêm cột"), U(OK, isMeta=True)], None, "deny"),
    ("labels only in a system-reminder", [U("thêm cột <system-reminder>" + OK + "</system-reminder>")], None, "deny"),
    # Bug mode.
    ("bug, bold repro labels", chat("tổng sai", T(OK + "**Trigger**: click\n**Expected**: 10\n**Actual**: 0")), None, "allow"),
    ("bug, lowercase repro labels", chat("tổng sai", T(OK + "trigger: click\nexpected: 10\nactual: 0")), None, "allow"),
    ("bug, no repro", chat("tổng sai", T(OK)), None, "deny+bug"),
    ("bug, empty Actual", chat("tổng sai", T(OK + "Trigger: click\nExpected: 10\nActual:")), None, "deny+bug"),
    ("'hiển thị sai' is a bug report", chat("ngày hiển thị sai", T(OK)), None, "deny+bug"),
    ("'sai chính tả' is not a bug report", chat("sửa sai chính tả nút Lưu", T(OK)), None, "allow"),
    ("old bug, then new request", [U("tổng sai"), A(T("fixed")), U("thêm cột ngày"), A(T(OK))], None, "allow"),
    ("bug, then 'làm đi'", [U("tổng sai"), A(T(OK)), U("làm đi")], None, "deny+bug"),
    ("bug, then interrupt", [U("tổng sai"), A(T(OK)), U("[Request interrupted by user]")], None, "deny+bug"),
    # Request scope.
    ("labels for an earlier task", [U("thêm cột A"), A(T(OK)), U("thêm cột B"), A(T("ok"))], None, "deny"),
    ("labels, then 'ok'", [U("thêm cột A"), A(T(OK)), U("ok")], None, "allow"),
    ("labels before compact", [U("thêm cột A"), A(T(OK)), U("Summary: the user asked to add a column. đang lỗi build.", isCompactSummary=True), U("tiếp tục")], None, "allow"),
    ("compact summary alone is not a bug report", [U("thêm cột A"), A(T(OK)), U("Summary: lỗi build earlier.", isCompactSummary=True)], None, "allow"),
    # One-line edits that are not conflicts.
    ("one line: className tweak", [U("đổi màu nút")], E("  <B className='p-1' />", "  <B className='p-2' />", "src/B.tsx"), "allow"),
    ("one line: JSX text wording", [U("sửa chữ")], E("  <p>Save</p>", "  <p>Store</p>", "src/B.tsx"), "allow"),
    ("one line: new handler", [U("sửa nút")], E("  <B label='x' />", "  <B label='x' onClick={save} />", "src/B.tsx"), "deny"),
    ("one line: new call", [U("sửa nút")], E("  {label}", "  {toHalf(label)}", "src/B.tsx"), "deny"),
    ("one line: changed value", [U("sửa bảng")], E("  <T limit={10} />", "  <T limit={20} />", "src/B.tsx"), "deny"),
    ("one line: new ?? default", [U("sửa nút")], E("  {label}", "  {label ?? 'OK'}", "src/B.tsx"), "deny"),
    # From a replay of real sessions: lines that change no behavior.
    ("one line: class list inside a multi-line string", [U("sửa")], E("        h-14.5 min-h-14.5", "        h-15.5 min-h-15.5", "src/B.tsx"), "allow"),
    ("one line: class list with arbitrary values", [U("sửa")], E("  [&>svg]:translate-y-0 [&>img]:translate-y-0\"", "  [&>svg]:translate-y-0 [&>svg]:self-center [&>img]:translate-y-0\"", "src/B.tsx"), "allow"),
    ("one line: // comment", [U("sửa")], E("  // Design: the chevron sits 8px from the edge.", "  // Design: the chevron starts 8px from the outer edge.", "src/B.tsx"), "allow"),
    ("one line: JSX comment", [U("sửa")], E("  {/* Until the search ends. */}", "  {/* Until the whole search ends. */}", "src/B.tsx"), "allow"),
    ("one line: doc comment", [U("sửa")], E("/** Design system button. */", "/** Design system button (Button.svg). */", "src/B.tsx"), "allow"),
    ("one line: import list", [U("sửa")], E("import { RotateCcw, Ban } from 'lucide-react';", "import { RotateCcw, Ban, ChevronRight } from 'lucide-react';", "src/B.tsx"), "allow"),
    ("one line: class string opens here", [U("sửa")], E('        className="inline-flex h-8 shrink-0 items-center', '        className="inline-flex h-5 shrink-0 items-center', "src/B.tsx"), "allow"),
    ("one line: class string closes here", [U("sửa")], E('        px-3 text-sm font-semibold text-primary">', '        px-3 text-sm font-medium text-brand-strong">', "src/B.tsx"), "allow"),
    ("one line: open JSX comment", [U("sửa")], E("  {/* The search buttons wait for the lock", "  {/* A search waits for the lock session, so its read shows. */}", "src/B.tsx"), "allow"),
    ("one line: comment end", [U("sửa")], E("   A file is a download link. */", "   A file is a ダウンロード link. */", "src/B.tsx"), "allow"),
    ("one line: export list", [U("sửa")], E("export { Alert, AlertTitle };", "export { Alert, AlertTitle, alertVariants };", "src/B.tsx"), "allow"),
    ("one line: first line of an import list", [U("sửa")], E("import { useCallback, useMemo,", "import { useCallback, useEffect, useMemo,", "src/B.tsx"), "allow"),
    ("one line: import with module on the next line", [U("sửa")], E("import { codeName, LOCKED_CLASS } from", "import { codeName } from", "src/B.tsx"), "allow"),
    ("one line: class string in cn()", [U("sửa")], E("    month: cn('flex flex-col w-full gap-4', defaultClassNames.month),", "    month: cn('flex flex-col w-full gap-2', defaultClassNames.month),", "src/B.tsx"), "allow"),
    ("one line: object key with a class string", [U("sửa")], E("    sm: 'h-8 rounded-md gap-1.5 px-3',", "    sm: 'h-7 rounded-md gap-1.5 px-3',", "src/B.tsx"), "allow"),
    ("one line: class string end with a hex color", [U("sửa")], E("      rounded-[8px] border px-4 bg-[#FFFFFF33]',", "      rounded-[8px] border px-3 has-[>svg]:px-3 bg-[#FFFFFF33]',", "src/B.tsx"), "allow"),
    ("one line: object flag is not a class list", [U("sửa")], E("    open: true,", "    open: false,", "src/B.tsx"), "deny"),
    ("one line: object number is not a class list", [U("sửa")], E("    max-rows: 10,", "    max-rows: 20,", "src/B.tsx"), "deny"),
    ("one line: key with a class string value change", [U("sửa")], E("    month: 'gap-4',", "    month: 'gap-2',", "src/B.tsx"), "allow"),
    ("one line: camelCase word is not a class list", [U("sửa")], E("  emptyRow", "  emptyRow={t('M00001')}", "src/B.tsx"), "deny"),
    ("one line: code after a closing class string", [U("sửa")], E('        px-3">', '        px-3" onClick={save}>', "src/B.tsx"), "deny"),
    ("one line: code before an open string", [U("sửa")], E('  <B a={x} label="one', '  <B a={y} label="one', "src/B.tsx"), "deny"),
    # From the same replay: lines that do change behavior.
    ("one line: hook deps change", [U("sửa")], E("  }, [fitRows, isEmpty]);", "  }, [fitRows, height, isEmpty]);", "src/B.tsx"), "deny"),
    ("one line: condition change", [U("sửa")], E("const failed = shouldSearch && isError && !isFetching;", "const failed = shouldSearch && mutation.isError;", "src/B.tsx"), "deny"),
    ("one line: new prop value", [U("sửa")], E("  emptyRow", "  emptyRow={t('M00001')}", "src/B.tsx"), "deny"),
    ("one line: new call argument", [U("sửa")], E("q.useCatalog('sales-persons');", "q.useCatalog('sales-persons', {});", "src/B.tsx"), "deny"),
    ("one line: arithmetic is not a class list", [U("sửa")], E("  total - discount", "  total + discount", "src/B.tsx"), "deny"),
    ("one line: code after a URL string", [U("sửa")], E("  fetchUrl('http://a/b')", "  fetchUrl('http://a/b', opts)", "src/B.tsx"), "deny"),
    # Conflict edits (from renew-core sessions).
    ("stash: remove one marker line", [U(STASH_USER), A(SUMMARY)], E("<<<<<<< Updated upstream\n                <AlertDialogFooter", "                <AlertDialogFooter"), "allow"),
    ("stash: combine sides", [U(STASH_USER), A(SUMMARY)], E(BLOCK, COMBINED), "allow"),
    ("stash: new code, no labels", [U(STASH_USER), A(SUMMARY)], E(BLOCK, NEW_CODE), "deny"),
    ("stash: new code, labels, no bug fields", [U(STASH_USER), A(T(OK))], E(BLOCK, NEW_CODE), "allow"),
    ("merge: width classes in one line", [U("fix conflict")], E(WIDTH, WIDTH_MERGED), "allow"),
    ("conflict: one line with a new call", [U("fix conflict")], E(M2, "  <A x={toHalf(2)} />"), "deny"),
    ("conflict: one line with a new ??", [U("fix conflict")], E(M2, "  <A x={y ?? 2} />"), "deny"),
    ("conflict: CRLF, pick one side", [U("fix conflict")], E(M2.replace("\n", "\r\n"), "  <A x={2} />"), "allow"),
    ("conflict: diff3, pick base", [U("fix conflict")], E(D3, "  <A x={0} />"), "allow"),
    ("conflict: diff3, new ||", [U("fix conflict")], E(D3, "  <A x={a || 2} />"), "deny"),
    ("conflict: keeps a marker", [U("fix conflict")], E(M2, "=======\n  <A x={2} />"), "deny"),
    ("conflict via MultiEdit", [U("fix conflict")], ("MultiEdit", {"file_path": "src/B.tsx", "edits": [{"old_string": M2, "new_string": "  <A x={2} />"}]}), "deny"),
    ("conflict via Write", [U("fix conflict")], ("Write", {"file_path": "src/B.tsx", "content": "x"}), "deny"),
    ("non-conflict edit after 'lỗi'", [U(STASH_USER), A(T(OK))], E("  a\n  b", "  a\n  c", "src/B.tsx"), "deny+bug"),
    # File types.
    (".ts file is not gated", [U("add field")], ("Edit", {"file_path": "src/b.ts", "old_string": "a\nb", "new_string": "c\nd"}), "allow"),
    (".vue file is gated", [U("add field")], ("Edit", {"file_path": "src/B.vue", "old_string": "a\nb", "new_string": "c\nd"}), "deny"),
]

def run_cases():
    failures = 0
    for name, entries, tool, want in CASES:
        got = pre_tool(entries, tool)
        failures += got != want
        print(("OK  " if got == want else "FAIL"), "%-8s %s" % (want, name) + ("" if got == want else "  (got %s)" % got))
    return failures

def run_special():
    failures = 0
    def check(name, got, want):
        nonlocal failures
        failures += got != want
        print(("OK  " if got == want else "FAIL"), "%-8s %s" % (want, name) + ("" if got == want else "  (got %s)" % got))

    # Subagent: the main transcript has no labels, the subagent transcript has them.
    main = write_transcript("sess.jsonl", [U("thêm cột")])
    write_transcript(os.path.join("sess", "subagents", "agent-abc.jsonl"), [U("thêm cột, edit B.tsx"), A(T(OK))])
    base = {"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "src/B.tsx", "content": "x"},
            "transcript_path": main, "cwd": TMP}
    check("subagent labels, agent_id given", decision(call_gate(dict(base, agent_id="abc"))), "allow")
    check("subagent labels, no agent_id", decision(call_gate(base)), "deny")

    # The reply text reaches the transcript 0.5 seconds after the hook starts.
    late = write_transcript("late.jsonl", [U("thêm cột")])
    def append_later():
        time.sleep(0.5)
        with open(late, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(A(T(OK))) + "\n")
    thread = threading.Thread(target=append_later)
    thread.start()
    check("labels written 0.5 s late", decision(call_gate(dict(base, transcript_path=late))), "allow")
    thread.join()

    # The deny message names the missing line, so the agent does not retry the same edit.
    only_owner = write_transcript("owner.jsonl", chat("add field", T("Runtime owner: OrderForm")))
    out = call_gate(dict(base, transcript_path=only_owner))
    check("deny names the missing Decision line", "allow" if "Not found after the latest request: `Decision:`" in out and "Runtime owner:` with a name" not in out.split("Not found")[1] else "deny", "allow")

    # UserPromptSubmit reads a Vietnamese prompt as UTF-8.
    def injects(prompt):
        out = call_gate({"hook_event_name": "UserPromptSubmit", "prompt": prompt, "cwd": TMP})
        return "allow" if "One-line is defined" in out else "deny"
    check("vi prompt 'đang lỗi màn hình trắng' injects rules (allow = injected)", injects("đang lỗi màn hình trắng"), "allow")
    check("vi prompt 'đổi màu nút' injects no impl rule (deny = none)", injects("đổi màu nút"), "deny")
    return failures

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    total = run_cases() + run_special()
    print("cases: %d, failures: %d" % (len(CASES) + 6, total))
    sys.exit(total)
