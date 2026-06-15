# -*- coding: utf-8 -*-
"""
病历质控 AI 分析引擎
读取提取后的病历文本 → DeepSeek 逐维度分析 → 输出缺陷 JSON → 可直接导入台账生成器
"""
import os, json, urllib.request, urllib.error, sys, re, time

# ==================== 配置 ====================
BASE = r'C:\Users\86132\AppData\Local\Programs\CC Switch\training-map\病历质控测试组'
INPUT_DIR = os.path.join(BASE, '_extracted')
OUTPUT_DIR = os.path.join(BASE, '_analysis')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# DeepSeek API 配置（从灵枢 config 读取）
CONFIG_PATH = r'C:\Users\86132\AppData\Local\Programs\CC Switch\palm-ai-app\config.json'
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    cfg = json.load(f)
API_URL = cfg['llm']['api_url']
API_KEY = cfg['llm']['api_key']
MODEL = cfg['llm'].get('model', 'deepseek-chat')

if '***' in API_KEY:
    print('❌ API Key 无效（包含***），请更新 config.json')
    sys.exit(1)

# ==================== 质控分析提示词 ====================
ANALYSIS_PROMPT = """你是辽宁中医嘉和医院病历质控专家。请对照以下六维标准，逐项检查这份病历，输出 JSON 格式结果。

## 六维检查标准

### 一、核心时限（7项）
1. 入院记录24h内完成并签名
2. 首次病程记录8h内完成
3. 主治医首次查房48h内完成
4. 主任医首次查房72h内完成
5. 新入院患者连续3天书写病程
6. 康复初始评定入院72h内完成
7. 阶段小结每30天完成1次

### 二、康复专项（4项）
1. 使用标准化量表评定（Fugl-Meyer/Barthel/MMSE等）
2. 中期评定每4周完成1次
3. 治疗记录单有具体项目、剂量、频次、部位、时长、签字
4. 医嘱单、治疗单、病程记录三单一致

### 三、病程记录质量（6项）
1. 首次病程有病例特点、诊断依据、鉴别诊断
2. 上级查房有分析意见和诊疗指导
3. 记录病情变化、异常检查结果及处理
4. 有创操作后即时书写记录
5. 向患者告知重要事项并有患方签名
6. 阶段小结体现病情变化与康复进展，非复制粘贴

### 四、文书完整性（8项）
1. 一般项目填写齐全无空项
2. 既往史、个人史、家族史无遗漏
3. 体格检查项目完整，专科查体重点突出
4. 辅助检查结果按时间顺序记录，外院检查注明机构名称
5. 辅助检查报告单有患者签名确认
6. 所有记录有医师亲笔签名，无代签漏签
7. 病案首页主要信息完整，诊断/操作名称规范
8. 出院前完成出院小结初稿，出院24h内正式提交

### 五、知情同意与告知（5项）
1. 患者授权委托书签署有效
2. 特殊检查/治疗知情同意书齐全且签署规范
3. 操作性治疗、康复治疗风险告知书已签署
4. 病危/病重、自费项目、输血等各类告知书齐全
5. 所有告知文书均有患方亲笔签名及日期

### 六、书写规范（4项）
1. 无大段复制粘贴内容
2. 修改用双线划改，注明修改时间和签名
3. 日期时间用24小时制，关键时间记录至分钟
4. 医学术语规范，无逻辑矛盾

### 一票否决项（5项）
1. 核心记录超时24h以上（首程、入院记录、手术记录）
2. 康复初始评定完全缺失
3. 知情同意书/告知书缺失或伪造签名
4. 主要诊断与治疗方案严重不符
5. 复制粘贴导致性别、左右侧等重大错误

## 输出格式（严格JSON，不要任何解释）
{
  "patient_name": "从病历中提取患者姓名",
  "admit_no": "病案号",
  "ward": "从科室字段提取(A/C/D)",
  "attending_doctor": "主管医师姓名",
  "summary": "一句话总结该病历质控情况",
  "defects": [
    {
      "dimension": "一、核心时限",
      "item": "入院记录24h内完成并签名",
      "description": "客观描述发现的问题",
      "responsible": "如有署名则填，否则填待确认"
    }
  ],
  "veto_items": ["触及的一票否决项，无则空数组"],
  "pass": true
}

只输出 JSON，不要任何解释。如果某项合格（未发现问题），不要列入 defects 数组。只列确实有问题的项。描述要专业客观，用"需关注""建议完善"等措辞。"""


