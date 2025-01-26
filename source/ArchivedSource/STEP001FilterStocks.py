import pandas as pd

# Assuming upAYear_df is the DataFrame for stocks with price increase over the last year
# Example: upAYear_df = data[data['close'] > data['close'].shift(365)] # for the last year increase

# Function to filter stocks based on multiple criteria
def filter_stocks(data, price_drop_threshold=0.2, volatility_threshold=0.05, min_volume=100000):
    # Calculate daily returns
    data['daily_return'] = data.groupby('ticker')['close'].pct_change()

    # Calculate volatility as the standard deviation of daily returns for the last 30 days
    data['volatility'] = data.groupby('ticker')['daily_return'].rolling(window=30).std().reset_index(level=0, drop=True)

    # Calculate the 7-day price change percentage (for price drop criterion)
    data['7_day_price_change'] = data.groupby('ticker')['close'].pct_change(periods=7)

    # Calculate the average volume over the last 30 days (for volume criterion)
    data['avg_volume'] = data.groupby('ticker')['volume'].rolling(window=30).mean().reset_index(level=0, drop=True)

    # Filter out stocks that don't meet the criteria
    filtered_data = data[
        (data['7_day_price_change'] > -price_drop_threshold) &  # Don't drop more than price_drop_threshold over 7 days
        (data['volatility'] < volatility_threshold) &          # Don't have too high volatility
        (data['avg_volume'] > min_volume)                       # Don't have too low trading volume
    ]

    # Drop any temporary columns used for filtering
    filtered_data = filtered_data.drop(columns=['daily_return', 'volatility', '7_day_price_change', 'avg_volume'])

    return filtered_data

# Example usage: Filter stocks from upAYear_df
filtered_stocks = filter_stocks(upAYear_df)

# Display the filtered DataFrame
print(filtered_stocks)
