#!/usr/bin/env python3
"""
NFL Data Integration for Fantasy Football
==========================================

This module integrates comprehensive NFL data using nfl-data-py to enhance
fantasy football projections with advanced analytics and historical data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import nfl_data_py as nfl

    NFL_DATA_AVAILABLE = True
except ImportError:
    logger.warning("nfl-data-py not available. Install with: pip install nfl-data-py")
    NFL_DATA_AVAILABLE = False


class NFLDataIntegrator:
    """Integrate NFL data for enhanced fantasy analysis"""

    def __init__(self):
        if not NFL_DATA_AVAILABLE:
            raise ImportError("nfl-data-py is required for NFL data integration")

        self.current_season = datetime.now().year
        self._cache = {}  # Simple caching mechanism

    def get_weekly_data(self, seasons: List[int] = None) -> pd.DataFrame:
        """Fetch weekly NFL player statistics"""
        if seasons is None:
            seasons = [self.current_season]

        cache_key = f"weekly_{'_'.join(map(str, seasons))}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            logger.info(f"Fetching weekly data for seasons: {seasons}")
            weekly_data = nfl.import_weekly_data(seasons)
            self._cache[cache_key] = weekly_data
            return weekly_data
        except Exception as e:
            logger.error(f"Error fetching weekly data: {e}")
            return pd.DataFrame()

    def get_seasonal_data(self, seasons: List[int] = None) -> pd.DataFrame:
        """Fetch seasonal NFL player statistics"""
        if seasons is None:
            seasons = [self.current_season]

        cache_key = f"seasonal_{'_'.join(map(str, seasons))}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            logger.info(f"Fetching seasonal data for seasons: {seasons}")
            seasonal_data = nfl.import_seasonal_data(seasons)
            self._cache[cache_key] = seasonal_data
            return seasonal_data
        except Exception as e:
            logger.error(f"Error fetching seasonal data: {e}")
            return pd.DataFrame()

    def get_roster_data(self, seasons: List[int] = None) -> pd.DataFrame:
        """Fetch NFL roster information"""
        if seasons is None:
            seasons = [self.current_season]

        cache_key = f"rosters_{'_'.join(map(str, seasons))}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            logger.info(f"Fetching roster data for seasons: {seasons}")
            roster_data = nfl.import_seasonal_rosters(seasons)
            self._cache[cache_key] = roster_data
            return roster_data
        except Exception as e:
            logger.error(f"Error fetching roster data: {e}")
            return pd.DataFrame()

    def get_depth_charts(self, seasons: List[int] = None) -> pd.DataFrame:
        """Fetch NFL depth chart information"""
        if seasons is None:
            seasons = [self.current_season]

        cache_key = f"depth_{'_'.join(map(str, seasons))}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            logger.info(f"Fetching depth chart data for seasons: {seasons}")
            depth_data = nfl.import_depth_charts(seasons)
            self._cache[cache_key] = depth_data
            return depth_data
        except Exception as e:
            logger.error(f"Error fetching depth chart data: {e}")
            return pd.DataFrame()

    def get_injuries(self, seasons: List[int] = None) -> pd.DataFrame:
        """Fetch NFL injury data"""
        if seasons is None:
            seasons = [self.current_season]

        cache_key = f"injuries_{'_'.join(map(str, seasons))}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            logger.info(f"Fetching injury data for seasons: {seasons}")
            injury_data = nfl.import_injuries(seasons)
            self._cache[cache_key] = injury_data
            return injury_data
        except Exception as e:
            logger.error(f"Error fetching injury data: {e}")
            return pd.DataFrame()

    def get_pbp_data(self, seasons: List[int] = None) -> pd.DataFrame:
        """Fetch play-by-play data for advanced analytics"""
        if seasons is None:
            seasons = [self.current_season]

        cache_key = f"pbp_{'_'.join(map(str, seasons))}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            logger.info(f"Fetching play-by-play data for seasons: {seasons}")
            pbp_data = nfl.import_pbp_data(seasons)
            self._cache[cache_key] = pbp_data
            return pbp_data
        except Exception as e:
            logger.error(f"Error fetching PBP data: {e}")
            return pd.DataFrame()

    def calculate_advanced_metrics(self, weekly_data: pd.DataFrame) -> pd.DataFrame:
        """Calculate advanced fantasy metrics from weekly data"""
        if weekly_data.empty:
            return pd.DataFrame()

        df = weekly_data.copy()

        # Calculate PPR points
        df["ppr_points"] = (
            df["passing_yards"] * 0.04
            + df["passing_tds"] * 4
            + df["interceptions"] * -2
            + df["rushing_yards"] * 0.1
            + df["rushing_tds"] * 6
            + df["receiving_yards"] * 0.1
            + df["receiving_tds"] * 6
            + df["receptions"] * 0.5
            + (df.get("rushing_fumbles_lost", 0) + df.get("receiving_fumbles_lost", 0))
            * -2
        )

        # Calculate efficiency metrics
        df["pass_completion_pct"] = df["completions"] / df["attempts"] * 100
        df["yds_per_attempt"] = df["passing_yards"] / df["attempts"]
        df["td_per_attempt"] = df["passing_tds"] / df["attempts"]
        df["int_per_attempt"] = df["interceptions"] / df["attempts"]

        # Rushing efficiency
        df["yds_per_carry"] = df["rushing_yards"] / df["carries"]
        df["td_per_carry"] = df["rushing_tds"] / df["carries"]

        # Receiving efficiency
        df["yds_per_reception"] = df["receiving_yards"] / df["receptions"]
        df["td_per_reception"] = df["receiving_tds"] / df["receptions"]

        return df

    def get_player_trends(
        self, player_name: str, seasons: List[int] = None
    ) -> pd.DataFrame:
        """Get performance trends for a specific player"""
        if seasons is None:
            seasons = list(range(self.current_season - 3, self.current_season + 1))

        weekly_data = self.get_weekly_data(seasons)

        if weekly_data.empty:
            return pd.DataFrame()

        # Filter for specific player
        player_data = weekly_data[
            weekly_data["player_display_name"].str.contains(
                player_name, case=False, na=False
            )
        ]

        if player_data.empty:
            return pd.DataFrame()

        # Calculate trends
        player_data = self.calculate_advanced_metrics(player_data)

        return player_data.sort_values(["season", "week"])

    def get_position_stats(
        self, position: str, seasons: List[int] = None
    ) -> pd.DataFrame:
        """Get aggregated statistics by position"""
        if seasons is None:
            seasons = [self.current_season]

        weekly_data = self.get_weekly_data(seasons)

        if weekly_data.empty:
            return pd.DataFrame()

        # Filter by position
        pos_data = weekly_data[weekly_data["position"] == position].copy()

        if pos_data.empty:
            return pd.DataFrame()

        # Calculate advanced metrics
        pos_data = self.calculate_advanced_metrics(pos_data)

        # Aggregate by player
        agg_stats = (
            pos_data.groupby(["player_display_name", "recent_team"])
            .agg(
                {
                    "ppr_points": ["mean", "std", "max", "count"],
                    "passing_yards": "mean",
                    "rushing_yards": "mean",
                    "receiving_yards": "mean",
                    "passing_tds": "sum",
                    "rushing_tds": "sum",
                    "receiving_tds": "sum",
                }
            )
            .round(2)
        )

        # Flatten column names
        agg_stats.columns = ["_".join(col).strip() for col in agg_stats.columns.values]
        agg_stats = agg_stats.reset_index()

        return agg_stats.sort_values("ppr_points_mean", ascending=False)

    def get_team_stats(self, seasons: List[int] = None) -> pd.DataFrame:
        """Get team-level statistics"""
        if seasons is None:
            seasons = [self.current_season]

        weekly_data = self.get_weekly_data(seasons)

        if weekly_data.empty:
            return pd.DataFrame()

        # Group by team and calculate totals
        team_stats = (
            weekly_data.groupby("recent_team")
            .agg(
                {
                    "passing_yards": "sum",
                    "rushing_yards": "sum",
                    "receiving_yards": "sum",
                    "passing_tds": "sum",
                    "rushing_tds": "sum",
                    "receiving_tds": "sum",
                    "interceptions": "sum",
                }
            )
            .round(2)
        )

        # Add fumbles if available
        fumble_cols = [
            "rushing_fumbles_lost",
            "receiving_fumbles_lost",
            "sack_fumbles_lost",
        ]
        available_fumble_cols = [
            col for col in fumble_cols if col in weekly_data.columns
        ]

        if available_fumble_cols:
            fumble_stats = (
                weekly_data.groupby("recent_team")[available_fumble_cols]
                .sum()
                .sum(axis=1)
            )
            team_stats["fumbles_lost"] = fumble_stats
        else:
            team_stats["fumbles_lost"] = 0

        # Calculate team efficiency metrics
        team_stats["total_yards"] = (
            team_stats["passing_yards"]
            + team_stats["rushing_yards"]
            + team_stats["receiving_yards"]
        )

        team_stats["total_tds"] = (
            team_stats["passing_tds"]
            + team_stats["rushing_tds"]
            + team_stats["receiving_tds"]
        )

        team_stats["turnovers"] = (
            team_stats["interceptions"] + team_stats["fumbles_lost"]
        )

        return team_stats.sort_values("total_yards", ascending=False)

    def get_season_projections(self, current_season_data: pd.DataFrame) -> pd.DataFrame:
        """Generate season projections based on current performance"""
        if current_season_data.empty:
            return pd.DataFrame()

        # Group by player and calculate projections
        projections = (
            current_season_data.groupby(["player_display_name", "position"])
            .agg(
                {
                    "ppr_points": "mean",
                    "passing_yards": "mean",
                    "rushing_yards": "mean",
                    "receiving_yards": "mean",
                    "passing_tds": "mean",
                    "rushing_tds": "mean",
                    "receiving_tds": "mean",
                    "receptions": "mean",
                }
            )
            .round(2)
        )

        # Project to full season (assuming 17 games)
        projection_cols = [
            "ppr_points",
            "passing_yards",
            "rushing_yards",
            "receiving_yards",
            "passing_tds",
            "rushing_tds",
            "receiving_tds",
            "receptions",
        ]

        for col in projection_cols:
            if col in projections.columns:
                projections[f"{col}_projected"] = (projections[col] * 17).round(1)

        return projections.reset_index()

    def export_data_summary(self, output_path: str = "nfl_data_summary.xlsx"):
        """Export comprehensive NFL data summary"""
        try:
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                # Get data for current season
                seasons = [self.current_season]

                # Export various datasets
                weekly_data = self.get_weekly_data(seasons)
                if not weekly_data.empty:
                    weekly_data.head(1000).to_excel(
                        writer, sheet_name="Weekly_Sample", index=False
                    )

                seasonal_data = self.get_seasonal_data(seasons)
                if not seasonal_data.empty:
                    seasonal_data.to_excel(
                        writer, sheet_name="Seasonal_Data", index=False
                    )

                roster_data = self.get_roster_data(seasons)
                if not roster_data.empty:
                    roster_data.head(500).to_excel(
                        writer, sheet_name="Roster_Sample", index=False
                    )

                # Position summaries
                for position in ["QB", "RB", "WR", "TE"]:
                    pos_stats = self.get_position_stats(position, seasons)
                    if not pos_stats.empty:
                        pos_stats.head(50).to_excel(
                            writer, sheet_name=f"{position}_Stats", index=False
                        )

                # Team stats
                team_stats = self.get_team_stats(seasons)
                if not team_stats.empty:
                    team_stats.to_excel(writer, sheet_name="Team_Stats", index=False)

            logger.info(f"NFL data summary exported to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting data summary: {e}")
            return False


def integrate_with_fantasy_projections(
    nfl_integrator: NFLDataIntegrator, fantasy_projections: pd.DataFrame
) -> pd.DataFrame:
    """Integrate NFL data insights with fantasy projections"""

    if fantasy_projections.empty:
        return pd.DataFrame()

    enhanced_projections = fantasy_projections.copy()

    # Get current season NFL data
    current_season = datetime.now().year
    weekly_data = nfl_integrator.get_weekly_data([current_season])

    if weekly_data.empty:
        logger.warning("No NFL weekly data available for enhancement")
        return enhanced_projections

    # Calculate advanced metrics
    weekly_data = nfl_integrator.calculate_advanced_metrics(weekly_data)

    # Merge with fantasy projections
    # This is a simplified example - in practice, you'd need proper name matching
    enhanced_projections["nfl_games_played"] = 0
    enhanced_projections["nfl_avg_ppr"] = 0.0
    enhanced_projections["nfl_trend"] = "Unknown"

    # For each player in fantasy projections, find NFL data
    for idx, row in enhanced_projections.iterrows():
        player_name = row.get("player", "").lower()

        # Find matching NFL player (simplified matching)
        nfl_player = weekly_data[
            weekly_data["player_display_name"]
            .str.lower()
            .str.contains(player_name.split()[0], na=False)
        ]

        if not nfl_player.empty:
            # Get player's season stats
            player_stats = (
                nfl_player.groupby("player_display_name")
                .agg({"ppr_points": ["mean", "count"], "week": "max"})
                .round(2)
            )

            if not player_stats.empty:
                avg_ppr = player_stats["ppr_points"]["mean"].iloc[0]
                games_played = player_stats["ppr_points"]["count"].iloc[0]

                enhanced_projections.at[idx, "nfl_games_played"] = games_played
                enhanced_projections.at[idx, "nfl_avg_ppr"] = avg_ppr

                # Simple trend analysis
                if games_played >= 5:
                    if avg_ppr > 15:
                        enhanced_projections.at[idx, "nfl_trend"] = "Hot"
                    elif avg_ppr < 8:
                        enhanced_projections.at[idx, "nfl_trend"] = "Cold"
                    else:
                        enhanced_projections.at[idx, "nfl_trend"] = "Steady"

    return enhanced_projections


# Example usage and testing
if __name__ == "__main__":
    try:
        integrator = NFLDataIntegrator()

        print("🔄 Fetching NFL data...")

        # Test basic data retrieval
        weekly_data = integrator.get_weekly_data([2024])
        print(f"✅ Weekly data: {len(weekly_data)} records")

        seasonal_data = integrator.get_seasonal_data([2024])
        print(f"✅ Seasonal data: {len(seasonal_data)} records")

        roster_data = integrator.get_roster_data([2024])
        print(f"✅ Roster data: {len(roster_data)} records")

        # Test advanced analytics
        if not weekly_data.empty:
            print("\n📊 Calculating advanced metrics...")
            advanced_data = integrator.calculate_advanced_metrics(weekly_data)
            print(f"✅ Advanced metrics calculated for {len(advanced_data)} records")

            # Test position analysis
            qb_stats = integrator.get_position_stats("QB", [2024])
            if not qb_stats.empty:
                print(f"✅ QB stats: {len(qb_stats)} players")
                print("Top 5 QBs by average PPR:")
                print(
                    qb_stats[["player_display_name", "ppr_points_mean"]]
                    .head()
                    .to_string(index=False)
                )

        # Export sample data
        print("\n💾 Exporting data summary...")
        success = integrator.export_data_summary("nfl_data_summary.xlsx")
        if success:
            print("✅ Data summary exported to nfl_data_summary.xlsx")

        print("\n🎯 NFL Data Integration Complete!")
        print("Available data types:")
        print("- Weekly player statistics")
        print("- Seasonal aggregations")
        print("- Roster information")
        print("- Depth charts")
        print("- Injury reports")
        print("- Advanced metrics and projections")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure nfl-data-py is installed: pip install nfl-data-py")
