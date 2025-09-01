import requests
import json

try:
    r = requests.get('http://127.0.0.1:5000/api/nfl_analytics')
    data = r.json()
    print(f'Total players: {len(data)}')
    
    if data:
        sample = data[0]
        print(f'Sample player: {sample.get("player", "N/A")}')
        print(f'NFL games played: {sample.get("nfl_games_played", "N/A")}')
        print(f'NFL avg PPR: {sample.get("nfl_avg_ppr_points", "N/A")}')
        print(f'NFL consistency: {sample.get("nfl_consistency_score", "N/A")}')
        print(f'NFL adjusted priority: {sample.get("nfl_adjusted_priority", "N/A")}')
        
        # Check if we have some real data (non-zero values)
        has_real_data = any([
            sample.get("nfl_games_played", 0) > 0,
            sample.get("nfl_avg_ppr_points", 0) > 0,
            sample.get("nfl_consistency_score", 0) > 0
        ])
        
        print(f'Has real NFL data: {has_real_data}')
    else:
        print('No data returned')
        
except Exception as e:
    print(f'Error: {e}')
