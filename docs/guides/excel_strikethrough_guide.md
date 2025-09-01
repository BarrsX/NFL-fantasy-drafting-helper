# Excel VBA Macro for Auto-Strikethrough in Draft Sheet

# ====================================================

#

# This VBA macro will automatically apply strikethrough formatting to a row

# when you enter "X" in the "Drafted" column of the Draft Board sheet.

#

# How to add this macro to your Excel file:

# =========================================

# 1. Open your generated dynasty_superflex_cheatsheet.xlsx file

# 2. Press Alt+F11 to open the VBA editor

# 3. Insert a new module (Insert > Module)

# 4. Copy and paste the VBA code below

# 5. Save the file as a .xlsm (macro-enabled) workbook

# 6. Enable macros when opening the file

#

# VBA Code:

# =========

Private Sub Worksheet_Change(ByVal Target As Range)
' This macro runs whenever a cell is changed in the Draft Board sheet

    ' Only process changes in the Drafted column (Column I = 9th column)
    If Target.Column = 9 Then
        Application.EnableEvents = False ' Prevent infinite loop

        ' Check if the changed cell contains "X" (case-insensitive)
        If LCase(Trim(Target.Value)) = "x" Then
            ' Apply strikethrough to the entire row (columns A-H)
            With Target.EntireRow.Range("A1:H1").Font
                .Strikethrough = True
                .Color = RGB(128, 128, 128) ' Gray out the text
            End With

            ' Optional: Add a checkmark or other visual indicator
            ' Target.Value = "✓" ' Uncomment to replace X with checkmark

        ElseIf Target.Value = "" Then
            ' Remove strikethrough if cell is cleared
            With Target.EntireRow.Range("A1:H1").Font
                .Strikethrough = False
                .Color = RGB(0, 0, 0) ' Back to black text
            End With
        End If

        Application.EnableEvents = True ' Re-enable events
    End If

End Sub

# Alternative: Simple Conditional Formatting (No VBA Required)

# ===========================================================

#

# If you prefer not to use VBA, you can manually add conditional formatting:

#

# 1. Select the entire Draft Board sheet (Ctrl+A)

# 2. Go to Home > Conditional Formatting > New Rule

# 3. Select "Use a formula to determine which cells to format"

# 4. Enter this formula: =$I2="X"

# 5. Click "Format" and go to the Font tab

# 6. Check "Strikethrough" and optionally change text color to gray

# 7. Click OK to apply

#

# This will automatically strikethrough all cells in a row when column I contains "X"

# Usage Instructions:

# ===================

# 1. During your draft, simply type "X" in the "Drafted" column next to any player

# 2. The entire row will automatically be crossed out

# 3. To undo, just clear the "X" from the cell

# 4. Sort by Draft_Priority to always see the best available players at the top
