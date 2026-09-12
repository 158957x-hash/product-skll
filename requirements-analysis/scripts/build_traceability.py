"""Build a traceability CSV from requirement and source ledgers, without overwriting by default."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_FIELDS = ["追踪编号", "原始条款编号", "来源文件", "章节/页码", "原文要求", "业务需求编号", "功能需求编号", "模块", "数据对象", "接口编号", "外部参考编号", "交付物", "验收标准", "覆盖状态", "待确认问题"]


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="项目目录")
    parser.add_argument("--output", type=Path, default=None, help="输出文件，默认写入台账/需求追踪矩阵-生成.csv")
    parser.add_argument("--overwrite", action="store_true", help="允许覆盖明确指定的输出文件")
    args = parser.parse_args()
    root = args.project.resolve()
    source_rows = rows(root / "台账" / "资料登记.csv")
    requirement_rows = rows(root / "台账" / "需求清单.csv")
    output = (args.output or root / "台账" / "需求追踪矩阵-生成.csv").resolve()
    if output.exists() and not args.overwrite:
        raise SystemExit(f"输出已存在，为防止覆盖请另指定 --output 或明确使用 --overwrite: {output}")
    source_by_name = {row.get("文件名称", "").strip(): row for row in source_rows}
    result: list[dict[str, str]] = []
    for index, item in enumerate(requirement_rows, start=1):
        filename = item.get("来源文件", "").strip()
        source = source_by_name.get(filename, {})
        source_location = item.get("来源位置", "").strip()
        result.append({
            "追踪编号": f"TR-{index:04d}",
            "原始条款编号": item.get("需求编号", "").strip(),
            "来源文件": filename,
            "章节/页码": source_location,
            "原文要求": item.get("原文摘录", "").strip(),
            "业务需求编号": item.get("需求编号", "").strip() if item.get("需求类型", "").strip() == "业务需求" else "",
            "功能需求编号": item.get("需求编号", "").strip() if item.get("需求类型", "").strip() in {"功能需求", "FR"} else "",
            "模块": item.get("模块", "").strip(),
            "数据对象": "",
            "接口编号": "",
            "外部参考编号": item.get("外部参考编号", "").strip(),
            "交付物": "",
            "验收标准": item.get("验收标准", "").strip(),
            "覆盖状态": "待确认" if not filename or not item.get("验收标准", "").strip() else "部分覆盖",
            "待确认问题": "缺少来源或验收标准" if not filename or not item.get("验收标准", "").strip() else "",
        })
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(result)
    print(f"已生成 {len(result)} 条追踪记录: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
