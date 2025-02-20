import pandas as pd

outlier_file_count = 0
current_directory = ""
current_file = ""

for year in range(2010, 2025):
    filename = f"{current_directory}/{current_file}{year}.csv"

    df = pd.read_csv(filename)

    if len(df) > 5:
        outlier_file_count += 1

print(f"Number of files with outliers: {outlier_file_count}")
