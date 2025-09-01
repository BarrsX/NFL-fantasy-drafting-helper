# Fantasy Football Draft Strikethrough - Programmatic Solutions

## 🎯 AUTOMATIC STRIKETHROUGH SOLUTIONS

I've created several **programmatic solutions** to automatically set up strikethrough formatting in your Excel files, saving you time from manual setup!

## 🚀 QUICKEST SOLUTION: One-Click Setup

### Option 1: Run the Batch File (Easiest)

```bash
# Just double-click this file:
setup_strikethrough.bat
```

This will automatically set up conditional formatting in your Excel file!

### Option 2: Run the PowerShell Script

```powershell
# Run this in PowerShell:
.\scripts\setup_excel_formatting.ps1
```

## 📁 Available Programmatic Solutions

### 1. **AUTO_SETUP.xlsx** (Recommended)

- **File**: `output/dynasty_superflex_cheatsheet_AUTO_SETUP.xlsx`
- **Method**: Python + win32com (fully automated)
- **Features**: Conditional formatting already applied
- **Usage**: Just open and type "X" in column I!

### 2. **MACRO.xlsm** (For Advanced Users)

- **File**: `output/dynasty_superflex_cheatsheet_MACRO.xlsm`
- **Method**: VBA macro embedded
- **Features**: Fully automatic strikethrough
- **Setup**: Enable macros when opening

### 3. **TEMPLATE.xlsx** (Manual but Guided)

- **File**: `output/dynasty_superflex_cheatsheet_TEMPLATE.xlsx`
- **Method**: Step-by-step instructions included
- **Features**: Clear setup guide in the file itself

## 🛠️ How the Automation Works

The programmatic solutions use:

1. **Python + win32com**: Directly controls Excel to add conditional formatting rules
2. **PowerShell COM**: Uses Excel's COM API for automation
3. **VBA Macros**: Embedded Excel macros for real-time automation

## 🎯 Usage Instructions

1. **Choose your preferred solution** from the files above
2. **Open the Excel file**
3. **Go to the "Draft Board" sheet**
4. **Type "X" in the Drafted column (Column I)**
5. **Watch the entire row get crossed out automatically!** ✅

## 🔧 Technical Details

### Conditional Formatting Rule Applied:

- **Formula**: `=$I2="X"`
- **Range**: `A2:H[last_row]`
- **Format**: Strikethrough + Gray text color
- **Trigger**: Any cell in column I containing "X"

### VBA Macro (Alternative):

```vba
Private Sub Worksheet_Change(ByVal Target As Range)
    If Target.Column = 9 And Target.Value = "X" Then
        Target.EntireRow.Range("A:H").Font.Strikethrough = True
    End If
End Sub
```

## 📋 Files Created

- ✅ `dynasty_superflex_cheatsheet_AUTO_SETUP.xlsx` - Ready to use with formatting
- ✅ `dynasty_superflex_cheatsheet_MACRO.xlsm` - Macro-enabled version
- ✅ `setup_strikethrough.bat` - One-click setup script
- ✅ `scripts/setup_excel_formatting.ps1` - PowerShell automation
- ✅ `docs/draft_board_macro.bas` - VBA code for manual import

## 🎉 Result

**Zero manual setup required!** Just open the AUTO_SETUP file and start drafting with automatic strikethrough functionality.

The programmatic approach saves you **5-10 minutes** of manual Excel configuration each time you want to set up strikethrough formatting! 🚀
