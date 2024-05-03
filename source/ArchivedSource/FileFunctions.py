#!!!!!!!!!!!!!!!!!!!!!!!!!! W H E R E  A R E  T H E  5  R E C O R D S ? ? ? !!!!!!!!!!!!!!!
# TODO: you need to test this completely because I just ran to put the other records in and the count
# between the combined file (88158) and the database table (88152) is off!!!!!!!!!!!!!! 
# ONE OF THEM IS THE TABLE HEADER
############################################################################################
import pandas as pd
import shutil
import os
import csv
from datetime import datetime
from TableFunctions import stocks_to_tables

        
        
    
    

    
    
    # # Insert all new/unique records to the database 
    # stocks_to_tables(input_file = "resources/HistoricalData/SendToDatabase.csv")                 
    # # TESTING: PASS (88152 => 88323) (171 records moved, there are top headers)
    
    # # this moves daily into combined file
    # backup_daily(source_file = 'resources/HistoricalData/StockPricesTodaysDaily.csv',
    #              destination_file = 'resources/HistoricalData/CombinedStockPrices.csv')
    
    # # After moving daily into combined file we must sort the combined file and eliminate any duplicates
    # sort_file(file_path = 'resources/HistoricalData/CombinedStockPrices.csv')
    # remove_dups(file_path = 'resources/HistoricalData/CombinedStockPrices.csv')
    
    # #TESTING: PASS
    #backup_input_tickers(ticker_input = 'resources/InputTickers.csv')

    
# def sort_file(file_path):
#     # Specify the chunk size for reading the CSV file, adjust the chunk size as needed based on your data size
#     chunk_size = 10000  
    
#     # Define a function to process each chunk
#     def process_chunk(chunk):
#         # Sort the chunk by 'ticker' and 'date'
#         chunk_sorted = chunk.sort_values(by=['ticker', 'date'])
#         return chunk_sorted    
        
#     # Read the CSV file in chunks and process each chunk
#     chunks = pd.read_csv(file_path, chunksize=chunk_size)
#     processed_chunks = [process_chunk(chunk) for chunk in chunks]
    
#     # Concatenate the processed chunks into a single DataFrame
#     df_sorted = pd.concat(processed_chunks)
    
#     # Sort the concatenated DataFrame again to ensure overall sorting
#     df_sorted = df_sorted.sort_values(by=['ticker', 'date'])
    
#     # Write the sorted DataFrame back to the file
#     df_sorted.to_csv(file_path, index=False)
    
#     print(f"File '{file_path}' sorted successfully.")

# def find_unique_records(compare_input_old,compare_input_new,resulting_records_to_db):
#     # # All stocks that have made it to the database already
#     # compare_input_old = 'resources/HistoricalData/CombinedStockPrices.csv'
#     # # All stocks received running GetAllStocksDatas
#     # compare_input_new = 'resources/HistoricalData/StockPricesTodaysDaily.csv'
#     # # All stocks not in compare_input_old
#     # resulting_records_to_db = 'resources/HistoricalData/SendToDatabase.csv'
     
#     try:
#         # Read compare_input_old.csv and compare_input_new.csv into DataFrames
#         df1 = pd.read_csv(compare_input_old)
#         df2 = pd.read_csv(compare_input_new)

#         # Combine the two columns into a single column for comparison
#         df1['combined'] = df1['ticker'] + df1['date']
#         df2['combined'] = df2['ticker'] + df2['date']

#         # Find records in compare_input_new that are not in compare_input_old and exclude combined column
#         unique_records = df2[~df2['combined'].isin(df1['combined'])].drop(columns=['combined'])

#         # Write unique records to output_file
#         unique_records.to_csv(resulting_records_to_db, index=False)

#         print(f"Unique records from {compare_input_new} not in {compare_input_old} written to {resulting_records_to_db} successfully.")
#     except FileNotFoundError as fnfe:
#         print(f"Error: {fnfe}. Check if file paths are correct.")
#     except Exception as e:
#         print(f"Error finding unique records or writing to {resulting_records_to_db}: {e}")

    
# def backup_daily(source_file, destination_file):
#     # File paths
#     # these are the final files
#     # input_file = 'resources/HistoricalData/StockPricesTodaysDaily.csv'
#     # output_file = 'resources/HistoricalData/StockPricesTodaysDailyAllDays.csv'
    
#     # append the source file to the destination file
#     try:
#         # Open the source file in read mode
#         with open(source_file, 'r') as source:
#             # Read the content of the source file
#             lines = source.read()
        
#         # Open the destination file in append mode
#         with open(destination_file, 'a') as dest:
#             # Write all lines except the first one (header)
#             dest.writelines(lines[1:])
        
#         print(f"File '{source_file}' appended to '{destination_file}' successfully.")
    
#     except Exception as e:
#         print(f"Error appending file: {e}")

    
# def remove_dups(file_path):    
#     # Specify the chunk size for reading the CSV file
#     chunk_size = 10000  # Adjust the chunk size as needed based on your data size
    
#     # Initialize a variable to keep track of the total number of duplicates dropped
#     total_duplicates_dropped = 0
    
#     # Define a function to process each chunk and drop duplicates
#     def process_chunk(chunk):
#         nonlocal total_duplicates_dropped  # Access the total_duplicates_dropped variable from the outer scope
#         chunk_duplicates_dropped = chunk.drop_duplicates(subset=['ticker', 'date'])
#         num_duplicates_dropped = len(chunk) - len(chunk_duplicates_dropped)
#         total_duplicates_dropped += num_duplicates_dropped
#         return chunk_duplicates_dropped
    
#     # Read the CSV file in chunks and process each chunk
#     chunks = pd.read_csv(file_path, chunksize=chunk_size)
#     processed_chunks = [process_chunk(chunk) for chunk in chunks]
    
#     # Concatenate the processed chunks into a single DataFrame
#     df_cleaned = pd.concat(processed_chunks)
    
#     # Write the cleaned DataFrame back to the file
#     df_cleaned.to_csv(file_path, index=False)
    
#     print(f"Duplicates removed from file '{file_path}' successfully.")
#     print(f"Total number of duplicates dropped: {total_duplicates_dropped}")

# def backup_input_tickers(ticker_input):
#     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    
#     # Create a backup file name with timestamp
#     bu_file = f"resources/InputTickers_{timestamp}.csv"
    
#     try:
#         # Copy the original file to the backup location
#         shutil.copyfile(ticker_input, bu_file)
#         print (f"Input tickers successfully backed-up to {bu_file}")
    
#     except Exception as e:
#         print(f"Error creating backup: {e}")
# MAIN
if __name__ == '__main__':

    file_function(file_path1, file_path2, output_file, function)