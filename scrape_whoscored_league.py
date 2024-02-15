# Get WhoScored event data for a whole season
import soccerdata as sd

# league = 'ENG-Premier League'
# league = 'ESP-La Liga'
# league = 'GER-Bundesliga'
league = 'ITA-Serie A'
# league =  'FRA-Ligue 1'
# league = 'INT-Women's World Cup'
# league = 'INT-World Cup'
# league = ['ENG-Premier League',
#           'ESP-La Liga',
#           'GER-Bundesliga',
#           'ITA-Serie A',
#           'FRA-Ligue 1'
#           ]

# season = '21-22'
# season = '22-23'
season = '23-24'

ws = sd.WhoScored(leagues=league, seasons=season)
# ws = sd.WhoScored(leagues=league, seasons=season,
#                   no_cache=True,
#                   no_store=True,
#                   headless=True)

schedule = ws.read_schedule()
# schedule = ws.read_schedule()
matchs_no = len(schedule)

# --------------------------- Uncomment either
# match_id = 1729468
match_id = ''

if match_id == '':
    events = ws.read_events(
        match_id=schedule['game_id'].values.tolist(),
    )
else:
    # Load one match
    events = ws.read_events(match_id=int(match_id))
