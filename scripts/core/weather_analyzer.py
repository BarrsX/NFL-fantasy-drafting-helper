#!/usr/bin/env python3
"""
Weather Impact Analysis for Fantasy Football
============================================

This module analyzes weather conditions and their impact on fantasy projections.
Cold/windy weather particularly affects QB and WR performance.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List


class WeatherAnalyzer:
    """Analyze weather impact on fantasy football projections"""

    def __init__(self, api_key: str = None):
        """
        Initialize with OpenWeatherMap API key
        Get free API key at: https://openweathermap.org/api
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_game_weather(self, city: str, date: str = None) -> Dict:
        """Get weather forecast for game location"""
        if not self.api_key:
            return {"error": "API key required"}

        endpoint = f"{self.base_url}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial",
            "cnt": 40,  # 5 day forecast
        }

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def analyze_weather_impact(self, weather_data: Dict) -> Dict:
        """Analyze weather conditions and their fantasy impact"""
        if "error" in weather_data:
            return weather_data

        # Extract relevant weather metrics
        forecasts = weather_data.get("list", [])

        # Find game-time forecast (assuming Sunday afternoon games)
        game_forecast = None
        for forecast in forecasts:
            dt = datetime.fromtimestamp(forecast["dt"])
            # Look for Sunday afternoon (game time around 1-4 PM)
            if dt.weekday() == 6 and 13 <= dt.hour <= 16:  # Sunday 1-4 PM
                game_forecast = forecast
                break

        if not game_forecast:
            # Fallback to first Sunday forecast
            for forecast in forecasts:
                dt = datetime.fromtimestamp(forecast["dt"])
                if dt.weekday() == 6:
                    game_forecast = forecast
                    break

        if not game_forecast:
            return {"error": "No suitable forecast found"}

        # Extract weather conditions
        main = game_forecast.get("main", {})
        wind = game_forecast.get("wind", {})
        weather = game_forecast.get("weather", [{}])[0]

        temp = main.get("temp", 70)
        wind_speed = wind.get("speed", 0)
        conditions = weather.get("main", "Clear")

        # Calculate fantasy impact scores
        impact = {
            "temperature": temp,
            "wind_speed": wind_speed,
            "conditions": conditions,
            "qb_impact": self._calculate_qb_impact(temp, wind_speed, conditions),
            "wr_impact": self._calculate_wr_impact(temp, wind_speed, conditions),
            "rb_impact": self._calculate_rb_impact(temp, wind_speed, conditions),
            "te_impact": self._calculate_te_impact(temp, wind_speed, conditions),
        }

        return impact

    def _calculate_qb_impact(self, temp: float, wind: float, conditions: str) -> float:
        """Calculate QB performance impact (-1.0 to 1.0)"""
        impact = 0.0

        # Temperature impact
        if temp < 40:
            impact -= 0.3  # Cold weather hurts QB accuracy
        elif temp > 80:
            impact -= 0.1  # Hot weather reduces performance

        # Wind impact
        if wind > 15:
            impact -= 0.4  # High winds hurt passing
        elif wind > 10:
            impact -= 0.2

        # Precipitation impact
        if conditions in ["Rain", "Snow", "Thunderstorm"]:
            impact -= 0.2

        return max(-1.0, min(1.0, impact))

    def _calculate_wr_impact(self, temp: float, wind: float, conditions: str) -> float:
        """Calculate WR performance impact"""
        impact = 0.0

        # Wind is biggest factor for WRs
        if wind > 15:
            impact -= 0.5  # High winds severely hurt WR production
        elif wind > 10:
            impact -= 0.3

        # Cold weather also hurts
        if temp < 50:
            impact -= 0.2

        # Rain hurts ball security
        if conditions == "Rain":
            impact -= 0.2

        return max(-1.0, min(1.0, impact))

    def _calculate_rb_impact(self, temp: float, wind: float, conditions: str) -> float:
        """Calculate RB performance impact"""
        impact = 0.0

        # RBs benefit from bad weather (less passing)
        if wind > 15:
            impact += 0.2
        elif wind > 10:
            impact += 0.1

        # Cold weather can help RBs
        if temp < 50:
            impact += 0.1

        return max(-1.0, min(1.0, impact))

    def _calculate_te_impact(self, temp: float, wind: float, conditions: str) -> float:
        """Calculate TE performance impact"""
        # TEs are less affected by weather than WRs/QBs
        impact = (
            self._calculate_qb_impact(temp, wind, conditions)
            + self._calculate_wr_impact(temp, wind, conditions)
        ) * 0.3
        return max(-1.0, min(1.0, impact))

    def get_nfl_weather_schedule(self) -> Dict[str, str]:
        """Get NFL team cities for weather lookup"""
        return {
            "ARI": "Phoenix,AZ",
            "ATL": "Atlanta,GA",
            "BAL": "Baltimore,MD",
            "BUF": "Buffalo,NY",
            "CAR": "Charlotte,NC",
            "CHI": "Chicago,IL",
            "CIN": "Cincinnati,OH",
            "CLE": "Cleveland,OH",
            "DAL": "Dallas,TX",
            "DEN": "Denver,CO",
            "DET": "Detroit,MI",
            "GB": "Green Bay,WI",
            "HOU": "Houston,TX",
            "IND": "Indianapolis,IN",
            "JAX": "Jacksonville,FL",
            "KC": "Kansas City,MO",
            "LAC": "Los Angeles,CA",
            "LAR": "Los Angeles,CA",
            "LV": "Las Vegas,NV",
            "MIA": "Miami,FL",
            "MIN": "Minneapolis,MN",
            "NE": "Foxborough,MA",
            "NO": "New Orleans,LA",
            "NYG": "East Rutherford,NJ",
            "NYJ": "East Rutherford,NJ",
            "PHI": "Philadelphia,PA",
            "PIT": "Pittsburgh,PA",
            "SEA": "Seattle,WA",
            "SF": "Santa Clara,CA",
            "TB": "Tampa,FL",
            "TEN": "Nashville,TN",
            "WAS": "Washington,DC",
        }


