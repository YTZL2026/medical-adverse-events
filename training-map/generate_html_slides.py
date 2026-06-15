# -*- coding: utf-8 -*-
"""
辽宁中医嘉和医院 · 培训HTML幻灯片批量生成
基于 嘉和医院病历质控培训_原始版.html 模板
运行: python generate_html_slides.py
"""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ppts', 'html')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ======================== SHARED CSS ========================
SHARED_CSS = r'''
:root{--primary:#1a5276;--accent:#2980b9;--bg:#f8fafc;--text:#1e293b;--muted:#64748b;--border:#e2e8f0;--red:#dc2626;--orange:#ea580c;--green:#16a34a;--gold:#b8860b}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif;background:#fff;overflow:hidden;height:100vh;width:100vw;display:flex;align-items:center;justify-content:center}
#app{width:100%;height:100%;position:relative;display:flex;align-items:center;justify-content:center}
.slide{display:none;width:100%;max-width:1920px;max-height:100vh;aspect-ratio:16/9;background:linear-gradient(175deg,#fafbfd 0%,#f2f5fa 40%,#f8f9fc 100%);position:relative;overflow:hidden}
.slide.active{display:block}
.slide::before{content:'';position:absolute;top:0;left:0;bottom:0;width:6px;background:linear-gradient(180deg,var(--primary) 0%,var(--accent) 60%,#93c5fd 100%);z-index:3;border-radius:0 3px 3px 0}
.slide-inner{width:100%;height:100%;padding:44px 68px;display:flex;flex-direction:column;overflow-y:auto}
.slide.cover{background:linear-gradient(150deg,#eef3fa 0%,#dce6f5 30%,#f0f4fa 60%,#e3eaf5 100%)}
.slide.cover::before{display:none}
.slide.cover .slide-inner{align-items:center;justify-content:center;text-align:center}
.cover-icon{font-size:64px;margin-bottom:16px}
.cover h1{font-size:48px;font-weight:900;color:var(--primary);margin-bottom:12px;letter-spacing:4px}
.cover .subtitle{font-size:24px;color:var(--accent);font-weight:500;margin-bottom:24px}
.cover .divider{width:100px;height:4px;background:linear-gradient(90deg,var(--accent),#93c5fd);margin:0 auto 24px;border-radius:2px}
.cover .info{font-size:19px;color:var(--muted);line-height:2}
.section-num{font-size:16px;color:var(--accent);font-weight:700;letter-spacing:4px;margin-bottom:10px;display:inline-block;padding:4px 14px;border-radius:4px;background:linear-gradient(90deg,rgba(41,128,185,0.08),rgba(41,128,185,0.02));border-left:3px solid var(--accent)}
.slide h2{font-size:38px;font-weight:800;color:var(--primary);margin-bottom:10px}
.slide h2::after{content:'';display:block;width:60px;height:4px;border-radius:2px;background:linear-gradient(90deg,var(--accent),#93c5fd);margin-top:8px}
.slide h3{font-size:24px;font-weight:700;color:var(--primary);margin:20px 0 10px}
.slide .sub{font-size:20px;color:var(--muted);margin-bottom:24px;line-height:1.6}
.card-grid{display:grid;gap:18px}
.card-grid.col2{grid-template-columns:1fr 1fr}
.card-grid.col3{grid-template-columns:1fr 1fr 1fr}
.card{background:#fff;border:1px solid #e8ecf1;border-radius:12px;padding:22px 26px;box-shadow:0 2px 8px rgba(0,0,0,0.04)}
.card h4{font-size:24px;font-weight:700;color:var(--primary);margin-bottom:8px}
.card p,.card li{font-size:16px;color:var(--text);line-height:1.7}
.card ul{padding-left:18px;margin-top:4px}
.card.accent{border-left:5px solid var(--accent);background:#f8faff}
.card.red{border-left:5px solid var(--red);background:#fffafa}
.card.green{border-left:5px solid var(--green);background:#f8fdf9}
.card.orange{border-left:5px solid var(--orange);background:#fffcf8}
.card.gold{border-left:5px solid var(--gold);background:#fffefa}
.tag{display:inline-block;padding:4px 12px;border-radius:50px;font-size:15px;font-weight:700}
.tag-red{background:#fee2e2;color:var(--red)}
.tag-orange{background:#ffedd5;color:var(--orange)}
.tag-green{background:#dcfce7;color:var(--green)}
.tag-blue{background:#dbeafe;color:var(--accent)}
.tag-gold{background:#fef3c7;color:var(--gold)}
.flow{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin:20px 0}
.flow .step{background:#fff;border:2px solid #dbeafe;border-radius:12px;padding:14px 20px;text-align:center;font-size:16px;font-weight:600;color:var(--primary);min-width:100px;box-shadow:0 2px 6px rgba(41,128,185,0.06)}
.flow .arrow{font-size:26px;color:var(--accent);font-weight:900}
.flow .step.red-step{background:#fff5f5;border-color:#fecaca;color:var(--red)}
.flow .step.green-step{background:#f0fdf4;border-color:#bbf7d0;color:var(--green)}
.flow .step.gold-step{background:#fffefa;border-color:#fde68a;color:var(--gold)}
.big-num{font-size:56px;font-weight:900;color:var(--accent);line-height:1}
.big-label{font-size:22px;color:var(--primary);margin-top:6px;font-weight:700}
.box{border:2px dashed var(--border);border-radius:12px;padding:20px 24px;margin:14px 0;background:#fff}
.box.red-box{border-color:#fecaca;background:#fffafa}
.box.blue-box{border-color:#bfdbfe;background:#f8faff}
.box.gold-box{border-color:#fde68a;background:#fffefa}
.box h4{font-size:22px;font-weight:700;margin-bottom:6px}
.box p,.box li{font-size:16px;line-height:1.7}
table{width:100%;border-collapse:separate;border-spacing:0;font-size:18px;margin:14px 0;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.04)}
th{background:linear-gradient(180deg,#f0f4f8,#e2e8f0);font-weight:700;padding:12px 14px;border-bottom:2px solid #cbd5e1;text-align:center;font-size:19px;color:var(--primary)}
td{padding:11px 14px;border-bottom:1px solid #f1f5f9;text-align:center;background:#fff}
td.l{text-align:left}
tr:last-child td{border-bottom:none}
tr:nth-child(even) td{background:#fafbfd}
tr.highlight td{background:#fefce8!important;font-weight:600}
.do-dont{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.do-box{border:2px solid var(--green);border-radius:12px;overflow:hidden}
.dont-box{border:2px solid var(--red);border-radius:12px;overflow:hidden}
.do-header{background:#f0fdf4;padding:10px 16px;font-weight:700;font-size:18px}
.dont-header{background:#fff5f5;padding:10px 16px;font-weight:700;font-size:18px}
.do-body,.dont-body{padding:10px 16px;font-size:15px;line-height:1.8}
.do-body li,.dont-body li{margin-bottom:4px}
#nav{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:10px;z-index:100;background:rgba(26,82,118,0.95);border-radius:50px;padding:8px 18px;box-shadow:0 4px 20px rgba(0,0,0,0.2)}
#nav button{border:none;background:transparent;cursor:pointer;font-size:18px;padding:5px 10px;border-radius:8px;color:#fff;transition:all 0.15s}
#nav button:hover{background:rgba(255,255,255,0.15)}
#nav .page-num{font-size:12px;font-weight:600;color:rgba(255,255,255,0.8);min-width:55px;text-align:center}
#nav .btn-export{font-size:11px;font-weight:700;background:var(--accent);color:#fff;padding:5px 12px;border-radius:20px}
@media(max-width:900px){.slide-inner{padding:20px 28px}.slide h2{font-size:24px}.cover h1{font-size:28px}.do-dont{grid-template-columns:1fr}.card-grid.col2,.card-grid.col3{grid-template-columns:1fr}}
'''

