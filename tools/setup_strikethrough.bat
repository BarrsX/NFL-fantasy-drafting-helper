@echo off
echo ========================================
echo  FANTASY DRAFT STRIKETHROUGH SETUP
echo ========================================
echo.
echo This script will automatically set up conditional formatting
echo in your Excel file for automatic strikethrough.
echo.
echo Available options:
echo [1] Use existing file (dynasty_superflex_cheatsheet.xlsx)
echo [2] Choose custom file
echo.

set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Setting up formatting for default file...
    python scripts\auto_setup_formatting.py
    goto end
)

if "%choice%"=="2" (
    echo.
    set /p inputfile="Enter the path to your Excel file: "
    echo Setting up formatting for: %inputfile%
    python scripts\auto_setup_formatting.py "%inputfile%"
    goto end
)

echo Invalid choice. Please run again and choose 1 or 2.
pause
exit /b 1

:end
echo.
echo ========================================
echo  SETUP COMPLETE!
echo ========================================
echo.
echo Your Excel file now has automatic strikethrough formatting!
echo Just type 'X' in the Drafted column and rows will be crossed out.
echo.
echo File saved as: dynasty_superflex_cheatsheet_AUTO_SETUP.xlsx
echo.
pause
