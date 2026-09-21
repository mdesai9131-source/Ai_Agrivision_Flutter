# PowerShell Launcher for AI-AgriVision Backend and ML Microservice
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Starting AI-AgriVision Services (Backend + ML Microservice)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start ML Microservice
Write-Host "`n[1/2] Starting Python ML Microservice on port 8000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\ml-service'; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

Start-Sleep -Seconds 2

# 2. Start Backend API
Write-Host "[2/2] Starting Node.js Backend API on port 5000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\backend'; npm run dev"

Write-Host "`nServices launched in separate windows!" -ForegroundColor Green
Write-Host "- ML Microservice: http://localhost:8000 (Swagger: http://localhost:8000/docs)" -ForegroundColor Yellow
Write-Host "- Backend API:    http://localhost:5000 (Health:  http://localhost:5000/health)" -ForegroundColor Yellow
Write-Host "`nYou can now tap 'Retry' in your Flutter application.`n" -ForegroundColor Green
