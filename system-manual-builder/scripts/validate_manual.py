#!/usr/bin/env python3
import argparse,csv,sys
from pathlib import Path
def read_csv(path):
    if not path.exists(): return []
    with path.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("project"); a=ap.parse_args(); root=Path(a.project).resolve(); errors=[]; warnings=[]
    for rel in ["台账/functions.csv","台账/flows.csv","台账/data_objects.csv","台账/inventory.json","截图原始","截图交付","手册/独立版","手册/最终版","测试问题"]:
        if not (root/rel).exists(): errors.append("缺少 "+rel)
    funcs=read_csv(root/"台账/functions.csv"); ids=[r.get("function_id","") for r in funcs]; dup={x for x in ids if x and ids.count(x)>1}
    if dup: errors.append("功能编号重复："+", ".join(sorted(dup)))
    shots={p.name for p in (root/"截图交付").glob("*")} if (root/"截图交付").exists() else set()
    for row in funcs:
        fid=row.get("function_id","")
        if row.get("status") in ("已验证","完成") and not row.get("screenshot"): warnings.append(f"{fid} 已验证但无截图")
        for s in [x.strip() for x in row.get("screenshot","").split(";") if x.strip()]:
            if Path(s).name not in shots and not Path(s).exists(): warnings.append(f"{fid} 截图不存在：{s}")
        if row.get("miniapp_entry") and not row.get("related_function_id"): warnings.append(f"{fid} 提到移动端但无关联编号")
    if not funcs: warnings.append("functions.csv 为空：尚未完成系统遍历")
    print(f"功能 {len(funcs)} 条")
    for x in errors: print("ERROR:",x)
    for x in warnings: print("WARN:",x)
    sys.exit(2 if errors else 0)
if __name__=="__main__": main()
