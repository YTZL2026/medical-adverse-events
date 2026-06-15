@echo off
chcp 65001 >nul
echo ============================================
echo  辽宁中医嘉和医院 · 医疗不良事件报告系统
echo  本地服务器启动中...
echo ============================================
echo.
echo   在浏览器打开: http://localhost:8000
echo.
python -m http.server 8000
pause