def analyze_record(filepath):
    """分析单份病历"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    fname = os.path.basename(filepath)
    print(f'\n{"="*60}')
    print(f'  分析中: {fname}')
    print(f'  文本长度: {len(text)} 字符')
    print(f'{"="*60}')

    # 截取前8000字符
    truncated = text[:8000] if len(text) > 8000 else text
    if len(text) > 8000:
        print(f'  ⚠️ 文本过长({len(text)}字符)，截取前8000字符')

    # 重试最多2次
    analysis = None
    for attempt in range(2):
        try:
            body = json.dumps({
                'model': MODEL,
                'messages': [
                    {'role': 'system', 'content': ANALYSIS_PROMPT},
                    {'role': 'user', 'content': f'请分析以下病历：\n\n{truncated}'}
                ],
                'max_tokens': 1500,
                'temperature': 0.1,
                'stream': False,
            }).encode('utf-8')

            req = urllib.request.Request(API_URL, data=body, method='POST')
            req.add_header('Content-Type', 'application/json')
            req.add_header('Authorization', f'Bearer {API_KEY}')

            resp = urllib.request.urlopen(req, timeout=90)
            result = json.loads(resp.read().decode('utf-8'))
            reply = result['choices'][0]['message']['content']

            # 提取 JSON
            json_match = re.search(r'\{[\s\S]*\}', reply)
            if json_match:
                analysis = json.loads(json_match.group())
                break  # 成功，跳出重试循环
            else:
                if attempt == 0:
                    print(f'  ⚠️ JSON解析失败，重试... (尝试{attempt+1}/2)')
                else:
                    print(f'  ❌ 无法解析 AI 返回的 JSON')
                    print(f'  原始回复前300字: {reply[:300]}')
                    # 保存原始回复以便调试
                    raw_path = os.path.join(OUTPUT_DIR, fname.replace('.txt','_raw.txt'))
                    with open(raw_path, 'w', encoding='utf-8') as f:
                        f.write(reply)
                    print(f'  原始回复已保存: {raw_path}')
                    return None

        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8') if e.fp else ''
            print(f'  ❌ HTTP {e.code}: {err_body[:300]}')
            if e.code == 429 and attempt == 0:
                print(f'  ⏳ 限流，等5秒重试...')
                time.sleep(5)
            else:
                return None
        except json.JSONDecodeError as e:
            print(f'  ❌ JSON解析错误: {e} (尝试{attempt+1}/2)')
            if attempt == 0:
                continue
            return None
        except Exception as e:
            print(f'  ❌ 错误: {e}')
            return None

    # 成功：保存并打印
    if analysis is None:
        print(f'  ❌ 分析失败：所有重试均未成功')
        return None

    # 保存结果
    json_name = fname.replace('.txt', '_analysis.json')
    json_path = os.path.join(OUTPUT_DIR, json_name)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    # 打印摘要
    defects = analysis.get('defects', [])
    veto = analysis.get('veto_items', [])
    print(f'\n  📋 患者: {analysis.get("patient_name", "?")}')
    print(f'  🏥 病区: {analysis.get("ward", "?")}')
    print(f'  👨‍⚕️ 主管医师: {analysis.get("attending_doctor", "?")}')
    print(f'  ✅ 通过: {analysis.get("pass", "?")}')
    print(f'  📊 缺陷: {len(defects)} 条')
    if veto:
        print(f'  🚨 一票否决: {len(veto)} 条 - {veto}')
    print(f'\n  缺陷列表:')
    for d in defects:
        print(f'    [{d.get("dimension","")}] {d.get("item","")}')
        print(f'      → {d.get("description","")}')
        print(f'      → 责任人: {d.get("responsible","")}')

    print(f'\n  💾 已保存: {json_path}')
    return analysis


def main():
    print('=' * 60)
    print('  辽宁中医嘉和医院 · 病历质控 AI 分析引擎')
    print('=' * 60)

    if not os.path.exists(INPUT_DIR):
        print(f'❌ 未找到提取目录: {INPUT_DIR}')
        print('   请先运行 extract_xps.py 提取病历文本')
        return

    txt_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.txt')])
    if not txt_files:
        print('❌ 未找到 .txt 文件')
        return

    print(f'\n找到 {len(txt_files)} 份病历：')
    for f in txt_files:
        print(f'  📄 {f}')

    results = []
    for i, fname in enumerate(txt_files):
        fpath = os.path.join(INPUT_DIR, fname)
        result = analyze_record(fpath)
        if result:
            results.append(result)
        if i < len(txt_files) - 1:
            print(f'\n  ⏳ 等待2秒后分析下一份...')
            time.sleep(2)

    # 汇总
    print(f'\n\n{"="*60}')
    print(f'  分析完成！{len(results)}/{len(txt_files)} 份成功')
    print(f'  结果保存在: {OUTPUT_DIR}')
    print(f'{"="*60}')

    total_defects = sum(len(r.get('defects', [])) for r in results)
    print(f'\n  总缺陷: {total_defects} 条')
    for r in results:
        d = r.get('defects', [])
        v = r.get('veto_items', [])
        status = '🚨' if v else '✅' if r.get('pass') else '⚠️'
        print(f'  {status} {r.get("patient_name","?")} ({r.get("ward","?")}) : {len(d)}条缺陷 {"| 否决:"+str(len(v)) if v else ""}')


if __name__ == '__main__':
    main()
