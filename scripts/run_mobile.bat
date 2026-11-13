@echo off
echo ==========================================================
echo Starting FraudShield Mobile App (Expo Metro Bundler)...
echo ==========================================================
echo.
echo 1. Open the "Expo Go" app on your Android or iPhone
echo 2. Scan the QR code shown below with your phone camera / Expo Go
echo 3. The mobile app will open immediately on your phone!
echo.
echo [Tip] Press 'w' in terminal to open Web Mobile Preview
echo [Tip] Press 'a' in terminal to run in Android Emulator
echo ==========================================================
echo.

cd /d "D:\Fraud Detection\mobile"
npx expo start
pause

