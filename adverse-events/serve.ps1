Write-Host "============================================" -ForegroundColor Blue
Write-Host " 辽宁中医嘉和医院 · 医疗不良事件报告系统" -ForegroundColor White
Write-Host " 本地服务器启动中..." -ForegroundColor Gray
Write-Host "============================================" -ForegroundColor Blue
Write-Host ""
Write-Host " 在浏览器打开: http://localhost:8000" -ForegroundColor Green
Write-Host ""
python -m http.server 8000
