"""Build a portable plugin archive from complete local skill folders; no installation."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


IGNORED = {".DS_Store", "__pycache__", ".git"}


def build_bundle(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output.suffix.lower() != ".zip":
        raise ValueError("输出必须是ZIP文件")
    if output.is_relative_to(root) and not output.is_relative_to(root / "dist"):
        raise ValueError("仓库内的输出只能保存在dist目录，不能覆盖源码")
    payload = {}

    def add(path):
        relative = path.relative_to(root)
        if path.is_symlink():
            raise ValueError(f"不打包软链接：{relative}")
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"打包文件缺失或为空：{relative}")
        payload[relative.as_posix()] = path.read_bytes()

    add(root / "plugin.json")
    add(root / "BUNDLE.md")
    plugin = json.loads(payload["plugin.json"])
    if not isinstance(plugin, dict):
        raise ValueError("plugin.json 必须是对象")
    if not isinstance(plugin.get("name"), str) or not re.fullmatch(r"[a-z][a-z0-9-]*", plugin["name"]):
        raise ValueError("插件名称无效")
    for key in ("version", "description"):
        if not isinstance(plugin.get(key), str) or not plugin[key].strip():
            raise ValueError(f"插件缺少 {key}")
    skills_root = root / "skills"
    if skills_root.is_symlink() or not skills_root.is_dir():
        raise ValueError("缺少本地 skills 目录")
    names = []
    for folder in sorted(skills_root.iterdir()):
        if folder.name in IGNORED:
            continue
        if folder.is_symlink() or not folder.is_dir() or not re.fullmatch(r"[a-z][a-z0-9-]*", folder.name):
            raise ValueError(f"技能目录无效：{folder.name}")
        if not (folder / "SKILL.md").is_file():
            raise ValueError(f"技能缺少 SKILL.md：{folder.name}")
        names.append(folder.name)
        for path in sorted(folder.rglob("*")):
            relative = path.relative_to(folder)
            if any(part in IGNORED for part in relative.parts) or path.suffix == ".pyc":
                continue
            if any(part.startswith(".") for part in relative.parts):
                raise ValueError(f"不打包隐藏配置：{path.relative_to(root)}")
            if path.is_symlink():
                raise ValueError(f"不打包软链接：{path.relative_to(root)}")
            if not path.is_dir():
                add(path)
    if not names:
        raise ValueError("套件没有技能")
    if output.is_relative_to(skills_root) or output in {root / name for name in payload}:
        raise ValueError("输出不能覆盖技能或源码文件")
    manifest = {
        "format": "oi-teaching-workflows-bundle-v1",
        "plugin": {"name": plugin["name"], "version": plugin["version"]},
        "skills": names,
        "files": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(payload.items())},
    }
    payload["bundle-manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="bundle-build-", dir=output.parent) as temp:
        archive = Path(temp) / "bundle.zip"
        with ZipFile(archive, "w", compression=ZIP_DEFLATED) as package:
            for name, data in sorted(payload.items()):
                entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.compress_type = ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                package.writestr(entry, data)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        checksum = Path(temp) / "checksum.txt"
        checksum.write_text(f"{digest}  {output.name}\n", encoding="utf-8")
        targets = [(archive, output), (checksum, output.with_suffix(output.suffix + ".sha256"))]
        backups = {}
        for index, (_, target) in enumerate(targets):
            if target.is_symlink() or (target.exists() and not target.is_file()):
                raise ValueError(f"产物目标必须是普通文件：{target}")
            backup = Path(temp) / f"previous-{index}"
            if target.exists():
                shutil.copy2(target, backup)
                backups[target] = backup
            else:
                backups[target] = None
        replaced = []
        try:
            for source, target in targets:
                source.replace(target)
                replaced.append(target)
        except OSError:
            for target in reversed(replaced):
                if backups[target] is None:
                    target.unlink()
                else:
                    backups[target].replace(target)
            raise
    return {"plugin": plugin["name"], "version": plugin["version"], "skills": len(names), "files": len(payload), "output": str(output), "sha256": digest}


def main():
    parser = argparse.ArgumentParser(description="把当前源码中的完整技能构建为统一插件ZIP；不安装或发布。")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build_bundle(Path(__file__).resolve().parents[1], args.output)
    except (OSError, ValueError) as error:
        print(json.dumps({"checks_passed": False, "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
