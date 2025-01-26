# This method helps you identify stocks that are moving in the same direction on a given day, 
# which can be useful if you are trying to group stocks that are likely to react similarly to 
# market conditions, news, or other factors. Adjust the threshold and filtering steps based 
# on your specific requirements.
import pandas as pd
import numpy as np

# Assuming you already have a dataFrame `df` with columns ['ticker', 'date', 'percent_change']
df = pd.read_csv('resources/HistoricalData/accumulated_data.csv')

# Sort the dataframe by 'date' and 'percent_change'
df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' is in datetime format
df = df.sort_values(by=['date', 'percent_change'], ascending=[True, False])  # Sorting by date and percent_change

# Initialize empty lists to collect the positive and negative stocks for each date
positive_moving_stocks = []
negative_moving_stocks = []

# Iterate through each unique date
for date in df['date'].unique():

    daily_data = df[df['date'] == date]  # Filter data for the current date
    
    # Create a new column to store the direction of the percent change (+ or -)
    df['direction'] = np.where(df['accum_prcnt_chg_close'] >= 0, 'positive', 'negative')
    # print(df.head(50))    

# save dataframe to csv file
output_file = 'resources/HistoricalData/directional.csv'  # Specify the path and filename
df.to_csv(output_file, index=False)

print(f"DataFrames has been saved to {output_file}")