def apply_weather_adjustments(
    projections_df: pd.DataFrame, weather_analyzer: WeatherAnalyzer, team_city_map: Dict
) -> pd.DataFrame:
    """Apply weather-based adjustments to fantasy projections"""

    adjusted_df = projections_df.copy()

    # Add weather impact columns
    for position in ["QB", "RB", "WR", "TE"]:
        adjusted_df[f"{position}_weather_impact"] = 0.0

    # Process each player's team
    for idx, row in adjusted_df.iterrows():
        team = row.get("team")
        position = row.get("position")

        if team in team_city_map and position in ["QB", "RB", "WR", "TE"]:
            city = team_city_map[team]

            # Get weather data
            weather_data = weather_analyzer.get_game_weather(city)
            if "error" not in weather_data:
                impact_analysis = weather_analyzer.analyze_weather_impact(weather_data)

                # Apply position-specific adjustment
                impact_key = f"{position.lower()}_impact"
                if impact_key in impact_analysis:
                    impact = impact_analysis[impact_key]

                    # Store the impact
                    adjusted_df.at[idx, f"{position}_weather_impact"] = impact

                    # Apply to projections (example: adjust passing/receiving yards)
                    if position == "QB":
                        # Adjust passing yards by impact percentage
                        if "pass_yd" in adjusted_df.columns:
                            adjusted_df.at[idx, "pass_yd"] *= 1 + impact * 0.1
                    elif position == "WR":
                        if "rec_yd" in adjusted_df.columns:
                            adjusted_df.at[idx, "rec_yd"] *= 1 + impact * 0.15

    return adjusted_df


# Example usage
if __name__ == "__main__":
    # Initialize weather analyzer
    analyzer = WeatherAnalyzer()

    # Test with a sample city
    weather = analyzer.get_game_weather("Green Bay,WI")
    if "error" not in weather:
        impact = analyzer.analyze_weather_impact(weather)
        print("Weather Impact Analysis:")
        print(json.dumps(impact, indent=2))
    else:
        print(f"Weather API Error: {weather['error']}")
        print("To use weather features:")
        print("1. Get free API key from https://openweathermap.org/api")
        print("2. Set OPENWEATHER_API_KEY environment variable")
        print("3. Or pass api_key parameter to WeatherAnalyzer()")
