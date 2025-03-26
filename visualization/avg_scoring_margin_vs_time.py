import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

# Initialize dictionary to store yearly averages
yearly_averages = {}

# Process each file
for year in range(2010, 2025):
    filename = f"average_scoring_margin_{year}.csv"
    try:
        if os.path.exists(filename):
            df = pd.read_csv(filename)

            # Calculate league average for this year
            league_avg = df['Average Scoring Margin'].mean()
            yearly_averages[year] = league_avg

            print(f"Processed {year}: {league_avg:.2f} average margin")
        else:
            print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error processing {year}: {str(e)}")

# Convert to DataFrame for plotting
trend_data = pd.DataFrame({
    'Year': list(yearly_averages.keys()),
    'League Avg Margin': list(yearly_averages.values())
})

# Create plot
plt.plot(trend_data['Year'], trend_data['League Avg Margin'],
         marker='o', linestyle='-', linewidth=2.5, markersize=8,
         color='#1f77b4')

# Add title and labels
plt.title('NBA Top-5 Teams Average Scoring Margin (2010-2024)', fontsize=16)
plt.xlabel('Season Year', fontsize=12)
plt.ylabel('Average Scoring Margin', fontsize=12)
plt.xticks(range(2010, 2025, 1), rotation=45)

# Add trend line
z = np.polyfit(trend_data['Year'], trend_data['League Avg Margin'], 1)
p = np.poly1d(z)
plt.plot(trend_data['Year'], p(trend_data['Year']), "r--",
         label=f'Trend (Slope: {z[0]:.3f} pts/year)')

# Add annotations for max/min years
max_year = trend_data.loc[trend_data['League Avg Margin'].idxmax()]
min_year = trend_data.loc[trend_data['League Avg Margin'].idxmin()]
plt.annotate(f'Max: {max_year["League Avg Margin"]:.2f} ({max_year["Year"]})',
             xy=(max_year['Year'], max_year['League Avg Margin']),
             xytext=(10, 10), textcoords='offset points')
plt.annotate(f'Min: {min_year["League Avg Margin"]:.2f} ({min_year["Year"]})',
             xy=(min_year['Year'], min_year['League Avg Margin']),
             xytext=(10, -20), textcoords='offset points')

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
