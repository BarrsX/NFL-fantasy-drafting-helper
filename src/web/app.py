#!/usr/bin/env python3
"""
Fantasy Drafting Web Dashboard
===============================

Web-based dashboard for fantasy football drafting with the same features as the Excel spreadsheet.
"""

import os
import sys
import json
import time
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import gzip
import functools
from functools import lru_cache
import threading
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Configure Flask for better performance
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  # Minify JSON responses
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300  # Cache static files for 5 minutes

# Global variables to store processed data
processed_data = {
    "overall": None,
    "by_position": {},
    "draft_board": None,
    "config": None,
}

# Cache management
data_cache = {
    "timestamp": None,
    "ttl": 300,  # 5 minutes cache TTL
    "file_hashes": {},  # Track file modification times
}

# Thread lock for data processing
data_lock = threading.Lock()


def get_file_hash(filepath):
    """Get file modification time as a simple hash"""
    try:
        return os.path.getmtime(filepath)
    except:
        return None


def gzip_response(f):
    """Decorator to gzip API responses"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        if isinstance(response, Response) and response.status_code == 200:
            # Check if client accepts gzip
            accept_encoding = request.headers.get('Accept-Encoding', '')
            if 'gzip' in accept_encoding:
                response.data = gzip.compress(response.data)
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Vary'] = 'Accept-Encoding'
        return response
    return wrapper


def is_cache_valid():
    """Check if cached data is still valid"""
    if data_cache["timestamp"] is None:
        return False
    
    # Check TTL
    if time.time() - data_cache["timestamp"] > data_cache["ttl"]:
        return False
    
    # Check if source files have changed
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    config_file = os.path.join(os.path.dirname(__file__), "..", "configs", "config_redraft.json")
    
    files_to_check = [
        os.path.join(data_dir, "offense_projections.csv"),
        os.path.join(data_dir, "sleeper_adp.csv"),
        config_file
    ]
    
    for filepath in files_to_check:
        if os.path.exists(filepath):
            current_hash = get_file_hash(filepath)
            if data_cache["file_hashes"].get(filepath) != current_hash:
                return False
    
    return True


def clean_dataframe_for_json(df):
    """Clean DataFrame to ensure it's JSON serializable"""
    if df is None or df.empty:
        return df

    # Replace NaN values with None (becomes null in JSON)
    df = df.replace({np.nan: None})

    # Also replace inf/-inf values
    df = df.replace({np.inf: None, -np.inf: None})

    # Ensure all object columns are strings or None
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).replace("nan", None).replace("None", None)

    return df


def update_cache_timestamp():
    """Update cache timestamp and file hashes"""
    data_cache["timestamp"] = time.time()
    
    # Update file hashes
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    config_file = os.path.join(os.path.dirname(__file__), "..", "..", "config", "config_redraft.json")
    
    files_to_check = [
        os.path.join(data_dir, "offense_projections.csv"),
        os.path.join(data_dir, "sleeper_adp.csv"),
        config_file
    ]
    
    for filepath in files_to_check:
        if os.path.exists(filepath):
            data_cache["file_hashes"][filepath] = get_file_hash(filepath)


def load_config(
    config_file="../../config/config_redraft.json", config_name="redraft_12team"
):
    """Load configuration from JSON file"""
    try:
        with open(config_file, "r") as f:
            config_data = json.load(f)
        return config_data.get(config_name, config_data)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}


def load_csv_data(filepath):
    """Load CSV data with error handling"""
    try:
        df = pd.read_csv(filepath)
        # Remove empty rows - check for empty strings and NaN values
        df = df.dropna(subset=["Player"]).reset_index(drop=True)
        # Also remove rows where Player is empty string
        df = df[df["Player"].str.strip() != ""].reset_index(drop=True)
        return df
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return pd.DataFrame()


