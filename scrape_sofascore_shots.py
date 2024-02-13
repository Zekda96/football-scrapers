import pandas as pd
import requests
import random
import json
import time


def scrape_shots(fixture_id: str, agents: list):
    headers = {
        'authority': 'api.sofascore.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"76f2a3635f"',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'User-Agent': random.choice(agents)
    }

    url = f'https://api.sofascore.com/api/v1/event/{fixture_id}/shotmap'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['shotmap']
    else:
        print(f'{response.status_code}: failed')
        return 'missing'


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]

# WE NEED TO GET GAMES SCHEDULE TO GET ALL GAMES' IDS
# 1. GET GAMES SCHEDULE
c = 0

rows = []
raw = []

for i in range(9):
    # Read fixtures files
    matches_fp = f'data/list{8-i}.txt'
    matches = json.loads(open(matches_fp, "r").read())

    # Loop through matches from list
    for j, match in enumerate(matches['events']):
        # Get team names and match_id
        if match['status']['description'] in ['Ended', 'AP']:
            fecha = match['roundInfo']['round']
            h = match['homeTeam']['name']
            hsc = match['homeScore']['normaltime']
            a = match['awayTeam']['name']
            asc = match['awayScore']['normaltime']
            id = match['id']

            time.sleep(3)

            print(f'{i}-{j}- MW{fecha}. {h} {hsc} - {asc} {a}: {id}')
            # Use match_id to scrape shots
            while 1:
                shots = scrape_shots(id, user_agents)
                if not shots == 'missing':
                    break
                time.sleep(5)

            shots.reverse()
            for shot in shots:
                if shot['isHome']:
                    team = h
                else:
                    team = a

                t = shot['time']
                p = shot['player']['name']

                goal = 0
                if shot['shotType'] == 'goal':
                    goal = 1
                # print(f'{t} mins - {team}: {p} - {goal}')

                row = {'match_id': id,
                       'home': h,
                       'away': a,
                       'time': shot['time'],
                       'time_seconds': shot['timeSeconds'],
                       'player': shot['player']['name'],
                       'team': team,
                       'pos': shot['player']['position'],
                       'goal': goal,
                       'type': shot['shotType'],
                       'situation': shot['situation'],
                       'body_part': shot['bodyPart'],
                       'x': shot['playerCoordinates']['x'],
                       'y': shot['playerCoordinates']['y'],
                       'goal_x': shot['goalMouthCoordinates']['x'],
                       'goal_y': shot['goalMouthCoordinates']['y'],
                       'goal_z': shot['goalMouthCoordinates']['z'],
                       }

                if shot['shotType'] == 'goal':
                    row['goal_type'] = shot['goalType']
                else:
                    row['goal_type'] = 'no-goal'

                rows.append(row)
            c += 1
print(c)

df = pd.DataFrame(rows)
save_fp = 'scrapers/data/LigaPro2023_all-shots.csv'
print(f'Saving df in {save_fp}')
df.to_csv(save_fp)
