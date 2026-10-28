import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from xml.sax.saxutils import escape
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/courseware-delivery/scripts/check_pptx.py"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"


class PackageChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.path = self.work / "课件.pptx"

    def make_deck(self, notes="讲解与预期回答", extra=None, omitted=(), undefined_reference=None):
        rels = [("n", "notesSlide", "../notesSlides/notesSlide9.xml", False)]
        if extra:
            rels.append(("extra", *extra))
        def relationship(items):
            return f'<Relationships xmlns="{REL}">' + "".join(
                f'<Relationship Id="{rid}" Type="{OFFICE}{kind}" Target="{escape(target, {chr(34): "&quot;"})}"' + (' TargetMode="External"' if external else '') + '/>'
                for rid, kind, target, external in items) + '</Relationships>'
        parts = {
            "[Content_Types].xml": '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="xml" ContentType="application/xml"/><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/></Types>',
            "_rels/.rels": relationship([("r", "officeDocument", "ppt/presentation.xml", False)]),
            "ppt/presentation.xml": f'<p:presentation xmlns:p="{P}" xmlns:r="{OFFICE[:-1]}"><p:sldIdLst><p:sldId id="256" r:id="chosen"/></p:sldIdLst></p:presentation>',
            "ppt/_rels/presentation.xml.rels": relationship([("chosen", "slide", "slides/slide7.xml", False)]),
            "ppt/slides/slide7.xml": f'<p:sld xmlns:p="{P}" xmlns:a="{A}"><p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r><a:t>先预测</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>',
            "ppt/slides/_rels/slide7.xml.rels": relationship(rels),
            "ppt/notesSlides/notesSlide9.xml": f'<p:notes xmlns:p="{P}" xmlns:a="{A}"><p:cSld><p:spTree><p:sp><p:nvSpPr><p:cNvPr id="2" name="Notes"/><p:cNvSpPr/><p:nvPr><p:ph type="body"/></p:nvPr></p:nvSpPr><p:txBody><a:p><a:r><a:t>{escape(notes)}</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:notes>',
        }
        if undefined_reference:
            xml = parts["ppt/slides/slide7.xml"]
            xml = xml.replace('<p:sld ', f'<p:sld xmlns:r="{OFFICE[:-1]}" ')
            xml = xml.replace('</p:spTree>', f'<p:pic><p:blipFill><a:blip r:{undefined_reference}="missing-resource"/></p:blipFill></p:pic></p:spTree>')
            parts["ppt/slides/slide7.xml"] = xml
        with ZipFile(self.path, "w") as package:
            for name, text in parts.items():
                if name not in omitted:
                    package.writestr(name, text)

    def check(self, root=None):
        args = [sys.executable, str(SCRIPT), str(self.path)]
        if root:
            args.extend(["--bundle-root", str(root)])
        result = subprocess.run(args, cwd=self.work, capture_output=True, text=True)
        self.assertTrue(result.stdout, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_ordered_slide_and_notes_follow_relationships(self):
        self.make_deck()
        code, report = self.check()
        self.assertEqual(code, 0, report)
        self.assertEqual(report["slides"][0]["part"], "ppt/slides/slide7.xml")
        self.assertEqual(report["slides"][0]["notes_characters"], 7)

    def test_missing_notes_part_fails(self):
        self.make_deck(omitted=["ppt/notesSlides/notesSlide9.xml"])
        code, report = self.check()
        self.assertNotEqual(code, 0)
        self.assertTrue(report["errors"])

    def test_empty_teacher_notes_fail(self):
        self.make_deck(notes="  ")
        code, _ = self.check()
        self.assertNotEqual(code, 0)

    def test_missing_internal_media_fails(self):
        self.make_deck(extra=("image", "../media/absent.png", False))
        code, report = self.check()
        self.assertNotEqual(code, 0)
        self.assertTrue(any("absent.png" in error for error in report["errors"]))

    def test_external_media_fails(self):
        self.make_deck(extra=("image", "https://example.com/image.png", True))
        code, report = self.check()
        self.assertNotEqual(code, 0)
        self.assertEqual(len(report["external_dependencies"]), 1)

    def test_web_source_hyperlink_is_allowed(self):
        self.make_deck(extra=("hyperlink", "https://example.com/source", True))
        code, report = self.check()
        self.assertEqual(code, 0, report)
        self.assertEqual(len(report["web_links"]), 1)

    def test_relative_demo_must_exist(self):
        self.make_deck(extra=("hyperlink", "demos/step%20demo.html", True))
        code, _ = self.check()
        self.assertNotEqual(code, 0)
        (self.work / "demos").mkdir()
        (self.work / "demos/step demo.html").write_text("fixture")
        code, report = self.check()
        self.assertEqual(code, 0, report)
        self.assertTrue(report["local_links"][0]["exists"])

    def test_absolute_local_hyperlinks_fail(self):
        for target in ("file:///Users/example/demo.html", "/Users/example/demo.html", "C:\\course\\demo.html"):
            with self.subTest(target=target):
                self.make_deck(extra=("hyperlink", target, True))
                code, _ = self.check()
                self.assertNotEqual(code, 0)

    def test_encoded_hash_is_part_of_attachment_filename(self):
        (self.work / "trace#1.html").write_text("fixture")
        self.make_deck(extra=("hyperlink", "trace%231.html#step2", True))
        code, report = self.check()
        self.assertEqual(code, 0, report)

    def test_encoded_question_mark_does_not_hide_missing_file(self):
        (self.work / "demo.html").write_text("different file")
        self.make_deck(extra=("hyperlink", "demo.html%3Fmissing", True))
        code, _ = self.check()
        self.assertNotEqual(code, 0)

    def test_undefined_xml_relationship_references_fail(self):
        for attribute in ("embed", "link", "id"):
            with self.subTest(attribute=attribute):
                self.make_deck(undefined_reference=attribute)
                code, report = self.check()
                self.assertNotEqual(code, 0)
                self.assertTrue(any("missing-resource" in error for error in report["errors"]))

    def test_relative_link_outside_bundle_fails(self):
        folder = self.work / "output"
        folder.mkdir()
        self.path = folder / "lesson.pptx"
        (self.work / "demo.html").write_text("fixture")
        self.make_deck(extra=("hyperlink", "../demo.html", True))
        code, _ = self.check()
        self.assertNotEqual(code, 0)
        code, report = self.check(root=self.work)
        self.assertEqual(code, 0, report)

    def test_corrupt_package_is_json_failure(self):
        self.path.write_bytes(b"not a zip")
        code, report = self.check()
        self.assertNotEqual(code, 0)
        self.assertTrue(report["errors"])

    def test_missing_required_part_fails(self):
        for part in ("[Content_Types].xml", "ppt/presentation.xml", "ppt/slides/slide7.xml"):
            with self.subTest(part=part):
                self.make_deck(omitted=[part])
                code, _ = self.check()
                self.assertNotEqual(code, 0)

    def test_internal_relationship_cannot_escape_package(self):
        self.make_deck(extra=("image", "../../../../outside.png", False))
        code, _ = self.check()
        self.assertNotEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
