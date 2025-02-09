import pandas as pd

# INPUT
stock_response_df = pd.read_csv('resources/HistoricalData/StockResponse.csv')
# INPUT - tickers
tickers_df = pd.read_csv("resources/InputTickers.csv")

# 1. get stock, date, and closing price in a dataframe
stock_close_data_df = stock_response_df[['ticker', 'date', 'close']]
#print(stock_close_data_df)

# 2. add columns and initialized
init_stock_data_df = stock_close_data_df.assign(
    percent_change=stock_close_data_df.groupby('ticker')['close'].pct_change() * 100,
    end_date=99999999,
    consecutive_days=0,
    total_percent_change=0.00)

print(init_stock_data_df)

# # 3. find percent change
# init_stock_data_df['percent_change'] = init_stock_data_df.groupby('ticker')['close'].pct_change() * 100
# print(init_stock_data_df)



# # 3. change data to start_date and add column end date. initialize the end date to 99999999
# # Rename 'date' column to 'start_date'
# stock_close_data_df.rename(columns={'date': 'start_date'}, inplace=True)

# # Add 'end_date' column and initialize it to 99999999


# # Now stock_close_data has 'start_date' and 'end_date' columns
# print(stock_close_data_df)

# # Rearrange columns to the desired order
# stock_close_data_df = stock_close_data_df[['ticker', 'start_date', 'end_date', 'close', 'percent_change']]
# print(stock_close_data_df)



# # 3. for each stock, capture the start date and end date and add up the total percent change for consecutive days the percent change went up or down 

# stock_percent_accumulated = 