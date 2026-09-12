"""Initialize a requirements-analysis project without deleting or overwriting files."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


CSV_HEADERS = {
    "资料登记.csv": ["资料编号", "文件名称", "类型", "版本", "发布日期", "来源", "页数", "可读性", "权威性", "备注"],
    "需求清单.csv": ["需求编号", "需求类型", "需求来源类别", "模块", "功能名称", "角色", "需求描述", "优先级", "来源文件", "来源位置", "原文摘录", "外部参考编号", "验收标准", "确认状态", "备注"],
    "需求追踪矩阵.csv": ["追踪编号", "原始条款编号", "来源文件", "章节/页码", "原文要求", "业务需求编号", "功能需求编号", "模块", "数据对象", "接口编号", "外部参考编号", "交付物", "验收标准", "覆盖状态", "待确认问题"],
    "外部调研台账.csv": ["调研编号", "研究问题", "搜索关键词", "标题", "发布机构", "来源类型", "URL", "发布日期", "访问日期", "关键摘录", "主要发现", "可信度", "适用性", "关联需求", "影响分析", "建议动作", "处理状态"],
    "竞品与案例对比.csv": ["对象编号", "对象名称", "对象类型", "所属行业", "适用地区", "目标用户", "核心流程", "系统模块", "数据能力", "接口能力", "安全能力", "实施运维", "亮点", "局限", "可借鉴内容", "不适用原因", "来源编号"],
    "数据与接口台账.csv": ["记录类型", "数据/接口编号", "名称", "提供方", "使用方", "数据对象", "字段或交换内容", "来源/方向", "频率", "规则或协议", "失败处理", "责任边界", "关联需求", "确认状态"],
    "风险与待确认事项.csv": ["问题编号", "问题类型", "问题描述", "来源", "影响范围", "当前判断", "建议方案", "建议确认人", "优先级", "处理状态", "确认结论", "处理日期", "关联需求"],
}


def write_if_missing(path: Path, headers: list[str]) -> str:
    if path.exists():
        return "保留已有文件"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle).writerow(headers)
    return "已创建"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="项目目录")
    args = parser.parse_args()
    root = args.project.resolve()
    for name in ["原始资料", "原始资料/版本归档", "研究资料", "报告", "图表", "台账", "测试问题"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    inventory = root / "台账" / "inventory.json"
    if not inventory.exists():
        inventory.write_text(json.dumps({"project": root.name, "sources": [], "notes": []}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"已创建: {inventory}")
    else:
        print(f"保留已有文件: {inventory}")
    for filename, headers in CSV_HEADERS.items():
        print(f"{filename}: {write_if_missing(root / '台账' / filename, headers)}")
    print(f"项目目录已准备: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
