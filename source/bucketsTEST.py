import pandas as pd

# Sample DataFrame setup
percent_change_df = pd.DataFrame({
    'ticker': ['AAOI', 'AAOI', 'AAOI', 'AAOI', 'AAOI', 'AAOI', 'AAOI', 'AAOI', 'AAOI'],
    'start_date': [20230927, 20230928, 20231001, 20231002, 20231003, 20231004, 20231005, 20231008, 20231009],
    'percent_change': [0.000000, -0.453721, 2.734731, -8.429459, -13.662791, 2.356902, -0.438596, -16.464758, -1.647989]
})

# Function to calculate consecutive days for each group (ticker)
def count_consecutive_days_for_ticker(ticker_data):
    # Compute whether percent change is the same as the previous day's change (sign-based)
    sign_change = (ticker_data['percent_change'] > 0) == (ticker_data['percent_change'].shift(1) > 0)
    
    # Count consecutive days (if the sign has not changed, continue counting)
    ticker_data['consecutive_days'] = sign_change.cumsum() + 1
    
    return ticker_data

# Initialize an empty list to hold the processed data
result_df_list = []

# Loop over each unique ticker
for ticker in percent_change_df['ticker'].unique():
    # Filter the DataFrame for the current ticker
    ticker_data = percent_change_df[percent_change_df['ticker'] == ticker]
    
    # Apply the function to calculate consecutive days
    ticker_data = count_consecutive_days_for_ticker(ticker_data)
    
    # Append the result to the list
    result_df_list.append(ticker_data)

# Concatenate all the results into a single DataFrame
final_result_df = pd.concat(result_df_list)

# Reset index after concatenating
final_result_df.reset_index(drop=True, inplace=True)

# Display the final result
print(final_result_df)
