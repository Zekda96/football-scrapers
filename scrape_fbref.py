# Scrape from FBRef and save it as csv
import soccerdata as sd
import os
import pandas as pd
from gspread_dataframe import set_with_dataframe

league = "ENG-Premier League"
season = '22-23'
stats_list = ["standard", 'shooting', "passing", "passing_types",
              "goal_shot_creation", 'defense', 'possession', "misc",
              "keeper", "keeper_adv"]
# stats_list = ["standard", "shooting"]

fbref = sd.FBref(leagues=league, seasons=season)

# Filepath for league folder
dir_fp = os.path.join('/Users/dgranja/PycharmProjects/dash-app', league, season)
# Create/Open league csv file
os.makedirs(dir_fp, exist_ok=True)
# Filepath
season_fp = f'{os.path.join(dir_fp, season)}_fbref_stats.csv'


stats_series = []
for i, stat in enumerate(stats_list):
    print(f'Saving [{stat}]')
    df_stats = fbref.read_player_season_stats(stat_type=stat)

    # Save and read csv to extend multi-index into columns
    df_stats.to_csv(season_fp)
    df = pd.read_csv(season_fp)
    # Multi-index splits into several rows. Grab all column names and put them together
    player_data = df.iloc[1, :4].reset_index(drop=True).tolist()  # Some are in row 1
    matches = df.columns[4:8].tolist()  # Some stayed as a column name
    stats = df.iloc[0, 8:].reset_index(drop=True).tolist()  # And other are on row 0

    df = df.loc[2:, :]
    df.columns = player_data + matches + stats
    df = df.reset_index(drop=True)
    data_dict = {f'{stat}': df}

    # Rename column names where desired
    if stat == 'standard':
        df = data_dict[stat].iloc[:, 0:12]  # Get players data
        df = df.join(data_dict[stat].iloc[:, 15])  # Get npG

        df = df.rename(columns={'G-PK': 'npGoals'})

    elif stat == 'shooting':
        df = df.rename(
            columns={'Gls': 'Goals',
                     'Sh': 'Shots',
                     'SoT': 'SoT',
                     'SoT%': 'SoT%',
                     'Sh/90': 'Sh/90',
                     'SoT/90': 'SoT/90',
                     'G/Sh': 'G/Sh',
                     'G/SoT': 'G/SoT',
                     'Dist': 'AvgShotDistance',
                     'FK': 'FKShots',
                     'PK': 'PK',
                     'PKatt': 'PKsAtt',
                     'xG': 'xG',
                     'npxG': 'npxG',
                     'npxG/Sh': 'npxG/Sh',
                     'G-xG': 'G-xG',
                     'np:G-xG': 'npG-xG'})

    elif stat == 'passing':
        df = df.rename(
            columns={'Cmp': 'PassesCompleted',
                     'Att': 'PassesAttempted',
                     'Cmp%': 'TotCmp%',
                     'TotDist': 'TotalPassDist',
                     'PrgDist': 'ProgPassDist',
                     'Cmp': 'ShortPassCmp',
                     'Att': 'ShortPassAtt',
                     'Cmp%': 'ShortPassCmp%',
                     'Cmp': 'MedPassCmp',
                     'Att': 'MedPassAtt',
                     'Cmp%': 'MedPassCmp%',
                     'Cmp': 'LongPassCmp',
                     'Att': 'LongPassAtt',
                     'Cmp%': 'LongPassCmp%',
                     'Ast': 'Assists',
                     'xAG': 'xAG',
                     'xA': 'xA',
                     'A-xAG': 'A-xAG',
                     'KP': 'KeyPasses',
                     '1/3': 'Final1/3Cmp',
                     'PPA': 'PenAreaCmp',
                     'CrsPA': 'CrsPenAreaCmp',
                     'PrgP': 'ProgPasses'
                     }
        )

    elif stat == 'passing_types':
        df = df.rename(
            columns={'Live': 'LivePass',
                     'Dead': 'DeadPass',
                     'FK': 'FKPasses',
                     'TB': 'ThruBalls',
                     'Sw': 'Switches',
                     'Crs': 'Crs',
                     'CK': 'CK',
                     'In': 'InSwingCK',
                     'Out': 'OutSwingCK',
                     'Str': 'StrCK',
                     'TI': 'ThrowIn',
                     'Off': 'PassesToOff',
                     'Blocks': 'PassesBlocked',
                     'Cmp': 'Cmpxxx'
                     }
        )

    elif stat == 'goal_shot_creation':
        df = df.rename(
            columns={'SCA': 'SCA',
                     'SCA90': 'SCA90',
                     'PassLive': 'SCAPassLive',
                     'PassDead': 'SCAPassDead',
                     'TO': 'SCADrib',
                     'Sh': 'SCASh',
                     'Fld': 'SCAFld',
                     'Def': 'SCADef',
                     'GCA': 'GCA',
                     'GCA90': 'GCA90',
                     'PassLive': 'GCAPassLive',
                     'PassDead': 'GCAPassDead',
                     'TO': 'GCADrib',
                     'Sh': 'GCASh',
                     'Fld': 'GCAFld',
                     'Def': 'GCADef'
                     }
        )

    elif stat == 'defense':
        df = df.rename(
            columns={'Tkl': 'Tkl',
                     'TklW': 'TklWinPoss',
                     'Def 3rd': 'Def3rdTkl',
                     'Mid 3rd': 'Mid3rdTkl',
                     'Att 3rd': 'Att3rdTkl',
                     'Tkl': 'DrbTkl',
                     'Att': 'DrbPastAtt',
                     'Tkl%': 'DrbTkl%',
                     'Lost': 'DrbPast',
                     'Blocks': 'Blocks',
                     'Sh': 'ShBlocks',
                     'Pass': 'PassBlocks',
                     'Int': 'Int',
                     'Tkl+Int': 'Tkl+Int',
                     'Clr': 'Clr',
                     'Err': 'Err'
                     }
        )

    elif stat == 'possession':
        df = df.rename(
            columns={'Touches': 'Touches',
                     'Def Pen': 'DefPenTouch',
                     'Def 3rd': 'Def3rdTouch',
                     'Mid 3rd': 'Mid3rdTouch',
                     'Att 3rd': 'Att3rdTouch',
                     'Att Pen': 'AttPenTouch',
                     'Live': 'LiveTouch',
                     'Succ': 'SuccDrb',
                     'Att': 'AttDrb',
                     'Succ%': 'DrbSucc%',
                     'Tkld': 'TimesTackled',
                     'Tkld%': 'TimesTackled%',
                     'Carries': 'Carries',
                     'TotDist': 'TotalCarryDistance',
                     'PrgDist': 'ProgCarryDistance',
                     'PrgC': 'ProgCarries',
                     '1/3': 'CarriesToFinalThird',
                     'CPA': 'CarriesToPenArea',
                     'Mis': 'CarryMistakes',
                     'Dis': 'Disposesed',
                     'Rec': 'ReceivedPass',
                     'PrgR': 'ProgPassesRec'})

    elif stat == 'misc':
        df = df.rename(
            columns={'CrdY': 'Yellows',
                     'CrdR': 'Reds',
                     '2CrdY': 'Yellow2',
                     'Fls': 'Fls',
                     'Fld': 'Fld',
                     'Off': 'Off',
                     'PKwon': 'PKwon',
                     'PKcon': 'PKcon',
                     'OG': 'OG',
                     'Recov': 'Recov',
                     'Won': 'AerialWins',
                     'Lost': 'AerialLoss',
                     'Won%': 'AerialWin%',
                     }
        )

    elif stat == 'keeper':
        df.rename(
            columns={'GA': 'GA',
                     'GA90': 'GA90',
                     'SoTA': 'SoTA',
                     'Saves': 'Saves',
                     'Save%.1': 'Save%',
                     'W': 'W',
                     'D': 'D',
                     'L': 'L',
                     'CS': 'CS',
                     'CS%': 'CS%',
                     'PKsFaced': 'PKsFaced',
                     'PKA': 'PKA',
                     'PKsv': 'PKsv',
                     'PKm': 'PKm',
                     'Save%.2': 'PKSave%'
                     }
        )

    elif stat == "keeper_adv":
        df.rename(
            columns={'PKA': 'PKGA',
                     'FK': 'FKGA',
                     'CK': 'CKGA',
                     'OG': 'OGA',
                     'PSxG': 'PSxG',
                     'PSxG/SoT': 'PSxG/SoT',
                     'PSxG+/-': 'PSxG+/-',
                     '/90': 'PSxG+/- /90',
                     'Cmp': 'LaunchCmp',
                     'Att': 'LaunchAtt',
                     'Cmp%': 'LaunchPassCmp%',
                     'Att': 'PassAtt',
                     'Thr': 'PassThr',
                     'Launch%': 'PassesLaunch%',
                     'AvgLen': 'AvgLenLaunch',
                     'Att': 'GoalKicksAtt',
                     'Launch%': 'GoalKicksLaunch%',
                     'AvgLen': 'AvgLen',
                     'Opp': 'OppCrs',
                     'Stp': 'StpCrs',
                     'Stp%': 'CrsStp%',
                     '#OPA': '#OPA',
                     '#OPA/90': '#OPA/90',
                     'AvgDist': 'AvgDistOPA'
                     }

        )

    data_df = ['league', 'season', 'team', 'player',
               'nation',  'pos', 'age', 'born', '90s',]  # Columns to exclude from ranking
    if i == 0:
        # Save players data
        stats_series.append(
            df.loc[:, df.columns.isin(data_df)]
        )

    # Save stats only
    stats_series.append(
        df.loc[:, ~df.columns.isin(data_df)]
    )


df2 = pd.concat(stats_series, axis=1).reset_index(drop=True)


df2.to_csv(f'{season_fp}', index=False)
print(f'Saved to {season_fp}')
# pickle_fp = f'{season_fp[:-4]}.pkl'
# df2.to_pickle(pickle_fp)