# ======================== SHARED JS ========================
SHARED_JS = r'''
let current=0;const slides=document.querySelectorAll('.slide');function show(i){slides.forEach((s,n)=>{s.classList.toggle('active',n===i)});document.getElementById('pageNum').textContent=(i+1)+'/'+slides.length}function next(){if(current<slides.length-1){current++;show(current)}}function prev(){if(current>0){current--;show(current)}}function goTo(i){if(i>=0&&i<slides.length){current=i;show(i)}}async function exportPNG(){document.getElementById('nav').style.display='none';try{const{default:html2canvas}=await import('https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.esm.js');for(let i=0;i<slides.length;i++){show(i);await new Promise(r=>setTimeout(r,400));const c=await html2canvas(slides[i],{scale:2,backgroundColor:'#ffffff'});const a=document.createElement('a');a.download='slide_'+(i+1).toString().padStart(2,'0')+'.png';a.href=c.toDataURL('image/png');a.click();await new Promise(r=>setTimeout(r,200))}alert('✅ 导出完成！共'+slides.length+'张图片')}catch(e){alert('导出失败：'+e.message)}finally{document.getElementById('nav').style.display='flex';show(current)}}document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key===' '){e.preventDefault();next()}if(e.key==='ArrowLeft'||e.key==='ArrowUp'){e.preventDefault();prev()}if(e.key==='Home'){e.preventDefault();goTo(0)}if(e.key==='End'){e.preventDefault();goTo(slides.length-1)}});show(0);
'''

def make_html(title, slides_html):
    """Wrap slide content in a complete HTML document"""
    slides = '\n'.join(slides_html)
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} · 辽宁中医嘉和医院</title>
<style>{SHARED_CSS}</style>
</head>
<body>
<div id="app">
{slides}
</div>
<nav id="nav">
  <button onclick="goTo(0)" title="首页">⏮</button>
  <button onclick="prev()" title="上一页">◀</button>
  <span class="page-num" id="pageNum">1/1</span>
  <button onclick="next()" title="下一页">▶</button>
  <button onclick="goTo({len(slides_html)-1})" title="末页">⏭</button>
  <button class="btn-export" onclick="exportPNG()">📷 导出图片</button>
</nav>
<script>{SHARED_JS}</script>
</body>
</html>'''

def cover_slide(icon, title, subtitle, info_lines):
    return f'''<div class="slide cover"><div class="slide-inner">
