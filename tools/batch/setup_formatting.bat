@echo off
echo Setting up automatic strikethrough formatting in Excel...
echo.

REM Run the PowerShell script to set up conditional formatting
powershell.exe -ExecutionPolicy Bypass -File "setup_excel_formatting.ps1"

echo.
echo If the PowerShell script worked, your Excel file now has automatic strikethrough!
echo File: ..\output\dynasty_superflex_cheatsheet_AUTO_FORMATTED.xlsx
echo.
echo Just type 'X' in column I and watch the row get crossed out automatically!
echo.
pause
