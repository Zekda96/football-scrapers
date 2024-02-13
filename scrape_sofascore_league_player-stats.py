import requests

groups = ['attack', 'defence', 'passing', 'goalkeeper']

# summary
params = {
    'group': 'summary',
    'order': '-rating',
}
# attack
params = {
    'group': 'attack',
    'order': '-goals',
}
# defence
defence = {
    'group': 'defence',
    'order': '-tackles',
}
#passing
passing = {
    'group': 'passing',
    'order': '-bigChancesCreated',
}
# goalkeepers
gk = {'group': 'goalkeeper',
      'order': '-savedShotsFromInsideTheBox',
      'filters': 'position.in.G',
      }

headers = {
    'authority': 'api.sofascore.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'if-none-match': 'W/"952ebcd026"',
    'origin': 'https://www.sofascore.com',
    'referer': 'https://www.sofascore.com/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

params = {
    'limit': '50',
    'order': '-tackles',
    # 'offset': '40',
    # 'minApps': 'yes', # At least half as player with max appearances
    # 'accumulation': 'total',
    # 'accumulation': 'per90',
    'group': 'defence',
}

response = requests.get(
    'https://api.sofascore.com/api/v1/unique-tournament/240/season/48720/statistics',
    params=params,
    headers=headers,
)

stats = response.json()['results']
