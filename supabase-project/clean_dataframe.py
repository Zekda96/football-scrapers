from datetime import datetime, timezone
import pandas as pd

def clean_df(dataframe: pd.DataFrame):
    """
    Cleans the dataframe, declares datatypes and adds audit columns.
    """
    # Reset index
    df = dataframe.reset_index()
    cols = df['game'].str.split(' ', n=1, expand=True)
    game = cols.iloc[:, 1].str.split('-', n=1, expand=True)
    df.insert(2, "date", cols[0])
    df.insert(3, "home", game[0])
    df.insert(4, "away", game[1])
    df.pop("game")

    # Cast types
    int_columns = ["player_id", "related_event_id", "related_player_id"]
    for col in int_columns:
        df[col] = df[col].astype('Int64')

    # Fill Booleans
    bool_columns = ["is_touch", "is_shot", "is_goal"]
    for col in bool_columns:
        df[col] = df[col].astype(bool).fillna(False)

    # Add PK to df
    df['PK'] = df['league'].astype(str) + \
    df['season'].astype(str) + \
    df['date'].astype(str) + \
    df['home'].astype(str) + \
    df['away'].astype(str) + \
    df['game_id'].astype(str) + \
    df['team_id'].astype(str) + \
    df['team'].astype(str) + \
    df['period'].astype(str) + \
    df['expanded_minute'].astype(str) + \
    df['second'].astype(str) + \
    df['type'].astype(str) + \
    df['is_touch'].astype(str) + \
    df['outcome_type'].astype(str) + \
    df['player'].astype(str) + \
    df['x'].astype(str) + \
    df['y'].astype(str)

    df["sent_timestamp"] = pd.Timestamp(datetime.timestamp(datetime.now(timezone.utc)), unit='s', tz='UTC')

    return df