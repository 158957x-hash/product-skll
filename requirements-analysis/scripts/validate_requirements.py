"""Validate requirement ledgers without modifying project files."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED = {
    "需求清单.csv": ["需求编号", "需求描述", "来源文件", "来源位置", "确认状态"],
    "需求追踪矩阵.csv": ["追踪编号", "原始条款编号", "覆盖状态"],
    "外部调研台账.csv": ["调研编号", "研究问题", "URL", "访问日期", "可信度"],
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="项目目录")
    args = parser.parse_args()
    ledger = args.project.resolve() / "台账"
    errors: list[str] = []
    warnings: list[str] = []
    for filename, required in REQUIRED.items():
        path = ledger / filename
        if not path.exists():
            errors.append(f"缺少文件: {path}")
            continue
        fields, rows = read_csv(path)
        missing = [field for field in required if field not in fields]
        if missing:
            errors.append(f"{filename} 缺少字段: {', '.join(missing)}")
        if not rows:
            warnings.append(f"{filename} 目前没有数据行")
    requirements = ledger / "需求清单.csv"
    if requirements.exists():
        _, rows = read_csv(requirements)
        ids = [row.get("需求编号", "").strip() for row in rows]
        duplicates = sorted({item for item in ids if item and ids.count(item) > 1})
        blank = sum(1 for item in ids if not item)
        if duplicates:
            errors.append(f"需求编号重复: {', '.join(duplicates)}")
        if blank:
            warnings.append(f"需求清单存在 {blank} 条空需求编号")
        unconfirmed = sum(1 for row in rows if row.get("确认状态", "").strip() in {"待确认", "未验证"})
        if unconfirmed:
            warnings.append(f"有 {unconfirmed} 条需求仍处于待确认或未验证状态")
    for message in warnings:
        print(f"WARN: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1
    print("需求台账静态检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
