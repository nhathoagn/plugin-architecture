import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "fe-gate.py"
FIXTURE = ROOT / "tests" / "rule-repo"


def run_gate(event):
    env = os.environ.copy()
    env["FE_ARCH_ROOT"] = str(ROOT)
    return subprocess.run(
        ["python3", str(GATE)],
        input=json.dumps(event),
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )


class RuleRepo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "rule-repo"
        shutil.copytree(FIXTURE, self.repo)
        script = self.repo / ".claude" / "rules.sh"
        script.chmod(script.stat().st_mode | stat.S_IXUSR)

    def tearDown(self):
        self.tmp.cleanup()

    def edit(self, name):
        return run_gate({
            "hook_event_name": "PostToolUse",
            "tool_name": "Edit",
            "cwd": str(self.repo),
            "tool_input": {"file_path": str(self.repo / "src" / name)},
        })

    def test_clean_edit_passes_and_pre_edit_injects_the_skill(self):
        target = self.repo / "src" / "Checkout.tsx"
        edited = self.edit("Checkout.tsx")
        self.assertEqual(edited.returncode, 0, edited.stderr)
        self.assertEqual(edited.stdout, "")
        before = run_gate({
            "hook_event_name": "PreToolUse",
            "tool_name": "Edit",
            "cwd": str(self.repo),
            "tool_input": {"file_path": str(target)},
        })
        self.assertEqual(before.returncode, 0, before.stderr)
        self.assertIn("read `skill://fe-kit`", before.stdout)

    def test_console_log_fails_repo_rules(self):
        result = self.edit("BadBanner.tsx")
        self.assertEqual(result.returncode, 2)
        self.assertIn("console.log", result.stderr)
        self.assertIn("VI PHẠM RULE", result.stderr)

    def test_secret_fails_repo_rules(self):
        result = self.edit("SecretForm.tsx")
        self.assertEqual(result.returncode, 2)
        self.assertIn("sk_live_", result.stderr)
        self.assertIn("VI PHẠM RULE", result.stderr)

    def test_conflict_markers_fail_before_the_next_edit(self):
        result = self.edit("Conflicted.tsx")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Conflict markers remain", result.stderr)
        self.assertIn("Conflicted.tsx", result.stderr)

    def test_hook_catches_mechanical_anti_patterns(self):
        cases = (
            ("Note.tsx", "HTML thô"),
            ("OrderList.tsx", "catch rỗng"),
            ("JobRows.tsx", "index làm key"),
        )
        for name, mark in cases:
            with self.subTest(name=name):
                result = self.edit(name)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(mark, result.stderr)

    def test_review_only_anti_patterns_do_not_fail_the_hook(self):
        for name in ("AddressForm.tsx", "CheckoutScreen.tsx", "NumberField.tsx", "price.ts", "saveCard.ts"):
            with self.subTest(name=name):
                result = self.edit(name)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, "")

    def test_new_view_in_this_repo_is_denied_without_a_decision(self):
        missing = self.repo / "src" / "NewScreen.tsx"
        transcript = self.repo / "transcript.jsonl"
        transcript.write_text("planning the screen\n", encoding="utf-8")
        denied = run_gate({
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "cwd": str(self.repo),
            "transcript_path": str(transcript),
            "tool_input": {"file_path": str(missing)},
        })
        self.assertEqual(denied.returncode, 0, denied.stderr)
        payload = json.loads(denied.stdout)["hookSpecificOutput"]
        self.assertEqual(payload["permissionDecision"], "deny")
