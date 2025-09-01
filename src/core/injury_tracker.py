#!/usr/bin/env python3
"""
Injury Impact Tracker for Fantasy Football
==========================================

This module tracks player injuries and analyzes their impact on fantasy projections.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional


class InjuryTracker:
    """Track and analyze player injuries"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def get_espn_injuries(self) -> pd.DataFrame:
        """Fetch injury data from ESPN"""
        url = "https://site.api.espn.com/apis/fantasy/v2/games/ffl/news/injuries"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            injuries = []
            for item in data.get("injuries", []):
                player = item.get("player", {})
                injury = item.get("injury", {})

                injuries.append(
                    {
                        "player_id": player.get("id"),
                        "player_name": player.get("fullName"),
                        "team": player.get("proTeamAbbreviation"),
                        "position": player.get("defaultPosition"),
                        "injury_status": injury.get("status"),
                        "injury_type": injury.get("type"),
                        "injury_description": injury.get("description"),
                        "last_updated": injury.get("lastUpdated"),
                        "expected_return": injury.get("expectedReturn"),
                    }
                )

            return pd.DataFrame(injuries)

        except requests.RequestException as e:
            print(f"ESPN injury API error: {e}")
            return pd.DataFrame()

    def get_rotoworld_injuries(self) -> pd.DataFrame:
        """Fetch injury data from Rotoworld (web scraping approach)"""
        # Note: This would require web scraping implementation
        # For now, return empty DataFrame
        return pd.DataFrame()

    def analyze_injury_impact(
        self, injuries_df: pd.DataFrame, projections_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Analyze how injuries affect player projections"""

        # Define injury status impact multipliers
        status_impact = {
            "Out": 0.0,  # Player completely out
            "Doubtful": 0.2,  # Major doubt
            "Questionable": 0.5,  # 50/50 chance
            "Probable": 0.9,  # Likely to play
            "Healthy": 1.0,  # No impact
        }

        # Merge injury data with projections
        merged_df = projections_df.merge(
            injuries_df,
            left_on=["player", "team"],
            right_on=["player_name", "team"],
            how="left",
        )

        # Apply injury adjustments
        for idx, row in merged_df.iterrows():
            status = row.get("injury_status", "Healthy")

            if pd.isna(status):
                status = "Healthy"

            impact_multiplier = status_impact.get(status, 1.0)

            # Apply to relevant projection columns
            projection_cols = [
                "pass_yd",
                "pass_td",
                "rush_yd",
                "rush_td",
                "rec_yd",
                "rec_td",
                "rec",
                "fumbles_lost",
            ]

            for col in projection_cols:
                if col in merged_df.columns and not pd.isna(row.get(col)):
                    original_value = row[col]
                    adjusted_value = original_value * impact_multiplier
                    merged_df.at[idx, f"{col}_adjusted"] = adjusted_value
                    merged_df.at[idx, f"{col}_injury_impact"] = (
                        original_value - adjusted_value
                    )

        return merged_df

    def get_injury_trends(
        self, injuries_df: pd.DataFrame, historical_days: int = 30
    ) -> pd.DataFrame:
        """Analyze injury trends by team and position"""

        if injuries_df.empty:
            return pd.DataFrame()

        # Convert timestamps
        injuries_df["last_updated"] = pd.to_datetime(
            injuries_df["last_updated"], unit="ms", errors="coerce"
        )

        # Filter recent injuries
        cutoff_date = datetime.now() - timedelta(days=historical_days)
        recent_injuries = injuries_df[injuries_df["last_updated"] >= cutoff_date]

        # Group by team and position
        trends = (
            recent_injuries.groupby(["team", "position"])
            .agg(
                {"player_name": "count", "injury_status": lambda x: (x == "Out").sum()}
            )
            .reset_index()
        )

        trends.columns = ["team", "position", "total_injuries", "out_count"]

        return trends


def generate_injury_report(
    injuries_df: pd.DataFrame, projections_df: pd.DataFrame
) -> str:
    """Generate a formatted injury impact report"""

    if injuries_df.empty:
        return "No injury data available"

    tracker = InjuryTracker()
    impact_df = tracker.analyze_injury_impact(injuries_df, projections_df)

    # Create summary
    total_injuries = len(injuries_df)
    out_count = len(injuries_df[injuries_df["injury_status"] == "Out"])
    doubtful_count = len(injuries_df[injuries_df["injury_status"] == "Doubtful"])

    report = f"""
🏥 FANTASY INJURY REPORT
========================

📊 Injury Summary:
• Total Injuries: {total_injuries}
• Players Out: {out_count}
• Doubtful: {doubtful_count}

🚨 Critical Injuries (Out/Doubtful):
"""

    critical_injuries = injuries_df[
        injuries_df["injury_status"].isin(["Out", "Doubtful"])
    ]

    for _, injury in critical_injuries.iterrows():
        report += f"• {injury['player_name']} ({injury['team']} {injury['position']}) - {injury['injury_status']}\n"
        if injury.get("injury_description"):
            report += f"  └─ {injury['injury_description']}\n"

    # Add projection impacts
    if not impact_df.empty:
        report += "\n💰 Projection Impacts:\n"
        for _, row in impact_df.iterrows():
            if row.get("injury_status") in ["Out", "Doubtful"]:
                player_name = row.get("player_name", row.get("player", "Unknown"))
                status = row.get("injury_status", "Unknown")
                report += f"• {player_name}: {status}\n"

    return report


# Example usage
if __name__ == "__main__":
    tracker = InjuryTracker()

    # Fetch current injuries
    injuries = tracker.get_espn_injuries()

    if not injuries.empty:
        print(f"Found {len(injuries)} injury reports")

        # Show sample data
        print("\nSample injury data:")
        print(injuries[["player_name", "team", "position", "injury_status"]].head())

        # Generate trends
        trends = tracker.get_injury_trends(injuries)
        if not trends.empty:
            print("\nInjury trends by team:")
            print(trends.head())

    else:
        print("No injury data retrieved")
        print("ESPN injury API may be rate-limited or unavailable")
