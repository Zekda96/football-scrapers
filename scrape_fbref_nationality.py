# libraries
import numpy as np
import pandas as pd
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import flag

# ---------------------------- INPUT ----------------------
country = 'ECUADOR'

# fbref table link
url = 'https://fbref.com/es/stathead/scout/ECU'

# Get today's date
today = date.today()
# Standardize two digit months (01, 02, ... 10, 11, 12)
if today.month < 10:
    today_mes = f'0{today.month}'
else:
    today_mes = f'{today.month}'

if today.day < 10:
    today_dia = f'0{today.day}'
else:
    today_dia = f'{today.day}'

hoy = f'{today.year}-{today_mes}-{today_dia}'  # Today's date in dataframe's format

# -------------------------------- CODE ----------------------
# Selenium for fixtures

driver = webdriver.Firefox(options=Options())
driver.get(url)

# Get column names
thead = driver.find_element(By.XPATH, '//*[@id="fixtures_players"]/thead')
header = thead.find_elements(By.XPATH, './/tr')
cols = header[0].text.split()

# Get rows
tbody = driver.find_element(By.XPATH, '//*[@id="fixtures_players"]/tbody')
data = []

# Iterate rows and get items
for tr in tbody.find_elements(By.XPATH, './/tr'):
    row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
    row.insert(0, tr.find_elements(By.XPATH, './/th')[0].text)
    data.append(row)
# Create dataframe with future fixtures
fixtures = pd.DataFrame(data=data, columns=cols)

# Format date
fixtures_date = fixtures.Fecha.str.split(',', expand=True)
fixtures.loc[:, 'Fecha'] = fixtures_date[0]
# Clean date
fixtures = fixtures[fixtures['Fecha'] != 'Fecha']

# Format time
fixtures_time = fixtures.Hora.str.split('(', expand=True)
for i, row in fixtures_time.iterrows():
    if row[1] is not None:
        fixtures_time.loc[i, :] = row[1][:-1]

fixtures.loc[:, 'Hora'] = fixtures_time[0]

# Replace Mediocentro with CC
fixtures.loc[:, 'Posc'] = fixtures.Posc.replace(to_replace='CC', value='MC')
fixtures.loc[:, 'Posc'] = fixtures.Posc.replace(to_replace='DF,CC', value='DF/MC')
fixtures.loc[:, 'Posc'] = fixtures.Posc.replace(to_replace='DL,CC', value='DL/MC')

fixtures.loc[:, 'Jugador'] = fixtures.Jugador.replace(to_replace='Félix Torres Caicedo', value='Félix Torres')

fixtures_today = fixtures[fixtures['Fecha'] == hoy]
fixtures_today = fixtures_today.sort_values(by='Hora')
fixtures_today = fixtures_today.reset_index(drop=True)
ec = flag.flag('EC')

tweet = [f'🇪🇨🇪🇨⚽⚽ #EcuatorianosEnElExterior que juegan hoy:\n\n']
for i, row in fixtures_today.iterrows():
    fecha = row['Fecha']
    player = row['Jugador']
    hora = row['Hora']
    edad = row['Edad'][:2]
    equipo = row['Equipo']
    rival = row['Adversario']
    pais = row['País']
    posc = row['Posc']

    if pais[:3] == 'eng':
        p_flag = '🏴󠁧󠁢󠁥󠁮󠁧󠁿'
    else:
        p_flag = flag.flag(f'{pais[:2]}')

    if np.remainder(i+1, 4) == 0:
        tweet.append('-'*45 + '\n\n')
    tweet.append(f'{player} ({edad} - {posc}) - [{p_flag}{pais[-3:]}] {equipo} vs {rival} - {hora}\n\n')

tweet = ''.join(tweet)
print(tweet)

with open('fixtures.txt', 'w') as f:
    f.write(tweet)

