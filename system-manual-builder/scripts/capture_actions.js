const { chromium } = require('playwright');
const fs=require('fs'),path=require('path');const url=process.argv[2],out=process.argv[3]||'截图交付';
if(!url){console.error('缺少 URL');process.exit(2)}
const ready=async p=>{await p.waitForLoadState('networkidle').catch(()=>{});await p.waitForTimeout(800);await p.locator('.el-loading-mask,.el-loading-spinner,.loading,.ant-spin').first().waitFor({state:'hidden',timeout:5000}).catch(()=>{})};
(async()=>{fs.mkdirSync(out,{recursive:true});const b=await chromium.launch({headless:false});const p=await b.newPage({viewport:{width:1440,height:900}});await p.goto(url);await ready(p);await p.screenshot({path:path.join(out,'00_首页_初始.png'),fullPage:true});console.log('初始页已截图；请在授权范围内点击并登记台账。按回车退出。');await new Promise(r=>process.stdin.once('data',r));await b.close()})().catch(e=>{console.error(e);process.exit(1)});
