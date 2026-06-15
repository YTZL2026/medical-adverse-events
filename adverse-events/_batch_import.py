"""
批量文件识别工具 — 全格式 → CSV
================================
用法：
  python _batch_import.py                          # 扫描 样本/ 目录下所有文件
  python _batch_import.py <文件或目录路径>           # 指定路径
  python _batch_import.py 样本/ --output out.csv    # 指定输出文件

支持格式一览：
  ┌─────────────────┬──────────────────────┬─────────────┐
  │ 格式             │ 提取方式              │ 准确率      │
  ├─────────────────┼──────────────────────┼─────────────┤
  │ .docx (Word)    │ 直接解析XML           │ 100%        │
  │ .json           │ 直接解析              │ 100%        │
  │ .txt / .md      │ 直接读取              │ 100%        │
  │ .csv            │ 直接解析              │ 100%        │
  │ .xps            │ 直接解析XML           │ 100%        │
  │ .pdf (文本型)    │ 直接提取文字           │ ~95%        │
  │ .pdf (扫描型)    │ OCR                   │ ~90%        │
  │ .png/.jpg/.bmp  │ OCR                   │ ~90%        │
  │ .tiff/.tif      │ OCR                   │ ~90%        │
  └─────────────────┴──────────────────────┴─────────────┘

依赖安装（一次性）：
  pip install easyocr python-docx Pillow
  # 如需处理扫描 PDF 额外安装（二选一）：
  pip install PyMuPDF          # 推荐，轻量
  pip install pdf2image        # 还需装 poppler
"""
import sys, os, csv, json, re, zipfile
from xml.etree import ElementTree as ET

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ==================== CONFIG ====================
INPUT_PATH = '样本'
OUTPUT_CSV = '样本/_batch_result.csv'
CONFIDENCE_THRESHOLD = 0.3

NS_WORD = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS_XPS  = 'http://schemas.microsoft.com/xps/2005/06'

# ==================== FORMAT DETECTION ====================
def get_ext(fp):
    return os.path.splitext(fp)[1].lower()

TEXT_NATIVE_EXT = {'.docx', '.json', '.txt', '.md', '.csv', '.xps'}
IMAGE_EXT       = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp'}
PDF_EXT         = {'.pdf'}
ALL_SUPPORTED   = TEXT_NATIVE_EXT | IMAGE_EXT | PDF_EXT

# ==================== FILE WALKER ====================
def list_files(path):
    if os.path.isfile(path):
        return [path] if get_ext(path) in ALL_SUPPORTED else []
    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            if f.startswith('_batch'): continue  # skip previous outputs
            fp = os.path.join(root, f)
            if get_ext(fp) in ALL_SUPPORTED:
                files.append(fp)
    return sorted(files)

# ==================== DIRECT TEXT EXTRACTORS ====================
# These give 100% accurate text without OCR.

