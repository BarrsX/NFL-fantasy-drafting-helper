@echo off
echo ========================================
echo   Fantasy Drafting Web Dashboard
echo ========================================
echo.

cd /d "%~dp0"

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Starting dashboard...
cd web_dashboard
python run_dashboard.py

pause
