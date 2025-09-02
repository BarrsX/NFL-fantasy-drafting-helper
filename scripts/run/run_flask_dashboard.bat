@echo off
echo ========================================
echo   Fantasy Drafting Web Dashboard
echo ========================================
echo.

cd /d "%~dp0\web_dashboard"

echo Installing dependencies...
pip install -r ../requirements.txt flask python-dotenv
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Starting dashboard with Flask CLI...
echo Dashboard will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

flask run
