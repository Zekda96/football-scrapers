import soccerdata as sd
import os
import logging
from time import sleep
from datetime import datetime, timedelta

# leagues = "ESP-La Liga"S
#leagues = 'ENG-Premier League'
leagues = 'ESP-La Liga'
# leagues = 'FRA-Ligue 1'
# leagues = 'GER-Bundesliga'
# leagues = "INT-Women's World Cup"
# leagues = 'INT-World Cup'
# leagues = 'ITA-Serie A'
seasons = '23-24'
wait_time = 60 * 20 #seconds

ws = sd.WhoScored(leagues=leagues, seasons=seasons)

schedule = ws.read_schedule(force_cache=True)
available_games = schedule['game_id'].values.tolist()

folder_path = f"C:\\Users\\USER\\soccerdata\\data\\WhoScored\\events\\{leagues}_{seasons.replace('-', '')}"
while 1:
    print(f"Starting at {datetime.now()}")
    
    # List all files in the folder
    cached_games = os.listdir(folder_path)
    cached_games = [int(os.path.splitext(filename)[0]) for filename in cached_games]

    print(f"Games in calendar: {len(available_games)}")
    print(f"Games in cache: {len(cached_games)}")

    missing = [id for id in available_games if id not in cached_games]

    print(f"Games missing: {len(missing)}")

    print(f"Match id to scrape: {missing[0]}")

    events = ws.read_events(match_id=missing[0])
    print(events.head())

        # Look for shots and goals for QA
    df = events[['team', 'minute', 'player', 'is_shot','is_goal']]
    teams = df["team"].unique()

    shots = df[df['is_shot'] == True]
    goals = df[df['is_goal'] == True]
    for team in teams:
        logging.info(f"Shots for {team}: {len(shots[shots['team'] == team])}")
        logging.info(f"Goals for {team}: {len(goals[goals['team'] == team])}\n")

    logging.info(df)

    print(f"Next run at {datetime.now() + timedelta(seconds=wait_time)}")
    sleep(wait_time)

