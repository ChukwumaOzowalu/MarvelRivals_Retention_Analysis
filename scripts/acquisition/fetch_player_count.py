import requests
import pandas as pd
import time

# Prompt the user for their Steam API key
API_KEY = input("Please enter your Steam API key: ")

# List of shooter game app IDs and their corresponding titles
games = [
    {"app_id": 2767030, "title": "Marvel Rivals"},
    {"app_id": 440, "title": "Team Fortress 2"},
    {"app_id": 2357570, "title": "Overwatch 2"},
    {"app_id": 1172470, "title": "Apex Legends"},
    {"app_id": 359550, "title": "Counter-Strike: GO"}
]

def get_game_details(app_id):
    url = f'http://store.steampowered.com/api/appdetails'
    params = {
        'appids': app_id
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def get_player_count(api_key, app_id):
    url = f'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/'
    params = {
        'appid': app_id,
        'key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Initialize an empty list to store game data
game_data_list = []

# Loop through each game app ID and fetch detailed game data
for game in games:
    try:
        game_details = get_game_details(game['app_id'])
        player_data = get_player_count(API_KEY, game['app_id'])
        if str(game['app_id']) in game_details and game_details[str(game['app_id'])]['success']:
            details = game_details[str(game['app_id'])]['data']
            game_data_list.append({
                'AppID': game['app_id'],
                'Title': game["title"],
                'Developer': ', '.join(details.get('developers', [])),
                'Publisher': ', '.join(details.get('publishers', [])),
                'Price': details.get('price_overview', {}).get('final', 0) / 100 if details.get('price_overview') else 'Free',
                'Release Date': details.get('release_date', {}).get('date', ''),
                'Current Players': player_data['response'].get('player_count', 0)
            })
        # Be respectful of the API rate limits
        time.sleep(1)  # Sleep for 1 second between requests
    except Exception as e:
        print(f"Failed to fetch data for app ID {game['app_id']}: {e}")

# Create a DataFrame from the game data
game_data_df = pd.DataFrame(game_data_list)

# Output the DataFrame to a CSV file
game_data_df.to_csv('steam_game_data.csv', index=False)

print('Game data has been successfully saved to steam_game_data.csv')
