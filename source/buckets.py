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
print(percent_change_df.head(50)) 
#print(percent_change_df.tail(50)) 

# 5. Create a dataframe with ticker, start_date, end_date, consecutive_days, 'total_percentage_change'
columns = ['ticker', 'start_date', 'end_date', 'consecutive_days', 'total_percentage_change']
total_changes_list = []

first_ticker_flag = True
total_percentage_change = 0.00

for i in range(0, len(tickers_df)): 
    ticker = tickers_df.iloc[i]['ticker']  # Get the ticker for the current row
    #print(ticker)
    sign_change = False
    
    # Initialize flags and variables to track consecutive days and percentage change
    saved_start_date = 99999999
    saved_end_date = 99999999
    consecutive_days = 0
    total_percentage_change = 0.00
    
    for j in range(0, len(percent_change_df)): 
        if percent_change_df['ticker'].iloc[j] == ticker:
            if first_ticker_flag: # this is the first record in the file
                # initialize values for dataframe
                saved_start_date = percent_change_df['start_date'].iloc[j+1]
                saved_end_date = saved_start_date 
                consecutive_days = 0
                total_percentage_change = percent_change_df['percent_change'].iloc[j]
                
                first_ticker_flag = False
                # we are about to read the rest of the records in a set of tickers, 
                # we need to know the next records percent_change_sign before we start
                last_sign_change = True if percent_change_df['percent_change'].iloc[j+1] > 0 else False
                
            else:
                if percent_change_df['percent_change'].iloc[j] == 0.00: # we are on the first record for a ticker
                    # save off values for last ticker
                    total_changes_list.append([ticker, saved_start_date, saved_end_date, consecutive_days, total_percentage_change])
                    
                    # we are about to read the rest of the records in a set of tickers, 
                    # we need to know the next records percent_change_sign before we start
                    last_sign_change = True if percent_change_df['percent_change'].iloc[j+1] > 0 else False
                
                    # initialize values for dataframe
                    saved_start_date = percent_change_df['start_date'].iloc[j]
                    saved_end_date = saved_start_date 
                    consecutive_days = 1
                    total_percentage_change = percent_change_df['percent_change'].iloc[j]
                    
                    #print(saved_start_date)
                    
                else: # rest of records
                    # find if the record has a neg or pos percent
                    sign_change = True if percent_change_df['percent_change'].iloc[j] > 0 else False
                    
                    if last_sign_change == sign_change: 
                        saved_end_date = percent_change_df['start_date'].iloc[j] # when there's a change we have last date saved
                        consecutive_days += 1
                        total_percentage_change += percent_change_df['percent_change'].iloc[j]
                        
                        last_sign_change = sign_change
                        
                    else: # the sign has changed
                        # save values
                        total_changes_list.append([ticker, saved_start_date, saved_end_date, consecutive_days, total_percentage_change])
                        
                        # initialize values for dataframe
                        saved_start_date = percent_change_df['start_date'].iloc[j]
                        saved_end_date = saved_start_date 
                        consecutive_days = 1
                        total_percentage_change = percent_change_df['percent_change'].iloc[j]
                        last_sign_change = sign_change
                        
# save the final row for the last streak of consecutive days
total_changes_list.append([ticker, saved_start_date, saved_end_date, consecutive_days, total_percentage_change])

# Convert the list of results into a DataFrame
total_changes_df = pd.DataFrame(total_changes_list, columns=columns)


print(total_changes_df.head(50)) 
#print(total_changes_df.tail(50))                       
    
                