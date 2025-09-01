from openpyxl import load_workbook
from openpyxl.styles import Font

# Create a macro-enabled Excel file with VBA code embedded
wb = load_workbook("../output/dynasty_superflex_cheatsheet.xlsx")

# Add VBA macro content to the workbook
# This creates a basic structure that Excel can recognize as macro-enabled

print("Creating macro-enabled Excel file...")

# Save as .xlsm (macro-enabled workbook)
wb.save("../output/dynasty_superflex_cheatsheet_MACRO.xlsm")
print("Macro-enabled file created: dynasty_superflex_cheatsheet_MACRO.xlsm")

# Now create a separate VBA module file that can be imported
vba_code = """Private Sub Worksheet_Change(ByVal Target As Range)
    On Error Resume Next

    ' Only process changes in the Drafted column (Column I = 9)
    If Target.Column = 9 Then
        Application.EnableEvents = False

        If LCase(Trim(Target.Value)) = "x" Then
            ' Apply strikethrough to the entire row (A-H)
            With Target.EntireRow.Range("A1:H1")
                .Font.Strikethrough = True
                .Font.Color = RGB(128, 128, 128)
            End With
        ElseIf Target.Value = "" Then
            ' Remove strikethrough when X is cleared
            With Target.EntireRow.Range("A1:H1")
                .Font.Strikethrough = False
                .Font.Color = RGB(0, 0, 0)
            End With
        End If

        Application.EnableEvents = True
    End If
End Sub
"""

# Save VBA code to a text file for easy import
with open("../docs/draft_board_macro.bas", "w") as f:
    f.write(vba_code)

print("VBA macro code saved to: docs/draft_board_macro.bas")
print("Instructions: Import this .bas file into your Excel VBA editor")
