# STEP001 - kjkubik - APPROVED
# Purpose: This program request daily ticker data and places it in an output file.
from config import stock_key        
from polygon import RESTClient  
import pandas as pd
import csv
from numpy import record
import datetime
import time

# Set client 
client = RESTClient(stock_key)

# INPUT - tickers
tickers_df = pd.read_csv("resources/InputTickers.csv")
# print(tickers_df)

# OUTPUT - appending data onto the end of whatever is present in this file.
output = open("resources/HistoricalData/StockResponse.csv", "w")

# request is called as follows: 
# aggs = client.list_aggs(ticker as a string, 1, time_span = "day" (or "minute"), from_, to)

from_ = (datetime.datetime.now() - datetime.timedelta(days=500)).strftime('%Y-%m-%d')
to = datetime.datetime.now().strftime('%Y-%m-%d')
time_span = "day"


# HEADER    
record = f"ticker,date,open,high,low,close,volume,volume_weight,number_of_transactions\n" # HEADER RECORD
        
output.write(record)
count_tickers_processed = 0
record_count = 1

# MAIN
if __name__ == '__main__':

    print('Starting GetStocks')
    
    # for each stock ticker in InputTickers.csv, get stock prices
    for record, row in tickers_df.iterrows():
        ticker =  row['ticker']
        #print (record_count)
        print ("attempting ticker:" + str(ticker))
        
        # preventing client error 429 - You are limited to 5 stocks a minute
        if record_count >= 5: 
            record_count = 1
            time.sleep(60) 
        else: 
            record_count = record_count + 1
        
        aggs = client.list_aggs(ticker, 1, time_span, from_, to)
            
        # Write each day to output
        for agg in aggs:
            #Extract the timestamp (in milliseconds)
            timestamp_ms = agg.timestamp

            # Convert to seconds
            timestamp_sec = timestamp_ms / 1000

            # Convert to a datetime object
            dt_object = datetime.datetime.fromtimestamp(timestamp_sec)

            # Format the datetime as yyyymmdd
            formatted_date = dt_object.strftime('%Y%m%d')
            
            record = f"{ticker},{formatted_date},{agg.open},{agg.high},{agg.low},{agg.close},{agg.volume},{agg.vwap},{agg.transactions}\n" # HEADER RECORD
        
            output.write(record)
    
    print ("Extraction complete")


#-------------------------------------------------SOLUTION--------------------------------------------------#

# To tackle the problem of dividing large stock data into smaller files and processing each file concurrently, you can use a combination of Python libraries and techniques. Here's a step-by-step approach using Python:

# 1. Splitting the Stock Data into Smaller Files
# For this task, you can use pandas to load the data, split it into smaller chunks, and save each chunk to a separate file.

# Tools/Libraries for Splitting:
# Pandas: To read, manipulate, and split large datasets.
# CSV/Parquet: To save the data into files.
# Example to Split Data:
# python
# Copy code
# import pandas as pd

# def split_data(input_file, chunk_size=100000):
#     # Load the data into a pandas DataFrame
#     df = pd.read_csv(input_file)
    
#     # Calculate the number of chunks required
#     num_chunks = len(df) // chunk_size + 1
    
#     for i in range(num_chunks):
#         # Get a chunk of data
#         chunk = df[i * chunk_size: (i + 1) * chunk_size]
        
#         # Save the chunk to a new file
#         chunk.to_csv(f'stock_data_chunk_{i+1}.csv', index=False)

# # Example usage
# split_data('large_stock_data.csv')
# This code will read the large stock data from a file (like a CSV), divide it into chunks (100,000 records per file by default), and save each chunk into a separate file. You can adjust the chunk_size parameter if needed.

# 2. Multithreading for Processing Each File
# Once the data is split into smaller files, you can use multithreading or multiprocessing to process each file concurrently. Since you're performing I/O-bound operations (file reading/writing), multithreading is appropriate. However, if your tasks are CPU-bound (e.g., heavy data processing), consider using multiprocessing.

# Libraries for Multithreading:
# Threading: For concurrent execution of tasks.
# concurrent.futures: A high-level interface for threading and parallel execution.
# Example to Process Files with Multithreading:
# python
# Copy code
# import threading
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor

# # Function to process each chunk
# def process_file(file_name):
#     print(f"Processing {file_name}")
#     df = pd.read_csv(file_name)
#     # Example filtering (you can replace this with your custom filter)
#     filtered_df = df[df['price'] > 100]  # Example condition
#     filtered_df.to_csv(f'filtered_{file_name}', index=False)
#     print(f"{file_name} processed and saved!")

# # Function to process all files concurrently
# def process_files_concurrently(files):
#     with ThreadPoolExecutor() as executor:
#         executor.map(process_file, files)

# # Example usage
# files_to_process = [f'stock_data_chunk_{i+1}.csv' for i in range(5)]  # Adjust based on your number of chunks
# process_files_concurrently(files_to_process)
# Key Concepts:
# ThreadPoolExecutor: This allows you to efficiently execute multiple tasks in parallel using threads. executor.map() applies process_file to each file concurrently.
# Multithreading: Each file will be processed in a separate thread, which is ideal if you're waiting for I/O operations (like reading and writing files).
# 3. Considerations
# Error Handling: Ensure you add error handling in the process_file function to deal with issues such as file read/write errors.
# Performance: If you find that the process is slow or uses too much memory, you could consider using multiprocessing (for CPU-bound tasks) or Dask (for distributed processing of larger-than-memory datasets).
# File Formats: If the stock data is very large, consider using efficient file formats like Parquet instead of CSV. Parquet supports better compression and faster I/O.
# Example using Dask (for larger datasets):
# Dask is a great option if you're working with datasets that don't fit in memory. It can scale out to multiple cores or even clusters.

# python
# Copy code
# import dask.dataframe as dd

# def process_with_dask(input_file):
#     # Read the file using Dask
#     ddf = dd.read_csv(input_file)
    
#     # Filter the data (Dask operates lazily)
#     filtered_ddf = ddf[ddf['price'] > 100]
    
#     # Write the output to a new file
#     filtered_ddf.to_csv(f'filtered_{input_file}', index=False)

# # Example usage for Dask (concurrent processing in large datasets)
# process_with_dask('large_stock_data.csv')
# Dask allows you to process large files in parallel and is optimized for handling larger-than-memory data. You can combine it with threading or multiprocessing if needed for optimal performance.

# Conclusion:
# Splitting the Data: Use Pandas to split the stock data into manageable chunks (e.g., 100K records per file).
# Multithreading for Processing: Use ThreadPoolExecutor or multiprocessing to process each chunk in parallel.
# Consider File Formats: Use efficient formats like Parquet or Dask if you have very large datasets.
# This approach will help you efficiently handle large datasets, process them concurrently, and scale your solution as needed.