def process_data_for_web():
    """Process fantasy data for web display with caching"""
    with data_lock:
        # Check cache validity
        if is_cache_valid() and processed_data["overall"] is not None:
            print("✅ Using cached data")
            return True
        
        print("🔄 Processing data for web dashboard...")
        
        try:
            # Load configuration
            cfg = load_config()
            processed_data["config"] = cfg

            # Get scoring configuration
            scoring_config = cfg.get("scoring", {}).get("offense", {})

            # Load basic data files
            data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")

            # Load ADP data
            adp_file = os.path.join(data_dir, "sleeper_adp.csv")
            adp = load_csv_data(adp_file)
            if not adp.empty:
                # Standardize ADP columns - handle actual CSV column names
                adp.columns = adp.columns.str.lower()
                player_cols = [
                    col for col in adp.columns if "player" in col or "name" in col
                ]
                if player_cols:
                    adp = adp.rename(columns={player_cols[0]: "player"})

                # Handle ADP column - might be "overall rank" or similar
                if "adp" not in adp.columns:
                    adp_cols = [
                        col for col in adp.columns if "overall" in col and "rank" in col
                    ]
                    if adp_cols:
                        adp = adp.rename(columns={adp_cols[0]: "adp"})
                    else:
                        # Look for any rank or pick column
                        rank_cols = [
                            col for col in adp.columns if "rank" in col or "pick" in col
                        ]
                        if rank_cols:
                            adp = adp.rename(columns={rank_cols[0]: "adp"})

                # Ensure ADP column is numeric
                if "adp" in adp.columns:
                    adp["adp"] = pd.to_numeric(adp["adp"], errors="coerce")

            # Load projection data
            proj_file = os.path.join(data_dir, "offense_projections.csv")
            projections = load_csv_data(proj_file)

            if projections.empty:
                print("❌ No projection data found")
                return False

            # Clean numeric columns that have commas
            numeric_cols = ["YDS", "FPTS", "YDS.1"]
            for col in numeric_cols:
                if col in projections.columns:
                    projections[col] = (
                        projections[col]
                        .astype(str)
                        .str.replace(",", "")
                        .replace("nan", "0")
                    )
                    projections[col] = pd.to_numeric(
                        projections[col], errors="coerce"
                    ).fillna(0)

            # Standardize projection columns - handle actual CSV column names
            projections.columns = projections.columns.str.lower()
            player_cols = [
                col for col in projections.columns if "player" in col or "name" in col
            ]
            if player_cols:
                projections = projections.rename(columns={player_cols[0]: "player"})

            # Handle position column
            if "position" not in projections.columns:
                pos_cols = [col for col in projections.columns if "pos" in col]
                if pos_cols:
                    projections = projections.rename(columns={pos_cols[0]: "position"})

            # Use existing FPTS if available, otherwise calculate
            if "fpts" in projections.columns:
                projections = projections.rename(columns={"fpts": "points"})
                # Ensure points is numeric
                projections["points"] = pd.to_numeric(
                    projections["points"], errors="coerce"
                ).fillna(0)
            elif "points" not in projections.columns:
                # Calculate points from available stats
                projections["points"] = 0.0

                # Ensure all stat columns are numeric before calculations
                stat_columns = [
                    "yds",
                    "tds",
                    "ints",
                    "yds.1",
                    "tds.1",
                    "rec",
                    "yds.2",
                    "tds.2",
                ]
                for col in stat_columns:
                    if col in projections.columns:
                        projections[col] = pd.to_numeric(
                            projections[col], errors="coerce"
                        ).fillna(0)

                # QB scoring - use config values
                if "yds" in projections.columns:  # passing yards
                    projections.loc[
                        projections["position"] == "QB", "points"
                    ] += projections["yds"] * scoring_config.get("pass_yd", 0.04)
                if "tds" in projections.columns:  # passing TDs
                    projections.loc[
                        projections["position"] == "QB", "points"
                    ] += projections["tds"] * scoring_config.get("pass_td", 4.0)
                if "ints" in projections.columns:  # interceptions
                    projections.loc[
                        projections["position"] == "QB", "points"
                    ] += projections["ints"] * scoring_config.get("pass_int", -2.0)

                # RB/WR/TE scoring - use config values
                for pos in ["RB", "WR", "TE"]:
                    if "yds.1" in projections.columns:  # rushing yards
                        projections.loc[
                            projections["position"] == pos, "points"
                        ] += projections["yds.1"] * scoring_config.get("rush_yd", 0.1)
                    if "tds.1" in projections.columns:  # rushing TDs
                        projections.loc[
                            projections["position"] == pos, "points"
                        ] += projections["tds.1"] * scoring_config.get("rush_td", 6.0)
                    if "rec" in projections.columns:  # receptions
                        projections.loc[
                            projections["position"] == pos, "points"
                        ] += projections["rec"] * scoring_config.get("rec", 1.0)
                    if "yds.2" in projections.columns:  # receiving yards
                        projections.loc[
                            projections["position"] == pos, "points"
                        ] += projections["yds.2"] * scoring_config.get("rec_yd", 0.1)
                    if "tds.2" in projections.columns:  # receiving TDs
                        projections.loc[
                            projections["position"] == pos, "points"
                        ] += projections["tds.2"] * scoring_config.get("rec_td", 6.0)

            # Merge with ADP if available
            if not adp.empty and "player" in adp.columns and "adp" in adp.columns:
                # Ensure ADP column is numeric
                adp["adp"] = pd.to_numeric(adp["adp"], errors="coerce")
                projections = projections.merge(
                    adp[["player", "adp"]], on="player", how="left"
                )
                projections["adp"] = projections["adp"].fillna(999)
            else:
                projections["adp"] = 999

            # Clean any remaining NaN values in projections
            projections = clean_dataframe_for_json(projections)

            # Ensure points column is numeric before any calculations
            projections["points"] = pd.to_numeric(
                projections["points"], errors="coerce"
            ).fillna(0)

            # Sort by points and add rankings
            projections = projections.sort_values("points", ascending=False).reset_index(
                drop=True
            )
            projections["rank"] = range(1, len(projections) + 1)
            projections["draft_value"] = ""

            # Ensure both rank and adp are numeric before calculations
            projections["rank"] = pd.to_numeric(projections["rank"], errors="coerce")
            projections["adp"] = pd.to_numeric(projections["adp"], errors="coerce").fillna(
                999
            )

            projections["adp_diff"] = projections["rank"] - projections["adp"]

            # Add value indicators
            projections.loc[projections["adp_diff"] >= 20, "draft_value"] = "STEAL"
            projections.loc[
                (projections["adp_diff"] >= 10) & (projections["adp_diff"] < 20),
                "draft_value",
            ] = "VALUE"
            projections.loc[projections["adp_diff"] <= -15, "draft_value"] = "REACH"

            # Add tier (simple tiering based on rank)
            projections["tier"] = 1
            projections.loc[projections["rank"] > 12, "tier"] = 2
            projections.loc[projections["rank"] > 24, "tier"] = 3
            projections.loc[projections["rank"] > 36, "tier"] = 4
            projections.loc[projections["rank"] > 48, "tier"] = 5

            # Add VORP (Value Over Replacement Player)
            # VORP = projected points - replacement level points

            # Ensure points column is numeric before quantile calculations
            projections["points"] = pd.to_numeric(
                projections["points"], errors="coerce"
            ).fillna(0)

            replacement_points = {
                "QB": (
                    projections[projections["position"] == "QB"]["points"].quantile(0.75)
                    if len(projections[projections["position"] == "QB"]) > 0
                    else 0
                ),
                "RB": (
                    projections[projections["position"] == "RB"]["points"].quantile(0.75)
                    if len(projections[projections["position"] == "RB"]) > 0
                    else 0
                ),
                "WR": (
                    projections[projections["position"] == "WR"]["points"].quantile(0.75)
                    if len(projections[projections["position"] == "WR"]) > 0
                    else 0
                ),
                "TE": (
                    projections[projections["position"] == "TE"]["points"].quantile(0.75)
                    if len(projections[projections["position"] == "TE"]) > 0
                    else 0
                ),
            }

            projections["vorp"] = projections.apply(
                lambda row: row["points"] - replacement_points.get(row["position"], 0),
                axis=1,
            )

            # Create position-adjusted overall rankings (sort by VORP instead of raw points)
            projections_vorp_sorted = projections.sort_values(
                "vorp", ascending=False
            ).reset_index(drop=True)
            projections_vorp_sorted["rank"] = range(1, len(projections_vorp_sorted) + 1)

            # Update tier based on VORP ranking
            projections_vorp_sorted["tier"] = 1
            projections_vorp_sorted.loc[projections_vorp_sorted["rank"] > 12, "tier"] = 2
            projections_vorp_sorted.loc[projections_vorp_sorted["rank"] > 24, "tier"] = 3
            projections_vorp_sorted.loc[projections_vorp_sorted["rank"] > 36, "tier"] = 4
            projections_vorp_sorted.loc[projections_vorp_sorted["rank"] > 48, "tier"] = 5

            # Store processed data with correct column names for frontend
            # The JavaScript expects lowercase property names, so we need to keep original names
            column_mapping = {
                "rank": "Rank",
                "tier": "Tier",
                "draft_value": "Draft_Value",
                "adp_diff": "ADP_Diff",
                "vorp": "VORP",
            }

            projections_for_frontend = projections_vorp_sorted.copy()

            # Add drafted status to overall dataframe
            projections_for_frontend["drafted"] = False

            # Rename only the specific columns that need capitalization
            for old_col, new_col in column_mapping.items():
                if old_col in projections_for_frontend.columns:
                    projections_for_frontend = projections_for_frontend.rename(
                        columns={old_col: new_col}
                    )

            # Keep these as lowercase to match JavaScript expectations
            # player, position, points, adp, team should stay lowercase

            # Create position-specific dataframes
            by_pos = {}
            for pos in ["QB", "RB", "WR", "TE"]:
                pos_df = projections[projections["position"] == pos].copy()
                if not pos_df.empty:
                    pos_df["pos_rank"] = range(1, len(pos_df) + 1)
                    pos_df["drafted"] = False

                    # Apply same column mapping for position data
                    pos_df_for_frontend = pos_df.copy()
                    for old_col, new_col in column_mapping.items():
                        if old_col in pos_df_for_frontend.columns:
                            pos_df_for_frontend = pos_df_for_frontend.rename(
                                columns={old_col: new_col}
                            )

                    pos_df_for_frontend["Pos_Rank"] = range(1, len(pos_df_for_frontend) + 1)
                    by_pos[pos] = pos_df_for_frontend

            # Create draft board (simplified view) - use VORP-sorted data
            draft_board = projections_vorp_sorted[
                ["rank", "player", "position", "points", "adp", "vorp", "draft_value"]
            ].copy()
            draft_board.columns = [
                "Proj_Rank",
                "Player",
                "Pos",
                "Points",
                "ADP",
                "VORP",
                "Value",
            ]

            # Calculate position scarcity based on league settings
            league_settings = cfg.get("league", {})
            num_teams = league_settings.get("num_teams", 12)
            starters = league_settings.get("starters", {})

            # Calculate total roster spots per position
            position_capacity = {}
            for pos in ["QB", "RB", "WR", "TE"]:
                starters_count = starters.get(pos, 1)
                bench_factor = league_settings.get("bench_factor", {}).get(pos, 0.5)
                total_spots = int(num_teams * (starters_count + bench_factor))

                # In superflex leagues, QBs can also be used in FLEX positions
                if pos == "QB" and league_settings.get("superflex", False):
                    flex_count = starters.get("FLEX", 1)
                    superflex_count = starters.get("SUPERFLEX", 1)
                    # QBs can fill FLEX + SUPERFLEX spots
                    total_spots += int(num_teams * (flex_count + superflex_count))

                position_capacity[pos] = total_spots

            # Add position scarcity score (higher = more scarce)
            draft_board["Pos_Scarcity"] = (
                draft_board["Pos"].map(position_capacity).fillna(20)
            )
            draft_board["Pos_Scarcity"] = (
                draft_board["Pos_Scarcity"] / draft_board["Pos_Scarcity"].max()
            )

            # Calculate composite draft priority
            # Normalize ADP and projection rank to 0-100 scale (lower rank/ADP = higher score)
            max_adp = draft_board[draft_board["ADP"] < 999]["ADP"].max()
            draft_board["ADP_Score"] = draft_board.apply(
                lambda row: 100 * (1 - row["ADP"] / max_adp) if row["ADP"] < 999 else 0,
                axis=1,
            )

            max_proj_rank = draft_board["Proj_Rank"].max()
            draft_board["Proj_Score"] = 100 * (1 - draft_board["Proj_Rank"] / max_proj_rank)

            # VORP bonus (normalize to 0-20 scale)
            max_vorp = draft_board["VORP"].max()
            min_vorp = draft_board["VORP"].min()
            draft_board["VORP_Bonus"] = (
                20 * (draft_board["VORP"] - min_vorp) / (max_vorp - min_vorp)
                if max_vorp > min_vorp
                else 0
            )

            # Composite priority score (weighted combination)
            # Weights: ADP (40%), Projections (40%), Position Scarcity (10%), VORP (10%)
            draft_board["Priority"] = (
                draft_board["ADP_Score"] * 0.4
                + draft_board["Proj_Score"] * 0.4
                + draft_board["Pos_Scarcity"] * 10  # Scale scarcity to 0-10
                + draft_board["VORP_Bonus"]
            )

            # Handle cases where ADP is 999 (no ADP data) - reduce priority
            draft_board.loc[draft_board["ADP"] == 999, "Priority"] *= 0.5

            draft_board["Drafted"] = ""
            draft_board["Round"] = ""
            draft_board["Pick"] = ""

            # Sort by priority (highest first) for better draft board ordering
            draft_board = draft_board.sort_values("Priority", ascending=False).reset_index(
                drop=True
            )

            # Update Rank column to reflect the new sorted order (draft order)
            draft_board["Rank"] = range(1, len(draft_board) + 1)

            # Keep only the columns needed for the frontend
            draft_board = draft_board[
                [
                    "Rank",
                    "Player",
                    "Pos",
                    "Points",
                    "ADP",
                    "Priority",
                    "Value",
                    "Proj_Rank",
                    "VORP",
                    "Drafted",
                    "Round",
                    "Pick",
                ]
            ]

            processed_data["overall"] = clean_dataframe_for_json(projections_for_frontend)
            processed_data["by_position"] = {
                pos: clean_dataframe_for_json(df) for pos, df in by_pos.items()
            }
            processed_data["draft_board"] = clean_dataframe_for_json(draft_board)

            # Update cache timestamp
            update_cache_timestamp()
            
            print("✅ Data processed successfully for web dashboard")
            return True

        except Exception as e:
            print(f"❌ Error processing data: {e}")
            import traceback

            traceback.print_exc()
            return False


