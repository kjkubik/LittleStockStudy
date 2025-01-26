import pandas as pd
from datetime import timedelta

# Load the data (assuming it's in a CSV file)
data = pd.read_csv("resources/HistoricalData/SevenDayLow.csv", parse_dates=['date'])

# Sort the data by ticker and date to ensure chronological order
data.sort_values(by=['ticker', 'date'], ascending=True, inplace=True)

# Get today's date
today = pd.to_datetime('today')

# Function to check if the stock has gone down over the last 7 days
def check_price_30day(data, days=30):
    count_stocks_moved = 0
    # Group data by ticker
    grouped = data.groupby('ticker')

    # Open the file to write once, using 'w' for write mode
    with open('resources/HistoricalData/ThirtyDaysAreHigher.csv', 'w') as f:
        # Write the header to the CSV file
        f.write("ticker,date,close\n")
        
        # Loop through each ticker group
        for ticker, ticker_data in grouped:
            # Loop through the data starting from the 7th row (index 6) because we need at least 7 days
            for i in range(days - 1, len(ticker_data)):
                # Get the closing price 30 days ago and today
                price_30_days_ago = ticker_data.iloc[i - (days - 1)]['close']
                current_price = ticker_data.iloc[i]['close']

                # the ratio needs to be between .66 and .95 for me to pay attention to
                ratio = current_price/price_30_days_ago
                # print(ratio)
                # If the price has decreased over the last 7 days, write all records for that ticker to the file
                if (current_price > price_30_days_ago) and (ratio > 1.1):
                    
                            count_stocks_moved += 1
                            for j in range(len(ticker_data)):
                                # Write each record for the ticker to the CSV file
                                f.write(f"{ticker_data.iloc[j]['ticker']},{ticker_data.iloc[j]['date']},{ticker_data.iloc[j]['close']}\n")
                            print(f"All records for {ticker} written to 'ThirtyDaysAreHigher.csv' because it increased in price over the last 30 days.")
                            break  # No need to check further for this ticker once we've written all its records
    print(count_stocks_moved)                
# Example usage: Check price drop for all tickers
check_price_30day(data)
