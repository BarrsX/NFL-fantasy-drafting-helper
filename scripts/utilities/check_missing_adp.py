import pandas as pd

# Check column names in the Excel file
excel_df = pd.read_excel(
    "../output/dynasty_superflex_cheatsheet.xlsx", sheet_name="Overall"
)

print("Available columns:")
for col in excel_df.columns:
    print(f"  {col}")

print(f"\nTotal rows: {len(excel_df)}")

# Check for players with ADP 999 (missing ADP)
missing_adp = excel_df[excel_df["adp"] == 999]

print(f"\nPlayers with missing ADP (total: {len(missing_adp)}):")
for _, row in missing_adp.head(10).iterrows():
    print(f'{row["Player"]:<25} - Points: {row["Points"]:.1f}')
