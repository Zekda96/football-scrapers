import soccerdata as sd
import os
import logging
from datetime import datetime

#leagues = 'ENG-Premier League'
leagues = 'ESP-La Liga'
# leagues = 'FRA-Ligue 1'
# leagues = 'GER-Bundesliga'
# leagues = "INT-Women's World Cup"
# leagues = 'INT-World Cup'
# leagues = 'ITA-Serie A'
seasons = '23-24'

ws = sd.WhoScored(leagues=leagues, seasons=seasons)

schedule = ws.read_schedule(force_cache=True)
available_games = schedule['game_id'].values.tolist()

folder_path = f"C:\\Users\\USER\\soccerdata\\data\\WhoScored\\events\\{leagues}_{seasons.replace('-', '')}"

logging.info(f"Starting at {datetime.now()}")

# List all files in the folder
cached_games = os.listdir(folder_path)
cached_games = [int(os.path.splitext(filename)[0]) for filename in cached_games]

logging.info(f"Games in calendar: {len(available_games)}")
logging.info(f"Games in cache: {len(cached_games)}")

missing = [id for id in available_games if id not in cached_games]

logging.info(f"Games missing: {len(missing)}")
logging.info(f"Match id to scrape: {missing[0]}")

if missing:
    events = ws.read_events(match_id=missing[0])

    # Look for shots and goals for QA
    df = events[['team', 'minute', 'player', 'is_shot','is_goal']]
    teams = df["team"].unique()

    df = df[df['is_shot'] == True]
    goals = df[df['is_goal'] == True]
    for team in teams:
        logging.info(f"Shots for {team}: {len(df[df['team'] == team])}")
        logging.info(f"Goals for {team}: {len(goals[goals['team'] == team])}\n")
    
    logging.info(df)

else:
    logging.warning("No games to scrape")

logging.info(f"Finished at {datetime.now()}")
