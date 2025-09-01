import pandas as pd

# Load the data files to check for other name variations
adp_df = pd.read_csv("../data/sleeper_adp.csv")
offense_df = pd.read_csv("../data/offense_projections.csv")
idp_df = pd.read_csv("../data/idp_projections.csv")

print("ADP data sample:")
print(adp_df.head())

print("\nOffense projections sample:")
print(offense_df.head())

print("\nIDP projections sample:")
print(idp_df.head())

# Check for common name variations
print("\nChecking for other name variations...")

# Look for players with apostrophes, periods, or other special characters
special_chars = []
for df, name in [(adp_df, "ADP"), (offense_df, "Offense"), (idp_df, "IDP")]:
    if "Player" in df.columns:
        for player in df["Player"].dropna():
            if any(char in player for char in ["'", ".", "-", "III", "IV", "V"]):
                special_chars.append((player, name))

if special_chars:
    print("Players with special characters:")
    for player, source in special_chars[:10]:
        print(f"  {player} ({source})")
else:
    print("No special characters found in player names.")
