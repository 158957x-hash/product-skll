#!/usr/bin/env python3
import argparse,csv
from pathlib import Path
def rows(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def main():
    ap=argparse.ArgumentParser();ap.add_argument("project");ap.add_argument("output");a=ap.parse_args();root=Path(a.project);fs=rows(root/"台账/functions.csv");fl=rows(root/"台账/flows.csv")
    out=["# 跨系统功能关系矩阵","","| 编号 | 平台/子系统 | 功能 | 角色 | 上游 | 下游 | 后台入口 | 小程序入口 | 状态 |","|---|---|---|---|---|---|---|---|---|"]
    for r in fs: out.append("| {function_id} | {platform}/{subsystem} | {menu}/{page} | {role} | {upstream} | {downstream} | {backend_entry} | {miniapp_entry} | {status} |".format(**{k:r.get(k,"").replace("|","/") for k in r}))
    out += ["","## 流程节点","","| 流程 | 步骤 | 角色 | 动作 | 系统 | 状态 | 下一角色 | 功能编号 |","|---|---:|---|---|---|---|---|---|"]
    for r in fl: out.append("| {flow_id} | {step} | {actor} | {action} | {system} | {status} | {next_actor} | {related_function_id} |".format(**{k:r.get(k,"").replace("|","/") for k in r}))
    Path(a.output).write_text("\n".join(out),encoding="utf-8");print(a.output)
if __name__=="__main__":main()
