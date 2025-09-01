#!/usr/bin/env python3
"""
Quick test of NFL data enhancement
"""

import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "scripts"))
from core.enhanced_fantasy_tool import EnhancedFantasyTool

# Load fantasy projections and filter out empty rows
fantasy = pd.read_csv("data/offense_projections.csv")
fantasy = fantasy[fantasy["Player"].notna() & (fantasy["Player"] != "\xa0")]
print(f"Loaded {len(fantasy)} valid fantasy players")

# Test with just a few players
test_players = fantasy.head(3)
print("Test players:")
for _, row in test_players.iterrows():
    print(f'  {row["Player"]} ({row["Pos"]})')

# Enhance with NFL data
tool = EnhancedFantasyTool()
enhanced = tool.enhance_projections_with_nfl_data(
    test_players, seasons_to_analyze=[2024]
)

print("\nEnhanced results:")
print("Columns:", enhanced.columns.tolist())
for _, row in enhanced.iterrows():
    games = row.get("nfl_games_played", 0)
    ppr = row.get("nfl_avg_ppr", 0)
    trend = row.get("nfl_trend", "Unknown")
    player_name = row.get("Player", row.get("player", "Unknown"))
    print(f"  {player_name}: {games} games, {ppr:.1f} PPR, {trend}")
