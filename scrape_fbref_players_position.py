# libraries
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# --------------------------------------- INPUT ----------------------------
# Filepath of fbref stats file to add positions columns
og_fp = '/Users/dgranja/PycharmProjects/dash-app/ENG-Premier League/22-23/22-23_fbref_stats.csv'
# Filepath of output file to save positions separately
positions_output = '/Users/dgranja/PycharmProjects/dash-app/ENG-Premier League/22-23/22-23_fbref_positions.csv'
# Season and league stats fbref link
url = 'https://fbref.com/en/comps/9/2022-2023/stats/2022-2023-Premier-League-Stats'
# Code from fbref link from player scouting report - EPL 2223
league_code = '11566'

# ---------------------------------------- CODE ----------------------------

# Selenium
driver = webdriver.Firefox(options=Options())
driver.get(url)

# Get column names
tbody = driver.find_element(By.XPATH, '//*[@id="stats_standard"]/tbody')

series = []
# player profile URL
for tr in tbody.find_elements(By.XPATH, './/tr'):
    # Skip headers (thead) between rows
    if tr.get_attribute("class") != 'thead':
        name = tr.find_element(By.XPATH, './/td[1]/a').text
        team = tr.find_element(By.XPATH, './/td[4]/a').text
        # Get each player's profile url
        url = tr.find_element(By.XPATH, './/td[1]/a').get_attribute('href')
        url = url.split('/')
        url.insert(-1, 'scout')
        url.insert(-1, league_code)
        url[-1] = url[-1] + '-Scouting-Report'
        url = '/'.join(url)
        series.append(pd.Series({'Team': team, 'Player': name, 'url': url}))

# Dataframe sorted by team and player with their profile url
df2 = pd.DataFrame(series).sort_values(['team', 'player']).reset_index(drop=True)


# Get all fbref rank positions for each player
pos_series = []
for i in df2.index:

    row = df2.iloc[i]

    team = row.team
    player = row.player
    url = row.url

    driver.get(url)
    position = {'team': team, 'player': player}

    tbody = driver.find_elements(By.XPATH, '//*[@id="all_scout_summary"]/div')

    # Find element in tbody that contains the positions
    for x, element in enumerate(tbody):
        if 'vs.' in element.text:

            # Get all positions
            # one column for each position
            for j, pos in enumerate(element.text.split('vs. ')[1:]):
                position[f'Pos{j+1}'] = pos.strip()

    pos_series.append(pd.Series(position))
    print(f'----- {round(((i+1) / len(df2.index)) * 100, 2)}% -----')
    print(position)

df_pos = pd.DataFrame(pos_series)
df_pos.to_csv(positions_output)

# MERGE PLAYERS POSITIONS TO STATS CSV
# Read CSV files into dataframes
df1 = pd.read_csv(og_fp)

merged_df = pd.merge(df1, df_pos)
merged_df.to_csv(og_fp)
