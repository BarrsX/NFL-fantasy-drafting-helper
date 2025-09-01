@echo off
echo ========================================
echo Fantasy Draft Cheat Sheet - Auto Setup
echo ========================================
echo.
echo This will apply automatic strikethrough formatting to your draft board.
echo.
echo Usage: Drag and drop your Excel file onto this batch file,
echo or run it from the command line with the file path as an argument.
echo.
echo Example: apply_formatting.bat "output\my_cheatsheet.xlsx"
echo.

if "%~1"=="" (
    echo Applying formatting to the default file: output\dynasty_superflex_cheatsheet.xlsx
    echo.
    set EXCEL_FILE=output\dynasty_superflex_cheatsheet.xlsx
) else (
    set EXCEL_FILE=%~1
    echo Applying formatting to: %EXCEL_FILE%
    echo.
)

if not exist "%EXCEL_FILE%" (
    echo ERROR: File not found: %EXCEL_FILE%
    echo.
    pause
    exit /b 1
)

echo Running PowerShell formatting script...
powershell.exe -ExecutionPolicy Bypass -File "scripts\formatting\setup_excel_formatting.ps1" -ExcelFile "%EXCEL_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS: Automatic strikethrough formatting applied!
    echo.
    echo 🎯 Your Excel file now has automatic strikethrough when you enter 'X' in the Drafted column.
    echo 📁 The formatting has been applied directly to your original file.
    echo.
    echo 💡 Tip: Open the file and try typing 'X' in column I (Drafted) to test it!
    echo.
) else (
    echo.
    echo ❌ ERROR: Failed to apply formatting.
    echo.
    echo Try running the PowerShell script manually or check the error messages above.
    echo.
)

pause