@app.route("/")
def index():
    """Main dashboard page"""
    if processed_data["overall"] is None:
        success = process_data_for_web()
        if not success:
            return "Error loading data. Please check the configuration and data files."

    return render_template(
        "dashboard.html",
        overall=processed_data["overall"],
        by_position=processed_data["by_position"],
        draft_board=processed_data["draft_board"],
        config=processed_data["config"],
    )


@app.route("/api/overall")
@gzip_response
def get_overall_data():
    """API endpoint for overall rankings"""
    print("🔍 API call: /api/overall")
    if processed_data["overall"] is None:
        print("⚠️  processed_data['overall'] is None, processing data...")
        process_data_for_web()

    if processed_data["overall"] is not None:
        try:
            data = processed_data["overall"].to_dict("records")
            print(f"✅ Returning {len(data)} overall players")
            return jsonify(data)
        except Exception as e:
            print(f"❌ Error converting overall data to JSON: {e}")
            return jsonify({"error": "Data conversion failed"}), 500
    print("❌ No overall data available")
    return jsonify([])


@app.route("/api/position/<pos>")
@gzip_response
def get_position_data(pos):
    """API endpoint for position-specific data"""
    if pos.upper() in processed_data["by_position"]:
        try:
            data = processed_data["by_position"][pos.upper()].to_dict("records")
            return jsonify(data)
        except Exception as e:
            print(f"Error converting {pos} data to JSON: {e}")
            return jsonify({"error": f"Data conversion failed for {pos}"}), 500
    return jsonify([])


