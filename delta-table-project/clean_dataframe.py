from datetime import datetime, timezone
import pandas as pd
from re import sub

pd.options.mode.copy_on_write = True

def to_snake_case(s: str):
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()


def transform_json_all(json_list: list):
    """
    Transforms a list of dictionaries into a single dictionary.
    """
    result = {}
    for item in json_list:
        display_name = to_snake_case(item['type']['displayName'])
        value = item.get('value', True)  # Get the value, default to None if not present
        result[display_name] = value
    return result


def transform_json(json_list: list, qualifiers):
    """
    Transforms a list of dictionaries into a single dictionary.
    """
    qualifiers = [to_snake_case(q) for q in qualifiers]

    result = {}
    for item in json_list:
        display_name = to_snake_case(item['type']['displayName'])
        if display_name in qualifiers:
            # Get the value, default to True if qualifier is present present
            result[display_name] = item.get('value', True) 

    return result

def parse_all_qualifiers(df: pd.DataFrame):

    #Load the qualifiers
    dfq = pd.read_csv("qualifiers.csv", names=["num", "name", "value", "type", "description", "qualifier"])
    qualifiers = dfq["name"].to_list()
    qualifiers = [to_snake_case(q) for q in qualifiers]

    # Fill missing values with NaN (optional, pandas does this by default)
    og_cols = df.columns.to_list()

    required_columns = og_cols + qualifiers

    # Convert the JSON strings into dictionaries and create a new DataFrame
    transformed_data = df["qualifiers"].apply(transform_json_all)

    # Convert the list of dictionaries into a DataFrame
    result_df = pd.DataFrame(transformed_data.tolist())

    # Concatenate with the original DataFrame if needed
    df = pd.concat([df, result_df], axis=1)

    # # Create a new DataFrame with all required columns, filling missing ones with pd.NA
    # final_df = pd.DataFrame(columns=required_columns)

    # # Fill the final DataFrame with values from result_df
    # for col in required_columns:
    #     try:
    #         final_df[col] = df.get(col, pd.NA)

    #     except ValueError as e:
    #         # Repeated columns
    #         final_df[col] = df.get(col).iloc[:,0]

    return df


def parse_chosen_qualifiers(df, qualifiers: list):

    transformed_data = df["qualifiers"].apply(lambda x: transform_json(x, qualifiers))
    new_df = pd.DataFrame(transformed_data.to_list())

    final_df = pd.concat([df, new_df], axis=1)
    return final_df


def clean_df(dataframe: pd.DataFrame, qualifiers = []):
    """
    Cleans the dataframe, declares datatypes and adds audit columns.
    """

    pd.set_option('future.no_silent_downcasting', True)

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
        df[col] = df[col].fillna(False).astype(bool)


    # Add PK to df
    df = df.reset_index()
    df = df.rename(columns={'index': 'match_event_id'})

    df['PK'] = df['league'].astype(str) + \
    df['season'].astype(str) + \
    df['date'].astype(str) + \
    df['home'].astype(str) + \
    df['away'].astype(str) + \
    df['game_id'].astype(str) + \
    df['match_event_id'].astype(str) + \
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

    # Add  qualifiers as new columns
    if not qualifiers:
        # Default: Don't parse
        return df
    elif qualifiers[0].lower() == "all":
        final_df = parse_all_qualifiers(df)
        #final_df.pop("qualifiers")
    else:
        # Parse chosen qualifiers
        final_df = parse_chosen_qualifiers(df, qualifiers)


    return final_df
