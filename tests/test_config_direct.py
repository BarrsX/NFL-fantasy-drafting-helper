import json

# Test loading the config file directly
try:
    with open("configs/config_redraft.json", "r") as f:
        config_data = json.load(f)

    redraft_config = config_data.get("redraft_12team", {})

    print("✅ Config file loaded successfully!")
    print("League settings:", json.dumps(redraft_config.get("league", {}), indent=2))
    print("Scoring settings:", json.dumps(redraft_config.get("scoring", {}), indent=2))

    # Test the format that should be returned to frontend
    frontend_format = {
        "league": redraft_config.get("league", {}),
        "scoring": redraft_config.get("scoring", {}),
    }
    print("\nFrontend format:", json.dumps(frontend_format, indent=2))

except Exception as e:
    print(f"❌ Error loading config: {e}")
