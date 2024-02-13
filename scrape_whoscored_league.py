# Get WhoScored event data for a whole season
import soccerdata as sd
import os
import pandas as pd
import json

league = 'ENG-Premier League'
season = '2324'  # Season as 22/23

# Read season
print('Reading season - ')
ws = sd.WhoScored(leagues=league, seasons=f'{season}')
schedule = ws.read_schedule()

# Get matches id from cached season file
season_fp = f'/Users/dgranja/soccerdata/data/WhoScored/matches/{league}_{season}.csv'
season_csv = pd.read_csv(season_fp)
games_id = season_csv['game_id'].unique().tolist()


# Filepath for CSV of matches
dir_fp = os.path.join('/Users/dgranja/PycharmProjects/dash-app', league, season)
os.makedirs(dir_fp, exist_ok=True)

# Create/Open league csv file
season_fp = f'{os.path.join(dir_fp, season)}_20240131.csv'
open(season_fp, 'a')

events_list = []
for i, match in enumerate(games_id):
    # Scrape
    percent = (i+1)/380 * 100
    print(f'Reading match Number {i+1}/380 - {round(percent,2)} %')
    events = ws.read_events(match_id=match)
    print('Got match event data\nSaving to list...')
    # Save to list
    events_list.append(events)

print('Saving file...')
league = pd.concat(events_list, ignore_index=True)
league.to_csv(season_fp)
print(f'Saved to {season_fp}')
