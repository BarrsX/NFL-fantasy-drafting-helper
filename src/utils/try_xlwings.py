# Try using xlwings for VBA macro injection
try:
    import xlwings as xw

    print("xlwings is available - creating Excel file with embedded VBA macro...")

    # Create Excel file with VBA macro
    wb = xw.Book()

    # Copy data from our existing file
    import pandas as pd

    df = pd.read_excel(
        "../output/dynasty_superflex_cheatsheet.xlsx", sheet_name="Draft Board"
    )

    # Write data to new workbook
    ws = wb.sheets[0]
    ws.name = "Draft Board"

    # Write headers
    for col, header in enumerate(df.columns, 1):
        ws.cells(1, col).value = header

    # Write data
    for row, data in enumerate(df.values, 2):
        for col, value in enumerate(data, 1):
            ws.cells(row, col).value = value

    # Add VBA macro
    vba_code = """
Private Sub Worksheet_Change(ByVal Target As Range)
    If Target.Column = 9 And Target.Value = "X" Then
        Target.EntireRow.Range("A:H").Font.Strikethrough = True
        Target.EntireRow.Range("A:H").Font.Color = vbGrayText
    ElseIf Target.Column = 9 And Target.Value = "" Then
        Target.EntireRow.Range("A:H").Font.Strikethrough = False
        Target.EntireRow.Range("A:H").Font.Color = vbBlack
    End If
End Sub
"""

    # Inject VBA code
    wb.api.VBProject.VBComponents(ws.name).CodeModule.AddFromString(vba_code)

    # Save as macro-enabled
    wb.save("../output/dynasty_superflex_AUTO_MACRO.xlsm")
    wb.close()

    print("✅ SUCCESS: Excel file with embedded VBA macro created!")
    print("File: dynasty_superflex_AUTO_MACRO.xlsm")
    print("The macro is already embedded - just open and use!")

except ImportError:
    print("❌ xlwings not available")
    print("Falling back to manual VBA approach...")
