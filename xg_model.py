# Data management
import numpy as np
import math
import pandas as pd

# Plotting
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch, Pitch, Standardizer

# Statistical fitting of models
import statsmodels.api as sm
import statsmodels.formula.api as smf

# ------------------------------------------------------------------------ DATA
# Standardizer
standard = Standardizer(pitch_from='opta', pitch_to='statsbomb')

df = pd.read_csv('data/LigaPro2023_all-shots.csv').iloc[:, 1:]

# Invert and normalize data
x1 = 100 - df['x']
y1 = 100 - df['y']
df.loc[:, 'x'], df.loc[:, 'y'] = standard.transform(x1, y1)

x2 = 100 - df['goal_x']
y2 = 100 - df['goal_y']
df.loc[:, 'goal_x'], df.loc[:, 'goal_y'] = standard.transform(x2, y2)

# Calculate distance
# sqrt((x_1 - x_2)^2 + (y_1 - y_2)^2)
# x_1,y_1 will be goal -> x1=120, y1=40
dx = 120 - df['x']
dy = 40 - df['y']
df.loc[:, 'distance'] = np.sqrt((dx ** 2) + (dy ** 2))

# Calculate angle
x = 120 - df['x']
y = 40 - df['y']  # this was a mess figuring out

a = np.arctan(
    (7.32 * x)
    /
    (x ** 2 + y ** 2 - (7.32 / 2) ** 2)
)

for i, angle in enumerate(a):
    if angle < 0:
        a[i] = np.pi + angle
# a = np.rad2deg(a)

df.loc[:, 'angle'] = a

# Filter headers
df = df[df['goal_type'] != 'own']
shots_df = df[df['body_part'] != 'head'].reset_index()
# Filter goals only
goals_df = shots_df[shots_df['goal'] == 1].reset_index()

# ---------------------------------------------------------------------- Figure
# pitch = VerticalPitch(
#     goal_type='box',
#     line_color='#03191E',
#     line_alpha=0.6,
#     linewidth=2,
#     # line_color='black',
#     line_zorder=2,
#     pad_bottom=-30,
#
# )
#
# fig, ax = pitch.draw()
#
# # plot shots
# xstart = shots_df['x']
# ystart = shots_df['y']
#
# shots = pitch.scatter(
#     x=xstart,
#     y=ystart,
#     ax=ax,
#     s=5,
#
#     facecolor='white',
#     edgecolors='black',
#     lw=0.3,
#     alpha=0.6,
#     zorder=3,
# )
#
# # plot goals
# xstart = goals_df['x']
# ystart = goals_df['y']
#
# goals = pitch.scatter(
#     x=xstart,
#     y=ystart,
#     ax=ax,
#     s=5,
#     facecolor='red',
#     edgecolors='black',
#     lw=0.4,
#     zorder=3,
# )
#
# plt.savefig('data/ligapro_shots.png',
#             bbox_inches='tight',
#             dpi=250
#             )
# xG model will be based on angle and distance to goal

# Two-dimensional histogram
# shotcount_dist = np.histogram(shots_df['angle'] * 180 / np.pi,
#                               bins=40,
#                               range=[0, 150]
#                               )
# goalcount_dist = np.histogram(goals_df['angle'] * 180 / np.pi,
#                               bins=40,
#                               range=[0, 150]
#                               )
# prob_goal = np.divide(goalcount_dist[0], shotcount_dist[0],
#                       out=np.zeros_like(goalcount_dist[0], dtype=float),
#                       where=shotcount_dist[0] != 0)
#
# angle = shotcount_dist[1]
# midangle = (angle[:-1] + angle[1:]) / 2

# # Make single variable model of angle
# # Using logistic regression we find the optimal values of b
# # This process minimizes the loglikelihood
# test_model = smf.glm(formula="goal ~ angle", data=shots_df,
#                      family=sm.families.Binomial()).fit()
# print(test_model.summary())
# b = test_model.params
#
# xGprob = 1 - (1 / (1 + np.exp(b[0] + b[1] * midangle * np.pi / 180)))
# fig, ax = plt.subplots(num=1)
# ax.plot(
#     midangle,
#     prob_goal,
#     linestyle='none',
#     marker='.',
#     color='black'
# )
# ax.plot(midangle, xGprob, linestyle='solid', color='black')
# ax.set_ylabel('Probability chance scored')
# ax.set_xlabel("Shot angle (degrees)")
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# plt.show()
# fig.savefig('scrapers/data/ProbabilityOfScoringAngleFit.pdf',
#             dpi=None, bbox_inches="tight")


