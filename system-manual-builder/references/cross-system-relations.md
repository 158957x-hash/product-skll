# 跨系统关联防遗漏

`functions.csv` 字段建议：`function_id,platform,subsystem,menu,page,role,precondition,input_data,output_data,upstream,downstream,backend_entry,miniapp_entry,external_system,screenshot,manual_chapter,status,evidence,related_function_id`。功能编号全局唯一，同一功能在后台和小程序分别登记并互相引用。

`flows.csv` 字段：`flow_id,step,actor,action,system,entry,input,output,status,next_actor,related_function_id,evidence`。每条链路覆盖产生、查看、录入、审核、实施、验收、结束节点；不适用填 N/A 并说明。

后台提到小程序时，小程序必须反向说明后台承接菜单；小程序提到审核/实施/验收时，必须说明后台模块、角色和状态变化。预警：有提交无承接、有状态无下一节点、有数据产生无使用位置、有按钮无截图、跨系统出现无关系编号。
