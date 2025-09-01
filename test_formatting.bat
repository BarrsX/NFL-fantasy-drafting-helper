@echo off
echo ========================================
echo Test Strikethrough Formatting
echo ========================================
echo.
echo This will test if the strikethrough formatting is working in your Excel file.
echo.

if not exist "output\dynasty_superflex_cheatsheet.xlsx" (
    echo ❌ ERROR: Excel file not found at output\dynasty_superflex_cheatsheet.xlsx
    echo.
    echo Please run generate_cheatsheet.bat first, then apply_formatting.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Excel file found!
echo.
echo 📋 To test the strikethrough formatting:
echo.
echo 1. Open: output\dynasty_superflex_cheatsheet.xlsx
echo 2. Go to the "Draft Board" sheet
echo 3. Find the "Drafted" column (Column I)
echo 4. Type "X" in any cell in that column
echo 5. The entire row should automatically get crossed out with gray text
echo.
echo 🎯 If it works: Great! The formatting is applied correctly.
echo ❌ If it doesn't work: Run apply_formatting.bat again
echo.
echo 💡 Pro tip: You can also drag and drop the Excel file onto apply_formatting.bat
echo    to reapply the formatting if needed.
echo.

pause
