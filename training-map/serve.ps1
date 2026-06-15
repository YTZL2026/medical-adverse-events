Write-Host "============================================" -ForegroundColor Cyan
Write-Host " 辽宁中医嘉和医院 · 标准化培训地图系统" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notmatch "Loopback" -and $_.PrefixOrigin -ne "WellKnown" } | Select-Object -First 1).IPAddress

if (-not $ip) { $ip = "localhost" }

Write-Host "📱 手机访问地址：" -ForegroundColor Green
Write-Host "   👉  http://${ip}:8000" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host ""
Write-Host "📍 电脑浏览器访问：http://localhost:8000" -ForegroundColor Gray
Write-Host ""

Set-Location $PSScriptRoot

try {
    python -m http.server 8000
} catch {
    try {
        python3 -m http.server 8000
    } catch {
        Write-Host "❌ 未找到 Python" -ForegroundColor Red
        Read-Host "按回车退出"
    }
}
