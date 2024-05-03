################################################################################
# Purpose: Sorts file, treating entire record as the key                       #
################################################################################
import pandas as pd
import shutil
import os
import csv
from datetime import datetime

def sort_file(file_path):
    # Specify the chunk size for reading the CSV file, adjust the chunk size as needed based on your data size
    chunk_size = 10000  
    
    # Define a function to process each chunk
    def process_chunk(chunk):
        # Sort the chunk by 'ticker' and 'date'
        chunk_sorted = chunk.sort_values(by=['ticker', 'date'])
        return chunk_sorted    
        
    # Read the CSV file in chunks and process each chunk
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    processed_chunks = [process_chunk(chunk) for chunk in chunks]
    
    # Concatenate the processed chunks into a single DataFrame
    df_sorted = pd.concat(processed_chunks)
    
    # Sort the concatenated DataFrame again to ensure overall sorting
    df_sorted = df_sorted.sort_values(by=['ticker', 'date'])
    
    # Write the sorted DataFrame back to the file
    df_sorted.to_csv(file_path, index=False)
    
    print(f"File '{file_path}' sorted successfully.")
    
# MAIN
if __name__ == '__main__':

    sort_file(file_path)