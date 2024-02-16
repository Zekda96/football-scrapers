import pandas as pd
import ast

fp = 'data/WhoScored/ITA-Serie A_2324.csv'

df = pd.read_csv(fp)

# Split game col into date, home and away
cols = df['game'].str.split(' ', n=1, expand=True)
game = cols.iloc[:, 1].str.split('-', n=1, expand=True)
df.insert(2, "date", cols[0])
df.insert(3, "home", game[0])
df.insert(4, "away", game[1])
df.pop("game")

# Remove unwanted events
# df = df[~df['type'].isin([
#
#     # Match Structure
#     'FormationSet',
#     'Start',
#     'End',
#     'FormationChange',
#     'SubstitutionOff',
#     'SubstitutionOn',
#     'Card',
#
#     # Keeper
#     'PenaltyFaced',
#     'KeeperSweeper',
#     'KeeperPickup',
#     'Smother',
#     'Punch',
#     'Claim',
#
#     # Not that important
#     'Dispossessed',  # Lost possession from Tackle
#     'BlockedPass',
#
#     # Rare defensive
#     'OffsideProvoked',  # Assigned to defender
#     'CornerAwarded',  # Successful when won, unsuccessful when caused
#     'ShieldBallOpp',  # Shielding ball to Opp so it goes out
#
#     # Rare
#     'BallTouch',
#     'ChanceMissed',  # Strange stat, few rows
#     'CrossNotClaimed',  # Strange stat, few rows
#     'OffsideGiven',  # Player who was offside from OffsidePass
#     'GoodSkill',  # Nice dribble
# ]
# )
# ]

# Or Choose Wanted Events
df = df[df['type'].isin([
    # Passing
    'Pass',
    'OffsidePass',

    # Shots
    'MissedShots',
    'ShotOnPost',
    'SavedShot',
    'Goal',

    # Possession
    'Aerial',  # Aerial Challenge. Always comes in pairs

    # Carrying
    'TakeOn',

    # Defensive
    'Save',  # Complementary action for SavedShot. Keeper or player
    'Clearance',
    'BallRecovery',
    'Interception',
    'Tackle',
    'Challenge',
    'Error',
    'Foul',  # Successful when received, unsuccessful when committed
]
)
]

# Now that we got all the rows we want, lets reset the index
df.reset_index(drop=True, inplace=True)


# Add relevant qualifiers as new columns (Length and angle)
lengths = []
angles = []
for idx, row in df.iterrows():
    if (idx % 10000) == 0:
        print(f"{round(idx/len(df) * 100, 1)}% - Scanning qualifiers")
    # Get qualifiers as list of JSON
    qual = ast.literal_eval(row.qualifiers.replace('\'', '"'))
    # Flags to fill w 0 if event doesn't have length or angle,
    has_length = False
    has_angle = False
    # List of qualifiers. Search for length or angle
    for q in qual:
        if q['type']['displayName'] == 'Length':
            l_val = q['value']
            lengths.append(float(l_val))
            has_length = True  # Flag

        elif q['type']['displayName'] == 'Angle':
            a_val = q['value']
            angles.append(float(a_val))
            has_angle = True  # Flag

    if not has_length:
        lengths.append(0.0)

    if not has_angle:
        angles.append(0.0)

df.insert(21, 'length', lengths)
df.insert(22, 'angle', angles)


# Now to choose columns
df = df[
    [
        'date',
        'home', 'away',
        'period', 'minute', 'second',
        'type', 'outcome_type',
        'team', 'player',
        'x', 'y', 'end_x', 'end_y',
        'length', 'angle',
        'goal_mouth_y', 'goal_mouth_z', 'blocked_x', 'blocked_y',
        'is_shot', 'is_goal',
    ]
]

# Fill NAs
df['is_shot'] = df['is_shot'].fillna('False')
df['is_goal'] = df['is_goal'].fillna('False')

# Set data types
df['date'] = pd.to_datetime(df['date']).dt.date
df = df.convert_dtypes()

# date_after = datetime.date(2023, 12, 15)
# look = df[df['date'] > date_after]

# Save
df.to_csv(f"{fp[:-4]}_upload.csv")
