# Purpose: creates a dataframe containing a record for each day giving whether the price was closeer or lower.

import pandas as pd
import numpy as np  # Import NumPy for np.select

# Read CSV file into DataFrame (has headers)
df = pd.read_csv('resources/HistoricalData/filtered_stocks.csv')
#print(df)

# Get previous day's close and today's close
df["prev_price"] = df.groupby("ticker")["close"].shift(1)
df["todays_price"] = df["close"]

# Calculate the percent change from the previous day's close to today's close
df["percent_change"] = ((df["todays_price"] - df["prev_price"]) / df["prev_price"]) * 100

# initialize the column for accumulated percentage changes
df['accum_prcnt_chg_close'] = 0.0

# initialize the number of days up or down to 0 for df
df["days_up_or_down"] = 0
print(df.head(20))  # This will print the first 50 rows

# for each ticker, accumulate each record's percent_change and adjacent to each having the same sign
previous_ticker = None # holding area is filled after checks for current ticker
previous_sign = None # holding area is filled after checks for sign
sum_percent_changes = 0
count_days = 1

#Iterate through all records
for i in range(1,len(df)):
    #what is the current ticker?
    current_ticker = df.loc[i,'ticker'] 
    # what is the current percent?
    current_percent = df.loc[i, 'percent_change']
    # what is the current sign? 
    current_sign = '+' if current_percent >= 0 else '-'
    
    if (previous_ticker != current_ticker or previous_sign != current_sign): 
        if  previous_ticker != None:
            # place the values in sum_percent_changes and count_days into last record read
            df.loc[i - 1, 'accum_prcnt_chg_close'] = sum_percent_changes
            df.loc[i - 1, 'days_up_or_down'] = count_days

        # get ready for next accumulation
        sum_percent_changes = current_percent
        count_days = 1 # initialize the day's counted
        # get ready for the next record
        previous_ticker = current_ticker 
        previous_sign = current_sign 

    else:                 
        # continue both accumulations
        sum_percent_changes += current_percent
        count_days +=1

    # Handle the last record (after the loop ends)
    if i == len(df) - 1:
        df.loc[i, 'accum_prcnt_chg_close'] = sum_percent_changes
        df.loc[i, 'days_up_or_down'] = count_days    
    
    
                    
# Display the result for verification
print(df.head(20))

# Remove rows where 'accum_prcnt_chg_close' is 0.00
accum_prcnt_chg_df = df[df['accum_prcnt_chg_close'] != 0.00]
print(accum_prcnt_chg_df.head(20))

# Save the DataFrame to a CSV file
output_file = 'resources/HistoricalData/accumulated_data.csv'  # Specify the path and filename
accum_prcnt_chg_df.to_csv(output_file, index=False)

print(f"DataFrame has been saved to {output_file}")
    