@app.route("/api/draft_board")
@gzip_response
def get_draft_board():
    """API endpoint for draft board"""
    if processed_data["draft_board"] is not None:
        try:
            # Convert to dict and ensure Priority is a regular float
            data = processed_data["draft_board"].to_dict("records")
            for player in data:
                if "Priority" in player and player["Priority"] is not None:
                    try:
                        player["Priority"] = float(player["Priority"])
                    except (ValueError, TypeError):
                        player["Priority"] = 0.0
            return jsonify(data)
        except Exception as e:
            print(f"Error converting draft board data to JSON: {e}")
            return jsonify({"error": "Data conversion failed"}), 500
    return jsonify([])


@app.route("/api/update_drafted", methods=["POST"])
def update_drafted():
    """API endpoint to update drafted status"""
    data = request.json

    # Handle reset request
    if data.get("reset"):
        # Reset all drafted status
        for df_name in ["overall", "draft_board"]:
            if processed_data[df_name] is not None:
                if df_name == "overall":
                    processed_data[df_name]["drafted"] = False
                else:
                    processed_data[df_name]["Drafted"] = ""
                    processed_data[df_name]["Round"] = ""
                    processed_data[df_name]["Pick"] = ""

        # Reset position dataframes
        for pos_df in processed_data["by_position"].values():
            if pos_df is not None:
                pos_df["drafted"] = False

        return jsonify({"success": True})

    # Handle individual player update
    player_name = data.get("player")
    drafted = data.get("drafted", False)
    round_num = data.get("round", "")
    pick_num = data.get("pick", "")

    # Update in all relevant dataframes
    for df_name in ["overall", "draft_board"]:
        if processed_data[df_name] is not None:
            if df_name == "overall":
                mask = processed_data[df_name]["player"] == player_name
                if mask.any():
                    processed_data[df_name].loc[mask, "drafted"] = drafted
            else:
                mask = processed_data[df_name]["Player"] == player_name
                if mask.any():
                    processed_data[df_name].loc[mask, "Drafted"] = (
                        "✓" if drafted else ""
                    )
                    if round_num:
                        processed_data[df_name].loc[mask, "Round"] = round_num
                    if pick_num:
                        processed_data[df_name].loc[mask, "Pick"] = pick_num

    # Update position dataframes
    for pos_df in processed_data["by_position"].values():
        if pos_df is not None:
            mask = pos_df["player"] == player_name
            if mask.any():
                pos_df.loc[mask, "drafted"] = drafted

    return jsonify({"success": True})