# ------------------------- ADD CUP SCHEDULES
url_c1 = 'https://fbref.com/es/comps/8/nacionalidades/Nacionalidades-en-Champions-League'
url_c2 = 'https://fbref.com/es/comps/19/nacionalidades/Nacionalidades-en-Europa-League'
url_c3 = 'https://fbref.com/es/comps/882/nacionalidades/Nacionalidades-en-Europa-Conference-League'
competitions = [{'name': 'Champions Lg', 'url': url_c1},
                {'name': 'Europa Lg',    'url': url_c2},
                {'name': 'Conf Lg', 'url': url_c3}
                ]

cups = []
for cup in competitions:
    player_data = []

    driver.get(cup['url'])
    # Get column names
    thead = driver.find_element(By.XPATH, '//*[@id="nations"]/thead')
    header = thead.find_element(By.XPATH, './/tr')
    # Split header
    cols = header.text.split()
    # Fix column name as it is split into separate columns
    idx = cols.index('N.°')
    cols[idx] = 'N.° de Jugadores'
    del cols[idx+1:idx+3]  # Delete the previous separate columns

    # Get rows from cup nationalities table
    tbody = driver.find_element(By.XPATH, '//*[@id="nations"]/tbody')

    # Iterate rows and find Ecuador row
    for tr in tbody.find_elements(By.XPATH, './/tr'):
        if tr.text.split()[2] == country.capitalize():
            players = []
            players_url = []
            print(f'\nSus equipos juegan {cup["name"]}:')
            # Iterate through ecuadorean players and get their profile url
            for player in tr.find_elements(By.XPATH, './/td[4]/a'):
                name = player.text
                player_url = player.get_attribute('href')

                print(f'{name}')
                players.append(name)
                players_url.append(player_url)

    player_data = pd.DataFrame({'Jugador': players, 'Jugador_url': players_url})

    # Iterate through players profile url to get data and their teams' profile url
    age = []
    position = []
    teams_url = []
    teams = []
    for url in players_url:
        driver.get(url)
        for p in driver.find_elements(By.XPATH, '//*[@id="meta"]/div/p'):

            for strong in p.find_elements(By.XPATH, './/strong'):
                # Get position
                if strong.text == 'Posición:':
                    position.append(p.text[10:12])
                # Get age
                if strong.text == 'Nacimiento:':
                    # print(f'{i} - {p.text}')
                    # print(f'strong: "{strong.text}"')
                    span = p.find_element(By.XPATH, './/span[2]').text
                    age.append(span.split()[1].split('-')[0])

                # Get club name and club profile URL
                if strong.text == 'Club :':
                    a = p.find_element(By.XPATH, './/a')
                    team_url = a.get_attribute('href')
                    teams.append(a.text)
                    teams_url.append(team_url)
                    # print(f'{cup["name"]} urls: {team_url}')

    player_data['Edad'] = age
    player_data['Posicion'] = position
    player_data['Equipo'] = teams
    player_data['Equipo_url'] = teams_url

    cup_data = []
    team_data = []
    drop_rows = []
    # Iterate through teams profiles to check if they play cup today
    for i, df_row in player_data.iterrows():
        url = df_row['Equipo_url']
        jugador = player_data.loc[i, "Jugador"]
        equipo = player_data.loc[i, "Equipo"]
        driver.get(url)
        # Iter rows and check date and comp
        for tr in driver.find_elements(By.XPATH, '//*[@id="matchlogs_for"]/tbody/tr[not(contains(@class, "thead rowSum"))]'):
            # If is not a header row
            if tr.text.split()[0] != 'Fecha':
                # Check if team plays today
                is_today = tr.find_element(By.XPATH, './/th').text == hoy
                is_cup = tr.find_element(By.XPATH, './/td[2]').text == cup['name']
                if is_today and is_cup:
                    print(f'{jugador} - {equipo} - {cup["name"]}: YES')
                    data = []
                    cols = []
                    for d in tr.find_elements(By.XPATH, './/td'):
                        data.append(d.text)

                    header = driver.find_element(By.XPATH, '//*[@id="matchlogs_for"]/thead/tr')
                    cols = header.text.split()[1:]
                    # Fix column name as it is split into separate columns
                    idx = cols.index('Informe')
                    cols[idx] = 'Informe del Partido'
                    del cols[idx+1:idx+3]  # Delete the previous separate columns

                    break

        # Append match info for qualifying matches
        if is_today and is_cup:
            team_data.append(pd.Series(data))
        else:
            print(f'{jugador} - {equipo} juega {cup["name"]}: NO')
            drop_rows.append(i)

    # Eliminate players that are not playing today from df
    player_data = player_data.drop(drop_rows)

    # Create df with match data if any player is playing today
    if len(team_data) > 0:
        # Create dataframe of matches data
        cup_data = pd.concat(team_data, axis=1, ignore_index=True).T
        cup_data.columns = cols

        # Concatenate df with matches data
        player_data = pd.concat([player_data, cup_data], axis=1)

        # Append to cups list of dataframes
        cups.append(player_data)

