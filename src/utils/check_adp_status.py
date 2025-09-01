import pandas as pd

# Check current status of these players
excel_df = pd.read_excel(
    "../output/dynasty_superflex_cheatsheet.xlsx", sheet_name="Overall"
)

test_players = ["Marvin Harrison", "Kyle Pitts", "Patrick Mahomes", "Deebo Samuel"]

print("Current ADP status:")
for player in test_players:
    player_data = excel_df[
        excel_df["Player"].str.contains(player, na=False, case=False)
    ]
    if not player_data.empty:
        row = player_data.iloc[0]
        print(
            f'{row["Player"]:<20} - ADP: {row["adp"]:<3} Priority: {row["Draft_Priority"]:.1f}'
        )
    else:
        print(f"{player:<20} - Not found")
