"""Read-only PPTX relationship, teacher-note and delivery-file checks."""

import argparse
import json
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile


NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def relationship_file(part):
    return posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")


def inspect_package(path, bundle_root):
    report = {"scope": "pptx-package-only", "pptx": str(path), "bundle_root": str(bundle_root), "slides": [], "local_links": [], "web_links": [], "other_links": [], "external_dependencies": [], "errors": []}
    errors = report["errors"]
    try:
        if not path.is_relative_to(bundle_root) or not bundle_root.is_dir():
            raise ValueError("PPTX 必须位于存在的交付根目录内")
        with ZipFile(path) as package:
            names = set(package.namelist())
            if len(names) != len(package.namelist()):
                errors.append("ZIP 中存在重名部件")
            damaged = package.testzip()
            if damaged:
                errors.append(f"ZIP 校验失败：{damaged}")
            required = {"[Content_Types].xml", "_rels/.rels", "ppt/presentation.xml", "ppt/_rels/presentation.xml.rels"}
            missing = sorted(required - names)
            if missing:
                raise ValueError("缺少必要部件：" + ", ".join(missing))
            ET.fromstring(package.read("[Content_Types].xml"))
            relationships = {}
            for name in sorted(names):
                if not name.endswith(".rels"):
                    continue
                base = posixpath.dirname(posixpath.dirname(name))
                mapping = relationships[name] = {}
                for relation in ET.fromstring(package.read(name)):
                    rid = relation.get("Id")
                    kind = relation.get("Type", "").rsplit("/", 1)[-1]
                    target = relation.get("Target", "")
                    if not rid or rid in mapping or not target:
                        errors.append(f"关系缺少 Id/Target 或 Id 重复：{name}")
                        continue
                    external = relation.get("TargetMode") == "External"
                    mapping[rid] = {"kind": kind, "target": target, "external": external}
                    if external:
                        item = {"owner": name, "target": target, "kind": kind}
                        if kind != "hyperlink":
                            report["external_dependencies"].append(item)
                            errors.append(f"外部资源依赖必须嵌入：{target}")
                            continue
                        parsed = urlsplit(target)
                        decoded_path = unquote(parsed.path)
                        if parsed.scheme.lower() in ("http", "https"):
                            report["web_links"].append(item)
                        elif parsed.scheme.lower() == "file" or decoded_path.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", decoded_path):
                            errors.append(f"本机文件协议或绝对路径链接：{target}")
                        elif parsed.scheme:
                            report["other_links"].append(item)
                        elif parsed.path:
                            resolved = (path.parent / decoded_path.replace("\\", "/")).resolve()
                            item.update(exists=resolved.is_file(), inside_bundle=resolved.is_relative_to(bundle_root))
                            report["local_links"].append(item)
                            if not item["exists"] or not item["inside_bundle"]:
                                errors.append(f"本地附件缺失或越出交付目录：{target}")
                    else:
                        decoded = unquote(urlsplit(target).path)
                        part = posixpath.normpath(decoded.lstrip("/") if decoded.startswith("/") else posixpath.join(base, decoded))
                        mapping[rid]["part"] = part
                        if part == ".." or part.startswith("../") or part not in names:
                            errors.append(f"包内目标缺失或越界：{name} -> {target}")
            reference_attributes = {"{" + NS["r"] + "}" + key for key in ("id", "embed", "link")}
            for part in sorted(name for name in names if name.endswith(".xml")):
                mapping = relationships.get(relationship_file(part), {})
                for element in ET.fromstring(package.read(part)).iter():
                    for attribute, rid in element.attrib.items():
                        if attribute in reference_attributes and rid not in mapping:
                            errors.append(f"关系引用未定义：{part} -> {rid}")
            root_rels = relationships.get("_rels/.rels", {}).values()
            if not any(r["kind"] == "officeDocument" and r.get("part") == "ppt/presentation.xml" for r in root_rels):
                errors.append("根关系没有指向主演示文稿")
            main_rels = relationships.get("ppt/_rels/presentation.xml.rels", {})
            presentation = ET.fromstring(package.read("ppt/presentation.xml"))
            seen = set()
            for index, slide in enumerate(presentation.findall("p:sldIdLst/p:sldId", NS), 1):
                relation = main_rels.get(slide.get("{" + NS["r"] + "}id"), {})
                part = relation.get("part")
                if relation.get("kind") != "slide" or part not in names or part in seen:
                    errors.append(f"第 {index} 页的幻灯片关系缺失或重复")
                    continue
                seen.add(part)
                slide_xml = ET.fromstring(package.read(part))
                record = {"slide": index, "part": part, "editable_text_runs": len(slide_xml.findall(".//a:t", NS)), "notes_characters": 0}
                notes = [r.get("part") for r in relationships.get(relationship_file(part), {}).values() if r["kind"] == "notesSlide"]
                if len(notes) == 1 and notes[0] in names:
                    record["notes_part"] = notes[0]
                    notes_xml = ET.fromstring(package.read(notes[0]))
                    text = []
                    for shape in notes_xml.findall(".//p:sp", NS):
                        placeholder = shape.find(".//p:ph", NS)
                        if placeholder is not None and placeholder.get("type") == "body":
                            text.extend(node.text or "" for node in shape.findall(".//a:t", NS))
                    record["notes_characters"] = len("".join(text).strip())
                if not record["notes_characters"]:
                    errors.append(f"第 {index} 页缺少非空教师备注正文")
                report["slides"].append(record)
            if not report["slides"]:
                errors.append("没有可检查的幻灯片")
    except (OSError, BadZipFile, ET.ParseError, KeyError, ValueError) as error:
        errors.append(str(error))
    report["checks_passed"] = not errors
    return report


def main():
    parser = argparse.ArgumentParser(description="只读检查 PPTX 包、教师备注和附件链接；不验证渲染、教学内容或代码正确性。")
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--bundle-root", type=Path, help="包含课件及其附件的交付根目录，默认 PPTX 所在目录")
    args = parser.parse_args()
    path = args.pptx.resolve()
    root = args.bundle_root.resolve() if args.bundle_root else path.parent
    report = inspect_package(path, root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["checks_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
