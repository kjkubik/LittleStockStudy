import pandas as pd

# Sample data (replace with your actual data)
df = pd.read_csv('resources/HistoricalData/directional.csv')

# Ensure 'date' is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Step 1: Identify the tickers with accum_prcnt_chg_close outside the range [-21, 51]
tickers_to_remove = df[df['accum_prcnt_chg_close'].lt(-21) | df['accum_prcnt_chg_close'].gt(51)]['ticker'].unique()
print(f'tickers removed {len(tickers_to_remove)}')

# Convert the array of tickers to a DataFrame
tickers_to_remove_df = pd.DataFrame(tickers_to_remove, columns=['ticker'])

extremes_file = 'resources/HistoricalData/extremes.csv'  # Specify the path and filename
tickers_to_remove_df.to_csv(extremes_file, index=False)

# Step 2: Remove all rows for these tickers
df_cleaned = df[~df['ticker'].isin(tickers_to_remove)]

# Count the number of unique tickers in df_cleaned
# num_tickers_cleaned = df_cleaned['ticker'].nunique()

# Step 3: Optionally, check the cleaned DataFrame
print(f'tickers left: {df_cleaned['ticker'].nunique()}')

output_file = 'resources/HistoricalData/extremesGone.csv'  # Specify the path and filename
df_cleaned.to_csv(output_file, index=False)