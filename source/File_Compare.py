################################################################################
# Purpose: This module compares two files and moves resulting records to an    #
#          output file.                                                        #
#                                                                              #
# NOTES: There are several ways in which a file can be compared against        #
#        another. Below is a description of each compare method created.       #
#                                                                              #
# find_unique_records: This method first removes any duplicate records from    #
#                      new file before comparing the old and new file. After   #
#                      that, it compares the old and new files, generating     #
#                      an output file containing records not in old file.      #
################################################################################
import pandas as pd
from File_Remove_Dups import remove_dups

def find_unique_records(old_file_path, new_file_path, output_file):
     
    try:
        # remove duplicates from new file to prevent duplicate records ending up in resulting file
        remove_dups(new_file_path)
        
        # Read old_file_path.csv and new_file_path.csv into DataFrames
        df1 = pd.read_csv(old_file_path)
        df2 = pd.read_csv(new_file_path)
        
        # Combine the two columns into a single column for comparison
        df1['combined'] = df1['ticker'] + df1['date']
        df2['combined'] = df2['ticker'] + df2['date']

        # Find records in new_file_path that are not in old_file_path and exclude combined column
        unique_records = df2[~df2['combined'].isin(df1['combined'])].drop(columns=['combined'])

        # Write unique records to output_file
        unique_records.to_csv(output_file, index=False)

        print(f"Unique records have been written to {output_file} successfully.")
        
    except FileNotFoundError as fnfe:
        print(f"Error: {fnfe}. Check if file paths are correct.")
    except Exception as e:
        print(f"Error finding unique records or writing to {output_file}: {e}")
        
# MAIN
if __name__ == '__main__':

    find_unique_records(old_file_path, new_file_path, output_file)