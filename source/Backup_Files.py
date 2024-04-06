import pandas as pd
import shutil
import os
import csv
from datetime import datetime


def backup_input_tickers():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    ticker_input = 'resources/InputTickers.csv'
    # Create a backup file name with timestamp
    bu_file = f"resources/InputTickers_{timestamp}.csv"
    
    try:
        # Copy the original file to the backup location
        shutil.copyfile(ticker_input, bu_file)
        print(f"Backup created successfully: bu_file")
    
    except Exception as e:
        print(f"Error creating backup: {e}")
    
    print (f"Input tickers have been backed up from {ticker_input} to {bu_file}")
    
def backup_daily():
    # File paths
    # these are the final files
    # input_file = 'resources/HistoricalData/StockPricesTodaysDaily.csv'
    # output_file = 'resources/HistoricalData/StockPricesTodaysDailyAllDays.csv'
    source_file = 'resources/HistoricalData/StockPricesTodaysDaily.csv'
    destination_file = 'resources/HistoricalData/CombinedStockPrices.csv'

    # append the source file to the destination file
    try:
        # Open the source file in read mode
        with open(source_file, 'r') as source:
            # Read the content of the source file
            content = source.read()
        
        # Open the destination file in append mode
        with open(destination_file, 'a') as dest:
            # Write the content of the source file to the end of the destination file
            dest.write(content)
        
        print(f"File '{source_file}' appended to '{destination_file}' successfully.")
    
    except Exception as e:
        print(f"Error appending file: {e}")
     
    # remove duplicates from the destination file
    try:
        file_path = 'resources/HistoricalData/CombinedStockPrices.csv'
        number_of_duplicates = 0
        # Create a dictionary to store unique lines and their order
        unique_lines_dict = {}

        # Read the file and remove duplicates while preserving order
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading and trailing whitespace
                if line not in unique_lines_dict:
                    unique_lines_dict[line] = True  # Mark line as seen
                    number_of_duplicates += 1

        # Write unique lines back to the file
        with open(file_path, 'w') as file:
            for line in unique_lines_dict.keys():
                file.write(line + '\n')  # Write unique lines to file

        print(f"Duplicates removed from file '{file_path}' successfully.")
        print(f"number_of_duplicates: {number_of_duplicates}")
    except Exception as e:
        print(f"Error removing duplicates: {e}") 

def find_unique_records():
    # All stocks that have made it to the database already
    file1 = 'resources/HistoricalData/CombinedStockPrices.csv'
    # All stocks received running GetAllStocksDatas
    file2 = 'resources/HistoricalData/StockPricesTodaysDaily.csv'
    # All stocks not in file1
    file3 = 'resources/HistoricalData/SendToDatabase.csv'
     
    try:
        # Read file1.csv and file2.csv into DataFrames
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        # Combine the two columns into a single column for comparison
        df1['combined'] = df1['ticker'] + df1['date']
        df2['combined'] = df2['ticker'] + df2['date']

        # Find records in file2 that are not in file1 and exclude combined column
        unique_records = df2[~df2['combined'].isin(df1['combined'])].drop(columns=['combined'])

        # Write unique records to output_file
        unique_records.to_csv(file3, index=False)

        print(f"Unique records from {file2} not in {file1} written to {file3} successfully.")
    except FileNotFoundError as fnfe:
        print(f"Error: {fnfe}. Check if file paths are correct.")
    except Exception as e:
        print(f"Error finding unique records or writing to {file3}: {e}")

# MAIN
if __name__ == '__main__':
    
    find_unique_records()
    # backup_daily()
    #backup_input_tickers()
    

