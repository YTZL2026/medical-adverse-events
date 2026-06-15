# -*- coding: utf-8 -*-
"""一键打包：将 training-map 项目打包为 ZIP"""
import zipfile, os, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(os.path.dirname(ROOT), '培训地图项目包.zip')
NAME = os.path.basename(ROOT)

def zipdir(path, zf, prefix=''):
    for root, dirs, files in os.walk(path):
        for file in files:
            fp = os.path.join(root, file)
            arcname = os.path.join(prefix, os.path.relpath(fp, path))
            zf.write(fp, arcname)
            print(f'  📦 {arcname}')

print('=' * 50)
print('  辽宁中医嘉和医院 · 培训地图项目打包')
print('=' * 50)
print()

with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zf:
    zipdir(ROOT, zf, NAME)

size_mb = os.path.getsize(OUTPUT) / (1024*1024)
print()
print(f'✅ 打包完成！')
print(f'📁 文件：{OUTPUT}')
print(f'📊 大小：{size_mb:.1f} MB')
print()
print('解压后双击 training-map/serve.bat 即可启动')
