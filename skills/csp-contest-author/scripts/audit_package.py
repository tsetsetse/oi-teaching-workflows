#!/usr/bin/env python3
"""Read-only layout/manifest audit. Does not execute solutions or certify answers."""

import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path


ROOT_FILES = ("README.md", "make_data.py", "verify.py", "validation-report.md")
PROBLEM_FILES = (
    "statement.md", "solution.md", "src/std.cpp", "src/brute.cpp", "src/gen.cpp",
    "work/data_plan.json", "work/make_data.py", "work/validate.py", "work/stress.py",
)


class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def positive_int(value):
    return type(value) is int and value > 0


def check_problem(problem):
    for relative in PROBLEM_FILES:
        path = problem / relative
        require(path.is_file(), f"missing {relative}")
        require(path.stat().st_size > 0, f"empty {relative}")

    statement = (problem / "statement.md").read_text(encoding="utf-8")
    inputs = re.findall(r"^## 样例输入 (\d+)\s*$", statement, re.MULTILINE)
    outputs = re.findall(r"^## 样例输出 (\d+)\s*$", statement, re.MULTILINE)
    require(inputs and inputs == outputs and len(inputs) == len(set(inputs)),
            "sample input/output headings must have matching unique IDs")

    plan = json.loads((problem / "work/data_plan.json").read_text(encoding="utf-8"))
    require(isinstance(plan, dict), "data_plan must be an object")
    scoring = plan.get("scoring")
    require(scoring in ("sum", "group-min"), "unknown scoring mode")
    cases, subtasks = plan.get("cases"), plan.get("subtasks")
    require(isinstance(cases, list) and cases, "cases must be a nonempty list")
    require(isinstance(subtasks, list) and subtasks, "subtasks must be a nonempty list")

    by_id = {}
    for case in cases:
        require(isinstance(case, dict), "case must be an object")
        case_id = case.get("id")
        require(positive_int(case_id), "case ID must be a positive integer")
        require(case_id not in by_id, f"duplicate case ID {case_id}")
        by_id[case_id] = case
        require(type(case.get("seed")) is int, f"case {case_id}: missing integer seed")
        args = case.get("args")
        require(isinstance(args, list) and args and all(isinstance(x, str) for x in args),
                f"case {case_id}: args must be nonempty strings list")
        require(isinstance(case.get("purpose"), str) and case["purpose"].strip(),
                f"case {case_id}: missing purpose")
        tags = case.get("tags")
        require(isinstance(tags, list) and tags and all(isinstance(x, str) and x for x in tags),
                f"case {case_id}: missing coverage tags")
        if scoring == "sum":
            require(positive_int(case.get("points")), f"case {case_id}: invalid points")
        else:
            require("points" not in case, "group-min assigns points to subtasks, not cases")

    membership, subtask_ids, total = [], set(), 0
    for subtask in subtasks:
        require(isinstance(subtask, dict), "subtask must be an object")
        sid = subtask.get("id")
        require(isinstance(sid, str) and sid and sid not in subtask_ids,
                "subtask ID missing or duplicated")
        subtask_ids.add(sid)
        require(positive_int(subtask.get("points")), f"subtask {sid}: invalid points")
        total += subtask["points"]
        require(isinstance(subtask.get("constraints"), str) and subtask["constraints"].strip(),
                f"subtask {sid}: missing constraints description")
        ids = subtask.get("cases")
        require(isinstance(ids, list) and ids and all(positive_int(x) for x in ids),
                f"subtask {sid}: cases must contain positive integers")
        require(all(x in by_id for x in ids), f"subtask {sid}: references unknown case")
        membership.extend(ids)
        if scoring == "sum":
            require(sum(by_id[x]["points"] for x in ids) == subtask["points"],
                    f"subtask {sid}: case points do not match subtask points")
    require(total == 100, "subtask points must total 100")
    require(set(membership) == set(by_id) and len(membership) == len(by_id),
            "each case must belong to exactly one subtask")

    expected = {f"{case_id}.{suffix}" for case_id in by_id for suffix in ("in", "out")}
    actual = {p.name for p in (problem / "data").glob("*") if p.suffix in (".in", ".out")}
    require(actual == expected,
            f"data pairs differ from plan: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
    seen = {}
    for case_id, case in by_id.items():
        for suffix in ("in", "out"):
            require((problem / "data" / f"{case_id}.{suffix}").is_file(),
                    f"{case_id}.{suffix} is not a file")
        digest = hashlib.sha256((problem / "data" / f"{case_id}.in").read_bytes()).hexdigest()
        reason = case.get("duplicate_reason")
        require(digest not in seen or (isinstance(reason, str) and reason.strip()),
                f"case {case_id}: duplicate input of {seen.get(digest)} without duplicate_reason")
        seen[digest] = case_id
    return len(cases)


def audit(root):
    errors, counts = [], {}
    for name in ROOT_FILES:
        if not (root / name).is_file() or (root / name).stat().st_size == 0:
            errors.append(f"root: missing or empty {name}")
    problems = sorted(p for p in root.glob("P[0-9]*-*") if p.is_dir())
    if not problems:
        errors.append("root: no P<number>-<slug> problem directories")
    for problem in problems:
        try:
            counts[problem.name] = check_problem(problem)
        except (AuditError, OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"{problem.name}: {exc}")
    return errors, counts


def self_test():
    # Structural fixtures only: deliberately not executable contest problems.
    with tempfile.TemporaryDirectory(prefix="csp-skill-audit-") as tmp:
        root = Path(tmp)
        problem = root / "P1-fixture"
        for path in [*(root / name for name in ROOT_FILES),
                     *(problem / name for name in PROBLEM_FILES)]:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("structure-test fixture\n", encoding="utf-8")
        statement = problem / "statement.md"
        statement.write_text("## 样例输入 1\n\n## 样例输出 1\n", encoding="utf-8")
        (problem / "data").mkdir()
        for case_id in (1, 2):
            (problem / "data" / f"{case_id}.in").write_text(f"{case_id}\n")
            (problem / "data" / f"{case_id}.out").write_text("0\n")
        plan = {
            "scoring": "sum",
            "subtasks": [{"id": "S1", "points": 100, "constraints": "fixture", "cases": [1, 2]}],
            "cases": [{"id": i, "points": 50, "seed": i, "args": ["min"],
                       "purpose": "fixture", "tags": ["boundary"]} for i in (1, 2)],
        }
        manifest = problem / "work/data_plan.json"

        def save():
            manifest.write_text(json.dumps(plan), encoding="utf-8")

        def expect(valid, label):
            errors, _ = audit(root)
            require((not errors) == valid, f"self-test {label}: {errors}")

        save()
        expect(True, "valid sum; equal outputs allowed")
        output = problem / "data/2.out"
        output.unlink()
        expect(False, "missing output")
        output.write_text("0\n")
        second = problem / "data/2.in"
        second.write_text("1\n")
        expect(False, "duplicate input")
        second.write_text("2\n")
        plan["subtasks"][0]["points"] = 90
        save()
        expect(False, "score mismatch")
        plan["subtasks"][0]["points"] = 100
        plan["subtasks"][0]["cases"] = [1, 1]
        save()
        expect(False, "duplicate membership")
        plan["subtasks"][0]["cases"] = [1, 2]
        plan["cases"][1]["seed"] = None
        save()
        expect(False, "missing seed")
        plan["cases"][1]["seed"] = 2
        plan["scoring"] = "group-min"
        for case in plan["cases"]:
            del case["points"]
        save()
        expect(True, "valid group-min")
        statement.write_text("## 样例输入 1\n\n## 样例输出 2\n", encoding="utf-8")
        expect(False, "sample ID mismatch")
    print("SELF_TEST_OK: 8 layout/manifest checks")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        if args.root is not None:
            parser.error("choose a package root or --self-test, not both")
        self_test()
        return 0
    if args.root is None:
        parser.error("a package root is required")
    errors, counts = audit(args.root.resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"LAYOUT_OK: {len(counts)} problems, {sum(counts.values())} paired cases")
    print("Only structure and manifest were checked; run the package's verify.py for algorithm/data checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
