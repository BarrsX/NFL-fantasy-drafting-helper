#!/usr/bin/env python3
"""
NFL Data Integration Demo
=========================

This script demonstrates how to integrate NFL data with your existing
fantasy drafting tool for enhanced projections and analysis.
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Add the scripts directory to the path
sys.path.append(str(Path(__file__).parent / "scripts"))

from core.enhanced_fantasy_tool import EnhancedFantasyTool
from core.nfl_data_integration import NFLDataIntegrator


def demo_nfl_integration():
    """Demonstrate NFL data integration capabilities"""

    print("🏈 NFL Data Integration Demo")
    print("=" * 50)

    try:
        # Initialize the enhanced tool
        enhanced_tool = EnhancedFantasyTool()
        nfl_integrator = NFLDataIntegrator()

        print("\n📊 Fetching NFL Data...")

        # Get current season data
        weekly_data = nfl_integrator.get_weekly_data([2024])
        seasonal_data = nfl_integrator.get_seasonal_data([2024])
        roster_data = nfl_integrator.get_roster_data([2024])

        print(f"✅ Weekly Data: {len(weekly_data):,} records")
        print(f"✅ Seasonal Data: {len(seasonal_data):,} records")
        print(f"✅ Roster Data: {len(roster_data):,} records")

        # Demonstrate advanced analytics
        print("\n📈 Advanced Analytics Demo")

        if not weekly_data.empty:
            # Calculate advanced metrics
            advanced_data = nfl_integrator.calculate_advanced_metrics(weekly_data)
            print("✅ Advanced metrics calculated")

            # Show top performers
            show_top_performers(advanced_data)

            # Show position analysis
            show_position_analysis(nfl_integrator)

        # Demonstrate team analysis
        show_team_analysis(nfl_integrator)

        # Show how to integrate with fantasy projections
        demo_fantasy_integration(enhanced_tool)

        print("\n🎯 Demo Complete!")
        print("\nTo integrate with your fantasy tool:")
        print("1. Import: from core.enhanced_fantasy_tool import EnhancedFantasyTool")
        print("2. Initialize: tool = EnhancedFantasyTool()")
        print(
            "3. Enhance: enhanced_projections = tool.enhance_projections_with_nfl_data(your_data)"
        )
        print("4. Generate: tool.generate_enhanced_cheatsheet(enhanced_projections)")

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure nfl-data-py is installed: pip install nfl-data-py")


def show_top_performers(advanced_data: pd.DataFrame):
    """Show top performers by position"""

    print("\n🔥 Top Performers by Position (2024)")

    positions = ["QB", "RB", "WR", "TE"]
    metrics = {
        "QB": "passing_yards",
        "RB": "rushing_yards",
        "WR": "receiving_yards",
        "TE": "receiving_yards",
    }

    for position in positions:
        pos_data = advanced_data[advanced_data["position"] == position]
        if not pos_data.empty:
            metric = metrics[position]
            top_players = (
                pos_data.groupby("player_display_name")[metric].sum().nlargest(3)
            )

            print(f"\n{position} - Top by {metric.replace('_', ' ').title()}:")
            for i, (name, value) in enumerate(top_players.items(), 1):
                print("2d")


def show_position_analysis(nfl_integrator: NFLDataIntegrator):
    """Show position-specific analysis"""

    print("\n📊 Position Analysis (2024)")

    for position in ["QB", "RB", "WR", "TE"]:
        pos_stats = nfl_integrator.get_position_stats(position, [2024])

        if not pos_stats.empty:
            avg_ppr = pos_stats["ppr_points_mean"].mean()
            top_player = pos_stats.iloc[0]["player_display_name"]
            top_ppr = pos_stats.iloc[0]["ppr_points_mean"]

            print("15" "2.1f" "15")


def show_team_analysis(nfl_integrator: NFLDataIntegrator):
    """Show team performance analysis"""

    print("\n🏟️  Team Performance Analysis (2024)")

    team_stats = nfl_integrator.get_team_stats([2024])

    if not team_stats.empty:
        # Top offensive teams
        top_offense = team_stats.nlargest(3, "total_yards")
        print("\nTop 3 Teams by Total Yards:")
        for i, (team, row) in enumerate(top_offense.iterrows(), 1):
            print("2d" "4.0f" "2.0f")

        # Teams with fewest turnovers (use interceptions as proxy)
        if "interceptions" in team_stats.columns:
            best_to = team_stats.nsmallest(3, "interceptions")
            print("\nMost Ball-Secure Teams (by Interceptions):")
            for i, (team, row) in enumerate(best_to.iterrows(), 1):
                print("2d")
        else:
            print("\nTurnover data not available")


def demo_fantasy_integration(enhanced_tool: EnhancedFantasyTool):
    """Demonstrate integration with fantasy projections"""

    print("\n🎯 Fantasy Integration Demo")

    # Create sample fantasy projection data
    sample_projections = pd.DataFrame(
        {
            "player": [
                "Josh Allen",
                "Lamar Jackson",
                "Patrick Mahomes",
                "Christian McCaffrey",
                "Austin Ekeler",
                "Derrick Henry",
                "Tyreek Hill",
                "Davante Adams",
                "Stefon Diggs",
                "Travis Kelce",
                "Mark Andrews",
                "George Kittle",
            ],
            "position": [
                "QB",
                "QB",
                "QB",
                "RB",
                "RB",
                "RB",
                "WR",
                "WR",
                "WR",
                "TE",
                "TE",
                "TE",
            ],
            "team": [
                "BUF",
                "BAL",
                "KC",
                "SF",
                "LAC",
                "TEN",
                "MIA",
                "LV",
                "HOU",
                "KC",
                "BAL",
                "SF",
            ],
            "adp": [12, 15, 18, 8, 22, 35, 5, 28, 32, 10, 45, 38],
        }
    )

    print(f"📋 Sample fantasy projections: {len(sample_projections)} players")

    # Enhance with NFL data (use 2024 data since 2025 doesn't exist yet)
    enhanced_projections = enhanced_tool.enhance_projections_with_nfl_data(
        sample_projections, seasons_to_analyze=[2024]  # Use 2024 data instead of 2025
    )

    print("\n✨ Enhanced Projections Preview:")
    if (
        not enhanced_projections.empty
        and "nfl_games_played" in enhanced_projections.columns
    ):
        preview_cols = [
            "player",
            "position",
            "nfl_games_played",
            "nfl_avg_ppr",
            "nfl_trend",
        ]
        print(enhanced_projections[preview_cols].head(8).to_string(index=False))
    else:
        print("NFL data enhancement failed - showing original projections:")
        print(sample_projections.head(8).to_string(index=False))

    # Generate recommendations
    recommendations = enhanced_tool.get_draft_recommendations(enhanced_projections)

    print("\n🎯 Top Draft Recommendations:")
    top_recs = recommendations.head(5)
    for i, row in top_recs.iterrows():
        print("2d" "2.1f" "10")


def create_integration_example():
    """Create an example of how to integrate with existing fantasy tool"""

    integration_code = '''
# Example: Integrating NFL Data with Your Fantasy Tool

from core.enhanced_fantasy_tool import EnhancedFantasyTool
from core.nfl_data_integration import NFLDataIntegrator

def enhance_existing_cheatsheet():
    """Enhance your existing fantasy cheatsheet with NFL data"""

    # Initialize enhanced tool
    enhanced_tool = EnhancedFantasyTool()

    # Your existing fantasy projections (load from your current system)
    fantasy_projections = pd.read_csv("data/offense_projections.csv")

    # Enhance with NFL data
    enhanced_projections = enhanced_tool.enhance_projections_with_nfl_data(
        fantasy_projections,
        seasons_to_analyze=[2023, 2024]  # Analyze multiple seasons
    )

    # Generate enhanced Excel file
    enhanced_tool.generate_enhanced_cheatsheet(
        enhanced_projections,
        "enhanced_fantasy_cheatsheet.xlsx"
    )

    print("Enhanced cheatsheet created with NFL data insights!")

if __name__ == "__main__":
    enhance_existing_cheatsheet()
'''

    with open("nfl_integration_example.py", "w") as f:
        f.write(integration_code)

    print("\n📝 Integration example saved to: nfl_integration_example.py")


if __name__ == "__main__":
    demo_nfl_integration()
    create_integration_example()