@app.route("/api/config", methods=["GET"])
def get_config():
    """Get current configuration"""
    try:
        config = load_config()
        # Return config in the format expected by frontend
        return jsonify(
            {"league": config.get("league", {}), "scoring": config.get("scoring", {})}
        )
    except Exception as e:
        print(f"Error loading config: {e}")
        return jsonify({"error": "Failed to load configuration"}), 500


@app.route("/api/config", methods=["POST"])
def update_config():
    """Update configuration"""
    try:
        new_config = request.json
        config_file = "../../config/config_redraft.json"

        # Load existing config
        with open(config_file, "r") as f:
            config = json.load(f)

        # Update the redraft_12team section
        if "redraft_12team" not in config:
            config["redraft_12team"] = {}

        # Update league settings
        if "league" in new_config:
            config["redraft_12team"]["league"] = new_config["league"]

        # Update scoring settings
        if "scoring" in new_config:
            config["redraft_12team"]["scoring"] = new_config["scoring"]

        # Save updated config
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)

        # Reprocess data with new configuration
        success = process_data_for_web()
        if not success:
            return (
                jsonify({"error": "Failed to reprocess data with new configuration"}),
                500,
            )

        return jsonify({"success": True})
    except Exception as e:
        print(f"Error updating config: {e}")
        return jsonify({"error": "Failed to update configuration"}), 500


