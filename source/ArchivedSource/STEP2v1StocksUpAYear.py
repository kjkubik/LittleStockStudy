import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from datetime import timedelta

# Load the stock data into a pandas DataFrame
stock_data = pd.read_csv('resources/HistoricalData/StockResponse.csv', parse_dates=['date'])

# Ensure data is sorted by ticker and date (important for time-based comparisons)
stock_data.sort_values(by=['ticker', 'date'], ascending=True, inplace=True)

# Get today's date (start date)
start_date = pd.to_datetime('11/17/2024')

# Calculate the date 365 days ago (end date)
end_date = start_date - timedelta(days=365)

# Calculate the date range for the past year, 3 months, 1 month, and 1 week
year_end_date = start_date - timedelta(days=363)  # 365 days minus 2 days for the end date
month_end_date = start_date - timedelta(days=28)  # 28 days for approximately 1 month
three_months_end_date = start_date - timedelta(days=88)  # Approx 3 months (90 days)
week_end_date = start_date - timedelta(days=5)  # 5 days for a week (Monday to Friday)

# Generate a list of U.S. federal holidays between today and 365 days ago
cal = USFederalHolidayCalendar()
holidays = cal.holidays(start=end_date, end=start_date).to_pydatetime()

# Convert holidays list to a set of datetime objects for faster lookup
holiday_set = set(holidays)

# Generate a list of all weekdays in the range (Monday=0, Sunday=6)
all_weekdays = pd.date_range(start=end_date, end=start_date, freq='B')  # freq='B' is business day

# Now count how many of the weekdays are not in the holidays set
valid_weekdays = [date for date in all_weekdays if date not in holiday_set]

volume_tolerance = 1000000
# Function to count valid weekdays for a given period
def count_valid_weekdays(start_date, end_date, holiday_set):
    all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
    valid_weekdays = [date for date in all_weekdays if date not in holiday_set]
    return len(valid_weekdays)

# Calculate the number of valid weekdays for each period
days_in_year = count_valid_weekdays(end_date, start_date, holiday_set)
days_in_week = count_valid_weekdays(week_end_date, start_date, holiday_set)
days_in_month = count_valid_weekdays(month_end_date, start_date, holiday_set)
days_in_three_months = count_valid_weekdays(three_months_end_date, start_date, holiday_set)

# Print the results
print(f"Days in year (valid weekdays excluding holidays): {days_in_year}")
print(f"Days in week (valid weekdays excluding holidays): {days_in_week}")
print(f"Days in month (valid weekdays excluding holidays): {days_in_month}")
print(f"Days in 3 months (valid weekdays excluding holidays): {days_in_three_months}")


# Function to check if the stock has gone up over the last 365 days
def filter_stocks(stock_data, days_in_year, days_in_week, days_in_month, days_in_three_months):
    # Initialize an empty list to store the upAYears (entire records)
    stocks_up_for_year = []
    qualifying_tickers = []
    
    # Group data by ticker
    grouped = stock_data.groupby('ticker')
    print(f"Starting with {len(grouped)} stocks")

    # Loop through each ticker group
    for ticker, ticker_data in grouped:
    
        for i in range(days_in_year - 1, len(ticker_data)):
    
            # Get the closing prices for different time periods
            price_365_days_ago = ticker_data.iloc[i - days_in_year]['close']
            price_7_days_ago = ticker_data.iloc[i - days_in_week]['close']
            price_22_days_ago = ticker_data.iloc[i - days_in_month]['close']
            price_78_days_ago = ticker_data.iloc[i - days_in_three_months]['close']
            current_price = ticker_data.iloc[i]['close']
            
            # Get the volume for different time periods
            volume_365_days_ago = ticker_data.iloc[i - days_in_year]['volume']
            volume_7_days_ago = ticker_data.iloc[i - days_in_week]['volume']
            volume_22_days_ago = ticker_data.iloc[i - days_in_month]['volume']
            volume_78_days_ago = ticker_data.iloc[i - days_in_three_months]['volume']
            current_volume = ticker_data.iloc[i]['volume']
            
                
            # Calculate the ratio
            ratio = current_price / price_365_days_ago

            # Apply the conditions to qualify the stock
            if (current_price > price_365_days_ago) and (ratio > 1.75) and (ratio < 5.0) and \
               (current_price < price_7_days_ago) and (current_price > price_22_days_ago) and (current_price > price_78_days_ago) and \
               (current_volume < volume_tolerance) and (volume_365_days_ago < volume_tolerance) and \
               (volume_7_days_ago < volume_tolerance) and (volume_22_days_ago < volume_tolerance) and \
               (volume_22_days_ago > volume_365_days_ago):
               
                stocks_up_for_year.append(ticker_data)
                qualifying_tickers.append(ticker)
                break  # No need to check further records for this ticker

    # Concatenate the qualifying stock records into a single DataFrame
    filtered_stocks_df = pd.concat(stocks_up_for_year, ignore_index=True) if stocks_up_for_year else pd.DataFrame()

    # Save all the qualifying stock records to filtered_stocks.csv
    if not filtered_stocks_df.empty:
        filtered_stocks_df.to_csv('resources/HistoricalData/filtered_stocks.csv', index=False)

        # Save the unique tickers to filtered_tickers.csv
        unique_tickers = set(qualifying_tickers)

        # Convert the set of unique tickers to a DataFrame
        tickers_df = pd.DataFrame(list(unique_tickers), columns=['ticker'])

        # Write the DataFrame to a CSV file
        tickers_df.to_csv('resources/HistoricalData/filtered_tickers.csv', index=False)

    # Print the results
    print(f"Total qualifying stocks: {len(unique_tickers)}")
    print(f"Total qualifying records in filtered_stocks.csv: {len(filtered_stocks_df)}")

stocks_up_for_year_df = filter_stocks(stock_data, days_in_year,days_in_week, days_in_month, days_in_three_months)
