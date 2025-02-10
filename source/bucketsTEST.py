import pandas as pd

# INPUT
stock_response_df = pd.read_csv('resources/HistoricalData/StockResponse.csv')
# INPUT - tickers
tickers_df = pd.read_csv("resources/InputTickers.csv")

# 1. get stock, date, and closing price in a dataframe
stock_close_data_df = stock_response_df[['ticker', 'date', 'close']]
#print(stock_close_data_df)

# 2. change date to start_date
stock_close_data_df = stock_close_data_df.rename(columns={'date': 'start_date'})

# 3. find percent change
percent_change_df = stock_close_data_df.assign(percent_change=stock_close_data_df.groupby('ticker')['close'].pct_change() * 100)

# NaN to 0.00
percent_change_df['percent_change'] = percent_change_df['percent_change'].fillna(0)

# 4. remove the close column
percent_change_df = percent_change_df.drop('close', axis = 1) 
#print(percent_change_df.head(50)) 
#print(percent_change_df.tail(50)) 

# 5. Create a dataframe with ticker, start_date, end_date, consecutive_days, 'total_percentage_change'
columns = ['ticker', 'start_date', 'end_date', 'consecutive_days', 'total_percentage_change']
total_changes_list = []  # Initialize the list to store rows

first_ticker_flag = True  # Flag to identify the first ticker
total_percentage_change = 0.00  # Initialize the percentage change accumulator

# Make sure percent_change_df is sorted by ticker and date (if not already)
percent_change_df = percent_change_df.sort_values(by=['ticker', 'start_date'])

for i in range(1, len(tickers_df)):  # Loop through each ticker
    ticker = tickers_df.iloc[i]['ticker']  # Get the ticker for the current row
    print(f"Processing {ticker}")
    sign_change = False  # Boolean to track whether the sign of the percent change has changed
    
    # Initialize flags and variables to track consecutive days and percentage change
    saved_start_date = None
    saved_end_date = None
    consecutive_days = 0
    total_percentage_change = 0.00
    
    for j in range(1, len(percent_change_df)):  # Loop through percent_change_df
        if percent_change_df['ticker'].iloc[j] == ticker:
            if first_ticker_flag:  # This is the first record for the ticker
                # Initialize values for the first row of the ticker
                saved_start_date = percent_change_df['start_date'].iloc[j]
                saved_end_date = saved_start_date
                consecutive_days = 1
                total_percentage_change = percent_change_df['percent_change'].iloc[j]
                
                first_ticker_flag = False  # Reset flag after the first ticker
                
                # Check the sign of the next record's percent change
                if j + 1 < len(percent_change_df):  # Ensure not out of range
                    last_sign_change = True if percent_change_df['percent_change'].iloc[j + 1] > 0 else False
                else:
                    break  # Exit if we are at the last record
                
            else:
                # If percent change is zero, reset and save the current streak
                if percent_change_df['percent_change'].iloc[j] == 0.00:
                    if saved_start_date is not None and saved_end_date is not None:  # Ensure initialization
                        total_changes_list.append([ticker, saved_start_date, saved_end_date, consecutive_days, total_percentage_change])
                    
                    # Reset for the new streak
                    saved_start_date = percent_change_df['start_date'].iloc[j]
                    saved_end_date = saved_start_date
                    consecutive_days = 1
                    total_percentage_change = percent_change_df['percent_change'].iloc[j]
                    
                    # Check the sign of the next record's percent change
                    if j + 1 < len(percent_change_df):  # Ensure not out of range
                        last_sign_change = True if percent_change_df['percent_change'].iloc[j + 1] > 0 else False
                    
                else:  # If percent change is non-zero
                    sign_change = True if percent_change_df['percent_change'].iloc[j] > 0 else False
                    
                    if last_sign_change == sign_change:  # If the sign is the same as the last one, accumulate
                        saved_end_date = percent_change_df['start_date'].iloc[j]  # Update end date for streak
                        consecutive_days += 1
                        total_percentage_change += percent_change_df['percent_change'].iloc[j]
                        last_sign_change = sign_change  # Update the sign for the next iteration
                        
                    else:  # If the sign has changed, save the current streak and reset for the new streak
                        if saved_start_date is not None and saved_end_date is not None:  # Ensure initialization
                            total_changes_list.append([ticker, saved_start_date, saved_end_date, consecutive_days, total_percentage_change])
                        
                        # Reset values for a new streak
                        saved_start_date = percent_change_df['start_date'].iloc[j]
                        saved_end_date = saved_start_date
                        consecutive_days = 1
                        total_percentage_change = percent_change_df['percent_change'].iloc[j]
                        
                        # Update the sign for the new streak
                        last_sign_change = sign_change
    
    # Save the final streak after the loop finishes
    if saved_start_date is not None and saved_end_date is not None:  # Ensure initialization
        total_changes_list.append([ticker, saved_start_date, saved_end_date, consecutive_days, total_percentage_change])

# Convert the list of results into a DataFrame
total_changes_df = pd.DataFrame(total_changes_list, columns=columns)

# Display the result
print(total_changes_df.head(50))
print(total_changes_df.tail(20))