$root = "D:\Fraud Detection"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " LAUNCHING FRAUDSHIELD FULL-STACK APPLICATION" -ForegroundColor Yellow
Write-Host " Backend:  FastAPI on http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host " Frontend: Next.js + Tailwind on http://localhost:3000" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Launch Backend in new window
Start-Process powershell.exe -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "Set-Location '$root'; .\scripts\run_backend.ps1"

# Launch Frontend in new window
Start-Process powershell.exe -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "Set-Location '$root'; .\scripts\run_frontend.ps1"

Write-Host "`nBoth terminal windows are launched!" -ForegroundColor Green
Write-Host "Wait 5-10 seconds for Next.js to compile, then open: http://localhost:3000" -ForegroundColor Yellow