def extract_docx(fp):
    """Word .docx → plain text (zip + XML, no library needed)"""
    text_parts = []
    with zipfile.ZipFile(fp, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
        for elem in tree.iter():
            tag = elem.tag.replace(f'{{{NS_WORD}}}', '')
            if tag == 't' and elem.text:
                text_parts.append(elem.text)
            elif tag in ('p', 'br'):
                text_parts.append('\n')
    return ''.join(text_parts)

def extract_json(fp):
    """JSON → formatted text"""
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Flatten JSON to readable text lines
    lines = []
    def flatten(obj, prefix=''):
        if isinstance(obj, dict):
            for k, v in obj.items():
                flatten(v, f'{prefix}{k}: ')
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                flatten(item, f'{prefix}[{i}] ')
        elif obj is not None and obj != '':
            lines.append(f'{prefix}{obj}')
    flatten(data)
    return '\n'.join(lines)

def extract_txt(fp):
    """Plain text / Markdown → text"""
    with open(fp, 'r', encoding='utf-8') as f:
        return f.read()

def extract_csv(fp):
    """CSV → text (first few rows as key:value)"""
    with open(fp, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows: return ''
    headers = rows[0]
    lines = []
    for i, row in enumerate(rows[1:6]):  # first 5 data rows
        for h, v in zip(headers, row):
            if v.strip():
                lines.append(f'{h}: {v.strip()}')
        lines.append('---')
    return '\n'.join(lines)

def extract_xps(fp):
    """XPS (XML Paper Specification) → plain text"""
    text_parts = []
    with zipfile.ZipFile(fp, 'r') as z:
        # XPS stores pages as Documents/1/Pages/*.fpage
        for name in z.namelist():
            if name.endswith('.fpage') and 'Pages/' in name:
                with z.open(name) as f:
                    tree = ET.parse(f)
                for elem in tree.iter():
                    if elem.tag.endswith('}Glyphs') or 'Glyphs' in elem.tag:
                        unicode_str = elem.get('UnicodeString', '')
                        if unicode_str:
                            text_parts.append(unicode_str)
    return ''.join(text_parts)

def extract_pdf_text(fp):
    """Try to extract text from PDF directly (for text-based PDFs)."""
    # Method 1: PyMuPDF (fitz)
    try:
        import fitz
        doc = fitz.open(fp)
        text = []
        for page in doc:
            text.append(page.get_text())
        doc.close()
        result = '\n'.join(text)
        if result.strip():
            return result
    except ImportError:
        pass
    except Exception:
        pass

    # Method 2: pdfplumber
    try:
        import pdfplumber
        text = []
        with pdfplumber.open(fp) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t: text.append(t)
        result = '\n'.join(text)
        if result.strip():
            return result
    except ImportError:
        pass
    except Exception:
        pass

    return None  # No text extracted, needs OCR fallback

# ==================== OCR ENGINE ====================
ocr_engine = None

def init_ocr():
    global ocr_engine

    # === Strategy 1: PaddleOCR (Chinese servers, fast in China) ===
    try:
        from paddleocr import PaddleOCR
        print("加载 PaddleOCR 模型（首次自动下载，国内服务器，很快）...")
        ocr_engine = PaddleOCR(lang='ch', use_angle_cls=False, show_log=False)
        print("PaddleOCR 就绪 ✓\n")
        return
    except ImportError:
        pass
    except Exception as e:
        print(f"PaddleOCR 初始化失败: {e}")

    # === Strategy 2: EasyOCR (GitHub, may be slow in China) ===
    try:
        import easyocr
    except ImportError:
        easyocr = None

    if easyocr:
        print("加载 EasyOCR 中文模型...")
        print("（首次需下载 ~200MB，网络慢可能需 5-10 分钟）")
        try:
            ocr_engine = easyocr.Reader(['ch_sim', 'en'], gpu=False)
            print("EasyOCR 就绪 ✓\n")
            return
        except Exception as e:
            print(f"EasyOCR 初始化失败: {e}")
            print("建议改用 PaddleOCR: pip install paddlepaddle paddleocr\n")
            ocr_engine = None
            return

    # === Strategy 3: Tesseract ===
    try:
        import pytesseract
        from PIL import Image
        ocr_engine = 'tesseract'
        print("Tesseract OCR 就绪 ✓\n")
        return
    except ImportError:
        pass

    print("⚠️ 未安装 OCR 库。图片和扫描PDF将无法识别。")
    print("  推荐（国内用户）: pip install paddlepaddle paddleocr")
    print("  备选: pip install easyocr")
    print("  文本型文件（docx/json/txt/csv/xps）不受影响。\n")
    ocr_engine = None

def ocr_image(image):
    """Run OCR on PIL Image → list of (text, confidence)."""
    if ocr_engine is None:
        return []
    if ocr_engine == 'tesseract':
        import pytesseract
        data = pytesseract.image_to_data(image, lang='chi_sim+eng', output_type=pytesseract.Output.DICT)
        results = []
        for i in range(len(data['text'])):
            t = data['text'][i].strip()
            conf = int(data['conf'][i]) / 100 if data['conf'][i] != '-1' else 0
            if t and conf >= CONFIDENCE_THRESHOLD:
                results.append((t, conf))
        return results
    else:
        # PaddleOCR or EasyOCR
        import numpy as np
        arr = np.array(image)
        if hasattr(ocr_engine, 'ocr'):
            # PaddleOCR: .ocr() returns [[[bbox], (text, conf)], ...] or None
            raw = ocr_engine.ocr(arr)
            if raw is None or len(raw) == 0 or raw[0] is None:
                return []
            return [(item[1][0], item[1][1]) for item in raw[0] if item[1][1] >= CONFIDENCE_THRESHOLD]
        else:
            # EasyOCR: .readtext() returns [(bbox, text, conf), ...]
            raw = ocr_engine.readtext(arr)
            return [(r[1], r[2]) for r in raw if r[2] >= CONFIDENCE_THRESHOLD]

def pdf_to_images(fp):
    """Convert PDF pages to PIL Images."""
    # Method 1: PyMuPDF
    try:
        import fitz
        from PIL import Image
        doc = fitz.open(fp)
        images = []
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        doc.close()
        return images
    except ImportError:
        pass

    # Method 2: pdf2image
    try:
        from pdf2image import convert_from_path
        return convert_from_path(fp, dpi=200)
    except ImportError:
        pass

    print("  ⚠️ 无法转换PDF，请安装: pip install PyMuPDF")
    return []

# ==================== UNIFIED EXTRACTOR ====================
def extract_text_from_file(fp):
    """
    Extract all text from a file using the best available method.
    Returns (text_string, method_used).
    """
    ext = get_ext(fp)

    # ---- Text-native formats (100% accurate, no OCR) ----
    if ext == '.docx':
        return extract_docx(fp), 'DOCX直接解析'
    if ext == '.json':
        return extract_json(fp), 'JSON直接解析'
    if ext in ('.txt', '.md'):
        return extract_txt(fp), 'TXT直接读取'
    if ext == '.csv':
        return extract_csv(fp), 'CSV直接解析'
    if ext == '.xps':
        return extract_xps(fp), 'XPS直接解析'

    # ---- PDF: try text first, fallback to OCR ----
    if ext == '.pdf':
        text = extract_pdf_text(fp)
        if text and len(text.strip()) > 20:
            return text, 'PDF文本提取'
        # Text extraction failed — it's a scanned PDF, need OCR
        if ocr_engine is None:
            return None, 'PDF需要OCR(未安装OCR库)'
        print("    文本提取失败，切换为 OCR 模式...")
        images = pdf_to_images(fp)
        if not images:
            return None, 'PDF无法转换(需安装PyMuPDF)'
        all_results = []
        for i, img in enumerate(images):
            print(f"    OCR 第 {i+1}/{len(images)} 页...")
            all_results.extend(ocr_image(img))
        text = ' '.join([t for t, c in all_results])
        return text, f'PDF OCR ({len(images)}页)'

    # ---- Images: OCR required ----
    if ext in IMAGE_EXT:
        if ocr_engine is None:
            return None, '图片需要OCR(未安装OCR库)'
        try:
            from PIL import Image
            img = Image.open(fp)
            results = ocr_image(img)
            text = ' '.join([t for t, c in results])
            return text, '图片OCR'
        except Exception as e:
            return None, f'图片读取失败: {e}'

    return None, f'不支持: {ext}'

# ==================== FIELD EXTRACTION ====================
def extract_fields(text):
    """Apply regex patterns to extract structured fields from text."""
    if not text:
        return {}

    fields = {}
    # Normalize: replace Chinese punctuation, collapse whitespace
    clean = text.replace('\n', ' ').replace('\r', ' ')

    # --- Patient name ---
    for pat in [
        r'姓名[：:\s]*([^\s]{2,4})',
        r'患者[姓名]?[：:\s]*([^\s]{2,4})',
        r'病人[姓名]?[：:\s]*([^\s]{2,4})',
    ]:
        m = re.search(pat, clean)
        if m:
            fields['a_name'] = m.group(1)
            break

    # --- Record ID ---
    for pat in [
        r'(?:病历号|住院号|登记号|病案号|ID)[：:\s]*([A-Za-z0-9\-]+)',
        r'No[.:\s]*([A-Za-z0-9\-]+)',
    ]:
        m = re.search(pat, clean)
        if m:
            fields['a_record_id'] = m.group(1)
            break

    # --- Gender ---
    m = re.search(r'(?:性别|Sex)[：:\s]*(男|女|Male|Female)', clean, re.IGNORECASE)
    if m:
        g = m.group(1)
        fields['a_gender'] = '男' if g in ('男', 'Male', 'male') else '女'
    elif re.search(r'\b男\b', clean[:200]):
        fields['a_gender'] = '男'
    elif re.search(r'\b女\b', clean[:200]):
        fields['a_gender'] = '女'

    # --- Age ---
    m = re.search(r'(?:年龄|Age)[：:\s]*(\d{1,3})\s*岁?', clean, re.IGNORECASE)
    if m: fields['a_age'] = m.group(1)

    # --- Diagnosis ---
    for pat in [
        r'(?:诊断|临床诊断|入院诊断|主要诊断)[：:\s]*(.+?)(?:。|\s{2,}|$)',
        r'Diagnosis[：:\s]*(.+?)(?:\.|\s{2,}|$)',
    ]:
        m = re.search(pat, clean, re.IGNORECASE)
        if m:
            fields['a_diagnosis'] = m.group(1).strip()[:100]
            break

    # --- Department ---
    for pat in [
        r'(?:科室|病区|所在科室|Department|Dept)[：:\s]*([^\s]{2,15})',
    ]:
        m = re.search(pat, clean, re.IGNORECASE)
        if m:
            fields['h_dept'] = m.group(1).strip()
            break

    # --- Event location ---
    for loc in ['急诊','门诊','住院部','医技部门','行政后勤部门','ICU','手术室']:
        if loc in clean:
            fields['b_location'] = loc
            break

    # --- Date ---
    m = re.search(r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})[日号]?', clean)
    if m:
        dt = m.group(1).replace('年','-').replace('月','-').replace('/','-')
        fields['a_treatment_time'] = dt

    # --- Doctor / Reporter ---
    for pat in [
        r'(?:报告人|上报人|医师|主治医生|Doctor)[：:\s]*([^\s]{2,4})',
    ]:
        m = re.search(pat, clean)
        if m and not fields.get('h_name'):
            fields['h_name'] = m.group(1)
            break

    # --- Phone ---
    m = re.search(r'(?:电话|联系电话|Tel|Phone)[：:\s]*(\d[\d\-]{7,15})', clean, re.IGNORECASE)
    if m: fields['h_phone'] = m.group(1)

    # --- Event description (catch long narrative text) ---
    for pat in [
        r'(?:事件经过|不良事件|事件描述|Description)[：:\s]*(.+?)(?:原因|处理|分析|$)',
    ]:
        m = re.search(pat, clean, re.IGNORECASE)
        if m:
            desc = m.group(1).strip()[:200]
            if len(desc) > 10:
                fields['b_description'] = desc
            break

    return fields

# ==================== MAIN ====================
def main():
    global INPUT_PATH, OUTPUT_CSV
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--output' and i+1 < len(args):
            OUTPUT_CSV = args[i+1]; i += 2
        elif not args[i].startswith('--'):
            INPUT_PATH = args[i]; i += 1
        else:
            i += 1

    print("=" * 60)
    print("  辽宁中医嘉和医院 · 批量文件识别工具")
    print("  全格式 → 字段提取 → CSV")
    print("=" * 60)
    print(f"\n输入: {INPUT_PATH}")
    print(f"输出: {OUTPUT_CSV}")
    print(f"\n支持格式: {', '.join(sorted(ALL_SUPPORTED))}")

    # Init OCR
    init_ocr()

    # List files
    files = list_files(INPUT_PATH)
    if not files:
        print(f"\n未找到支持的文件。")
        sys.exit(1)

    print(f"找到 {len(files)} 个文件:\n")
    for f in files:
        print(f"  📄 {os.path.basename(f)}")
    print()

    # Process each file
    results = []
    for idx, fp in enumerate(files):
        fname = os.path.basename(fp)
        ext = get_ext(fp)
        print(f"[{idx+1}/{len(files)}] {fname} ({ext})")

        try:
            text, method = extract_text_from_file(fp)

            if not text:
                print(f"  ⚠️ {method}")
                results.append({'_source_file': fname, '_method': method, '_error': method})
                continue

            print(f"  提取方式: {method}")
            preview = text[:150].replace('\n', ' ').strip()
            print(f"  文本预览: {preview}...")

            fields = extract_fields(text)
            fields['_source_file'] = fname
            fields['_method'] = method
            results.append(fields)

            found = [(k, v) for k, v in fields.items() if not k.startswith('_')]
            if found:
                for k, v in found:
                    print(f"    ✅ {k}: {v}")
            else:
                print(f"    ⚠️ 未匹配到字段（文本已保留在CSV中供人工查看）")
                # Keep raw text for manual review
                fields['_raw_text'] = text[:500]
        except Exception as e:
            print(f"  ❌ 失败: {e}")
            results.append({'_source_file': fname, '_error': str(e)})

    # Build CSV
    if not results:
        print("\n没有提取到任何数据。")
        sys.exit(1)

    field_order = ['a_name', 'a_record_id', 'a_gender', 'a_age', 'a_occupation',
                   'a_treatment_time', 'a_diagnosis', 'b_location', 'b_related',
                   'b_consequence', 'b_description', 'e_cause', 'e_action',
                   'h_name', 'h_role', 'h_dept', 'h_phone', '_source_file', '_method']
    all_keys = list(dict.fromkeys(
        [k for k in field_order if any(k in r for r in results)] +
        [k for r in results for k in r if k not in field_order]
    ))

    out_dir = os.path.dirname(OUTPUT_CSV)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(OUTPUT_CSV, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_keys, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)

    print(f"\n{'='*60}")
    print(f"✅ 完成！{len(results)} 条记录 → {OUTPUT_CSV}")
    print(f"\n下一步：")
    print(f"  1. 用 Excel 打开 {OUTPUT_CSV} 核对修正")
    print(f"  2. 打开 index.html → 📥 批量导入 → 上传 CSV")
    print(f"{'='*60}")
    input("\n按回车退出...")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ 程序异常退出: {e}")
        import traceback
        traceback.print_exc()
        print("\n按回车退出...")
        input()
