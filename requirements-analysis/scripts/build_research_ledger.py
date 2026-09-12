"""Normalize and deduplicate web research records without overwriting the input."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


FIELDS = ["调研编号", "研究问题", "搜索关键词", "标题", "发布机构", "来源类型", "URL", "发布日期", "访问日期", "关键摘录", "主要发现", "可信度", "适用性", "关联需求", "影响分析", "建议动作", "处理状态"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="外部调研台账 CSV")
    parser.add_argument("--output", type=Path, default=None, help="输出 CSV，默认在输入文件旁生成 -去重.csv")
    parser.add_argument("--overwrite", action="store_true", help="允许覆盖明确指定的输出文件")
    args = parser.parse_args()
    source = args.input.resolve()
    if not source.exists():
        raise SystemExit(f"输入不存在: {source}")
    output = (args.output or source.with_name(f"{source.stem}-去重{source.suffix}")).resolve()
    if output.exists() and not args.overwrite:
        raise SystemExit(f"输出已存在，为防止覆盖请另指定 --output 或明确使用 --overwrite: {output}")
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle))
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for record in records:
        item = {field: (record.get(field, "") or "").strip() for field in FIELDS}
        key = item["URL"] or "|".join([item["标题"], item["发布机构"], item["发布日期"]])
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        item["调研编号"] = f"WEB-{len(result) + 1:04d}"
        result.append(item)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(result)
    print(f"已保留 {len(result)} 条记录，输出到: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
