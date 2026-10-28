"""Read-only checks of a manually reviewed exam inventory and its local artifacts."""

import argparse
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


MODES = {"single", "gesp", "csp-first", "csp-second"}
KINDS = {"choice", "judgement", "reading", "completion", "program"}
STATUSES = {"pending", "written", "verified", "blocked"}


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} 必须是非空字符串")
    return value


def artifact(value, root, code=False):
    value = text(value, "产物路径")
    uri = urlsplit(value)
    if uri.scheme or uri.netloc or uri.query or "\\" in value or (code and uri.fragment):
        raise ValueError(f"产物须使用本地相对路径，代码不能引用片段：{value}")
    relative = Path(unquote(uri.path))
    path = (root / relative).resolve()
    if relative.is_absolute() or not path.is_relative_to(root):
        raise ValueError(f"产物越出清单目录：{value}")
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"产物文件缺失或为空：{value}")
    if code and path.suffix.lower() not in {".cpp", ".cc", ".cxx", ".py"}:
        raise ValueError(f"分层方案须关联程序文件：{value}")
    return path


def inspect(path):
    report = {
        "scope": "inventory-and-files-only",
        "note": "只检查人工清单和文件，不读取原卷、不执行代码，不证明答案、程序完整性、评分或交互正确。verified 是填写者声明。",
        "expected_count": 0, "item_count": 0, "programs": [], "unfinished": [], "errors": [],
    }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("paper"), dict):
            raise ValueError("清单必须包含 paper 对象")
        paper = data["paper"]
        for field in ("id", "mode", "source"):
            text(paper.get(field), "paper." + field)
        if paper["mode"] not in MODES:
            raise ValueError("paper.mode 必须为 single、gesp、csp-first 或 csp-second")
        report["paper"] = paper
        expected = data.get("expected_ids")
        items = data.get("items")
        if not isinstance(expected, list) or not expected or not isinstance(items, list):
            raise ValueError("expected_ids 必须是非空数组，items 必须是数组")
        for number in expected:
            text(number, "预期题号")
        if len(set(expected)) != len(expected):
            raise ValueError("expected_ids 中存在重复题号")
        actual = []
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("items 中每项必须是对象")
            actual.append(text(item.get("id"), "题号"))
        report.update(expected_count=len(expected), item_count=len(items))
        if len(set(actual)) != len(actual):
            report["errors"].append("items 中存在重复题号")
        missing, extra = set(expected) - set(actual), set(actual) - set(expected)
        if missing:
            report["errors"].append("缺少题号/小问：" + ", ".join(sorted(missing)))
        if extra:
            report["errors"].append("出现非本清单题号：" + ", ".join(sorted(extra)))
        root = path.resolve().parent
        for item in items:
            number = item["id"]
            text(item.get("kind"), f"题目 {number} 的 kind")
            text(item.get("status"), f"题目 {number} 的 status")
            if item.get("kind") not in KINDS or item.get("status") not in STATUSES:
                raise ValueError(f"题目 {number} 的 kind 或 status 无效")
            if item["status"] != "verified":
                report["unfinished"].append(number)
            artifact(item.get("analysis"), root)
            artifact(item.get("verification"), root)
            if item["kind"] == "program":
                solutions = item.get("solutions")
                if not isinstance(solutions, list) or not solutions:
                    raise ValueError(f"编程题 {number} 缺少分层/完整方案")
                ids, paths = set(), set()
                for solution in solutions:
                    if not isinstance(solution, dict):
                        raise ValueError(f"编程题 {number} 的方案必须是对象")
                    name = text(solution.get("id"), "方案编号")
                    if name in ids:
                        raise ValueError(f"编程题 {number} 的方案编号重复：{name}")
                    ids.add(name)
                    text(solution.get("basis"), "适用范围/得分依据")
                    source = artifact(solution.get("code"), root, code=True)
                    artifact(solution.get("verification"), root)
                    if source in paths:
                        raise ValueError(f"编程题 {number} 的多个方案引用同一代码文件")
                    paths.add(source)
                    report["programs"].append({"question": number, "solution": name, "code": str(source)})
    except (OSError, ValueError) as error:
        report["errors"].append(str(error))
    report["checks_passed"] = not report["errors"] and not report["unfinished"]
    return report


def main():
    parser = argparse.ArgumentParser(description="只读检查人工题号清单与分层代码文件；不执行程序或证明评分。")
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    report = inspect(args.inventory)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["checks_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
