import pandas as pd

# Load the stock data into a pandas DataFrame
stock_data = pd.read_csv('resources/HistoricalData/StockResponse.csv', parse_dates=['date'])

# Ensure data is sorted by ticker and date (important for time-based comparisons)
stock_data.sort_values(by=['ticker', 'date'], ascending=True, inplace=True)

# Function to calculate the percentage change over a given number of days
def calculate_pct_change(data, periods):
    return data['close'].pct_change(periods=periods)

# Function to check the conditions for filtering stocks
def filter_stocks(stock_data):
    # Initialize a list to hold filtered tickers
    filtered_tickers = []

    # Initialize a list to hold the filtered stock records
    filtered_data = []

    # Group data by ticker
    grouped = stock_data.groupby('ticker')

    # Loop through each ticker group
    for ticker, ticker_data in grouped:
        # Calculate the price change for the last 7 days, 365 days, 72 days, and 20 days
        ticker_data['7_day_pct_change'] = calculate_pct_change(ticker_data, 7)
        ticker_data['365_day_pct_change'] = calculate_pct_change(ticker_data, 365)
        ticker_data['72_day_pct_change'] = calculate_pct_change(ticker_data, 72)
        ticker_data['20_day_pct_change'] = calculate_pct_change(ticker_data, 20)

        # Check if the stock has gone down in the last 7 days (7_day_pct_change < 0)
        if ticker_data.iloc[-1]['7_day_pct_change'] < 0:
            # Check if the stock has gone up over the last 365, 72, and 20 days
            if (ticker_data.iloc[-1]['365_day_pct_change'] > 0 and 
                ticker_data.iloc[-1]['72_day_pct_change'] > 0 and 
                ticker_data.iloc[-1]['20_day_pct_change'] > 0):
                
                # If all conditions are met, add the ticker to the filtered list
                filtered_tickers.append(ticker)
                filtered_data.append(ticker_data)

    return filtered_tickers, pd.concat(filtered_data)

# Apply the filter to the stock data
filtered_tickers, filtered_stocks = filter_stocks(stock_data)

# Write the filtered tickers to 'tickerFiltered.csv'
tickers_df = pd.DataFrame(filtered_tickers, columns=['ticker'])
tickers_df.to_csv('resources/HistoricalData/tickerFiltered.csv', index=False)

# Write the filtered stock records to 'stockFiltered.csv'
filtered_stocks.to_csv('resources/HistoricalData/stockFiltered.csv', index=False)

# Print the results
print(f"Filtered Tickers: {filtered_tickers}")
print(f"Filtered Stocks written to stockFiltered.csv")
