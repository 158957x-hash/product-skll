#!/usr/bin/env python3
import argparse,json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser();ap.add_argument("inventory");ap.add_argument("output");a=ap.parse_args();d=json.loads(Path(a.inventory).read_text(encoding="utf-8-sig"));out=[f"# {d.get('project','系统')} 功能遍历清单",""]
    for p in d.get("platforms",[]):
        out.append(f"## {p.get('name','未命名平台')}（{p.get('status','未验证')}）")
        for s in p.get("subsystems",[]):
            out.append(f"- {s.get('name','未命名子系统')}：{s.get('status','未验证')}")
            for m in s.get("menus",[]):
                out.append(f"  - {m.get('name','未命名菜单')}：{m.get('status','未验证')}")
                for page in m.get("pages",[]): out.append(f"    - {page.get('name','未命名页面')}：{page.get('status','未验证')}；截图：{page.get('screenshot','待补充')}")
    Path(a.output).write_text("\n".join(out),encoding="utf-8");print(a.output)
if __name__=="__main__":main()
