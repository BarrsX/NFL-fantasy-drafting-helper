# MANUAL STRIKETHROUGH SETUP GUIDE

# ================================

#

# Since automatic conditional formatting isn't working with your Excel version,

# here's the MANUAL approach that works in ALL Excel versions:

#

# STEP-BY-STEP INSTRUCTIONS:

# ==========================

#

# 1. Open your Excel file: dynasty_superflex_cheatsheet.xlsx

# 2. Go to the "Draft Board" sheet

# 3. Select the entire data range (columns A:H, from row 2 to the end)

# 4. Go to: Home > Conditional Formatting > New Rule

# 5. Select: "Use a formula to determine which cells to format"

# 6. Enter this EXACT formula: =$I2="X"

# 7. Click the "Format" button

# 8. Go to the "Font" tab

# 9. Check the "Strikethrough" checkbox

# 10. Optional: Change font color to gray (Color dropdown)

# 11. Click OK twice

#

# That's it! Now any row with "X" in column I will be automatically crossed out.

#

# TROUBLESHOOTING:

# ================

#

# If it doesn't work:

# 1. Make sure you're selecting the correct range (A:H)

# 2. Make sure the formula is exactly: =$I2="X" (dollar sign before I, no spaces)

# 3. Make sure column I is the "Drafted" column

# 4. Try applying to a smaller range first (like A2:H10) to test

#

# ALTERNATIVE: QUICK MANUAL METHOD

# ================================

#

# If conditional formatting is too complex:

# 1. Type "X" in the Drafted column

# 2. Select the entire row (click the row number)

# 3. Right-click > Format Cells > Font tab > Strikethrough

# 4. This manually crosses out the row

#

# VBA MACRO ALTERNATIVE:

# ======================

#

# For fully automatic strikethrough, you can add this VBA macro:

#

# 1. Press Alt+F11 to open VBA editor

# 2. Find "Draft Board" in the left panel (under Microsoft Excel Objects)

# 3. Double-click it to open the code window

# 4. Paste this code:

#

# Private Sub Worksheet_Change(ByVal Target As Range)

# If Target.Column = 9 And Target.Value = "X" Then

# Target.EntireRow.Range("A:H").Font.Strikethrough = True

# ElseIf Target.Column = 9 And Target.Value = "" Then

# Target.EntireRow.Range("A:H").Font.Strikethrough = False

# End If

# End Sub

#

# 5. Save and enable macros when opening the file
