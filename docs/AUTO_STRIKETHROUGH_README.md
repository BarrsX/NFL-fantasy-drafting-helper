# Fantasy Draft Cheat Sheet - Auto Strikethrough Setup

## Quick Start for Future Worksheets

Every time you generate a new cheat sheet with `python scripts/sleeper_cheatsheet.py`, you have two options to add automatic strikethrough:

### Option 1: One-Click Batch File (Recommended)

1. After generating your Excel file, simply run:

   ```batch
   .\apply_formatting.bat
   ```

   This will automatically apply strikethrough formatting to `output/dynasty_superflex_cheatsheet.xlsx`

2. Or drag and drop any Excel file onto `apply_formatting.bat`

### Option 2: PowerShell Script

For more control, run the PowerShell script directly:

```powershell
.\scripts\setup_excel_formatting.ps1 -ExcelFile "output\your_cheatsheet.xlsx"
```

## What the Formatting Does

- **Automatic Strikethrough**: When you type "X" in the "Drafted" column, the entire row (columns A-H) gets crossed out
- **Gray Text**: The crossed-out text appears in gray for better visibility
- **Live Updates**: Works immediately as you draft - no need to refresh or recalculate

## Troubleshooting

If the batch file doesn't work:

1. Make sure Excel is installed on your system
2. Check that the Excel file exists in the output folder
3. Try running the PowerShell script directly

## Making It Fully Automatic

If you want this formatting applied automatically every time you run the main script, let me know and I can integrate it more reliably into the Python code.

## Files Involved

- `apply_formatting.bat` - One-click formatting application
- `scripts/setup_excel_formatting.ps1` - PowerShell script that does the actual work
- `scripts/sleeper_cheatsheet.py` - Main script (tries to apply formatting automatically but falls back gracefully)
