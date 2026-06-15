# -*- coding: utf-8 -*-
"""Extract text from HIS-exported XPS files for AI analysis"""
import zipfile, os, re, xml.etree.ElementTree as ET

BASE = r'C:\Users\86132\AppData\Local\Programs\CC Switch\training-map\病历质控测试组'
OUT = os.path.join(BASE, '_extracted')
os.makedirs(OUT, exist_ok=True)

for ward in ['A组','C组','D组']:
    ward_dir = os.path.join(BASE, ward)
    if not os.path.exists(ward_dir): continue
    for fname in os.listdir(ward_dir):
        if not fname.endswith('.xps'): continue
        fpath = os.path.join(ward_dir, fname)
        print(f'\n{"="*60}')
        print(f'  {ward} / {fname}')
        print(f'{"="*60}')

        patient_name = fname.split('（')[0] if '（' in fname else fname.replace('.xps','')
        all_text = []

        try:
            with zipfile.ZipFile(fpath, 'r') as z:
                # Find page files
                pages = [n for n in z.namelist() if n.endswith('.fpage')]
                pages.sort()

                for i, page_path in enumerate(pages, 1):
                    xml_data = z.read(page_path).decode('utf-8')
                    # Extract all Glyphs elements (contain text)
                    root = ET.fromstring(xml_data)
                    ns = {'x': 'http://schemas.microsoft.com/xps/2005/06'}
                    glyphs = root.findall('.//x:Glyphs', ns)
                    page_text = []
                    for g in glyphs:
                        text = g.get('UnicodeString', '')
                        if text and text.strip():
                            page_text.append(text.strip())
                    if page_text:
                        all_text.append(f'--- Page {i} ---')
                        all_text.append('\n'.join(page_text))
        except Exception as e:
            print(f'  ERROR: {e}')
            continue

        full_text = '\n'.join(all_text)

        # Save extracted text
        txt_name = fname.replace('.xps','.txt')
        txt_path = os.path.join(OUT, f'{ward}_{txt_name}')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        print(f'\n  Extracted: {len(full_text)} chars')
        print(f'  Saved to: {txt_path}')
        print(f'\n  --- Preview (first 500 chars) ---')
        print(full_text[:500])

print(f'\n\nDone! All files saved to: {OUT}')
