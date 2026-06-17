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
