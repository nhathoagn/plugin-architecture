import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "fe-gate.py"
RULE = ROOT / "rules" / "reuse-duplication.md"

REUSE_MARK = "Duplicated code means the same statements written again"
NOT_CODE_DUP = "A repeated value or a repeated request is not this check."
FE_MARK = "read `skill://fe-kit`"
CONFLICT_MARK = "Do not paste both conflict blocks into the file."


def run_gate(event):
    event.setdefault("cwd", "/tmp")
    env = os.environ.copy()
    env["FE_ARCH_ROOT"] = str(ROOT)
    result = subprocess.run(
        ["python3", str(GATE)],
        input=json.dumps(event),
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    if not result.stdout.strip():
        return None
    return json.loads(result.stdout)["hookSpecificOutput"]


def context(event):
    spec = run_gate(event)
    if spec is None:
        return ""
    return spec.get("additionalContext") or ""


class ReuseRuleText(unittest.TestCase):
    def test_rule_defines_duplicated_code_as_the_same_lines(self):
        text = RULE.read_text(encoding="utf-8")
        self.assertIn("alwaysApply: true", text)
        self.assertIn("search before you write it", text)
        self.assertIn(REUSE_MARK, text)
        self.assertIn(NOT_CODE_DUP, text)
        self.assertIn("`reuse`, `extend`, `feature-local`, or `shared`", text)
        self.assertIn("Name both locations of any duplicated code", text)
        self.assertIn("differ only by data", text)
        self.assertIn("as const satisfies", text)
        self.assertIn("value[field.key]", text)
        self.assertNotIn("type Address", text)
        self.assertNotIn("same literal under two names", text)


class ReuseRuleInjection(unittest.TestCase):
    def test_wording_and_style_prompts_skip_the_rule(self):
        for prompt in (
            "Fix the typo on the Submit button.",
            "Change the button color from blue to gray.",
            "What does omp v18.12.6 change?",
        ):
            with self.subTest(prompt=prompt):
                self.assertEqual(context({"hook_event_name": "UserPromptSubmit", "prompt": prompt}), "")

    def test_new_code_prompt_injects_reuse_without_the_frontend_skill(self):
        text = context({
            "hook_event_name": "UserPromptSubmit",
            "prompt": "Add a retry to the Go payment worker.",
        })
        self.assertIn(REUSE_MARK, text)
        self.assertIn(NOT_CODE_DUP, text)
        self.assertNotIn(FE_MARK, text)
        self.assertNotIn(CONFLICT_MARK, text)

    def test_frontend_prompt_injects_the_skill_and_the_reuse_rule(self):
        text = context({
            "hook_event_name": "UserPromptSubmit",
            "prompt": "Viết component form địa chỉ cho trang checkout, đừng tạo form library mới.",
        })
        self.assertIn(FE_MARK, text)
        self.assertIn(REUSE_MARK, text)
        self.assertNotIn(CONFLICT_MARK, text)

    def test_duplicated_code_prompt_injects_the_code_check(self):
        text = context({
            "hook_event_name": "UserPromptSubmit",
            "prompt": "Hai file đang lặp code cùng một hàm tính giảm giá.",
        })
        self.assertIn(REUSE_MARK, text)
        self.assertIn(NOT_CODE_DUP, text)
        self.assertNotIn(CONFLICT_MARK, text)

    def test_merge_conflict_prompt_injects_the_conflict_rule(self):
        text = context({
            "hook_event_name": "UserPromptSubmit",
            "prompt": "Resolve the merge conflict in checkout.",
        })
        self.assertIn(CONFLICT_MARK, text)
        self.assertNotIn(REUSE_MARK, text)

    def test_source_edit_injects_reuse_for_backend_and_frontend(self):
        with tempfile.TemporaryDirectory() as directory:
            py = Path(directory) / "worker.py"
            tsx = Path(directory) / "Checkout.tsx"
            md = Path(directory) / "README.md"
            py.write_text("def retry():\n    pass\n", encoding="utf-8")
            tsx.write_text("export {}\n", encoding="utf-8")
            md.write_text("# notes\n", encoding="utf-8")
            py_text = context({
                "hook_event_name": "PreToolUse",
                "tool_name": "Edit",
                "cwd": directory,
                "tool_input": {"file_path": str(py)},
            })
            tsx_text = context({
                "hook_event_name": "PreToolUse",
                "tool_name": "Edit",
                "cwd": directory,
                "tool_input": {"file_path": str(tsx)},
            })
            md_text = context({
                "hook_event_name": "PreToolUse",
                "tool_name": "Edit",
                "cwd": directory,
                "tool_input": {"file_path": str(md)},
            })
        self.assertIn(REUSE_MARK, py_text)
        self.assertNotIn(FE_MARK, py_text)
        self.assertIn(REUSE_MARK, tsx_text)
        self.assertIn(FE_MARK, tsx_text)
        self.assertEqual(md_text, "")

    def test_new_view_is_denied_until_the_reuse_decision_is_recorded(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / "Checkout.vue")
            transcript = Path(directory) / "transcript.jsonl"
            transcript.write_text("planning the screen\n", encoding="utf-8")
            denied = run_gate({
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "cwd": directory,
                "transcript_path": str(transcript),
                "tool_input": {"file_path": missing},
            })
            transcript.write_text(
                "Runtime owner: checkout\nReuse Decision: reuse\n",
                encoding="utf-8",
            )
            allowed = run_gate({
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "cwd": directory,
                "transcript_path": str(transcript),
                "tool_input": {"file_path": missing},
            })
        self.assertEqual(denied["permissionDecision"], "deny")
        self.assertNotIn("additionalContext", denied)
        self.assertNotIn("permissionDecision", allowed)
        self.assertIn(REUSE_MARK, allowed["additionalContext"])

    def test_conflict_markers_in_source_inject_both_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "worker.py"
            target.write_text("<<<<<<< HEAD\nold\n=======\nnew\n>>>>>>> topic\n", encoding="utf-8")
            text = context({
                "hook_event_name": "PreToolUse",
                "tool_name": "Edit",
                "cwd": directory,
                "tool_input": {"file_path": str(target)},
            })
        self.assertIn(REUSE_MARK, text)
        self.assertIn(CONFLICT_MARK, text)

    def test_empty_and_invalid_input_emit_nothing(self):
        env = os.environ.copy()
        env["FE_ARCH_ROOT"] = str(ROOT)
        for raw in ("", "not-json"):
            result = subprocess.run(
                ["python3", str(GATE)],
                input=raw,
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
