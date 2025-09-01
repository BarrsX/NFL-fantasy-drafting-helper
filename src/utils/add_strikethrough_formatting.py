import pandas as pd
from openpyxl import load_workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Font

# Load the workbook
wb = load_workbook("../output/dynasty_superflex_cheatsheet.xlsx")
ws = wb["Draft Board"]

# Add conditional formatting for strikethrough
strikethrough_rule = FormulaRule(
    formula=['$I2="X"'], font=Font(strikethrough=True, color="808080")
)

# Apply to columns A-H
for col in ["A", "B", "C", "D", "E", "F", "G", "H"]:
    ws.conditional_formatting.add(f"{col}2:{col}1500", strikethrough_rule)

# Save the workbook
wb.save("../output/dynasty_superflex_cheatsheet_with_strikethrough.xlsx")
print("✅ Added conditional formatting to Excel file!")
print("📁 New file saved as: dynasty_superflex_cheatsheet_with_strikethrough.xlsx")
print('🎯 Now try entering "X" in the Drafted column - rows should auto-strikethrough!')
