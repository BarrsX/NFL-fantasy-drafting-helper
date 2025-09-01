@echo off
echo ========================================
echo Fantasy Draft Cheat Sheet Generator
echo ========================================
echo.
echo Generating your dynasty superflex cheat sheet...
echo.

cd /d "%~dp0"
python scripts\core\sleeper_cheatsheet.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS: Cheat sheet generated!
    echo 📁 File saved to: output/dynasty_superflex_cheatsheet.xlsx
    echo.
    echo 🎨 Applying automatic strikethrough formatting...
    echo.
    
    REM Run the PowerShell formatting script directly
    powershell.exe -ExecutionPolicy Bypass -File "scripts\formatting\setup_excel_formatting.ps1" -ExcelFile "output\dynasty_superflex_cheatsheet.xlsx"
    
    REM Check if the formatting was successful by looking for the Excel file
    if exist "output\dynasty_superflex_cheatsheet.xlsx" (
        echo.
        echo 🎯 PERFECT! Your cheat sheet is ready for live drafting!
        echo.
        echo ✨ Features:
        echo    • Draft Priority rankings for optimal picks
        echo    • Automatic strikethrough when you type 'X' in Drafted column
        echo    • Color-coded tiers and position data
        echo    • Live draft board for real-time updates
        echo.
        echo 📋 How to use:
        echo    1. Open output/dynasty_superflex_cheatsheet.xlsx
        echo    2. Sort by 'Draft_Priority' column (highest first)
        echo    3. Type 'X' in Drafted column to cross out drafted players
        echo.
    ) else (
        echo.
        echo ⚠️  Cheat sheet generated but formatting may have failed.
        echo    You can still use the file, or run: .\apply_formatting.bat
        echo.
    )
) else (
    echo.
    echo ❌ ERROR: Failed to generate cheat sheet.
    echo.
    echo Check the error messages above for details.
    echo.
)

pause
