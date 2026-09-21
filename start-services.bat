@echo off
echo ==========================================================
echo Starting AI-AgriVision Services (Backend + ML Microservice)
echo ==========================================================
echo.

echo [1/2] Starting Python ML Microservice on port 8000...
start "AI-AgriVision ML Microservice (:8000)" cmd /k "cd /d %~dp0ml-service && call .venv\Scripts\activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 2 /nobreak >nul

echo [2/2] Starting Node.js Backend API on port 5000...
start "AI-AgriVision Backend API (:5000)" cmd /k "cd /d %~dp0backend && npm run dev"

echo.
echo ==========================================================
echo All services launched in separate windows!
echo - ML Microservice: http://localhost:8000 (Swagger: http://localhost:8000/docs)
echo - Backend API:    http://localhost:5000 (Health:  http://localhost:5000/health)
echo.
echo You can now tap 'Retry' in your Flutter application.
echo ==========================================================
pause
