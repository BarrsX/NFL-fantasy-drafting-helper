import requests
import json

# Test the config endpoint
try:
    response = requests.get("http://127.0.0.1:5000/api/config")
    if response.status_code == 200:
        config = response.json()
        print("✅ Config endpoint working!")
        print("League settings:", json.dumps(config.get("league", {}), indent=2))
        print("Scoring settings:", json.dumps(config.get("scoring", {}), indent=2))
    else:
        print(f"❌ Config endpoint failed with status {response.status_code}")
except Exception as e:
    print(f"❌ Error testing config endpoint: {e}")
