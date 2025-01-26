import pandas as pd

# Load the large file into a DataFrame
large_file = 'resources/HistoricalData/ResponseLargeFile.csv'
df = pd.read_csv(large_file, parse_dates=['date'])

# # Ensure the data is sorted by 'ticker' and 'date' (if not already sorted)
# df.sort_values(by=['ticker', 'date'], ascending=True, inplace=True)

# Group by 'ticker'
grouped = df.groupby('ticker')

# Initialize variables for the splitting process
records_per_file = 100000
file_index = 1
current_file_records = []
current_record_count = 0

# Function to write records to a new file
def write_to_new_file(records, file_index):
    file_name = f"resources/HistoricalData/StockResponse{file_index}.csv"
    records_df = pd.DataFrame(records)
    records_df.to_csv(file_name, index=False)
    print(f"Written {len(records)} records to {file_name}")

# Process each ticker's records
for ticker, ticker_data in grouped:
    ticker_data_length = len(ticker_data)

    # If adding this ticker's records exceeds the 100,000 threshold, write current records and start a new file
    if current_record_count + ticker_data_length > records_per_file:
        # Write current records to file
        write_to_new_file(current_file_records, file_index)
        # Increment the file index
        file_index += 1
        # Reset for the next file
        current_file_records = []
        current_record_count = 0

    # Add the current ticker's data to the current file
    current_file_records.append(ticker_data)
    current_record_count += ticker_data_length

# Write any remaining records to the last file
if current_file_records:
    write_to_new_file(current_file_records, file_index)

print("Splitting complete.")