<div class="cover-icon">{icon}</div>
<h1>{title}</h1>
<div class="subtitle">{subtitle}</div>
<div class="divider"></div>
<div class="info">{"<br>".join(info_lines)}</div>
</div></div>'''

def content_slide(title_text, body_html, section=None):
    sec = f'<div class="section-num">{section}</div>' if section else ''
    return f'''<div class="slide"><div class="slide-inner">
{sec}<h2>{title_text}</h2>
<div class="sub">{body_html}</div>
</div></div>'''

def bullet_slide(title_text, bullets, section=None):
    items = ''.join(f'<li>{b}</li>' for b in bullets)
    sec = f'<div class="section-num">{section}</div>' if section else ''
    return f'''<div class="slide"><div class="slide-inner">
{sec}<h2>{title_text}</h2>
<div class="sub"><ul style="font-size:19px;line-height:2;padding-left:20px">{items}</ul></div>
</div></div>'''

def card_slide(title_text, cards, cols=2, section=None):
    """cards: list of {title, body, style} where style is accent/red/green/orange/gold"""
    sec = f'<div class="section-num">{section}</div>' if section else ''
    cards_html = ''.join(f'<div class="card {c.get("style","")}"><h4>{c["title"]}</h4><p>{c["body"]}</p></div>' for c in cards)
    return f'''<div class="slide"><div class="slide-inner">
{sec}<h2>{title_text}</h2>
<div class="card-grid col{cols}">{cards_html}</div>
</div></div>'''

def table_slide(title_text, headers, rows, section=None):
    sec = f'<div class="section-num">{section}</div>' if section else ''
    th_html = ''.join(f'<th>{h}</th>' for h in headers)
    tr_html = ''.join(f'<tr>{"".join(f"<td class=\"l\">{c}</td>" if i==0 else f"<td>{c}</td>" for i,c in enumerate(r))}</tr>' for r in rows)
    return f'''<div class="slide"><div class="slide-inner">
{sec}<h2>{title_text}</h2>
<table><thead><tr>{th_html}</tr></thead><tbody>{tr_html}</tbody></table>
</div></div>'''

def flow_slide(title_text, steps, section=None):
    """steps: list of {label, style}"""
    sec = f'<div class="section-num">{section}</div>' if section else ''
    flow_html = ''
    for i,s in enumerate(steps):
        if i>0: flow_html += '<div class="arrow">→</div>'
        flow_html += f'<div class="step {s.get("style","")}">{s["label"]}</div>'
    return f'''<div class="slide"><div class="slide-inner">
{sec}<h2>{title_text}</h2>
<div class="flow">{flow_html}</div>
</div></div>'''


# ======================== MODULE CONTENT BUILDERS ========================

def build_m01():
    """医保飞行检查迎检全流程 - 18 slides"""
    slides = []
    slides.append(cover_slide('🛡️', '医保飞行检查迎检全流程', '五阶迎检：自查→入场→应对→收尾→整改闭环', [
        '辽宁中医嘉和医院 · 标准化培训体系', '目标受众：全院 · 时长：90分钟 · 2026年8月'
    ]))
    slides.append(bullet_slide('🎯 培训目标', [
        '说出医保飞检的五个阶段和每阶段关键动作',
        '独立完成"三合一核对"(病历+收费+医嘱一致性检查)',
        '在面对飞检组质疑时，使用标准应答公式应对',
        '背出"十要十不要"中的核心要诀',
        '知晓丙级违规的后果和自己科室的自查清单'
    ], 'Part 0'))
    slides.append(flow_slide('📊 五阶迎检全流程总览', [
        {'label':'1.飞检前自查\n问题清单·数据筛查\n病历复核·全员培训','style':''},
        {'label':'2.飞检组入场\n指定迎检室·资料分区\n人员分工·态度端正','style':''},
        {'label':'3.现场应对\n十要话术·科室响应\n证据链·避开十不要','style':'gold-step'},
        {'label':'4.检查收尾\n当场领问题·记录意见\n表达感谢·主动问整改','style':''},
        {'label':'5.整改闭环\n建台账·退资金\n制度修订·回头看验收','style':'green-step'}
    ], 'Part 1 · 总览'))
    slides.append(bullet_slide('🏗️ 专项工作组组织架构', [
        '组长：院长（总负责）',
        '医保办 — 统筹协调 · 政策解读 · 对外联络',
        '医务科 — 病历审查 · 诊疗规范性检查',
        '药剂科 — 中药饮片进销存 · 处方规范审查',
        '财务科 — 收费项目核对 · 违规金额核算',
        '护理部 — 护理记录 · 治疗执行记录核查',
        '信息科 — HIS数据提取 · 智能审核规则配置',
        '各临床科室主任 — 科室自查第一责任人',
        '📋 关键动作：获取九大领域问题清单+辽宁省本地化清单'
    ], 'Part 1 · 组织'))
    slides.append(bullet_slide('🔍 核心方法：三合一核对', [
        '📝 病历记录(医嘱/病程) ←→ 📋 收费清单(结算明细) ←→ 💊 医嘱单',
        '✅ 三者一致 → 通过',
        '❌ 不一致 → 标记为问题项 → 进入整改台账',
        '',
        '🔴 五大高频违规类型：',
        '① 重复收费：温针+普通针刺同时收费',
        '② 分解收费：全腹CT拆上中下三段',
        '③ 串换项目：微波治疗串换红外线',
        '④ 超标准收费：超过医保限价或计价单位错误',
        '⑤ 过度诊疗：无指征检查、超频次治疗'
    ], 'Part 1 · 方法'))
    slides.append(bullet_slide('💉 针灸科/推拿科/康复科自查清单', [
        '□ 温针、电针、普通针刺是否叠加收费',
        '□ 灸法、隔物灸、督灸是否同时计费(应只收一种)',
        '□ 推拿治疗等级(大/中/小)与收费是否匹配',
        '□ 小针刀是否与关节松解术重复收费',
        '□ 治疗记录单是否逐次逐项记录完整',
        '□ 单日治疗项目数是否超出常规',
        '□ 操作人员资质是否合规'
    ], 'Part 1 · 分科室'))
    slides.append(bullet_slide('💊 中药房/煎药室自查清单', [
        '□ 药食同源单味饮片是否单独纳入医保',
        '□ 中药饮片加成比例是否 ≤ 25%',
        '□ 进销存台账与实物是否一致(全品种盘点)',
        '□ 处方是否有医师+审方+调配+核对四签名',
        '□ 贵细中药是否在医保支付限定内',
        '□ 中药颗粒是否存在串换编码',
        '□ 中药熏蒸/热奄包是否重复收取饮片费用',
        '🔴 重点：随机抽3个品种，现场称重核对账实'
    ], 'Part 1 · 分科室'))
    slides.append(content_slide('⚖️ 迎检对话黄金法则', '''
      <div class="box blue-box"><h4>应答公式</h4><p style="font-size:20px;text-align:center;font-weight:700;color:var(--primary)">政策依据(文号/页码) + 原始记录(病历/签字) + 逻辑关联</p></div>
      <div class="do-dont" style="margin-top:14px">
        <div class="do-box"><div class="do-header">✅ 十要 (积极引导)</div><div class="do-body"><ol>
          <li>先接"锅"再递办法 — "您说得对，马上补"</li>
          <li>资料触手可及 — 医保目录放抽屉第一层</li>
          <li>笑着说"您提醒得好" — 用配合姿态回应</li>
          <li>喊对人，不硬扛 — "我马上叫XX过来"</li>
          <li>说大白话 — 不用术语绕圈子</li>
        </ol></div></div>
        <div class="dont-box"><div class="dont-header">❌ 十不要 (绝对避开)</div><div class="dont-body"><ol>
          <li>✘ "我们一直这么做的"</li>
          <li>✘ "我不知道"</li>
          <li>✘ "这是其他科室的事"</li>
          <li>✘ "我也没办法"</li>
          <li>✘ 皱眉抱胳膊</li>
        </ol></div></div>
      </div>''', 'Part 2 · 黄金法则'))

    # Scene cards for 6 scenarios
    scenes = [
        ('场景① 质疑针灸项目重复收费', '飞检组："温针和普通针刺为什么同时收费？"', '应答：温针项目编码已包含针刺操作，不应同时计普通针刺。马上逐条核对，多收的核算金额，3天内退费。'),
        ('场景② 质疑推拿治疗等级', '飞检组："这个患者为什么收\'大\'推拿费用？"', '应答：该患者肩、肘、腕三关节均受累，推拿时长45分钟，符合(大)标准。这是病历、记录单、价格手册对应页复印件。'),
        ('场景③ 质疑中药饮片加成', '飞检组："中药饮片怎么定价？加成多少？"', '应答：我院严格按国家规定加成≤25%。以当归为例，采购价100元/kg，零售价125元/kg。这是采购发票和盘点表。'),
        ('场景④ 质疑入院必要性', '飞检组："这个患者是不是门诊就能处理？"', '应答：该患者腰椎间盘突出急性发作，VAS评分8分，无法站立行走。需住院系统治疗。入院记录、疼痛评估表、知情同意书都在这。'),
        ('场景⑤ 质疑中医理疗频次', '飞检组："为什么一天做这么多理疗项目？"', '应答：针刺醒脑、推拿通络、灸法补气，三个项目作用机理不同，属于辨证施治的综合方案。这是疗程计划书和治疗记录。'),
        ('场景⑥ 质疑项目编码串换', '飞检组："这个收费编码与实际操作不一致。"', '应答：编码XX对应红外线，实际做的是微波(编码YY)，操作人员选错了。马上更正编码，已发生的错误收费全额退回。'),
    ]
    for t,q,a in scenes:
        slides.append(card_slide(t, [
            {'title':'🔴 质疑','body':q,'style':'red'},
            {'title':'🟢 标准应答','body':a,'style':'green'}
        ], 1, 'Part 3 · 场景应对'))

    slides.append(flow_slide('📅 整改闭环时间线', [
        {'label':'检查当日\n总结会·逐条认领','style':'red-step'},
        {'label':'3日内\n整改方案+退费清单','style':''},
        {'label':'1周内\n全院通报+制度修订','style':''},
        {'label':'1月内\nHIS预警+回头看','style':''},
        {'label':'长期\n每月自查·考核挂钩','style':'green-step'}
    ], 'Part 4 · 整改'))
    slides.append(bullet_slide('📋 问题台账模板（每科一表）', [
        '表头：序号 | 问题类别 | 违规描述 | 涉及金额 | 责任人 | 整改时限 | 是否完成',
        '示例：1 | 重复收费/诊疗类 | 温针与普通针刺同时收费 | xxx元 | 张xx | 立即 | ✓',
        '退费要求：银行转账凭证留存复印件，附于自查报告后'
    ], 'Part 4 · 台账'))
    slides.append(content_slide('📋 培训总结', '''
      <div class="box gold-box" style="text-align:center;padding:30px">
        <p style="font-size:24px;font-weight:700;color:var(--primary);margin-bottom:16px">自查认真、主动退费 = 从轻处理</p>
        <p style="font-size:24px;font-weight:700;color:var(--red);margin-bottom:16px">敷衍塞责、隐瞒不报 = 从重处理</p>
        <p style="font-size:18px;color:var(--muted);margin-top:20px">感谢聆听 · 欢迎再来指导！</p>
      </div>'''))
    return make_html('医保飞行检查迎检全流程', slides)


def build_m17():
    """院感防控与医疗废物管理 - 14 slides"""
    slides = []
    slides.append(cover_slide('🔬', '院感防控与医疗废物管理', '手卫生·无菌操作·消毒隔离·医疗废物分类处置', [
        '辽宁中医嘉和医院 · 标准化培训体系', '目标受众：全院医护 · 时长：60分钟 · 2026年12月'
    ]))
    slides.append(bullet_slide('🎯 培训目标', [
        '正确执行六步洗手法，知晓五个洗手时刻',
        '准确区分五类医疗废物', '正确使用黄色医疗废物袋和利器盒',
        '知晓职业暴露后的应急处理流程', '了解本院院感考核指标和奖惩制度'
    ]))
    slides.append(bullet_slide('🚨 院感不良事件警示', [
        '📊 全国每年约XX万例医院感染，直接经济损失超百亿',
        '📊 80%的院感通过手传播(WHO数据)',
        '⚖️ 法规：《医院感染管理办法》《医疗废物管理条例》',
        '⚠️ 违规后果：罚款+停业整顿+责任人追责'
    ], 'Part 1 · 重要性'))
    slides.append(bullet_slide('🧼 六步洗手法', [
        '① 掌心相对，手指并拢相互揉搓（内）',
        '② 手心对手背，沿指缝相互揉搓（外）',
        '③ 掌心相对，双手交叉指缝揉搓（夹）',
        '④ 弯曲手指，关节在掌心旋转揉搓（弓）',
        '⑤ 一手握另一手大拇指旋转揉搓（大）',
        '⑥ 五个手指尖并拢在掌心旋转揉搓（立）',
        '⏱️ 每次洗手 ≥ 15秒 · 流动水+洗手液'
    ], 'Part 2 · 手卫生'))
    slides.append(bullet_slide('⏰ 五个洗手时刻', [
        '1. 接触患者前 — 保护患者', '2. 无菌操作前 — 保护患者免受病菌侵入',
        '3. 接触体液后 — 保护自己', '4. 接触患者后 — 保护自己和下一位患者',
        '5. 接触患者环境后 — 即使没接触患者本人',
        '🔴 中医提醒：针灸/埋线/小针刀操作前后必须洗手+手消毒'
    ], 'Part 2 · 手卫生'))
    slides.append(bullet_slide('🗑️ 五类医疗废物分类', [
        '🔴 感染性废物：棉签、纱布、输液器、引流袋 → 黄色专用袋',
        '⚡ 损伤性废物：针头、刀片、安瓿 → 利器盒(禁止徒手处理)',
        '🧬 病理性废物：手术组织 → 双层黄色袋+标识',
        '☣️ 化学性废物：废弃消毒剂 → 专用容器',
        '💊 药物性废物：过期药品 → 药房统一回收',
        '❌ 常见错误：针头混入感染性废物袋→保洁人员刺伤!'
    ], 'Part 3 · 废物分类'))
    slides.append(bullet_slide('📦 利器盒使用规范', [
        '✅ 利器使用后立即投入(不暂存、不中转)',
        '✅ 装至3/4满时封口(禁止超满)',
        '✅ 封口后不可重新打开',
        '❌ 双手回套针帽 — 最高频针刺伤原因!', '❌ 徒手处理裸露针头',
        '❌ 利器投入普通垃圾袋',
        '⚠️ 针灸科特别注意：拔针后针具第一时间入利器盒'
    ], 'Part 3 · 利器盒'))
    slides.append(bullet_slide('🏪 医疗废物暂存与转运', [
        '暂存间要求：远离医疗区/食品加工区/人员活动区',
        '低温存放(≤25℃)·防鼠防蝇·≤48小时·明显警示标识',
        '转运交接：三联单·核对类别+重量+袋数·双方签名',
        '转运记录保存 ≥ 3年',
        '🧹 中药药渣→按生活垃圾处理(非医疗废物)'
    ], 'Part 3 · 暂存转运'))
    slides.append(bullet_slide('🧴 常用消毒剂及使用规范', [
        '含氯消毒液：500mg/L(一般物表) / 2000mg/L(血液体液污染)',
        '→ 现配现用，每24小时更换', '75%酒精：皮肤消毒、物体表面擦拭(易燃，远离火源)',
        '碘伏：皮肤消毒(注射、穿刺前)',
        '治疗室：每日紫外线消毒≥1小时(有记录)',
        '治疗台/床：每次治疗后消毒'
    ], 'Part 4 · 消毒'))
    slides.append(bullet_slide('📊 院感考核指标', [
        '手卫生依从率 ≥ 85% · 手卫生正确率 ≥ 90%',
        '消毒合格率 ≥ 95% · 医疗废物规范处置率 = 100%',
        '🔴 一票否决：废物混入生活垃圾 · 一次性器械复用 · 消毒记录造假'
    ], 'Part 5 · 考核'))
    slides.append(card_slide('👨‍⚕️ 各科室院感重点', [
        {'title':'🏥 针灸科/埋线门诊','body':'针具一穴一用·皮肤消毒≥5cm×5cm·棉球一穴一换','style':'accent'},
        {'title':'🩺 康复科','body':'治疗床每次消毒·理疗电极片专人专用','style':'accent'},
        {'title':'💊 中药房','body':'煎药室紫外线消毒·煎药机每日清洗','style':'green'},
        {'title':'🔬 检验科','body':'血液标本处理·生物安全柜使用','style':'red'},
        {'title':'🛏️ 住院部','body':'多重耐药菌隔离·床单位终末消毒','style':'orange'},
        {'title':'🏢 全院','body':'手卫生依从率·医疗废物正确分类','style':'gold'}
    ], 3, 'Part 5 · 科室重点'))
    slides.append(content_slide('📋 培训总结', '''
      <div class="box gold-box" style="text-align:center;padding:30px">
        <p style="font-size:24px;font-weight:700;color:var(--primary);margin-bottom:12px">院感无小事</p>
        <p style="font-size:20px;color:var(--accent);margin-bottom:8px">手卫生是防线 · 废物分类是底线</p>
        <p style="font-size:16px;color:var(--muted);margin-top:20px">感谢聆听</p>
      </div>'''))
    return make_html('院感防控与医疗废物管理', slides)


def build_m18():
    """职业暴露应急处置 - 12 slides"""
    slides = []
    slides.append(cover_slide('🚨', '职业暴露应急处置', '针刺伤·血液体液暴露·应急流程·上报追踪', [
        '辽宁中医嘉和医院 · 标准化培训体系', '目标受众：全院医护 · 时长：45分钟 · 2026年12月'
    ]))
    slides.append(bullet_slide('🎯 培训目标', [
        '识别职业暴露的高危场景和高危操作',
        '掌握针刺伤后"一挤二冲三消毒四上报"标准流程', '掌握血液/体液黏膜暴露紧急冲洗流程',
        '知晓本院职业暴露报告路径和追踪检测时间表', '了解HIV/HBV/HCV暴露后预防用药方案'
    ]))
    slides.append(card_slide('⚠️ 什么是职业暴露', [
        {'title':'定义','body':'医务人员在诊疗护理中，意外被感染性病原体携带者的血液、体液污染了皮肤、黏膜或被锐器刺伤。','style':'red'},
        {'title':'四种暴露类型','body':'①针刺伤(最高发>70%) ②刀割伤/玻璃割伤 ③黏膜溅洒(眼/口/鼻) ④破损皮肤接触','style':'accent'},
        {'title':'主要风险病原体','body':'HIV · HBV · HCV · 梅毒螺旋体','style':'orange'}
    ], 3, 'Part 1 · 认识'))
    slides.append(bullet_slide('🔴 高危操作清单', [
        '1. 回套针帽 — 禁止！最高频针刺伤原因', '2. 拔针/拔输液器时反弹刺伤',
        '3. 手术中徒手传递锐器', '4. 处理医疗废物时被袋内隐藏锐器刺伤',
        '5. 针灸科拔针时刺伤(⚠️ 中医特色风险点)', '6. 抽血/注射操作不规范',
        '高危科室：手术室 · 针灸科 · 检验科 · 护理 · 保洁'
    ], 'Part 1 · 高危场景'))
    slides.append(flow_slide('🩹 针刺伤处理流程', [
        {'label':'① 挤🩸\n近心端→远心端\n挤出少量血液','style':'red-step'},
        {'label':'② 冲🚿\n流动清水\n冲洗5分钟','style':''},
        {'label':'③ 消毒🧴\n75%酒精\n或碘伏消毒','style':''},
        {'label':'④ 包扎🩹\n无菌敷料\n覆盖伤口','style':''},
        {'label':'⑤ 报告📋\n30分钟内\n口头报告','style':'green-step'}
    ], 'Part 2 · 应急流程'))
    slides.append(bullet_slide('👁️ 黏膜暴露处理', [
        '眼部溅洒：生理盐水或流动清水反复冲洗 ≥ 15分钟',
        '→ 冲洗时翻开眼睑，确保结膜穹窿部充分冲洗 → 眼科检查',
        '口腔溅洒：立即吐出，清水反复漱口(禁止吞咽)',
        '破损皮肤：肥皂水+流动水清洗 → 碘伏消毒',
        '⚠️ 第一时间充分冲洗是最有效的措施！'
    ], 'Part 2 · 黏膜暴露'))
    slides.append(content_slide('📋 报告流程时间线', '''
      <div class="flow">
        <div class="step red-step">30min内<br>口头报告科室</div><div class="arrow">→</div>
        <div class="step">1h内<br>填写登记表</div><div class="arrow">→</div>
        <div class="step">2h内<br>评估暴露级别</div><div class="arrow">→</div>
        <div class="step">当天<br>抽血检测基线</div><div class="arrow">→</div>
        <div class="step green-step">4周/8周/12周/6月<br>追踪检测</div>
      </div>
      <p style="font-size:16px;color:var(--muted);margin-top:16px">登记表关键信息：暴露时间·暴露源患者·暴露类型·处理措施·见证人签名</p>''', 'Part 2 · 报告'))
    slides.append(card_slide('💊 暴露后预防用药(PEP)', [
        {'title':'🦠 HIV','body':'暴露后2h内用药最佳，最迟≤72h。三联药方案，全程服药28天不可自行停药。遵感染科医嘱。','style':'red'},
        {'title':'🦠 HBV','body':'抗体<10 mIU/mL→HBIG+乙肝疫苗加强。抗体>10→无需特殊处理。','style':'orange'},
        {'title':'🦠 HCV','body':'目前无有效预防性疫苗/药物。随访监测，如感染则抗病毒治疗。','style':'accent'}
    ], 3, 'Part 3 · PEP'))
    slides.append(bullet_slide('🛡️ 标准预防与个人防护', [
        '🔑 核心原则：所有患者的血液/体液均视为有传染性',
        '🧤 PPE按需选用：手套·口罩·护目镜·隔离衣',
        '❌ 绝对禁止：双手回套针帽·徒手处理锐器·利器投入普通垃圾袋'
    ], 'Part 4 · 预防'))
    slides.append(content_slide('📋 培训总结', '''
      <div class="box gold-box" style="text-align:center;padding:30px">
        <p style="font-size:20px;font-weight:700;color:var(--primary)">职业暴露无小事</p>
        <p style="font-size:18px;color:var(--accent);margin:12px 0">预防为主 · 及时处理 · 规范上报</p>
        <p style="font-size:14px;color:var(--muted)">暴露后2h内用药最佳 · 不要因为害怕而延误报告</p>
      </div>'''))
    return make_html('职业暴露应急处置', slides)


def build_m14():
    """十八项核心制度 - 16 slides"""
    slides = []
    slides.append(cover_slide('📜', '十八项核心制度与优势病种培训', '医疗质量安全核心制度要点 · 中医优势病种诊疗规范', [
        '辽宁中医嘉和医院 · 标准化培训体系', '目标受众：全院 · 时长：120分钟 · 2026年10月'
    ]))
    slides.append(bullet_slide('🎯 培训目标', [
        '说出十八项核心制度的名称和要点', '对照本科室识别制度落实薄弱环节',
        '掌握嘉和医院优势病种的诊疗规范', '知晓违反核心制度的后果和追责机制'
    ]))
    slides.append(bullet_slide('核心制度 1-5', [
        '1. 首诊负责制：首诊医师对患者全程负责，不得推诿',
        '2. 三级查房制度：住院医每日/主治48h内/副高72h内',
        '3. 会诊制度：科内24h/科间48h/急诊即时',
        '4. 分级护理制度：特级/一级/二级/三级标准明确',
        '5. 值班和交接班制度：危重床旁交接、"四交清"',
        '🔴 高频违规：首诊推诿、三级查房超时、值班交接不清'
    ], 'Part 1 · 制度1-5'))
    slides.append(bullet_slide('核心制度 6-9', [
        '6. 疑难病例讨论：入院1周未确诊→科内/2周→全院',
        '7. 急危重抢救制度：抢救记录6h内补记(注明补记时间)',
        '8. 术前讨论制度：所有手术必须术前讨论',
        '9. 死亡病例讨论：死亡后1周内(尸检病例2周内)',
        '🔴 抢救记录超6h未补记→病历丙级红线!'
    ], 'Part 1 · 制度6-9'))
    slides.append(bullet_slide('核心制度 10-14', [
        '10. 查对制度：身份(姓名+病案号+腕带)/药品/输血/手术部位',
        '11. 手术安全核查：麻醉前→切皮前→出室前三方核查',
        '12. 手术分级管理：四级手术+医师手术权限分级',
        '13. 新技术准入：伦理审查+技术论证+卫健委备案',
        '14. 危急值报告：接收→确认→处置→记录，10分钟通知临床',
        '🔴 检验科10分钟内通知，临床15分钟内处置'
    ], 'Part 1 · 制度10-14'))
    slides.append(bullet_slide('核心制度 15-18', [
        '15. 病历管理制度：24h入院记录+8h首程+出院3天归档',
        '16. 抗菌药物分级管理：非限制/限制/特殊使用三级',
        '17. 临床用血审核：输血前检查+知情同意+输血记录',
        '18. 信息安全管理制度：患者隐私保护+系统访问权限',
        '🔴 首程超24h→丙级病历+违反核心制度双重处罚'
    ], 'Part 1 · 制度15-18'))
    slides.append(bullet_slide('⚠️ 违反核心制度追责机制', [
        '个人：一般违规→扣质控分2-5分/严重→全院通报+扣500-1000元',
        '严重后果→暂停执业+吊销证书',
        '科室：违规率超标→扣科室质控分+科主任连带责任',
        '年度：核心制度知晓率纳入考核/连续两次不达标→不得评优',
        '💡 自查从轻·被查从重·屡犯从重'
    ], 'Part 1 · 追责'))

    diseases = [
        ('中风(脑梗死恢复期)', '辨证：风痰瘀阻/气虚血瘀/肝肾亏虚。针灸醒脑开窍法(内关+人中+三阴交)。康复评定：Fugl-Meyer+Barthel+Holden'),
        ('腰痛(腰椎间盘突出)', '辨证：气滞血瘀/寒湿痹阻/肝肾亏虚。推拿：按揉+弹拨+斜扳法。辅助：穴位注射+中药熏蒸'),
        ('面瘫(面神经炎)', '分期：急性期浅刺/恢复期电针+隔姜灸/后遗症期透刺+埋线。⚠️急性期禁止强刺激'),
        ('膝痹(膝关节骨性关节炎)', '小针刀规范：定位准确+深度≤关节囊+术后加压24h。关节腔注射：严格无菌操作'),
        ('项痹(颈椎病)', '牵引：坐位/仰卧、体重10-15%、15-20min。推拿：颈项放松+定点旋转扳法(C1-C2禁止暴力旋转)'),
        ('不寐(失眠)', '中药辨证：肝郁化火(龙胆泻肝汤)/心脾两虚(归脾汤)/阴虚火旺(天王补心丹)。针灸：神门+三阴交+百会+安眠。耳穴：神门+心+皮质下'),
        ('咳嗽(慢性支气管炎)', '中药辨证：风寒袭肺(三拗汤)/痰热壅肺(清金化痰汤)。穴位贴敷：肺俞+定喘+天突(三伏贴/三九贴)'),
    ]
    for t,b in diseases:
        slides.append(card_slide(f'优势病种：{t}', [{'title':t,'body':b,'style':'accent'}], 1, 'Part 2 · 优势病种'))

    slides.append(content_slide('📋 培训总结', '''
      <div class="box gold-box" style="text-align:center;padding:30px">
        <p style="font-size:24px;font-weight:700;color:var(--primary);margin-bottom:12px">核心制度是底线 · 优势病种是特色</p>
        <p style="font-size:20px;color:var(--accent)">知制度、守底线、扬特色</p>
      </div>'''))
    return make_html('十八项核心制度与优势病种', slides)


def build_m02():
    """穴位埋线门诊合规操作 - 14 slides"""
    slides = []
    slides.append(cover_slide('🌿', '穴位埋线门诊合规操作', '资质·收费·操作·院感·文书 全维度自查', [
        '辽宁中医嘉和医院 · 标准化培训体系', '目标受众：针灸科 · 时长：60分钟 · 2026年9月'
    ]))
    slides.append(bullet_slide('🎯 培训目标', [
        '准确说出2025年穴位埋线收费模式三大变更', '正确按"次·日"收费，不再按穴位个数计费',
        '掌握埋线操作的院感规范要点', '独立完成知情同意书的规范签署', '在飞检质疑时使用标准话术应答'
    ]))
    slides.append(content_slide('⚠️ 2025年收费模式重大变更', '''
      <div class="do-dont">
        <div class="dont-box"><div class="dont-header">❌ 旧模式(已废止)</div><div class="dont-body"><ul>
          <li>按穴位个数收费</li><li>埋线针/线体单独收费</li><li>埋线与普通针刺叠加收费</li><li>特殊穴位不限数量</li></ul></div></div>
        <div class="do-box"><div class="do-header">✅ 新模式(强制执行)</div><div class="do-body"><ul>
          <li>统一按"次·日"收费</li><li>针具+线体计入基本物耗</li><li>按最高项目标准计费</li><li>特殊穴位严格限制数量</li></ul></div></div>
      </div>
      <p style="margin-top:12px;font-size:14px;color:var(--red)">📜 辽医保发〔2025〕36号 · 违规：追回全部基金+约谈+通报</p>'''))
    slides.append(bullet_slide('💰 收费合规自查要点', [
        '计价单位：按"次·日"收费 / 单日仅收费1次', '耗材禁止单独收费：埋线针/线体/局麻药均含在项目价格中',
        '叠加禁止：埋线+针刺→只收一种 / 埋线+温针/电针→禁止',
        '🚨 警示：某门诊部按8穴收费+材料另收→追回全部基金+通报'
    ]))
    slides.append(bullet_slide('📜 机构与人员资质', [
        '机构：许可证有效·核准中医/针灸/中西医结合科·卫健委备案',
        '人员：中医执业资格·注册本院·埋线培训≥80学时·有效证书',
        '设施：独立治疗室·紫外线消毒·急救药品·吸氧设备',
        '❌ 禁止：非卫生技术人员从事穴位埋线操作'
    ]))
    slides.append(card_slide('🩺 适应症与禁忌症', [
        {'title':'✅ 适应症','body':'慢性功能性疾病·慢性疼痛·代谢性疾病·美容调理','style':'green'},
        {'title':'❌ 禁忌症(治疗前必须排查)','body':'皮肤破损·凝血障碍·过敏体质·孕妇·5岁以下儿童·活动期结核·严重心脏病','style':'red'}
    ], 2, 'Part 2 · 操作规范'))
    slides.append(bullet_slide('🧫 院感无菌操作要点', [
        '手卫生：操作前后六步洗手+75%酒精手消毒',
        '皮肤消毒：面积≥5cm×5cm / 由内向外2遍 / 棉球一穴一换',
        '器械：埋线针一次性使用(禁止复用) / 打开后4h内使用 / 缝线包装完整+有效期',
        '环境：治疗室每日紫外线消毒(有记录) / 治疗床每次消毒',
        '废物：废弃针具→利器盒 / 棉球手套→黄色感染性废物袋'
    ], 'Part 3 · 院感(高频扣分项)'))
    slides.append(bullet_slide('📝 医疗文书与知情同意', [
        '知情同意书六要素：①适应症 ②操作过程 ③可能风险 ④术后注意 ⑤不良反应 ⑥替代方案',
        '患者亲笔签名+日期 / 医师签名',
        '操作记录：穴位+线体类型+操作时长+患者反应+术后指导+医师签字',
        '中医辨证记录：理→法→方→穴→术 完整记录'
    ]))
    slides.append(bullet_slide('🚨 不良反应应急预案', [
        '晕针：立即起针→平卧→保暖→饮温水→急救穴→必要时120',
        '过敏：抗组胺药→局部处理→必要时取出线体→激素',
        '感染：局部热敷+抗感染→脓肿形成时切开引流',
        '急救设备：药品在有效期内·氧气充足·急救车每月清点'
    ]))
    # Scenario cards
    for t,q,a in [
        ('质疑"为什么按穴位个数收费？"','检查方：穴位埋线收了8个穴位的费用？','应答：根据2025年统一规范，埋线已统一按"次·日"收费，不应按穴位个数计费。系统更新滞后，马上更正。'),
        ('质疑"埋线材料为何单独收费？"','检查方：埋线的针和线为什么另外收费？','应答：针具和缝线均属基本物耗，已计入项目价格。本周更新收费系统，多收的全额退回。'),
        ('质疑操作资质','检查方：操作医师有埋线资质吗？','应答：医师均具备中医执业资格+系统专业培训。这是执业证书和培训结业证明。'),
        ('质疑无菌操作','检查方：消毒操作规范吗？','应答：严格按GB/T 21709.10-2008执行。六步洗手+皮肤消毒≥5cm×5cm+棉球一穴一换+针具一次性4h内使用。'),
    ]:
        slides.append(card_slide(t, [{'title':'🔴 质疑','body':q,'style':'red'},{'title':'🟢 应答','body':a,'style':'green'}], 1))
    slides.append(content_slide('📋 培训总结', '''
      <div class="box gold-box" style="text-align:center;padding:30px">
        <p style="font-size:24px;font-weight:700;color:var(--primary)">按次收费是底线</p>
        <p style="font-size:20px;color:var(--accent);margin:8px 0">无菌操作是生命线 · 资质合规是红线 · 文书完整是保障线</p>
      </div>'''))
    return make_html('穴位埋线门诊合规操作', slides)


def build_m03():
    """心电图室合规设置方案 - 10 slides"""
    slides = []
    slides.append(cover_slide('🫀', '心电图室合规设置方案', '辽宁省标准 · 资质要求 · 四种实施方案 · 沈阳办事指南', [
        '辽宁中医嘉和医院 · 标准化培训体系', '目标受众：心电图室/医务科 · 时长：45分钟 · 2026年10月'
    ]))
    slides.append(bullet_slide('📜 核心资质要求', [
        '🔑 出具心电图诊断报告的，必须是经注册的执业医师',
        '两类报告：客观描述(技师可出) vs 诊断报告(仅医师)',
        '路径一(首选)：注册"医学影像和放射治疗专业"的临床医师',
        '路径二(次选)：注册"内科"+从事心血管内科(两个条件缺一不可)',
        '📜 依据：卫政法发〔2004〕163号 · 卫医政函〔2008〕557号'
    ]))
    slides.append(content_slide('⚖️ 中医大夫能不能做心电？', '''
      <div class="box red-box"><h4>辽宁省专门文件：辽卫办发〔2016〕25号</h4>
      <p>第四条：纯中医专业执业范围<strong>不含</strong>医学影像</p>
      <p>第四条：中西医结合专业<strong>含</strong>医学影像和放射治疗</p>
      <p>第七条：老人老办法截止2015.12.31，仅限放射/检验/病理</p></div>
      <div class="card-grid col2" style="margin-top:12px">
        <div class="card green"><h4>✅ 可以做</h4><p>中西医结合医师→注册医学影像→可做心电诊断</p></div>
        <div class="card red"><h4>❌ 不能做</h4><p>纯中医医师→执业范围不含医学影像<br>违规处罚：罚款1-3万元(医师法第57条)</p></div>
      </div>'''))
    slides.append(card_slide('💡 四种解决方案', [
        {'title':'方案一 ⭐⭐⭐','body':'招聘临床类别执业医师(医学影像专业)。最稳妥、最合规。','style':'green'},
        {'title':'方案二','body':'现有中西医结合医师变更执业范围。依据辽卫办发25号第九条，通过考核后在备注栏注明。','style':'accent'},
        {'title':'方案三','body':'现有临床医师转岗培训。需脱产进修2年。依据卫医发〔2001〕169号。时间成本高。','style':'orange'},
        {'title':'方案四','body':'远程心电诊断合作。本院技师操作，委托有资质中心远程出报告。过渡方案。','style':'gold'}
    ], 2))
    slides.append(bullet_slide('📋 沈阳办事指南', [
        '前置步骤：向沈阳市卫健委申请增设"32.06 心电诊断专业"',
        '办理地点：沈阳市政务服务中心(沈河区市府大路260号)',
        '咨询电话：024-83962575 / 024-23412090',
        '线上：沈阳政务服务网 → 医疗机构执业登记-变更诊疗科目',
        '所需材料：许可证副本·设备配置表·变更注册书·人员登记表·资格证·平面图·执业证',
        '承诺时限：5个工作日(法定20-45个工作日)'
    ]))
    slides.append(content_slide('📋 培训总结', '''
      <div class="box gold-box" style="text-align:center;padding:30px">
        <p style="font-size:24px;font-weight:700;color:var(--primary)">执业范围是红线 · 合规运营是底线</p>
        <p style="font-size:18px;color:var(--accent);margin-top:12px">早规划、早申请、早落地</p>
      </div>'''))
    return make_html('心电图室合规设置方案', slides)


def build_m15():
    """岗前培训与考核 - 10 slides"""
    slides = []
    slides.append(cover_slide('🌱', '岗前培训与考核', '新员工入职培训体系：医院文化·规章制度·基本技能·考核标准', [
        '辽宁中医嘉和医院 · 标准化培训体系', '目标受众：新员工 · 周期：多日制 · 7月启动'
    ]))
    slides.append(flow_slide('📅 四阶段培训体系（30天）', [
        {'label':'阶段一(第1天)\n医院通识\n文化+规章+参观','style':''},
        {'label':'阶段二(第2-3天)\n制度法规\n医保+病历+院感','style':''},
        {'label':'阶段三(第4-5天)\n专业技能\n按岗位分流培训','style':'gold-step'},
        {'label':'阶段四(第6-30天)\n科室跟岗实操\n带教老师一对一','style':'green-step'},
    ]))
    slides.append(bullet_slide('🏥 阶段一：医院通识（入职第1天）', [
        '08:30-09:00 院领导致辞 / 医院发展历程与文化', '09:00-09:30 组织架构与科室介绍(医务科)',
        '09:30-10:30 员工手册与基本规章制度(人事科)', '10:30-12:00 参观各科室(带教老师)',
        '14:00-15:00 工资福利/考勤/职业发展(人事科)', '15:00-16:00 信息系统操作HIS/LIS/PACS(信息科)',
        '16:00-17:00 消防与安全生产(后勤科)'
    ]))
    slides.append(bullet_slide('📜 阶段二：制度法规（第2-3天）', [
        '医保政策基础(2h)：医保类型/报销比例/飞检常识',
        '病历书写规范(2h)：六大质控模块/丙级红线',
        '院感基础知识(1.5h)：手卫生/消毒/废物分类',
        '职业安全(1h)：职业暴露预防/针刺伤应急',
        '医患沟通(1.5h)：沟通技巧/投诉处理',
        '🔴 重点：首程8小时·丙级红线5条·六步洗手法'
    ]))
    slides.append(bullet_slide('🩺 阶段三：专业技能（第4-5天按岗分流）', [
        '👨‍⚕️ 医师：病历书写实操·中医四诊·急救CPR·合理用药',
        '👩‍⚕️ 护理：护理文书·基础操作(输液/导尿/吸氧)·急救配合·中药给药',
        '🔬 技师：设备操作规范·报告书写·院感操作',
        '💻 行政：医保收费规范·病案管理基础'
    ]))
    slides.append(bullet_slide('👥 阶段四：科室跟岗实操（第6-30天）', [
        '指定带教老师(高年资主治及以上)，一对一跟岗',
        '每日填写《新员工跟岗日志》', '带教老师每周评价(A/B/C/D四级)',
        '纪律：前2周不单独值夜班·不带教不在不做有创操作',
        '连续2周评价为D→延长跟岗或劝退'
    ]))
    slides.append(card_slide('📝 考核体系', [
        {'title':'入职第7天考核','body':'闭卷考试25道选择(≥80分) + 心肺复苏实操(按压深度+频率达标)','style':'accent'},
        {'title':'第30天转正考核','body':'岗位技能实操+病例分析 + 跟岗评价(带教≥85分) + 科室反馈(科主任评价合格)','style':'gold'}
    ], 2))
    slides.append(content_slide('📋 培训总结', '''
      <div class="box gold-box" style="text-align:center;padding:30px">
        <p style="font-size:24px;font-weight:700;color:var(--primary)">岗前培训是职业生涯第一课</p>
        <p style="font-size:18px;color:var(--accent);margin-top:12px">严进严出 · 对患者负责 · 对医院负责</p>
      </div>'''))
    return make_html('岗前培训与考核', slides)


def build_m16():
    """新版院内培训方案宣贯 - 8 slides"""
    slides = []
    slides.append(cover_slide('📜', '新版院内培训方案宣贯', '六大培训域 · 三级受众 · 学分考核 · 百日攻坚', [
        '辽宁中医嘉和医院 · 标准化培训体系', '目标受众：全院 · 时长：45分钟 · 2026年7月'
    ]))
    slides.append(card_slide('🏗️ 六大培训域全景图', [
        {'title':'🛡️ 医保合规','body':'飞检迎检·收费合规·ICD编码','style':'accent'},
        {'title':'📋 病历质控','body':'六大模块·丙级红线·三级质控','style':'green'},
        {'title':'🩺 临床技能','body':'急救流程·临床路径·医患沟通','style':'red'},
        {'title':'🌿 中医特色','body':'针灸推拿·中药管理·康复评定','style':'gold'},
        {'title':'📜 制度规范','body':'核心制度·岗前培训·绩效考核','style':'orange'},
        {'title':'🔬 院感安全','body':'无菌操作·废物管理·职业暴露','style':'accent'}
    ], 3))
    slides.append(bullet_slide('👥 三级受众划分', [
        '🏥 全院必修(所有人)：医保飞检·病历质控·急救·院感防控·核心制度',
        '🏢 科室专项：针灸科→埋线/中风针灸·康复科→评定质控·病案室→ICD编码',
        '👤 角色必修：新员工→岗前培训·医师→病历质控·护士→护理文书·技师→院感规范'
    ]))
    slides.append(bullet_slide('📅 下半年培训日历', [
        '7月 病历质控月：病历质控(医师)+急救(医护)+岗前(新员工)',
        '8月 医保合规月：飞检迎检+ICD编码系列(病案/医师)',
        '9月 中医特色月：穴位埋线(针灸)+中风针灸(针灸康复)',
        '10月 制度规范月：核心制度(全院)+心电图合规(相关科室)',
        '11月 DRG路径月：DRG首页(病案/医师)+康复路径(康复)',
        '12月 院感安全月：院感防控+职业暴露+年度总结(全院)'
    ]))
    slides.append(card_slide('📊 学分与考核挂钩', [
        {'title':'学分计算','body':'每次培训：出勤20% + 理论考核40% + 实操40%。年度学分为所有培训得分总和。','style':'accent'},
        {'title':'与绩效挂钩','body':'学分不达标→年度考核降级。出勤<80%→不得评优。丙级病历+培训不合格→双倍扣罚。','style':'red'},
        {'title':'与晋升挂钩','body':'职称晋升评审→培训学分作为参考条件。连续两年学分倒数→推迟晋升资格。','style':'orange'},
        {'title':'激励措施','body':'年度学分前三→评优加分。月度"学习之星"→额外奖励。承担讲师→教学积分×2。','style':'green'}
    ], 2))
    slides.append(bullet_slide('🎬 百日攻坚培训视频计划', [
        '目标：100天内完成核心培训模块的视频化制作',
        '✅ 已完成的视频：病历质控培训(16页)·急救流程(21页)',
        '🔶 制作中：医保飞检迎检·ICD-10编码·中风针灸',
        '使用方式：院内学习平台·线下预习(翻转课堂)·新人标准课程'
    ]))
    slides.append(content_slide('📋 培训总结', '''
      <div class="box gold-box" style="text-align:center;padding:30px">
        <p style="font-size:24px;font-weight:700;color:var(--primary)">培训是医院送给员工最好的福利</p>
        <p style="font-size:18px;color:var(--accent);margin-top:12px">学以致用 · 知行合一</p>
      </div>'''))
    return make_html('新版院内培训方案宣贯', slides)


# ======================== MAIN ========================
def main():
    print('=' * 60)
    print('  辽宁中医嘉和医院 · HTML培训幻灯片批量生成')
    print('  模板：嘉和医院病历质控培训_原始版.html')
    print('=' * 60)
    print()

    modules = [
        ('m01', build_m01, 'm01-医保飞行检查迎检全流程.html'),
        ('m02', build_m02, 'm02-穴位埋线门诊合规操作.html'),
        ('m03', build_m03, 'm03-心电图室合规设置方案.html'),
        ('m14', build_m14, 'm14-十八项核心制度与优势病种.html'),
        ('m15', build_m15, 'm15-岗前培训与考核.html'),
        ('m16', build_m16, 'm16-新版院内培训方案宣贯.html'),
        ('m17', build_m17, 'm17-院感防控与医疗废物管理.html'),
        ('m18', build_m18, 'm18-职业暴露应急处置.html'),
    ]

    for mid, build_func, fname in modules:
        try:
            html = build_func()
            filepath = os.path.join(OUTPUT_DIR, fname)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            # Count slides
            slide_count = html.count('class="slide')
            print(f'  ✅ {mid}: {fname} ({slide_count}页) → {filepath}')
        except Exception as e:
            print(f'  ❌ {mid}: 生成失败 - {e}')
            import traceback
            traceback.print_exc()

    print()
    print(f'📁 所有HTML幻灯片已保存至: {OUTPUT_DIR}')
    print('  在浏览器中直接打开即可演示（支持键盘翻页+导出图片）')
    print('=' * 60)


if __name__ == '__main__':
    main()
