#!/usr/bin/env python3
"""
Enhanced Fantasy Draft Tool with NFL Data Integration
======================================================

This module demonstrates how to integrate NFL data with your existing
fantasy drafting tool for enhanced projections and analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from datetime import datetime

from nfl_data_integration import NFLDataIntegrator

# Optional imports - only import if available
try:
    from weather_analyzer import WeatherAnalyzer

    WEATHER_AVAILABLE = True
except ImportError:
    WEATHER_AVAILABLE = False
    WeatherAnalyzer = None

try:
    from injury_tracker import InjuryTracker

    INJURY_AVAILABLE = True
except ImportError:
    INJURY_AVAILABLE = False
    InjuryTracker = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedFantasyTool:
    """Enhanced fantasy drafting tool with NFL data integration"""

    def __init__(self):
        self.nfl_integrator = NFLDataIntegrator()
        self.weather_analyzer = WeatherAnalyzer() if WEATHER_AVAILABLE else None
        self.injury_tracker = InjuryTracker() if INJURY_AVAILABLE else None
        # Use multiple seasons for better analysis (2022-2024)
        self.current_season = 2024
        self.analysis_seasons = [2022, 2023, 2024]

    def enhance_projections_with_nfl_data(
        self, fantasy_projections: pd.DataFrame, seasons_to_analyze: List[int] = None
    ) -> pd.DataFrame:
        """Enhance fantasy projections with NFL data insights"""

        if seasons_to_analyze is None:
            seasons_to_analyze = (
                self.analysis_seasons
            )  # Use multiple seasons by default

        logger.info("🔄 Enhancing projections with NFL data...")

        enhanced_projections = fantasy_projections.copy()

        # Get NFL data
        weekly_data = self.nfl_integrator.get_weekly_data(seasons_to_analyze)
        seasonal_data = self.nfl_integrator.get_seasonal_data(seasons_to_analyze)
        roster_data = self.nfl_integrator.get_roster_data(seasons_to_analyze)

        if weekly_data.empty:
            logger.warning("No NFL weekly data available")
            return enhanced_projections

        # Calculate advanced metrics
        weekly_data = self.nfl_integrator.calculate_advanced_metrics(weekly_data)

        # Add NFL performance columns
        enhanced_projections["nfl_games_played"] = 0
        enhanced_projections["nfl_avg_ppr"] = 0.0
        enhanced_projections["nfl_trend"] = "Unknown"
        enhanced_projections["nfl_consistency_score"] = 0.0
        enhanced_projections["nfl_volume_trend"] = "Unknown"
        enhanced_projections["nfl_team"] = "Unknown"

        # Process each player
        for idx, row in enhanced_projections.iterrows():
            # Try different possible column names for player
            player_name = ""
            for col_name in ["player", "Player", "name", "Name"]:
                if col_name in row and pd.notna(row[col_name]):
                    player_name = str(row[col_name]).lower().strip()
                    break

            if not player_name:
                continue

            # Find matching NFL player data
            nfl_matches = self._find_player_matches(player_name, weekly_data)

            if not nfl_matches.empty:
                player_stats = self._calculate_player_stats(nfl_matches, roster_data)

                # Update enhanced projections
                enhanced_projections.at[idx, "nfl_games_played"] = player_stats[
                    "games_played"
                ]
                enhanced_projections.at[idx, "nfl_avg_ppr"] = player_stats["avg_ppr"]
                enhanced_projections.at[idx, "nfl_trend"] = player_stats["trend"]
                enhanced_projections.at[idx, "nfl_consistency_score"] = player_stats[
                    "consistency"
                ]
                enhanced_projections.at[idx, "nfl_volume_trend"] = player_stats[
                    "volume_trend"
                ]
                enhanced_projections.at[idx, "nfl_team"] = player_stats["team"]

        logger.info("✅ NFL data enhancement complete")
        return enhanced_projections

    def _find_player_matches(
        self, player_name: str, weekly_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Find NFL player data matching fantasy player name"""

        # Clean and normalize the player name
        player_name = str(player_name).lower().strip()

        # Remove common suffixes that might differ
        suffixes = [" jr.", " sr.", " ii", " iii", " iv", " v"]
        clean_name = player_name
        for suffix in suffixes:
            clean_name = clean_name.replace(suffix, "")

        # Split name for better matching
        name_parts = clean_name.split()
        if not name_parts:
            return pd.DataFrame()

        first_name = name_parts[0]
        last_name = name_parts[-1] if len(name_parts) > 1 else ""

        # Try multiple matching strategies
        matches = pd.DataFrame()

        # Strategy 1: Exact match on display name (after cleaning)
        cleaned_display_names = weekly_data["player_display_name"].str.lower()
        for suffix in suffixes:
            cleaned_display_names = cleaned_display_names.str.replace(
                suffix, "", regex=False
            )

        exact_matches = weekly_data[
            cleaned_display_names.str.strip() == clean_name.strip()
        ]
        if not exact_matches.empty:
            matches = exact_matches
        else:
            # Strategy 2: Match on last name + first initial
            if last_name and first_name:
                initial = first_name[0]
                pattern = f"{last_name}, {initial}"
                initial_matches = weekly_data[
                    weekly_data["player_display_name"]
                    .str.lower()
                    .str.contains(pattern.lower(), na=False)
                ]
                if not initial_matches.empty:
                    matches = initial_matches
                else:
                    # Strategy 3: Partial match on last name only
                    last_name_matches = weekly_data[
                        weekly_data["player_display_name"]
                        .str.lower()
                        .str.contains(last_name.lower(), na=False)
                    ]
                    if not last_name_matches.empty:
                        # Filter to most likely matches (prefer exact last name matches)
                        last_name_matches = last_name_matches[
                            last_name_matches["player_display_name"]
                            .str.lower()
                            .str.contains(f"^{last_name}", na=False)
                        ]
                        if not last_name_matches.empty:
                            matches = last_name_matches

        # Remove duplicates by player_id if available
        if not matches.empty and "player_id" in matches.columns:
            matches = matches.drop_duplicates(subset=["player_id", "season", "week"])
        elif not matches.empty:
            matches = matches.drop_duplicates(
                subset=["player_display_name", "season", "week"]
            )

        return matches

    def _calculate_player_stats(
        self, player_data: pd.DataFrame, roster_data: pd.DataFrame = None
    ) -> Dict:
        """Calculate comprehensive player statistics"""

        if player_data.empty:
            return {
                "games_played": 0,
                "avg_ppr": 0.0,
                "trend": "Unknown",
                "consistency": 0.0,
                "volume_trend": "Unknown",
                "team": "Unknown",
            }

        # Basic stats - count unique games per season
        # Group by season and week to count actual games played
        if (
            not player_data.empty
            and "season" in player_data.columns
            and "week" in player_data.columns
        ):
            games_played = player_data.groupby(["season", "week"]).size().count()
        else:
            games_played = len(player_data)

        # Use the correct PPR column name
        ppr_col = (
            "ppr_points"
            if "ppr_points" in player_data.columns
            else "fantasy_points_ppr"
        )
        avg_ppr = player_data[ppr_col].mean() if ppr_col in player_data.columns else 0.0

        # Trend analysis (recent vs earlier performance)
        if games_played >= 4:
            midpoint = games_played // 2
            early_games = player_data.iloc[:midpoint][ppr_col].mean()
            late_games = player_data.iloc[midpoint:][ppr_col].mean()

            if late_games > early_games * 1.2:
                trend = "Improving"
            elif late_games < early_games * 0.8:
                trend = "Declining"
            else:
                trend = "Steady"
        else:
            trend = "Too Few Games"

        # Consistency score (lower std dev = more consistent)
        ppr_std = player_data[ppr_col].std()
        consistency = max(0, 10 - ppr_std) if not pd.isna(ppr_std) else 5.0

        # Volume trend analysis
        if "position" in player_data.columns:
            position = player_data["position"].iloc[0]

            if position == "QB":
                volume_metric = "attempts"
                volume_trend = self._analyze_volume_trend(player_data, volume_metric)
            elif position in ["RB", "WR", "TE"]:
                volume_metric = (
                    "targets" if "targets" in player_data.columns else "receptions"
                )
                volume_trend = self._analyze_volume_trend(player_data, volume_metric)
            else:
                volume_trend = "N/A"
        else:
            volume_trend = "Unknown"

        # Extract team information
        team = "Unknown"
        if roster_data is not None and not roster_data.empty:
            # Try to find player in roster data
            player_id = (
                player_data["player_id"].iloc[0]
                if "player_id" in player_data.columns
                else None
            )
            if player_id:
                player_roster = roster_data[roster_data["player_id"] == player_id]
                if not player_roster.empty and "team" in player_roster.columns:
                    team = player_roster["team"].iloc[0]

        return {
            "games_played": games_played,
            "avg_ppr": round(avg_ppr, 2),
            "trend": trend,
            "consistency": round(consistency, 2),
            "volume_trend": volume_trend,
            "team": team,
        }

    def _analyze_volume_trend(
        self, player_data: pd.DataFrame, volume_column: str
    ) -> str:
        """Analyze if player's volume is trending up or down"""

        if volume_column not in player_data.columns:
            return "Unknown"

        volume_data = player_data[volume_column].dropna()
        if len(volume_data) < 4:
            return "Too Few Games"

        midpoint = len(volume_data) // 2
        early_volume = volume_data.iloc[:midpoint].mean()
        late_volume = volume_data.iloc[midpoint:].mean()

        if pd.isna(early_volume) or pd.isna(late_volume):
            return "Unknown"

        ratio = late_volume / early_volume if early_volume > 0 else 1

        if ratio > 1.15:
            return "Increasing"
        elif ratio < 0.85:
            return "Decreasing"
        else:
            return "Stable"

    def generate_enhanced_cheatsheet(
        self,
        fantasy_projections: pd.DataFrame,
        output_path: str = "enhanced_cheatsheet.xlsx",
    ) -> bool:
        """Generate enhanced cheatsheet with NFL data insights"""

        try:
            # Enhance projections
            enhanced_data = self.enhance_projections_with_nfl_data(fantasy_projections)

            # Add weather and injury data if available
            enhanced_data = self._add_weather_data(enhanced_data)
            enhanced_data = self._add_injury_data(enhanced_data)

            # Create multiple sheets
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

                # Overall enhanced projections
                enhanced_data.to_excel(
                    writer, sheet_name="Enhanced_Overall", index=False
                )

                # Position-specific analysis
                for position in ["QB", "RB", "WR", "TE"]:
                    pos_data = enhanced_data[
                        enhanced_data.get("position") == position
                    ].copy()
                    if not pos_data.empty:
                        # Sort by NFL performance insights
                        pos_data = pos_data.sort_values(
                            ["nfl_avg_ppr", "nfl_games_played"],
                            ascending=[False, False],
                        )
                        pos_data.to_excel(
                            writer, sheet_name=f"{position}_Analysis", index=False
                        )

                # Trending players
                trending_up = enhanced_data[
                    (enhanced_data["nfl_trend"] == "Improving")
                    & (enhanced_data["nfl_games_played"] >= 5)
                ].sort_values("nfl_avg_ppr", ascending=False)

                if not trending_up.empty:
                    trending_up.to_excel(writer, sheet_name="Trending_Up", index=False)

                # Value picks (high NFL performance, lower ADP)
                if "adp" in enhanced_data.columns:
                    value_picks = enhanced_data[
                        (enhanced_data["nfl_avg_ppr"] > 12)
                        & (enhanced_data["adp"] > 50)
                        & (enhanced_data["nfl_games_played"] >= 5)
                    ].sort_values("nfl_avg_ppr", ascending=False)

                    if not value_picks.empty:
                        value_picks.to_excel(
                            writer, sheet_name="Value_Picks", index=False
                        )

            logger.info(f"✅ Enhanced cheatsheet saved to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error generating enhanced cheatsheet: {e}")
            # Try to save basic version if advanced fails
            try:
                enhanced_data.to_excel(output_path, index=False)
                logger.info(f"✅ Basic enhanced cheatsheet saved to {output_path}")
                return True
            except Exception as e2:
                logger.error(f"Failed to save even basic version: {e2}")
                return False

    def _add_weather_data(self, projections: pd.DataFrame) -> pd.DataFrame:
        """Add weather impact analysis"""
        try:
            # This would integrate with weather data
            # For now, just add placeholder columns
            projections["weather_impact"] = "Unknown"
            projections["game_conditions"] = "Unknown"
            return projections
        except Exception as e:
            logger.warning(f"Weather data integration failed: {e}")
            return projections

    def _add_injury_data(self, projections: pd.DataFrame) -> pd.DataFrame:
        """Add injury impact analysis"""
        try:
            # This would integrate with injury data
            # For now, just add placeholder columns
            projections["injury_status"] = "Unknown"
            projections["injury_impact"] = 0.0
            return projections
        except Exception as e:
            logger.warning(f"Injury data integration failed: {e}")
            return projections

    def get_draft_recommendations(
        self, enhanced_projections: pd.DataFrame
    ) -> pd.DataFrame:
        """Generate draft recommendations based on NFL data insights"""

        recommendations = enhanced_projections.copy()

        # Calculate recommendation score
        recommendations["recommendation_score"] = 0.0

        for idx, row in recommendations.iterrows():
            score = 0

            # NFL performance (40% weight)
            nfl_ppr = row.get("nfl_avg_ppr", 0)
            if nfl_ppr > 20:
                score += 40
            elif nfl_ppr > 15:
                score += 30
            elif nfl_ppr > 10:
                score += 20
            elif nfl_ppr > 5:
                score += 10

            # Trend (30% weight)
            trend = row.get("nfl_trend", "")
            if trend == "Improving":
                score += 30
            elif trend == "Steady":
                score += 20
            elif trend == "Declining":
                score += 5

            # Consistency (20% weight)
            consistency = row.get("nfl_consistency_score", 5)
            score += consistency * 2

            # Games played (10% weight)
            games = row.get("nfl_games_played", 0)
            if games >= 10:
                score += 10
            elif games >= 5:
                score += 5

            recommendations.at[idx, "recommendation_score"] = score

        # Sort by recommendation score
        recommendations = recommendations.sort_values(
            "recommendation_score", ascending=False
        )

        return recommendations


