import requests
import json
import time

print("🔍 Testing NFL Analytics endpoint...")
time.sleep(2)  # Give Flask time to start

try:
    print("📡 Making request to http://127.0.0.1:5000/api/nfl_analytics")
    response = requests.get('http://127.0.0.1:5000/api/nfl_analytics', timeout=10)
    print(f"📊 Response status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"✅ NFL Analytics endpoint working! Returned {len(data)} players")
        if data:
            print("\n📋 Sample player data:")
            print(json.dumps(data[0], indent=2))
        else:
            print("⚠️  No player data returned")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        print(f"Response: {response.text}")
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection Error: Could not connect to Flask app")
    print("Make sure the Flask app is running on http://127.0.0.1:5000")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    print(f"Error type: {type(e)}")
