import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/contest-exam-analysis/scripts/check_inventory.py"


class InventoryChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "inventory.json"
        (self.root / "analysis.md").write_text("解析正文\n")
        (self.root / "verification.md").write_text("人工核对记录\n")
        (self.root / "tier.cpp").write_text("int main() { return 0; }\n")
        self.data = {
            "paper": {"id": "自编小卷", "mode": "csp-first", "source": "人工核对的自编原稿"},
            "expected_ids": ["1", "2.1"],
            "items": [self.item("1", "choice"), self.item("2.1", "program")],
        }

    def item(self, number, kind):
        item = {"id": number, "kind": kind, "status": "verified", "analysis": "analysis.md#题目", "verification": "verification.md"}
        if kind == "program":
            item["solutions"] = [{"id": "brute", "code": "tier.cpp", "basis": "仅有小范围覆盖依据；未测正式数据", "verification": "verification.md#brute"}]
        return item

    def check(self):
        self.path.write_text(json.dumps(self.data, ensure_ascii=False))
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], cwd=self.root, capture_output=True, text=True)
        self.assertTrue(result.stdout, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_complete_inventory_is_explicitly_static(self):
        code, report = self.check()
        self.assertEqual(code, 0, report)
        self.assertEqual(report["scope"], "inventory-and-files-only")
        self.assertEqual(report["expected_count"], 2)
        self.assertEqual(len(report["programs"]), 1)

    def test_missing_subquestion_and_unexpected_id_fail(self):
        self.data["items"][1]["id"] = "2.2"
        code, report = self.check()
        self.assertNotEqual(code, 0)
        self.assertIn("2.1", " ".join(report["errors"]))
        self.assertIn("2.2", " ".join(report["errors"]))

    def test_duplicate_expected_or_actual_ids_fail(self):
        for field in ["expected_ids", "items"]:
            with self.subTest(field=field):
                self.data[field].append(self.data[field][0])
                code, _ = self.check()
                self.assertNotEqual(code, 0)
                self.data[field].pop()

    def test_unverified_item_cannot_count_as_complete(self):
        self.data["items"][0]["status"] = "written"
        code, report = self.check()
        self.assertNotEqual(code, 0)
        self.assertIn("1", report["unfinished"])

    def test_every_tier_requires_code_and_evidence(self):
        solution = self.data["items"][1]["solutions"][0]
        for field in ["code", "basis", "verification"]:
            with self.subTest(field=field):
                value = solution.pop(field)
                code, _ = self.check()
                self.assertNotEqual(code, 0)
                solution[field] = value

    def test_program_cannot_have_no_solutions(self):
        self.data["items"][1]["solutions"] = []
        code, _ = self.check()
        self.assertNotEqual(code, 0)

    def test_missing_or_empty_code_fails(self):
        for content in [None, ""]:
            with self.subTest(content=content):
                path = self.root / "tier.cpp"
                if content is None:
                    path.unlink()
                else:
                    path.write_text(content)
                code, _ = self.check()
                self.assertNotEqual(code, 0)

    def test_multiple_tiers_cannot_alias_same_code_file(self):
        self.data["items"][1]["solutions"].append(dict(self.data["items"][1]["solutions"][0], id="full"))
        code, _ = self.check()
        self.assertNotEqual(code, 0)

    def test_external_absolute_and_escaping_artifacts_fail(self):
        for value in ["https://example.com/code.cpp", str(self.root / "tier.cpp"), "../outside.cpp", "C:\\course\\code.cpp"]:
            with self.subTest(value=value):
                self.data["items"][1]["solutions"][0]["code"] = value
                code, _ = self.check()
                self.assertNotEqual(code, 0)

    def test_encoded_filename_and_fragment_are_resolved_correctly(self):
        (self.root / "analysis#1.md").write_text("解析\n")
        self.data["items"][0]["analysis"] = "analysis%231.md#选择题"
        code, report = self.check()
        self.assertEqual(code, 0, report)

    def test_static_check_does_not_execute_code(self):
        marker = self.root / "executed.txt"
        (self.root / "tier.py").write_text("from pathlib import Path\nPath('executed.txt').write_text('bad')\n")
        self.data["items"][1]["solutions"][0]["code"] = "tier.py"
        code, report = self.check()
        self.assertEqual(code, 0, report)
        self.assertFalse(marker.exists())

    def test_malformed_input_returns_json_failure(self):
        for value in [[], {"paper": {}}, dict(self.data, expected_ids=[True]), dict(self.data, items=[None])]:
            with self.subTest(value=value):
                self.data = value
                code, report = self.check()
                self.assertNotEqual(code, 0)
                self.assertFalse(report["checks_passed"])

    def test_non_scalar_kind_and_status_return_json_failure(self):
        for field in ["kind", "status"]:
            for value in [[], {}]:
                with self.subTest(field=field, value=value):
                    self.data["items"][0][field] = value
                    code, report = self.check()
                    self.assertNotEqual(code, 0)
                    self.assertFalse(report["checks_passed"])
            self.data["items"][0][field] = "choice" if field == "kind" else "verified"


if __name__ == "__main__":
    unittest.main()
