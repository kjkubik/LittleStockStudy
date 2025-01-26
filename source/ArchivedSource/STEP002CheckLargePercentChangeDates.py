import pandas as pd

# Load the stock data from the input file
input_file_path = 'resources/HistoricalData/StockResponse.csv'  # The input file path
df = pd.read_csv(input_file_path)

# Convert the 'date' column to datetime format using the correct format
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# Function to filter data between two specified dates
def select_data_by_dates(df, start_date, end_date):
    # Ensure that start_date and end_date are converted to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Return the filtered data by comparing to datetime objects
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Specify the date range (start and end dates)
start_date = '2024-10-22'  # Modify this as needed
end_date = '2024-11-11'    # Modify this as needed

# Specify the percentage threshold (e.g., 5% increase)
threshold = 20

# Empty list to store stocks that meet the condition
stocks_up_by_threshold = []

# Loop through each stock's data
for ticker, group in df.groupby('ticker'):
    # Filter data by the user-specified date range
    select_group = select_data_by_dates(group, start_date, end_date)
    
    # Make a deep copy of the filtered group to avoid SettingWithCopyWarning
    select_group = select_group.copy()
    
    # Calculate the percentage change between consecutive rows in the 'close' column
    select_group.loc[:, 'pct_change'] = select_group['close'].pct_change() * 100
    
    # Loop through the filtered stock data to find percentage changes above the threshold
    for i in range(1, len(select_group)):
        row = select_group.iloc[i]
        # If percentage change exceeds threshold, append the original row to the result
        if row['pct_change'] > threshold:
            # Add the 'pct_change' value to the last row of the original group
            original_row = group.loc[group['date'] == row['date']].iloc[0]
            original_row['pct_change'] = row['pct_change']  # Add the percentage change to the row
            stocks_up_by_threshold.append(original_row)

# Convert the result to a DataFrame for better visualization
result_df = pd.DataFrame(stocks_up_by_threshold)

# Specify the output file path
output_file_path = 'resources/HistoricalData/stocks_LARGE_percentage_change.csv'  # Output file path

# Write the result to a CSV file
result_df.to_csv(output_file_path, index=False)

# Print the results and confirm that it has been written to the file
print(f"Results written to {output_file_path}")
print(result_df)