"""Check Markdown fences; execute reviewed C++/Python only with --cases."""

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


LANGUAGES = {"cpp": ".cpp", "c++": ".cpp", "python": ".py", "py": ".py"}


def extract_programs(text):
    programs, errors = [], []
    fence, language, start, lines = "", "", 0, []
    quote_depth = 0
    for number, original in enumerate(text.splitlines(), 1):
        line = original
        if fence:
            for _ in range(quote_depth):
                line = re.sub(r"^ {0,3}> ?", "", line, count=1)
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                if language in LANGUAGES:
                    programs.append({"block": len(programs) + 1, "line": start, "language": language, "source": "\n".join(lines) + "\n"})
                fence = ""
            else:
                lines.append(line)
        else:
            prefix = re.match(r"^(?: {0,3}> ?)*", line).group()
            line = line[len(prefix):]
            match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if match:
                quote_depth = prefix.count(">")
                fence, info = match.groups()
                language = info.strip().split()[0].lower() if info.strip() else ""
                start, lines = number, []
    if fence:
        errors.append(f"第 {start} 行代码围栏未闭合")
    if text.startswith("---\n") and "\n---" not in text[4:]:
        errors.append("frontmatter 未闭合")
    return programs, errors


def validate_manifest(data, count):
    if not isinstance(data, dict) or not isinstance(data.get("programs"), list):
        raise ValueError("测试清单必须是含 programs 数组的 JSON 对象")
    entries = {}
    for entry in data["programs"]:
        if not isinstance(entry, dict):
            raise ValueError("programs 中每项必须是对象")
        block = entry.get("block")
        if type(block) is not int or not 1 <= block <= count or block in entries:
            raise ValueError(f"代码块编号重复或越界：{block!r}（共 {count} 块）")
        if "skip" in entry:
            if not isinstance(entry["skip"], str) or not entry["skip"].strip() or "cases" in entry:
                raise ValueError(f"代码块 {block} 必须提供非空 skip 原因，且不能同时带 cases")
        else:
            cases = entry.get("cases")
            if not isinstance(cases, list) or not cases:
                raise ValueError(f"代码块 {block} 缺少非空 cases 数组")
            for case in cases:
                if not isinstance(case, dict) or not all(isinstance(case.get(key), str) for key in ("stdin", "stdout")):
                    raise ValueError(f"代码块 {block} 每个用例的 stdin 和 stdout 都必须是字符串")
        entries[block] = entry
    return entries


def run_program(program, cases, directory):
    path = directory / (str(program["block"]) + LANGUAGES[program["language"]])
    path.write_text(program["source"], encoding="utf-8")
    record = {"status": "passed", "cases": []}
    command = [sys.executable, str(path)]
    if path.suffix == ".cpp":
        compiler = shutil.which("c++")
        if compiler is None:
            return {"status": "failed", "error": "找不到 C++ 编译器 c++"}
        executable = path.with_suffix("")
        command = [compiler, "-std=c++14", "-Wall", "-Wextra", "-pedantic", str(path), "-o", str(executable)]
        compiled = subprocess.run(command, capture_output=True, text=True, cwd=directory, timeout=30)
        record["compile"] = {"command": command, "returncode": compiled.returncode, "diagnostics": compiled.stderr}
        if compiled.returncode:
            record["status"] = "failed"
            return record
        command = [str(executable)]
    for number, case in enumerate(cases, 1):
        try:
            result = subprocess.run(command, input=case["stdin"], capture_output=True, text=True, cwd=directory, timeout=2)
            passed = result.returncode == 0 and result.stdout == case["stdout"]
            record["cases"].append({"case": number, "passed": passed, "stdin": case["stdin"], "expected": case["stdout"], "actual": result.stdout, "returncode": result.returncode, "stderr": result.stderr})
        except subprocess.TimeoutExpired:
            passed = False
            record["cases"].append({"case": number, "passed": False, "error": "运行超时（2秒）"})
        if not passed:
            record["status"] = "failed"
    return record


def main():
    parser = argparse.ArgumentParser(description="Markdown 围栏检查；--cases 会执行已审阅代码（临时目录不提供安全隔离）。")
    parser.add_argument("note", type=Path)
    parser.add_argument("--cases", type=Path, help="显式启用程序执行的 JSON 清单；不提供则只检查结构")
    args = parser.parse_args()
    report = {"scope": "structure-and-listed-cases" if args.cases else "structure-only", "note": str(args.note.resolve()), "programs": [], "errors": []}
    try:
        programs, errors = extract_programs(args.note.read_text(encoding="utf-8"))
        report["errors"].extend(errors)
        report["programs"] = [{key: value for key, value in program.items() if key != "source"} | {"status": "untested"} for program in programs]
        entries = validate_manifest(json.loads(args.cases.read_text(encoding="utf-8")), len(programs)) if args.cases else {}
        if not errors:
            with tempfile.TemporaryDirectory(prefix="lesson-check-") as temp:
                for program, record in zip(programs, report["programs"]):
                    entry = entries.get(program["block"])
                    if entry is None:
                        if args.cases:
                            report["errors"].append(f"代码块 {program['block']} 未在测试清单中说明")
                    elif "skip" in entry:
                        record.update(status="skipped", reason=entry["skip"])
                    else:
                        record.update(run_program(program, entry["cases"], Path(temp)))
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        report["errors"].append(str(error))
    report["checks_passed"] = not report["errors"] and all(p["status"] != "failed" for p in report["programs"])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["checks_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