# Create dataframe
if len(cups) > 0:
    cups_df = pd.concat(cups)
    cups_df['Comp'] = pd.Categorical(cups_df['Comp'], ["Champions Lg", "Europa Lg", "Conf Lg"])
    cups_df = cups_df.sort_values(['Comp', 'Hora']).reset_index(drop=True)

    # Fix position names
    cups_df.loc[:, 'Posicion'] = cups_df.Posicion.replace(to_replace='CC', value='MC')
    cups_df.loc[:, 'Posicion'] = cups_df.Posicion.replace(to_replace='DF,CC', value='DF/MC')
    cups_df.loc[:, 'Posicion'] = cups_df.Posicion.replace(to_replace='DL,CC', value='DL/MC')

    cups_df.loc[:, 'Jugador'] = cups_df.Jugador.replace(to_replace='Félix Torres Caicedo', value='Félix Torres')

    # Format time
    time_matches = cups_df.Hora.str.split('(', expand=True)
    for i, row in time_matches.iterrows():
        if row[1] is not None:
            time_matches.loc[i, :] = row[1][:-1]

    cups_df.loc[:, 'Hora'] = time_matches[0]

    # Time to print Tweet
    for cup in competitions:
        print(cup["name"])
        if cup["name"] == 'Champions Lg':
            torneo = 'Champions League🔵️⚪'
        elif cup["name"] == 'Europa Lg':
            torneo = 'Europa League 🟠⚫'
        elif cup["name"] == 'Conf Lg':
            torneo = 'Conference League 🟢⚫'

        tweet = [f'{torneo}:\n']
        for row in cups_df[cups_df['Comp'] == cup['name']].itertuples():
            jug = row.Jugador
            edad = row.Edad
            posc = row.Posicion
            equipo = row.Equipo
            hora = row.Hora
            rival = ' '.join(row.Adversario.split()[1:])

            flag_riv = row.Adversario.split()[0]
            if flag_riv[:3] == 'eng':
                flag_riv = '🏴󠁧󠁢󠁥󠁮󠁧󠁿'
            else:
                flag_riv = flag.flag(f'{flag_riv[:2]}')

            if equipo == "Eintracht Frankfurt":
                equipo = '🇩🇪' + equipo
            elif equipo == 'Leverkusen':
                equipo = '🇩🇪' + equipo
            elif equipo == 'Brighton & Hove Albion':
                equipo = '🏴󠁧󠁢󠁥󠁮󠁧󠁿Brighton'
            elif equipo == 'Rangers':
                equipo = '🏴󠁧󠁢󠁳󠁣󠁴󠁿' + equipo
            elif equipo == 'Union SG':
                equipo = '󠁧󠁢󠁳🇧🇪󠁴󠁿' + equipo
            elif equipo == 'Sparta Prague':
                equipo = '󠁧󠁢󠁳🇨🇿' + equipo
            elif equipo == 'Olympiacos':
                equipo = '🇬🇷' + equipo
            elif equipo == 'Lugano':
                equipo = '🇨🇭' + equipo
            elif equipo == 'Ferencváros':
                equipo = '🇭🇺' + equipo

            tweet.append(f'{hora} - {jug} ({edad} - {posc}) - {equipo} vs {flag_riv}{rival}\n')

        tweet = ''.join(tweet)
        print(tweet)
else:
    print('\nNo es dia de copas')
