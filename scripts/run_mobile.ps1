Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting FraudShield Mobile App (Expo Metro Bundler)..." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Install and open the free 'Expo Go' app on your Android or iPhone" -ForegroundColor Yellow
Write-Host "2. Scan the QR code in terminal using your phone camera or Expo Go" -ForegroundColor Yellow
Write-Host "3. The mobile app loads immediately on your phone!" -ForegroundColor Green
Write-Host ""
Write-Host "[Tip] Press 'w' in terminal to preview in web browser" -ForegroundColor Gray
Write-Host "[Tip] Press 'a' to run in Android emulator" -ForegroundColor Gray
Write-Host ""

Set-Location -Path "D:\Fraud Detection\mobile"
npx expo start

