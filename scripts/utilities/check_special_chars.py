import pandas as pd

# Check ADP status of players with special characters
excel_df = pd.read_excel(
    "../output/dynasty_superflex_cheatsheet.xlsx", sheet_name="Overall"
)

special_char_players = [
    "Ja'Marr Chase",
    "A.J. Brown",
    "Amon-Ra St. Brown",
    "TreVeyon Henderson",
    "DeVonta Smith",
    "D'Andre Swift",
    "C.J. Stroud",
    "T.J. Hockenson",
    "Jaxon Smith-Njigba",
    "De'Von Achane",
]

print("ADP status for players with special characters:")
print("=" * 60)
for player in special_char_players:
    player_data = excel_df[
        excel_df["Player"].str.contains(player, na=False, case=False)
    ]
    if not player_data.empty:
        row = player_data.iloc[0]
        print(
            f'{row["Player"]:<25} - ADP: {row["adp"]:<3} Priority: {row["Draft_Priority"]:.1f}'
        )
    else:
        print(f"{player:<25} - Not found")
