# STEP002 - kjkubik - APPROVED: NO!!!! needs comments corrected/shortened or both!
# Filtering all stocks received by this criteria. Note: The ratio is over a year's time.
    # condition = (
    #     (stock_data['close'] > stock_data['price_365_days_ago']) &
    #     (stock_data['ratio'] > 1.75) &
    #     (stock_data['ratio'] < 5.0) &
    #     (stock_data['close'] < stock_data['price_7_days_ago']) &
    #     (stock_data['close'] > 25.00) &
    #     (stock_data['close'] < 1000.00)
    # )
#
# Instructions: Change start_date. You are always going to be two days behind so keep the other days as-is
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import BDay
from datetime import timedelta
import numpy as np

# Load the stock data into dataframe
stock_data = pd.read_csv('resources/HistoricalData/StockResponse1.csv', parse_dates=['date'], low_memory=False)
print(f"Starting with {stock_data['ticker'].nunique()} stocks")
# sort by ticker and date
#stock_data.sort_values(by=['date','ticker'], ascending=True, inplace=True)

# Define the date range
start_date = pd.to_datetime('2024-01-02') # must be a business day!
end_date = pd.to_datetime('2024-01-21') 

# we have to find the actual number of business days recorded 
# count the number of business days
business_days = len(pd.date_range(start=start_date, end=end_date, freq='B'))  # freq='B' is business day
print(f'business days between {start_date} and {end_date} : {business_days}') 

# # count the number of holidays
# cal = USFederalHolidayCalendar()
# holidays = len(set(cal.holidays(start=start_date, end=end_date).to_pydatetime()))
# print(f'holidays:{holidays}') # 2

# # actual number of business days
# actual_business_days = range_business_days - holidays # WHY !?!?!?!?!?
# print(type(actual_business_days))
# print(actual_business_days)

# we need to get all records needed
start_date_for_all_records = start_date - timedelta(days=business_days)
print(f'We start getting data on this date: {start_date_for_all_records}')

# Filter the DataFrame to include only rows between the specified dates
stock_data_between_dates = stock_data[(stock_data['date'] >= start_date_for_all_records) & (stock_data['date'] <= end_date)]
#print(stock_data_between_dates)                           


# date_xdays_from_end_date will be used to see if end close price is less than 7 days ago.
date_xdays_from_end_date = end_date - timedelta(days=7)  
print(date_xdays_from_end_date)

# count the number of business days within timeframe (x days ago)
x_business_days = len(pd.date_range(start=date_xdays_from_end_date, end=end_date, freq='B'))  # freq='B' is business day
print(type(x_business_days))
print(x_business_days)


# count the number of holidays in last week
cal = USFederalHolidayCalendar()
x_holidays = len(set(cal.holidays(start=date_xdays_from_end_date, end=end_date).to_pydatetime()))

# actual number of days in the last seven days
actual_x_days = x_business_days - x_holidays
print(actual_x_days)

def filter_stocks(stock_data_between_dates, business_days, x_business_days):
    # Sort data by ticker and date (if not already sorted)
    #stock_data_between_dates = stock_data_between_dates.sort_values(by=['ticker', 'date'])
    #print(stock_data_between_dates.head(50))
    
    # Create arrays for calculations to avoid using `iloc` repeatedly
    stock_data_between_dates['price_x_days_ago'] = stock_data_between_dates.groupby('ticker')['close'].shift(x_business_days)
    stock_data_between_dates['price_actual_business_days'] = stock_data_between_dates.groupby('ticker')['close'].shift(36)
    print(stock_data_between_dates.head(60))
    
    # Calculate the ratio directly on the entire DataFrame
    stock_data_between_dates['ratio'] = stock_data_between_dates['close'] / stock_data_between_dates['price_actual_business_days']
    print(stock_data_between_dates.head(60))
    # Apply conditions using vectorized operations
    condition = (
        (stock_data_between_dates['close'] > stock_data_between_dates['price_actual_business_days']) &
        (stock_data_between_dates['ratio'] > 1.0) &
        (stock_data_between_dates['ratio'] < 5.0) &
        (stock_data_between_dates['close'] < stock_data_between_dates['price_x_days_ago']) &
        (stock_data_between_dates['close'] > 15.00) &
        (stock_data_between_dates['close'] < 600.00)
    )
    
    # Filter the stock data using the conditions
    filtered_stocks_df = stock_data_between_dates[condition]
    # print(filtered_stocks_df)
    # Get the qualifying tickers
    qualifying_tickers = filtered_stocks_df['ticker'].unique()
    print(qualifying_tickers)
    
    # The result, filtered_data, contains only rows from stock_data_between_dates that have qualifying tickers
    # Filter stock data to only include rows with tickers in the list
    filtered_data = stock_data[stock_data['ticker'].isin(qualifying_tickers)]
    filtered_data = stock_data[(stock_data['date'] >= start_date) & (stock_data['date'] <= end_date)]
    print(filtered_data.head(60))
    
# #     # Save the filtered stocks to CSV
# #     filtered_data.to_csv('resources/HistoricalData/filtered_stocks.csv', index=False)

# #     # Save the unique tickers to CSV
# #     tickers_df = pd.DataFrame(qualifying_tickers, columns=['ticker'])
# #     tickers_df.to_csv('resources/HistoricalData/filtered_tickers.csv', index=False)

#     # Print results
#     print(f"Total qualifying stocks: {len(qualifying_tickers)}")
#     #print(f"Total qualifying records in filtered_stocks.csv: {len(filtered_data)}")

stocks_up_df = filter_stocks(stock_data_between_dates, business_days, x_business_days)

