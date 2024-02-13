# Get WhoScored event data for a whole season
import soccerdata as sd


ws = sd.WhoScored(leagues='ENG-Premier League', seasons=f'23-24')

events = ws.read_events(match_id=1796086)
events.head()
