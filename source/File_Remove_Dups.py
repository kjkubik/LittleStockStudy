################################################################################
# Purpose: This module removes duplicates from a single file                   #
#                                                                              #
################################################################################
import pandas as pd

def remove_dups(file_path):    
    # Specify the chunk size for reading the CSV file
    chunk_size = 10000  # Adjust the chunk size as needed based on your data size
    
    # Initialize a variable to keep track of the total number of duplicates dropped
    total_duplicates_dropped = 0
    
    # Define a function to process each chunk and drop duplicates
    def process_chunk(chunk):
        nonlocal total_duplicates_dropped  # Access the total_duplicates_dropped variable from the outer scope
        chunk_duplicates_dropped = chunk.drop_duplicates(subset=['ticker', 'date'])
        num_duplicates_dropped = len(chunk) - len(chunk_duplicates_dropped)
        total_duplicates_dropped += num_duplicates_dropped
        return chunk_duplicates_dropped
    
    # Read the CSV file in chunks and process each chunk
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    processed_chunks = [process_chunk(chunk) for chunk in chunks]
    
    # Concatenate the processed chunks into a single DataFrame
    df_cleaned = pd.concat(processed_chunks)
    
    # Write the cleaned DataFrame back to the file
    df_cleaned.to_csv(file_path, index=False)
    
    print(f"Duplicates removed from file '{file_path}' successfully.")
    print(f"Total number of duplicates dropped: {total_duplicates_dropped}")

if __name__ == '__main__':
    
    remove_dups(file_path)