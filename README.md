<div align="center">

# 医疗不良事件报告系统

<p>
  <strong>辽宁中医嘉和医院 · 院内不良事件全流程管理平台</strong>
</p>

<p>
  <a href="https://github.com/YTZL2026/medical-adverse-events/stargazers"><img src="https://img.shields.io/github/stars/86132/medical-adverse-events?style=flat-square" alt="Stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/86132/medical-adverse-events?style=flat-square" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/PRs-Welcome-green?style=flat-square" alt="PRs Welcome"></a>
</p>

<p>
  <a href="#-功能特性">功能</a> ·
  <a href="#-快速开始">快速开始</a> ·
  <a href="#-系统架构">架构</a> ·
  <a href="#-截图演示">截图</a> ·
  <a href="#-开源协议">开源协议</a>
</p>

</div>

---

## 简介

一套**纯前端 + Python 后端**的医疗不良事件报告系统，覆盖从事件填报、科室审核、根因分析到整改闭环的完整 PDCA 管理流程。

> 为什么造这个轮子？市面上医院不良事件系统要么几十万一套，要么功能残缺还不上心维护。我的想法很简单：**让中小医院也能零成本用上好系统**。

## 功能特性

| 功能模块 | 说明 |
| :---: | :--- |
|  📝 **事件填报** | A-H 八大板块完整映射：患者资料、事件情况、7大类多选、4级分级、处理分析、改进措施 |
|  📊 **事件台账** | 状态流转（草稿→已提交→已审核→已评价→已闭环），多维筛选，详情弹窗 |
|  📈 **统计分析** | 按等级/类别/科室/场所/月度自动聚合，可视化呈现 |
|  📥 **批量导入** | CSV/Excel 上传 + 列映射 + 预览 + 批量生成，支持 docx/json/pdf/图片自动提取 |
|  🔍 **全局搜索** | 跨项目目录扫描患者文件，自动提取 → AI 分析 → 导入台账 |
|  🏥 **培训联动** | 高发不良事件 → 自动推荐对应培训模块 |

## 快速开始

### 环境要求

- Python 3.10+
- 现代浏览器（Chrome / Edge / Firefox）

### 安装运行

```bash
git clone https://github.com/YTZL2026/medical-adverse-events.git
cd medical-adverse-events/adverse-events
python -m http.server 8000
```

打开浏览器访问 `http://localhost:8000`

### 批量导入功能（可选）

```bash
pip install python-docx openpyxl PyMuPDF
python _batch_import.py
```

## 系统架构

