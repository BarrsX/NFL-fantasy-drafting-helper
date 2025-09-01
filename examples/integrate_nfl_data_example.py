#!/usr/bin/env python3
"""
Integration Example: Adding NFL Data to Your Fantasy Tool
==========================================================

This shows exactly how to integrate NFL data enhancement into your
existing sleeper_cheatsheet.py without breaking anything.
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Add scripts to path
sys.path.append(str(Path(__file__).parent / "scripts"))

from core.enhanced_fantasy_tool import EnhancedFantasyTool


def integrate_nfl_data_with_existing_tool():
    """
    Example of how to add NFL data enhancement to your existing workflow
    """

    print("🔄 Integrating NFL Data with Fantasy Tool...")

    # Step 1: Load your existing fantasy projections
    # (This is what you already do in your main script)
    fantasy_projections = pd.read_csv("data/offense_projections.csv")
    print(f"📋 Loaded {len(fantasy_projections)} fantasy projections")

    # Step 2: Initialize the NFL enhancement tool
    enhanced_tool = EnhancedFantasyTool()

    # Step 3: Enhance your projections with NFL data
    # This adds new columns: nfl_games_played, nfl_avg_ppr, nfl_trend, etc.
    enhanced_projections = enhanced_tool.enhance_projections_with_nfl_data(
        fantasy_projections, seasons_to_analyze=[2024]  # Use 2024 season data
    )

    # Step 4: Show the enhancement results
    print("\n✨ NFL Data Enhancement Results:")
    print(f"Original columns: {len(fantasy_projections.columns)}")
    print(f"Enhanced columns: {len(enhanced_projections.columns)}")
    print(
        f"New NFL columns added: {len(enhanced_projections.columns) - len(fantasy_projections.columns)}"
    )

    # Show sample of enhanced data
    if not enhanced_projections.empty:
        # Handle different possible column names
        player_col = None
        for col in ["player", "Player", "PLAYER", "name", "Name"]:
            if col in enhanced_projections.columns:
                player_col = col
                break

        if player_col:
            sample_cols = [
                player_col,
                "position",
                "nfl_team",
                "nfl_games_played",
                "nfl_avg_ppr",
                "nfl_trend",
            ]
            available_cols = [
                col for col in sample_cols if col in enhanced_projections.columns
            ]
            print("\n📊 Sample Enhanced Projections:")
            print(enhanced_projections[available_cols].head().to_string(index=False))
        else:
            print("\n📊 Sample Enhanced Projections (showing first 5 rows):")
            print(enhanced_projections.head().to_string(index=False))

    # Step 5: Generate enhanced Excel file (optional)
    output_file = "enhanced_cheatsheet_with_nfl_data.xlsx"
    success = enhanced_tool.generate_enhanced_cheatsheet(
        enhanced_projections, output_file
    )

    if success:
        print(f"\n✅ Enhanced Excel file saved: {output_file}")
        print("📁 Check the file for NFL-enhanced draft insights!")

    return enhanced_projections


def show_nfl_insights(enhanced_projections):
    """
    Show key insights from NFL data integration
    """

    if enhanced_projections.empty or "nfl_avg_ppr" not in enhanced_projections.columns:
        print("❌ No NFL data available for insights")
        return

    print("\n🎯 NFL Data Insights:")

    # Top performers by NFL PPR
    if "nfl_avg_ppr" in enhanced_projections.columns:
        # Find player column name
        player_col = None
        for col in ["player", "Player", "PLAYER", "name", "Name"]:
            if col in enhanced_projections.columns:
                player_col = col
                break

        if player_col:
            top_nfl_performers = enhanced_projections.nlargest(5, "nfl_avg_ppr")
            print("\n🔥 Top NFL Performers (by average PPR):")
            for _, row in top_nfl_performers.iterrows():
                player_name = row[player_col]
                ppr = row.get("nfl_avg_ppr", 0)
                games = row.get("nfl_games_played", 0)
                print(f"  • {player_name}: {ppr:.1f} PPR ({games} games)")
        else:
            print("\n🔥 Top NFL Performers (by average PPR):")
            top_nfl_performers = enhanced_projections.nlargest(5, "nfl_avg_ppr")
            print(
                top_nfl_performers[["nfl_avg_ppr", "nfl_games_played"]].to_string(
                    index=False
                )
            )

    # Trending players
    if "nfl_trend" in enhanced_projections.columns:
        improving = enhanced_projections[
            enhanced_projections["nfl_trend"] == "Improving"
        ]
        if not improving.empty:
            print("\n🚀 Improving Players:")
            for _, row in improving.head(3).iterrows():
                player_name = (
                    row.get(player_col, "Unknown Player")
                    if player_col
                    else "Unknown Player"
                )
                team = row.get("nfl_team", "Unknown")
                games = row.get("nfl_games_played", 0)
                print(f"  • {player_name} ({team}) - {games} games")

    # Value opportunities (high NFL PPR, reasonable ADP)
    if (
        "adp" in enhanced_projections.columns
        and "nfl_avg_ppr" in enhanced_projections.columns
    ):
        value_picks = enhanced_projections[
            (enhanced_projections["nfl_avg_ppr"] > 15)
            & (enhanced_projections["adp"] > 30)
            & (enhanced_projections["nfl_games_played"] >= 10)
        ]
        if not value_picks.empty:
            print("\n💎 Potential Value Picks:")
            for _, row in value_picks.head(3).iterrows():
                player_name = (
                    row.get(player_col, "Unknown Player")
                    if player_col
                    else "Unknown Player"
                )
                ppr = row.get("nfl_avg_ppr", 0)
                adp = row.get("adp", 0)
                print(f"  • {player_name}: {ppr:.1f} PPR (ADP: {adp})")


if __name__ == "__main__":
    try:
        # Run the integration
        enhanced_data = integrate_nfl_data_with_existing_tool()

        # Show insights
        show_nfl_insights(enhanced_data)

        print("\n🎉 NFL Data Integration Complete!")
        print("\n💡 Next Steps:")
        print("1. Review the enhanced Excel file")
        print("2. Compare NFL performance with ADP rankings")
        print("3. Use insights for better draft decisions")
        print("4. Integrate this into your main sleeper_cheatsheet.py")

    except Exception as e:
        print(f"❌ Integration failed: {e}")
        print("Make sure all required packages are installed")
