import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/lesson-preparation/scripts/check_lesson.py"


class LessonChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def check(self, note, cases=None):
        path = self.work / "中文 讲义.md"
        path.write_text(note, encoding="utf-8")
        args = [sys.executable, str(SCRIPT), str(path)]
        if cases is not None:
            manifest = self.work / "cases.json"
            manifest.write_text(json.dumps(cases), encoding="utf-8")
            args.extend(["--cases", str(manifest)])
        result = subprocess.run(args, cwd=self.work, capture_output=True, text=True)
        self.assertTrue(result.stdout, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_static_mode_does_not_execute_code(self):
        marker = self.work / "should-not-exist"
        code, report = self.check(f"```python\nfrom pathlib import Path\nPath({str(marker)!r}).touch()\n```\n")
        self.assertEqual(code, 0)
        self.assertFalse(marker.exists())
        self.assertEqual(report["programs"][0]["status"], "untested")

    def test_nested_callout_and_long_fence(self):
        note = "> > [!example]- 答案\n> > ````python\n> > print('ok')\n> > ````\n"
        code, report = self.check(note, {"programs": [{"block": 1, "cases": [{"stdin": "", "stdout": "ok\n"}]}]})
        self.assertEqual(code, 0, report)
        self.assertEqual(report["programs"][0]["status"], "passed")

    def test_greater_than_inside_python_string_is_preserved(self):
        for prefix in ("", "> > "):
            with self.subTest(prefix=prefix):
                lines = ["```python", 'print("""', "> hello", '""")', "```"]
                note = "\n".join(prefix + line for line in lines) + "\n"
                code, report = self.check(note, {"programs": [{"block": 1, "cases": [{"stdin": "", "stdout": "\n> hello\n\n"}]}]})
                self.assertEqual(code, 0, report)

    def test_cpp_input_operator_on_new_line_is_preserved(self):
        source = '#include <iostream>\nint main() { int n; std::cin\n>> n; std::cout << n << "\\n"; }'
        code, report = self.check(f"```cpp\n{source}\n```\n", {"programs": [{"block": 1, "cases": [{"stdin": "4\n", "stdout": "4\n"}]}]})
        self.assertEqual(code, 0, report)

    def test_unclosed_fence_is_failure(self):
        code, report = self.check("```cpp\nint main() {}\n")
        self.assertNotEqual(code, 0)
        self.assertTrue(report["errors"])

    def test_missing_mapping_cannot_pass(self):
        code, report = self.check("```python\nprint(1)\n```\n", {"programs": []})
        self.assertNotEqual(code, 0)
        self.assertEqual(report["programs"][0]["status"], "untested")

    def test_output_mismatch_fails(self):
        code, report = self.check("```python\nprint(1)\n```\n", {"programs": [{"block": 1, "cases": [{"stdin": "", "stdout": "2\n"}]}]})
        self.assertNotEqual(code, 0)
        self.assertEqual(report["programs"][0]["status"], "failed")

    def test_skip_needs_reason_and_is_reported(self):
        code, report = self.check("```cpp\nreturn x < y;\n```\n", {"programs": [{"block": 1, "skip": "比较器片段，完整版本另测"}]})
        self.assertEqual(code, 0, report)
        self.assertEqual(report["programs"][0]["status"], "skipped")
        code, _ = self.check("```cpp\nreturn x < y;\n```\n", {"programs": [{"block": 1, "skip": ""}]})
        self.assertNotEqual(code, 0)

    def test_duplicate_or_out_of_range_mapping_fails(self):
        for entries in ([{"block": 2, "skip": "片段"}], [{"block": 1, "skip": "片段"}] * 2):
            with self.subTest(entries=entries):
                code, _ = self.check("```cpp\nint x;\n```\n", {"programs": entries})
                self.assertNotEqual(code, 0)

    def test_invalid_json_has_actionable_error(self):
        path = self.work / "bad.json"
        path.write_text("{", encoding="utf-8")
        note = self.work / "note.md"
        note.write_text("正文\n", encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), str(note), "--cases", str(path)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("errors", json.loads(result.stdout))

    def test_invalid_manifest_shapes_fail(self):
        for manifest in ([], {"programs": "oops"}, {"programs": [{"block": True, "skip": "片段"}]}, {"programs": [{"block": 1, "cases": []}]}):
            with self.subTest(manifest=manifest):
                code, report = self.check("```python\nprint(1)\n```\n", manifest)
                self.assertNotEqual(code, 0)
                self.assertTrue(report["errors"])

    def test_runtime_failure_and_timeout_fail(self):
        for source in ("raise RuntimeError('oops')", "while True: pass"):
            with self.subTest(source=source):
                code, report = self.check(f"```python\n{source}\n```\n", {"programs": [{"block": 1, "cases": [{"stdin": "", "stdout": ""}]}]})
                self.assertNotEqual(code, 0)
                self.assertEqual(report["programs"][0]["status"], "failed")

    def test_cpp14_compiles_and_runs(self):
        source = '#include <iostream>\nint main() { int n; std::cin >> n; std::cout << n + 1 << "\\n"; }'
        code, report = self.check(f"```cpp\n{source}\n```\n", {"programs": [{"block": 1, "cases": [{"stdin": "4\n", "stdout": "5\n"}]}]})
        self.assertEqual(code, 0, report)
        self.assertEqual(report["programs"][0]["status"], "passed")

    def test_cpp_compile_error_is_failure(self):
        code, report = self.check("```cpp\nint main( broken\n```\n", {"programs": [{"block": 1, "cases": [{"stdin": "", "stdout": ""}]}]})
        self.assertNotEqual(code, 0)
        self.assertEqual(report["programs"][0]["status"], "failed")


if __name__ == "__main__":
    unittest.main()
