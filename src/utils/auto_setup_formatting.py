import os
import sys


def setup_excel_formatting():
    """Set up conditional formatting in Excel programmatically"""

    try:
        # Try using win32com for Excel automation
        import win32com.client as win32

        print("Setting up Excel conditional formatting using win32com...")

        # Create Excel application
        excel = win32.gencache.EnsureDispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False

        # Open workbook
        input_file = os.path.join("..", "output", "dynasty_superflex_cheatsheet.xlsx")
        workbook = excel.Workbooks.Open(os.path.abspath(input_file))
        worksheet = workbook.Sheets("Draft Board")

        print("Opened Excel file successfully")

        # Get used range
        used_range = worksheet.UsedRange
        last_row = used_range.Rows.Count

        print(f"Found {last_row} rows of data")

        # Define the range for conditional formatting (A2:H[last_row])
        range_string = f"A2:H{last_row}"
        target_range = worksheet.Range(range_string)

        # Add conditional formatting rule
        # xlExpression = 2
        conditional_format = target_range.FormatConditions.Add(
            2, 0, '=$I2="X"', target_range
        )

        # Set formatting (strikethrough and gray color)
        conditional_format.Font.Strikethrough = True
        conditional_format.Font.Color = 8421504  # Gray

        print("Conditional formatting rule applied")

        # Save with new name
        output_file = os.path.join(
            "..", "output", "dynasty_superflex_cheatsheet_AUTO_SETUP.xlsx"
        )
        workbook.SaveAs(os.path.abspath(output_file))

        print("File saved successfully!")
        print(f"Output: {output_file}")

        # Clean up
        workbook.Close(False)
        excel.Quit()

        return True

    except ImportError:
        print("win32com not available. Trying alternative method...")
        return False

    except Exception as e:
        print(f"Error setting up formatting: {e}")
        return False


if __name__ == "__main__":
    success = setup_excel_formatting()

    if success:
        print("\n✅ SUCCESS! Excel file with automatic strikethrough created!")
        print(
            "Just type 'X' in the Drafted column and rows will be crossed out automatically!"
        )
    else:
        print("\n❌ Could not set up automatic formatting.")
        print("Please use the manual setup instructions in the template file.")
