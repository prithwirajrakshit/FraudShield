@echo off
echo ==========================================================
echo Starting FraudShield Backend (Port 8000) and Frontend (Port 3000)...
echo ==========================================================

start "FraudShield Backend" /D "%~dp0.." cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"
start "FraudShield Frontend" /D "%~dp0..\frontend" cmd /k "npm run dev"

echo Both windows opened!
echo Wait a few seconds, then open: http://localhost:3000