@app.route("/api/config/reset", methods=["POST"])
def reset_config():
    """Reset configuration to defaults"""
    try:
        # Create default configuration
        default_config = {
            "redraft_12team": {
                "league": {
                    "num_teams": 12,
                    "superflex": True,
                    "starters": {
                        "QB": 1,
                        "RB": 2,
                        "WR": 2,
                        "TE": 1,
                        "FLEX": 1,
                        "SUPERFLEX": 1,
                    },
                },
                "scoring": {
                    "offense": {
                        "pass_yd": 0.04,
                        "pass_td": 4.0,
                        "pass_int": -2.0,
                        "pass_2pt": 2.0,
                        "rush_yd": 0.1,
                        "rush_td": 6.0,
                        "rec": 1.0,
                        "rec_yd": 0.1,
                        "rec_td": 6.0,
                        "rec_2pt": 2.0,
                    }
                },
            }
        }

        config_file = "../../config/config_redraft.json"
        with open(config_file, "w") as f:
            json.dump(default_config, f, indent=2)

        # Reprocess data with default configuration
        success = process_data_for_web()
        if not success:
            return (
                jsonify(
                    {"error": "Failed to reprocess data with default configuration"}
                ),
                500,
            )

        return jsonify({"success": True})
    except Exception as e:
        print(f"Error resetting config: {e}")
        return jsonify({"error": "Failed to reset configuration"}), 500


if __name__ == "__main__":
    # For development - can still run with python app.py
    # Process data before starting the server
    if processed_data["overall"] is None:
        process_data_for_web()
    app.run(debug=True, host="0.0.0.0", port=5000)
else:
    # For flask run command
    if processed_data["overall"] is None:
        process_data_for_web()
