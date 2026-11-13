Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting FraudShield AI Backend (FastAPI on Port 8000)..." -ForegroundColor Cyan
Write-Host " Loaded Model: PyTorch Focal Loss Deep Neural Network" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

Set-Location -Path (Split-Path -Parent $PSScriptRoot)
$pyExe = "C:\Users\praks\AppData\Local\Programs\Python\Python312\python.exe"
if (Test-Path $pyExe) {
    & $pyExe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
} else {
    python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
}
