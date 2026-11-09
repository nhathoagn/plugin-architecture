import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]


def command(event):
    group = CONFIG[event][0]
    return group["hooks"][0]["command"].replace("${CLAUDE_PLUGIN_ROOT}", str(ROOT)).strip('"')


def rule_marks():
    marks = {}
    for name, path in (
        ("fe", "fe-implementation.md"),
        ("reuse", "reuse-duplication.md"),
        ("review", "review-diff.md"),
        ("conflict", "conflict-fix.md"),
    ):
        text = (ROOT / "rules" / path).read_text(encoding="utf-8").split("---", 2)[2]
        marks[name] = " ".join(text.split())
    return marks


def context_of(stdout):
    try:
        return json.loads(stdout)["hookSpecificOutput"]["additionalContext"]
    except (json.JSONDecodeError, KeyError):
        return stdout


def only_rules_in(text):
    flat = " ".join(context_of(text).split())
    return {name for name, body in rule_marks().items() if body in flat}


class HooksWiring(unittest.TestCase):
    def run_event(self, event, payload):
        env = os.environ.copy()
        env.pop("CLAUDE_PROJECT_DIR", None)
        return subprocess.run(
            ["sh", "-c", command(event)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_every_hook_points_at_an_executable_script(self):
        for event, groups in CONFIG.items():
            with self.subTest(event=event):
                self.assertEqual(len(groups), 1)
                script = Path(command(event))
                self.assertTrue(script.is_file(), script)
                self.assertTrue(os.access(script, os.X_OK), script)

    def test_edit_before_and_after_use_the_same_matcher(self):
        self.assertEqual(
            CONFIG["PreToolUse"][0]["matcher"],
            CONFIG["PostToolUse"][0]["matcher"],
        )

    def test_frontend_work_gets_its_rules_on_every_event(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            source = repo / "Checkout.tsx"
            source.write_text("export {}\n", encoding="utf-8")
            transcript = repo / "transcript.jsonl"
            transcript.write_text('{"text": "skill://fe-kit"}\n', encoding="utf-8")
            cases = (
                ("UserPromptSubmit", {"prompt": "add a checkout component"}, {"fe", "reuse", "review"}, 0),
                ("UserPromptSubmit", {"prompt": "review the diff before I commit"}, {"review"}, 0),
                ("UserPromptSubmit", {"prompt": "fix the merge conflict"}, {"conflict"}, 0),
                ("UserPromptSubmit", {"prompt": "what is the capital of France"}, set(), 0),
                ("PreToolUse", {"tool_name": "Edit", "cwd": str(repo), "tool_input": {"file_path": str(source)}}, {"fe", "reuse"}, 0),
                ("SessionStart", {"source": "compact", "transcript_path": str(transcript)}, {"fe", "review"}, 0),
                ("SessionStart", {"source": "startup", "transcript_path": str(transcript)}, set(), 0),
                ("PreCompact", {"transcript_path": str(transcript)}, set(), 0),
            )
            for event, payload, expected, code in cases:
                with self.subTest(event=event, payload=payload):
                    result = self.run_event(event, dict(payload, hook_event_name=event))
                    self.assertEqual(result.returncode, code, result.stderr)
                    found = only_rules_in(result.stdout)
                    self.assertEqual(found, expected)
            kept = self.run_event("PreCompact", {"hook_event_name": "PreCompact", "transcript_path": str(transcript)})
            self.assertIn("Keep these rules in the summary.", kept.stdout)

    def test_post_edit_exits_2_on_a_conflict_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "Broken.tsx"
            target.write_text("<<<<<<< HEAD\na\n=======\nb\n>>>>>>> topic\n", encoding="utf-8")
            result = self.run_event("PostToolUse", {
                "hook_event_name": "PostToolUse",
                "tool_name": "Edit",
                "cwd": directory,
                "tool_input": {"file_path": str(target)},
            })
        self.assertEqual(result.returncode, 2)
        self.assertIn("Conflict markers remain", result.stderr)


if __name__ == "__main__":
    unittest.main()
