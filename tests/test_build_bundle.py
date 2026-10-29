import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/build_bundle.py"


class BundleChecks(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("build_bundle", SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "dist/bundle.zip"
        (self.root / "plugin.json").write_text(json.dumps({"name": "teaching-bundle", "version": "0.4.0-dev", "description": "测试套件"}))
        (self.root / "BUNDLE.md").write_text("完整套件说明\n")
        for name in ["alpha", "beta"]:
            p = self.root / "skills" / name
            (p / "references").mkdir(parents=True)
            (p / "SKILL.md").write_text(f"---\nname: {name}\ndescription: test\n---\n")
            (p / "references/guide.md").write_text("支持资源\n")

    def build(self):
        return self.module.build_bundle(self.root, self.output)

    def test_complete_modules_and_hashes_are_in_archive(self):
        report = self.build()
        with ZipFile(self.output) as package:
            data = json.loads(package.read("bundle-manifest.json"))
            self.assertEqual(data["skills"], ["alpha", "beta"])
            self.assertIn("skills/beta/references/guide.md", package.namelist())
            self.assertEqual(set(package.namelist()), set(data["files"]) | {"bundle-manifest.json"})
            for name, digest in data["files"].items():
                self.assertEqual(hashlib.sha256(package.read(name)).hexdigest(), digest)
        self.assertEqual(report["skills"], 2)
        self.assertEqual(report["sha256"], hashlib.sha256(self.output.read_bytes()).hexdigest())
        self.assertIn(report["sha256"], self.output.with_suffix(".zip.sha256").read_text())

    def test_repository_bundle_contains_complete_project_workflow(self):
        repository = SCRIPT.parents[1]
        self.module.build_bundle(repository, self.output)
        with ZipFile(self.output) as package:
            manifest = json.loads(package.read("bundle-manifest.json"))
            self.assertIn("project-teaching", manifest["skills"])
            folder = repository / "skills/project-teaching"
            for name in [
                "SKILL.md", "agents/openai.yaml",
                "references/learning-design.md", "references/language-paths.md",
                "references/handoffs-and-verification.md",
                "assets/project-design-template.md", "assets/acceptance-template.md",
            ]:
                member = "skills/project-teaching/" + name
                self.assertEqual(package.read(member), (folder / name).read_bytes())

    def test_runtime_caches_are_excluded(self):
        p = self.root / "skills/alpha"
        (p / ".DS_Store").write_bytes(b"cache")
        (p / "__pycache__").mkdir()
        (p / "__pycache__/module.pyc").write_bytes(b"cache")
        self.build()
        with ZipFile(self.output) as package:
            self.assertFalse(any(".DS_Store" in name or "__pycache__" in name for name in package.namelist()))

    def test_missing_skill_entrypoint_fails(self):
        (self.root / "skills/beta/SKILL.md").unlink()
        with self.assertRaises(ValueError):
            self.build()

    def test_symlink_cannot_pull_in_external_files(self):
        (self.root / "secret.txt").write_text("private")
        (self.root / "skills/alpha/references/external.md").symlink_to(self.root / "secret.txt")
        with self.assertRaises(ValueError):
            self.build()

    def test_hidden_configuration_is_rejected(self):
        (self.root / "skills/alpha/.env").write_text("SECRET=value")
        with self.assertRaises(ValueError):
            self.build()

    def test_invalid_manifest_and_empty_tree_fail(self):
        (self.root / "plugin.json").write_text("[]")
        with self.assertRaises(ValueError):
            self.build()
        (self.root / "plugin.json").write_text(json.dumps({"name": "teaching-bundle", "version": "0.4.0-dev", "description": "测试套件"}))
        for name in ["alpha", "beta"]:
            shutil.rmtree(self.root / "skills" / name)
        with self.assertRaises(ValueError):
            self.build()

    def test_failed_rebuild_preserves_old_package(self):
        self.build()
        before = self.output.read_bytes()
        (self.root / "skills/beta/SKILL.md").unlink()
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(before, self.output.read_bytes())

    def test_rebuild_is_reproducible_and_does_not_overwrite_source(self):
        self.build()
        before = self.output.read_bytes()
        self.build()
        self.assertEqual(before, self.output.read_bytes())
        self.output = self.root / "plugin.json"
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(json.loads(self.output.read_text())["name"], "teaching-bundle")

    def test_repository_output_is_limited_to_dist(self):
        for name in ["README.md", "scripts/build_bundle.py", "archive.zip"]:
            with self.subTest(name=name):
                self.output = self.root / name
                self.output.parent.mkdir(parents=True, exist_ok=True)
                self.output.write_text("source file")
                with self.assertRaises(ValueError):
                    self.build()
                self.assertEqual(self.output.read_text(), "source file")

    def test_directory_checksum_target_preserves_old_zip(self):
        self.build()
        before = self.output.read_bytes()
        checksum = self.output.with_suffix(".zip.sha256")
        checksum.unlink()
        checksum.mkdir()
        (self.root / "BUNDLE.md").write_text("changed payload\n")
        with self.assertRaises((OSError, ValueError)):
            self.build()
        self.assertEqual(self.output.read_bytes(), before)
        self.assertTrue(checksum.is_dir())

    def test_second_replace_failure_restores_both_old_files(self):
        self.build()
        before = self.output.read_bytes()
        checksum = self.output.with_suffix(".zip.sha256")
        previous_checksum = checksum.read_bytes()
        (self.root / "BUNDLE.md").write_text("changed payload\n")
        original = Path.replace

        def fail_checksum(source, target):
            if source.name == "checksum.txt":
                raise OSError("simulated checksum replacement failure")
            return original(source, target)

        with patch.object(Path, "replace", fail_checksum):
            with self.assertRaises(OSError):
                self.build()
        self.assertEqual(self.output.read_bytes(), before)
        self.assertEqual(checksum.read_bytes(), previous_checksum)


if __name__ == "__main__":
    unittest.main()
