import zipfile
import os
import csv
import pandas as pd 

#3930562 - APEX
    
# Path to the ZIP archive
input_folder = 'E:/StockData/NASDAQ/DATA/' # Assuming ZIP files are in this folder

# Output file path for combined data
output_file = 'resources/HistoricalData/Year2010-2020.csv'

try:
    # Open the output file in write mode
    with open(output_file, 'a') as combined_file:
        # Iterate through each ZIP file in the input folder
        for zip_file_name in os.listdir(input_folder):
            if zip_file_name.endswith('.zip'):
                zip_file_path = os.path.join(input_folder, zip_file_name)
                
                # Open the ZIP file
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    # Iterate through each file in the ZIP file
                    for file_name in zip_ref.namelist():
                        if file_name.endswith('.txt'):
                            # Extract the file to a temporary location
                            zip_ref.extract(file_name, path='temp')
                            temp_file_path = os.path.join('temp', file_name)
                            
                            # Read the content of the extracted file
                            with open(temp_file_path, 'r') as temp_file:
                                lines = temp_file.readlines()
                                # Write each line to the combined file after stripping newline characters
                                for line in lines:
                                    combined_file.write(line.rstrip('\n') + '\n')
                            
                            # Remove the temporary file
                            os.remove(temp_file_path)
                
                print(f"Processed ZIP file: {zip_file_name}")

    print(f"All files processed and combined into '{output_file}' successfully.")

except Exception as e:
    print(f"Error processing files: {e}")
    

# Read the CSV file into a DataFrame
file_path = 'resources/HistoricalData/Year2010-2020.csv'

df = pd.read_csv(file_path)

# Add the 'volume_weight' and 'number_of_transactions' columns with default values of 0
df['volume_weight'] = 0
df['number_of_transactions'] = 0

# Write the modified DataFrame back to the same file
df.to_csv(file_path, index=False)

print(f"Columns 'volume_weight' and 'number_of_transactions' added to '{file_path}' successfully.")
