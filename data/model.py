import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

years = list(range(2010, 2024))  # Training data (2010–2023)
champions = {
    2010: 'LAL', 2011: 'DAL', 2012: 'MIA', 2013: 'MIA', 2014: 'SAS',
    2015: 'GSW', 2016: 'CLE', 2017: 'GSW', 2018: 'GSW', 2019: 'TOR',
    2020: 'LAL', 2021: 'MIL', 2022: 'GSW', 2023: 'DEN', 2024: 'BOS'
}

# Load each metric
def load_metric(metric_name, years, top_n=10):
    data = []
    for year in years:
        file = f"{metric_name}_{year}.csv"
        if not os.path.exists(file):
            continue
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]
        for _, row in df.iterrows():
            rank = int(row.iloc[0])
            team = row.iloc[1].strip()
            value = float(row.iloc[2])
            label = 1 if champions.get(year) == team else 0
            data.append({'Team': team, 'Year': year, f'{metric_name}_rank': rank,
                         f'{metric_name}_value': value, 'Champion': label})
    return pd.DataFrame(data)

# Merge all metric DataFrames
metrics = ["offensive_rating", "defensive_rating", "average_scoring_margin",
           "win_percentage", "efg_percentage", "opponent_efg_percentage", "plus_minus"]

df_all = pd.DataFrame()
for metric in metrics:
    metric_df = load_metric(metric, years, top_n=10)
    df_all = pd.merge(df_all, metric_df, on=['Team', 'Year', 'Champion'], how='outer') if not df_all.empty else metric_df

df_all = df_all.fillna(0)

# Features and labels
X = df_all.drop(columns=['Team', 'Year', 'Champion'])
y = df_all['Champion']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nEvaluation on test split:")
print(classification_report(y_test, y_pred, zero_division=0))

def load_metric_for_prediction(metric_name, year):
    file = f"{metric_name}_{year}.csv"
    if not os.path.exists(file):
        return pd.DataFrame()
    df = pd.read_csv(file)
    df.columns = [col.strip() for col in df.columns]
    rows = []
    for _, row in df.iterrows():
        rank = int(row.iloc[0])
        team = row.iloc[1].strip()
        value = float(row.iloc[2])
        rows.append({'Team': team, 'Year': year,
                     f'{metric_name}_rank': rank,
                     f'{metric_name}_value': value})
    return pd.DataFrame(rows)

# Load 2025 prediction input data
year_to_predict = 2025
df_2025 = pd.DataFrame()
for metric in metrics:
    metric_df = load_metric_for_prediction(metric, year_to_predict)
    df_2025 = pd.merge(df_2025, metric_df, on=['Team', 'Year'], how='outer') if not df_2025.empty else metric_df

df_2025 = df_2025.fillna(0)

# Prepare and predict
X_2025 = df_2025.drop(columns=['Team', 'Year'])
y_2025_pred = model.predict_proba(X_2025)[:, 1]  # probability of being champion

# Normalize the probabilities so that the sum is 1 (or 100%)
total_prob = y_2025_pred.sum()  # Sum of all probabilities
y_2025_pred_normalized = y_2025_pred / total_prob  # Normalize each probability

y_2025_pred_percentage = y_2025_pred_normalized * 100  # Convert to percentage

df_2025['Champion_Probability'] = y_2025_pred_percentage

prediction_results = df_2025[['Team', 'Champion_Probability']].sort_values(by='Champion_Probability', ascending=False)
print("\n 2025 Championship Predictions (Normalized to 100%):")
print(prediction_results)

top_team = prediction_results.iloc[0]
print(f"\n🎯 Predicted 2025 Champion: {top_team['Team']} with probability {top_team['Champion_Probability']:.2f}%")