# Now lets look at distance from goal
# Show empirically how distance from goal predicts probability of scoring
# shotcount_dist = np.histogram(shots_df['distance'],
#                               bins=40,
#                               range=[0, 70])
# goalcount_dist = np.histogram(goals_df['distance'],
#                               bins=40,
#                               range=[0, 70])
# prob_goal = np.divide(goalcount_dist[0],
#                       shotcount_dist[0])
# distance = shotcount_dist[1]
# middistance = (distance[:-1] + distance[1:]) / 2
#
# fig, ax = plt.subplots(num=1)
# ax.plot(middistance, prob_goal, linestyle='none', marker='.', color='black')
# ax.set_ylabel('Probability chance scored')
# ax.set_xlabel("Distance from goal (metres)")
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)

# Make single variable model of distance
# test_model = smf.glm(formula="goal ~ distance", data=shots_df,
# #                      family=sm.families.Binomial()).fit()
# test_model = smf.glm(formula="goal ~ distance", data=shots_df,
#                      family=sm.families.Binomial()).fit()
#
# print(test_model.summary())
# b = test_model.params
# xGprob = 1 - (1 / (1 + np.exp(b[0] + b[1] * middistance)))
# ax.plot(middistance, xGprob, linestyle='solid', color='black')
# plt.show()


# -------------------- Adding distance squared
# squaredD = shots_df['distance']**2
# shots_model = shots_df.assign(D2=squaredD)
# test_model = smf.glm(formula="goal ~ distance + D2", data=shots_model,
#                      family=sm.families.Binomial()).fit()
# print(test_model.summary())
# b=test_model.params
# xGprob = 1 - (1/(1+np.exp(b[0]+b[1]*middistance+b[2]*pow(middistance, 2))))
# fig,ax=plt.subplots(num=1)
# ax.plot(middistance, prob_goal, linestyle='none', marker= '.', color='black')
# ax.set_ylabel('Probability chance scored')
# ax.set_xlabel("Distance from goal (metres)")
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.plot(middistance, xGprob, linestyle='solid', color='black')
# plt.show()


# -------------------- Adding even more variables to the model.
# squaredD = shots_df['distance']**2
# shots_df = shots_df.assign(D2=squaredD)
# squaredX = shots_df['x']**2
# shots_df = shots_df.assign(x2=squaredX)
# squaredY = shots_df['y']**2
# shots_model = shots_df.assign(y2=squaredY)
# AX = shots_df['angle']*shots_df['x']
# shots_df = shots_df.assign(ax=AX)

# A general model for fitting goal probability
# List the model variables you want here
model_variables = ['angle', 'distance', 'x', 'y']

model = ''
for v in model_variables[:-1]:
    model = model + v + ' + '
model = model + model_variables[-1]

# Fit the model
test_model = smf.glm(formula="goal ~ " + model, data=shots_df,
                     family=sm.families.Binomial()).fit()
# print(test_model.summary())

b = test_model.params


# Return xG value for more general model
def calculate_xG(sh):
    bsum = b[0]
    for i, v in enumerate(model_variables):
        bsum = bsum+b[i+1]*sh[v]
    xG = 1 - (1/(1+np.exp(bsum)))
    return xG


# Add xG to dataframe
xG = shots_df.apply(calculate_xG, axis=1)
shots_df = shots_df.assign(xG=xG)

save_fp = 'data/LigaPro2023_xg.csv'
print(f'Saving df in {save_fp}')
shots_df.to_csv(save_fp)
#
# # ------------ Figure
# pitch = VerticalPitch(
#     goal_type='box',
#     line_color='#03191E',
#     line_alpha=0.6,
#     linewidth=2,
#     # line_color='black',
#     line_zorder=1,
#     pad_bottom=-30,
#
# )
#
# fig, ax = pitch.draw()
# team = 'Delfín'
# team_df = shots_df[shots_df['team'] == team]
#
# # Plot shots
# pitch.scatter(
#     x=team_df[team_df['goal'] == 0]['x'],
#     y=team_df[team_df['goal'] == 0]['y'],
#     s=team_df[team_df['goal'] == 0]['xG'] * 80,
#     ax=ax,
#     facecolor='white',
#     edgecolors='black',
#     alpha=0.5,
#     linewidths=1,
# )
#
# # Plot goals
# pitch.scatter(
#     x=team_df[team_df['goal'] == 1]['x'],
#     y=team_df[team_df['goal'] == 1]['y'],
#     s=team_df[team_df['goal'] == 1]['xG'] * 80,
#     ax=ax,
#     facecolor='red',
#     edgecolors='black',
#     linewidths=1,
# )
#
# shot_count = team_df[['player', 'xG']].groupby('player').count()
#
# xg_sum = team_df[['player', 'xG']].groupby('player').sum()
#
# top5 = xg_sum.head().index.to_list()
#
# plt.savefig('data/delfin_xG.png',
#             bbox_inches='tight',
#             dpi=500
#             )
#
