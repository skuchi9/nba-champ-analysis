import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

champions_data = [
    {"year": 2023, "team": "Denver Nuggets", "win_pct": 0.683, "all_nba_players": 1},  # Jokic
    {"year": 2022, "team": "Golden State Warriors", "win_pct": 0.646, "all_nba_players": 1},  # Curry
    {"year": 2021, "team": "Milwaukee Bucks", "win_pct": 0.639, "all_nba_players": 1},  # Giannis
    {"year": 2020, "team": "Los Angeles Lakers", "win_pct": 0.732, "all_nba_players": 2},  # LeBron, AD
    {"year": 2019, "team": "Toronto Raptors", "win_pct": 0.707, "all_nba_players": 1},  # Kawhi
    {"year": 2018, "team": "Golden State Warriors", "win_pct": 0.707, "all_nba_players": 2},  # Curry, Durant
    {"year": 2017, "team": "Golden State Warriors", "win_pct": 0.817, "all_nba_players": 3},  # Curry, Durant, Draymond
    {"year": 2016, "team": "Cleveland Cavaliers", "win_pct": 0.683, "all_nba_players": 2},  # LeBron, Kyrie
    {"year": 2015, "team": "Golden State Warriors", "win_pct": 0.817, "all_nba_players": 2},  # Curry, Klay
    {"year": 2014, "team": "San Antonio Spurs", "win_pct": 0.756, "all_nba_players": 1},  # Parker
    {"year": 2013, "team": "Miami Heat", "win_pct": 0.805, "all_nba_players": 2},  # LeBron, Wade
    {"year": 2012, "team": "Miami Heat", "win_pct": 0.697, "all_nba_players": 2},  # LeBron, Wade
    {"year": 2011, "team": "Dallas Mavericks", "win_pct": 0.695, "all_nba_players": 1},  # Dirk
    {"year": 2010, "team": "Los Angeles Lakers", "win_pct": 0.720, "all_nba_players": 2},  # Kobe, Pau
]

# Convert to DataFrame
df = pd.DataFrame(champions_data)

# Calculate correlation coefficient
correlation = df['all_nba_players'].corr(df['win_pct'])

# Set style
sns.set_style("whitegrid")

# Create scatter plot with consistent size
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    data=df,
    x='all_nba_players',
    y='win_pct',
    hue='team',
    size=None,  # Remove size variation
    s=100,     # Set consistent size for all points
    palette='tab20',
    legend='brief'
)

# Add labels and title
plt.title('All-NBA Players vs Win Percentage for NBA Champions (2010-2024)', fontsize=14)
plt.xlabel('Number of All-NBA Players', fontsize=12)
plt.ylabel('Regular Season Win Percentage', fontsize=12)

# Add correlation annotation
plt.annotate(f'Correlation: {correlation:.2f}',
             xy=(0.7, 0.85),
             xycoords='axes fraction',
             fontsize=12,
             bbox=dict(boxstyle='round', fc='white'))

# Add year labels for each point with adjusted positioning
for i, row in df.iterrows():
    plt.text(row['all_nba_players']+0.05,
             row['win_pct']+0.005,  # Slight vertical offset
             str(row['year']),
             fontsize=9,
             ha='left')

# Adjust legend position and size
plt.legend(bbox_to_anchor=(1.05, 1),
           loc='upper left',
           borderaxespad=0,
           title='Team')

# Adjust x-axis ticks (since it's discrete)
plt.xticks(np.arange(1, 4, 1))

# Show plot
plt.tight_layout()
plt.show()