# Example usage
if __name__ == "__main__":
    try:
        tool = EnhancedFantasyTool()

        print("🏈 Enhanced Fantasy Draft Tool with NFL Data Integration")
        print("=" * 60)

        # Test NFL data integration
        print("\n📊 Testing NFL Data Integration...")

        # Get some sample NFL data
        weekly_data = tool.nfl_integrator.get_weekly_data([2024])
        if not weekly_data.empty:
            print(f"✅ NFL Weekly Data: {len(weekly_data)} records")

            # Show top QB performances
            qb_data = weekly_data[weekly_data["position"] == "QB"]
            if not qb_data.empty:
                top_qbs = (
                    qb_data.groupby("player_display_name")["passing_yards"]
                    .sum()
                    .nlargest(5)
                )
                print("\n🔥 Top 5 QBs by Passing Yards (2024):")
                for name, yards in top_qbs.items():
                    print("2d")

        # Test enhanced projections (would need actual fantasy data)
        print("\n📈 NFL Data Integration Features:")
        print("✅ Advanced player performance metrics")
        print("✅ Trend analysis (improving/declining)")
        print("✅ Consistency scoring")
        print("✅ Volume trend analysis")
        print("✅ Position-specific insights")
        print("✅ Value pick identification")
        print("✅ Draft recommendation scoring")

        print("\n🎯 Ready to enhance your fantasy projections!")
        print("Use: enhanced_tool.enhance_projections_with_nfl_data(your_projections)")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure all required packages are installed")
