Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting FraudShield Next.js App (Port 3000)..." -ForegroundColor Cyan
Write-Host " URL: http://localhost:3000" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

Set-Location -Path "D:\Fraud Detection\frontend"
npm run dev
