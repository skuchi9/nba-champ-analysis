import pandas as pd
import os

all_data = []
for year in range(2010, 2025):
    file_path = f"team_stats_{year}.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df["Year"] = year  # Add year column
        all_data.append(df)
    else:
        print(f"Warning: File not found - {file_path}")

full_data = pd.concat(all_data)

# 2. Label champions (manually add winners here)
champions_by_year = {
    2010: "LAL", 2011: "DAL", 2012: "MIA", 2013: "MIA",
    2014: "SAS", 2015: "GSW", 2016: "CLE", 2017: "GSW",
    2018: "GSW", 2019: "TOR", 2020: "LAL", 2021: "MIL",
    2022: "GSW", 2023: "DEN", 2024: "BOS"
}

full_data["Is_Champion"] = full_data.apply(
    lambda row: 1 if row["Team"] == champions_by_year.get(row["Year"], 0) else 0,
    axis=1
)

# 3. Calculate championship thresholds
champs = full_data[full_data["Is_Champion"] == 1]

thresholds = {
    "Avg_Wins": champs["Wins"].mean(),
    "Avg_Net_Rtg": champs["Net_Rtg"].mean(),
    "Avg_Def_Rtg": champs["Defensive_Rtg"].mean(),
    "Min_Wins": champs["Wins"].quantile(0.25),  # 25th percentile
    "Min_Net_Rtg": champs["Net_Rtg"].quantile(0.25)
}

print("\nHistorical Championship Thresholds (2010-2024):")
print(f"- Average Wins: {thresholds['Avg_Wins']:.1f}")
print(f"- Average Net Rating: {thresholds['Avg_Net_Rtg']:.1f}")
print(f"- Average Defensive Rating: {thresholds['Avg_Def_Rtg']:.1f}")
print(f"- Minimum Wins (75% of champs had more than): {thresholds['Min_Wins']:.1f}")
print(f"- Minimum Net Rating (75% of champs had more than): {thresholds['Min_Net_Rtg']:.1f}")

# 4. Save the labeled data for modeling
full_data.to_csv("labeled_championship_data.csv", index=False)
print("\nSaved labeled data to 'labeled_championship_data.csv'")