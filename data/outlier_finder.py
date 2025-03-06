import pandas as pd

outlier_file_count = 0

top_five_files = {"average_scoring_margin", "defensive_rating", "efg_percentage", "offensive_rating", "win_percentage"}
top_ten_files = {"defensive_efficiency", "offensive_efficiency", "opponent_efg_percentage", "plus_minus"}

all_files = top_five_files | top_ten_files

outlier_counts = {file: 0 for file in all_files}

for year in range(2010, 2025):
    for file in all_files:
        filename = f"{file}/{file}_{year}.csv"

        try:
            df = pd.read_csv(filename)

            if (file in top_five_files and len(df) > 5) or (file in top_ten_files and len(df) > 10):
                outlier_counts[file] += 1
                outlier_file_count += 1

        except FileNotFoundError:
            print(f"File not found: {filename}")

for file, count in outlier_counts.items():
    if count > 1:
        print(f"{file}: {count} years have an outlier")
    elif count == 0:
        print(f"{file} has no outliers")
    else:
        print(f"{file}: {count} year has an outlier")

print(f"Total number of files with outliers: {outlier_file_count}")