```
adverse-events/
├── index.html          # 主应用（SPA，1300+行）
│   ├── 事件填报模块     # A-H 八大板块映射
│   ├── 事件台账模块     # 状态流转 + 筛选 + 详情
│   ├── 统计分析模块     # 多维度自动聚合
│   └── 批量导入模块     # CSV/Excel 列映射导入
├── _batch_import.py   # 全格式文件识别提取
│   ├── 文本类: docx/json/txt/csv/xps → 零依赖提取
│   └── 图像类: pdf/png/jpg → OCR 提取
└── serve.bat          # 一键启动脚本
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | HTML5 + CSS3 + Vanilla JS（零框架） |
| 后端 | Python 3（HTTP Server + Flask） |
| 数据处理 | python-docx, PyMuPDF, openpyxl |
| AI 分析 | DeepSeek API（可选） |

## 同类对比

| 特性 | 本项目 | 商业系统 | 开源替代 |
|------|:---:|:---:|:---:|
| 完全免费 |  ✅ | ❌ 数十万/年 | ✅ |
| 开源可审计 |  ✅ | ❌ | ✅ |
| 中文界面 |  ✅ | ✅ | ❌ 多数英文 |
| PDCA 闭环 |  ✅ | ✅ | ❌ |
| 批量导入 |  ✅ | ✅ | ❌ |
| AI 辅助分析 |  ✅ | ❌ | ❌ |

## 贡献指南

欢迎提 Issue 和 PR！目前最需要的帮助：

- 🏥 其他医院的真实使用反馈
- 🐛 Bug 报告和改进建议
- 📝 文档翻译和完善

[查看 CONTRIBUTING.md](./CONTRIBUTING.md) 了解详细规范。

## 开源协议

本项目采用 [MIT License](LICENSE) 开源，允许自由使用、修改和分发。

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/86132">86132</a> for 辽宁中医嘉和医院</sub>
</p>

  <strong>杈藉畞涓尰鍢夊拰鍖婚櫌 路 闄㈠唴涓嶈壇浜嬩欢鍏ㄦ祦绋嬬鐞嗗钩鍙?/strong>
  <a href="https://github.com/YTZL2026/medical-adverse-events/stargazers"><img src="https://img.shields.io/github/stars/YTZL2026/medical-adverse-events?style=flat-square" alt="Stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/YTZL2026/medical-adverse-events?style=flat-square" alt="License"></a>
  <a href="#-鍔熻兘鐗规€?>鍔熻兘</a> 路
  <a href="#-蹇€熷紑濮?>蹇€熷紑濮?/a> 路
  <a href="#-寮€婧愬崗璁?>寮€婧愬崗璁?/a>
## 绠€浠?
涓€濂?*绾墠绔?+ Python 鍚庣**鐨勫尰鐤椾笉鑹簨浠舵姤鍛婄郴缁燂紝瑕嗙洊浠庝簨浠跺～鎶ャ€佺瀹ゅ鏍搞€佹牴鍥犲垎鏋愬埌鏁存敼闂幆鐨勫畬鏁?PDCA 绠＄悊娴佺▼銆?
> 涓轰粈涔堥€犺繖涓疆瀛愶紵甯傞潰涓婂尰闄笉鑹簨浠剁郴缁熻涔堝嚑鍗佷竾涓€濂楋紝瑕佷箞鍔熻兘娈嬬己杩樹笉涓婂績缁存姢銆傛垜鐨勬兂娉曞緢绠€鍗曪細**璁╀腑灏忓尰闄篃鑳介浂鎴愭湰鐢ㄤ笂濂界郴缁?*銆?
## 鍔熻兘鐗规€?
|  馃摑 **浜嬩欢濉姤** | A-H 鍏ぇ鏉垮潡瀹屾暣鏄犲皠锛氭偅鑰呰祫鏂欍€佷簨浠舵儏鍐点€?澶х被澶氶€夈€?绾у垎绾с€佸鐞嗗垎鏋愩€佹敼杩涙帾鏂?|
|  馃搱 **缁熻鍒嗘瀽** | 鎸夌瓑绾?绫诲埆/绉戝/鍦烘墍/鏈堝害鑷姩鑱氬悎锛屽彲瑙嗗寲鍛堢幇 |
|  馃摜 **鎵归噺瀵煎叆** | CSV/Excel 涓婁紶 + 鍒楁槧灏?+ 棰勮 + 鎵归噺鐢熸垚锛屾敮鎸?docx/json/pdf/鍥剧墖鑷姩鎻愬彇 |
|  馃攳 **鍏ㄥ眬鎼滅储** | 璺ㄩ」鐩洰褰曟壂鎻忔偅鑰呮枃浠讹紝鑷姩鎻愬彇 鈫?AI 鍒嗘瀽 鈫?瀵煎叆鍙拌处 |
|  馃彞 **鍩硅鑱斿姩** | 楂樺彂涓嶈壇浜嬩欢 鈫?鑷姩鎺ㄨ崘瀵瑰簲鍩硅妯″潡 |
## 蹇€熷紑濮?
- 鐜颁唬娴忚鍣紙Chrome / Edge / Firefox锛?
git clone https://github.com/YTZL2026/medical-adverse-events.git
鎵撳紑娴忚鍣ㄨ闂?`http://localhost:8000`
鈹溾攢鈹€ index.html          # 涓诲簲鐢紙SPA锛?300+琛岋級
鈹?  鈹溾攢鈹€ 浜嬩欢濉姤妯″潡     # A-H 鍏ぇ鏉垮潡鏄犲皠
鈹?  鈹溾攢鈹€ 浜嬩欢鍙拌处妯″潡     # 鐘舵€佹祦杞?+ 绛涢€?+ 璇︽儏
鈹?  鈹溾攢鈹€ 缁熻鍒嗘瀽妯″潡     # 澶氱淮搴﹁嚜鍔ㄨ仛鍚?鈹?  鈹斺攢鈹€ 鎵归噺瀵煎叆妯″潡     # CSV/Excel 鍒楁槧灏勫鍏?鈹溾攢鈹€ _batch_import.py   # 鍏ㄦ牸寮忔枃浠惰瘑鍒彁鍙?鈹?  鈹溾攢鈹€ 鏂囨湰绫? docx/json/txt/csv/xps 鈫?闆朵緷璧栨彁鍙?鈹?  鈹斺攢鈹€ 鍥惧儚绫? pdf/png/jpg 鈫?OCR 鎻愬彇
鈹斺攢鈹€ serve.bat          # 涓€閿惎鍔ㄨ剼鏈?```
| 灞傜骇 | 鎶€鏈?|
| 鍓嶇 | HTML5 + CSS3 + Vanilla JS锛堥浂妗嗘灦锛?|
| 鍚庣 | Python 3锛圚TTP Server + Flask锛?|
| 鐗规€?| 鏈」鐩?| 鍟嗕笟绯荤粺 | 寮€婧愭浛浠?|
| 瀹屽叏鍏嶈垂 |  鉁?| 鉂?鏁板崄涓?骞?| 鉁?|
| 寮€婧愬彲瀹¤ |  鉁?| 鉂?| 鉁?|
| 涓枃鐣岄潰 |  鉁?| 鉁?| 鉂?澶氭暟鑻辨枃 |
| PDCA 闂幆 |  鉁?| 鉁?| 鉂?|
| 鎵归噺瀵煎叆 |  鉁?| 鉁?| 鉂?|
| AI 杈呭姪鍒嗘瀽 |  鉁?| 鉂?| 鉂?|
娆㈣繋鎻?Issue 鍜?PR锛佺洰鍓嶆渶闇€瑕佺殑甯姪锛?
- 馃彞 鍏朵粬鍖婚櫌鐨勭湡瀹炰娇鐢ㄥ弽棣?- 馃悰 Bug 鎶ュ憡鍜屾敼杩涘缓璁?- 馃摑 鏂囨。缈昏瘧鍜屽畬鍠?
[鏌ョ湅 CONTRIBUTING.md](./CONTRIBUTING.md) 浜嗚В璇︾粏瑙勮寖銆?
## 寮€婧愬崗璁?
鏈」鐩噰鐢?[MIT License](LICENSE) 寮€婧愶紝鍏佽鑷敱浣跨敤銆佷慨鏀瑰拰鍒嗗彂銆?
  <sub>Built with 鉂わ笍 by <a href="https://github.com/YTZL2026">YTZL2026</a> for 杈藉畞涓尰鍢夊拰鍖婚櫌</sub>