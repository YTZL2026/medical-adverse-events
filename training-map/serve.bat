@echo off
chcp 65001 >nul
echo ============================================
echo  辽宁中医嘉和医院 · 标准化培训地图系统
echo  本地服务器启动中...
echo ============================================
echo.

:: Try Python 3
echo 浏览器访问: http://localhost:8000
echo.
python -m http.server 8000
pause
