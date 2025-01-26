############################################################################
#STEP002 - keep stocks if: 
#             1) if the stock is higher for the year
#             2) gained more than 20%, but not more than 500%
#             3) if the stock price is lower now than it was a week ago
#             4) if the stock is less that $1000
############################################################################
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import BDay
from datetime import timedelta
import numpy as np

# Load the stock data into dataframe
stock_data = pd.read_csv('resources/HistoricalData/StockResponse.csv', parse_dates=['date'], low_memory=False)
print(f"Starting with {stock_data['ticker'].nunique()} stocks")
# sort by ticker and date
stock_data.sort_values(by=['ticker', 'date'], ascending=True, inplace=True)

# Get today's date and subtract 2 business days, your input is 2 business days old!
today = pd.to_datetime('today').normalize()  # Get today's date without time
start_date = today - BDay(2)  # Subtract 2 business days
print("Start date is: ", start_date)

# calculate end date - I use 363 (instead of 365), because stocks are 2 days old
end_date = start_date - timedelta(days=363)
print("End date is: ", end_date)

# Calculate the date range for the past year, 3 months, 1 month, and 1 week
year_end_date = start_date - timedelta(days=363)  # 365 days - 2 days for the end date
month_end_date = start_date - timedelta(days=28)  # 30 days - 2 days
three_months_end_date = start_date - timedelta(days=88)  # 90 days - 2 days)
week_end_date = start_date - timedelta(days=5)  # 5 days for a week (Monday to Friday)

# list U.S. federal holidays into a set
cal = USFederalHolidayCalendar()
holiday_set = set(cal.holidays(start=end_date, end=start_date).to_pydatetime())

# Generate a list of all weekdays in the range (Monday=0, Sunday=6)
all_weekdays = pd.date_range(start=end_date, end=start_date, freq='B')  # freq='B' is business day

# Now count how many of the weekdays are not in the holidays set
valid_weekdays = [date for date in all_weekdays if date not in holiday_set]

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


def filter_stocks(stock_data, days_in_year, days_in_week):
    # Convert the 'ticker' and 'date' columns to avoid repetitive groupby operations
    stock_data['date'] = pd.to_datetime(stock_data['date'])  # Ensure 'date' is datetime type
    
    # Sort data by ticker and date (if not already sorted)
    stock_data = stock_data.sort_values(by=['ticker', 'date'])

    # Create arrays for calculations to avoid using `iloc` repeatedly
    stock_data['price_365_days_ago'] = stock_data.groupby('ticker')['close'].shift(days_in_year)
    stock_data['price_7_days_ago'] = stock_data.groupby('ticker')['close'].shift(days_in_week)

    # Calculate the ratio directly on the entire DataFrame
    stock_data['ratio'] = stock_data['close'] / stock_data['price_365_days_ago']

    # Apply conditions using vectorized operations
    condition = (
        (stock_data['close'] > stock_data['price_365_days_ago']) &
        (stock_data['ratio'] > 1.2) &
        (stock_data['ratio'] < 5.0) &
        (stock_data['close'] < stock_data['price_7_days_ago']) &
        (stock_data['close'] > 25.00) &
        (stock_data['close'] < 1000.00)
    )
    
    # Filter the stock data using the conditions
    filtered_stocks_df = stock_data[condition]
    # print(filtered_stocks_df)
    # Get the qualifying tickers
    qualifying_tickers = filtered_stocks_df['ticker'].unique()
    #print(qualifying_tickers)
    
    # Filter stock data to only include rows with tickers in the list
    filtered_data = stock_data[stock_data['ticker'].isin(qualifying_tickers)]
    #print(filtered_data.head(50))
    
    # Save the filtered stocks to CSV
    filtered_data.to_csv('resources/HistoricalData/filtered_stocks.csv', index=False)

    # Save the unique tickers to CSV
    tickers_df = pd.DataFrame(qualifying_tickers, columns=['ticker'])
    tickers_df.to_csv('resources/HistoricalData/filtered_tickers.csv', index=False)

    # Print results
    print(f"Total qualifying stocks: {len(qualifying_tickers)}")
    print(f"Total qualifying records in filtered_stocks.csv: {len(filtered_data)}")

stocks_up_for_year_df = filter_stocks(stock_data, days_in_year,days_in_week)