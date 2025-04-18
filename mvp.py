import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load Excel file
file_path = "nba_player_data.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")

# Filter Regular Season games
df_regular = df[df['Season_type'] == 'Regular%20Season'].copy()

# Select desired stat categories
required_cols = ['Year', 'PLAYER', 'TEAM', 'GP', 'PTS', 'AST', 'REB', 'FGA', 'FGM']
df_regular = df_regular[required_cols].dropna()

# Compute per-game stats
df_regular['PTS_PG'] = (df_regular['PTS'] / df_regular['GP']).round(1)
df_regular['AST_PG'] = (df_regular['AST'] / df_regular['GP']).round(1)
df_regular['REB_PG'] = (df_regular['REB'] / df_regular['GP']).round(1)

# Compute field goal (FG) efficiency
df_regular['FG_EFFICIENCY'] = (df_regular['FGM'] / df_regular['FGA']).round(3)
df_regular['FG_EFFICIENCY'].replace([float('inf'), -float('inf')], 0, inplace=True)
df_regular['FG_EFFICIENCY'].fillna(0, inplace=True)

# My MVP scoring formula, favoring offensively oriented play
df_regular['MVP_SCORE'] = (
    df_regular['PTS_PG'] * 2.0 +
    df_regular['AST_PG'] * 1.0 +
    df_regular['REB_PG'] * 0.5 +
    df_regular['FG_EFFICIENCY'] * 20
).round(2)

# Top 3 MVP candidates based on my formula
top3_mvp = df_regular.sort_values(by='MVP_SCORE', ascending=False).groupby('Year').head(3).copy()

actual_mvps = {
    '2013-14': 'Kevin Durant',
    '2014-15': 'Stephen Curry',
    '2015-16': 'Stephen Curry',
    '2016-17': 'Russell Westbrook',
    '2017-18': 'James Harden',
    '2018-19': 'Giannis Antetokounmpo',
    '2019-20': 'Giannis Antetokounmpo',
    '2020-21': 'Nikola Jokic',
    '2021-22': 'Nikola Jokic',
    '2022-23': 'Joel Embiid',
    '2023-24': 'Nikola Jokic'
}

top3_mvp['ACTUAL_MVP'] = top3_mvp['Year'].map(actual_mvps)
top3_mvp['IS_ACTUAL'] = top3_mvp['PLAYER'] == top3_mvp['ACTUAL_MVP']
top3_mvp['LABEL'] = top3_mvp['Year'] + " - " + top3_mvp['PLAYER']

# Y-axis spacing for plotting
top3_mvp_sorted = top3_mvp.sort_values(by=['Year', 'MVP_SCORE'], ascending=[True, False])
unique_years = top3_mvp_sorted['Year'].unique()

grouped_positions = []
labels = []
start = 0
gap = 1.0  # gap between seasons
bar_height = 0.8

for year in unique_years:
    group = top3_mvp_sorted[top3_mvp_sorted['Year'] == year]
    n = len(group)
    positions = list(np.linspace(start, start + n - 1, n))
    grouped_positions.extend(positions)
    labels.extend(group['LABEL'])
    start += n + gap

# Plotting data
plt.figure(figsize=(14, 10))
colors = top3_mvp_sorted['IS_ACTUAL'].map({True: 'green', False: 'skyblue'}).values
bars = plt.barh(grouped_positions, top3_mvp_sorted['MVP_SCORE'], color=colors, height=bar_height)

plt.yticks(grouped_positions, labels)
plt.title('Top 3 MVP Scores by Season (Separated by Year)')
plt.xlabel('Calculated MVP Score')
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()

# Add value labels on bars
for pos, bar in zip(grouped_positions, bars):
    plt.text(bar.get_width() + 0.5, pos, f'{bar.get_width():.2f}', va='center')

plt.show()
