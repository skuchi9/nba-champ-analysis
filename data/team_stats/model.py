import pandas as pd
import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load all top8_YYYY.csv files
all_data = []
for year in range(2010, 2025):
    file_path = f"team_stats_{year}.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df["Year"] = year
        all_data.append(df)
    else:
        print(f"Warning: File not found - {file_path}")

full_data = pd.concat(all_data)

# Label champions (manually defined)
champions_by_year = {
    2010: "LAL", 2011: "DAL", 2012: "MIA", 2013: "MIA",
    2014: "SAS", 2015: "GSW", 2016: "CLE", 2017: "GSW",
    2018: "GSW", 2019: "TOR", 2020: "LAL", 2021: "MIL",
    2022: "GSW", 2023: "DEN", 2024: None  # TBD after 2024 playoffs
}

full_data["Is_Champion"] = full_data.apply(
    lambda row: 1 if row["Team"] == champions_by_year.get(row["Year"], None) else 0,
    axis=1
)


# Features and target
features = ["Wins", "Net_Rtg", "Defensive_Rtg"]
X = full_data[features]
y = full_data["Is_Champion"]

# Model 1: Logistic Regression (Baseline)
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X, y)

# Model 2: Random Forest (Advanced)
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X, y)


# Load 2024 data
current = pd.read_csv("top8_2024.csv")  # Your provided example

# Predict probabilities
current["LogReg_Probability"] = logreg.predict_proba(current[features])[:, 1]
current["RF_Probability"] = rf.predict_proba(current[features])[:, 1]

# Get final predictions (average of both models)
current["Combined_Probability"] = (current["LogReg_Probability"] + current["RF_Probability"]) / 2
contenders = current.sort_values("Combined_Probability", ascending=False)


print("\n2025 Championship Contenders:")
print(contenders[["Team", "Wins", "Net_Rtg", "Defensive_Rtg",
                 "Combined_Probability"]].head(5))

# Model evaluation
print("\nLogistic Regression Performance:")
print(classification_report(y, logreg.predict(X)))

# Feature importance
print("\nRandom Forest Feature Importance:")
for feature, importance in zip(features, rf.feature_importances_):
    print(f"{feature}: {importance:.3f}")

# Save predictions
contenders.to_csv("2025_champion_predictions.csv", index=False)
print("\nPredictions saved to '2025_champion_predictions.csv'")


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.barh(contenders["Team"], contenders["Combined_Probability"], color="darkgreen")
plt.xlabel("Championship Probability")
plt.title("2025 NBA Championship Contenders")
plt.tight_layout()
plt.savefig("2025_predictions.png", dpi=120)
print("\nVisualization saved to '2025_predictions.png'")