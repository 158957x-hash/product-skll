#!/usr/bin/env python3
import argparse,csv,json
from pathlib import Path
FUNCTIONS=["function_id","platform","subsystem","menu","page","role","precondition","input_data","output_data","upstream","downstream","backend_entry","miniapp_entry","external_system","screenshot","manual_chapter","status","evidence","related_function_id"]
FLOWS=["flow_id","step","actor","action","system","entry","input","output","status","next_actor","related_function_id","evidence"]
DATA=["object_id","name","producer","storage","consumers","statuses","retention","related_functions","related_flows"]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("project"); a=ap.parse_args(); root=Path(a.project).resolve()
    for rel in ["原始资料","截图原始","截图交付","台账","手册/独立版","手册/最终版","手册/整合版","测试问题"]: (root/rel).mkdir(parents=True,exist_ok=True)
    for name,fields in [("functions.csv",FUNCTIONS),("flows.csv",FLOWS),("data_objects.csv",DATA)]:
        with (root/"台账"/name).open("w",newline="",encoding="utf-8-sig") as f: csv.DictWriter(f,fieldnames=fields).writeheader()
    (root/"台账/inventory.json").write_text(json.dumps({"project":root.name,"platforms":[]},ensure_ascii=False,indent=2),encoding="utf-8")
    (root/"测试问题/issues.csv").write_text("issue_id,发现日期,平台,子系统,页面,问题,复现步骤,影响,状态,截图\n",encoding="utf-8-sig")
    print(f"已初始化：{root}")
if __name__=="__main__": main()
