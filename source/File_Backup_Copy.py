################################################################################
# Purpose: Backs up any input using the file_path. The back up file name will  #
#          be in file_path_timestamp format                                    #
#                                                                              #
# NOTES: 
################################################################################    
import shutil
from datetime import datetime


def backup_file(file_path):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    
    # Create a backup file name with timestamp
    #bu_file = f"resources/InputTickers_{timestamp}.csv"
    bu_file = f"{file_path}_{timestamp}.csv"
    file_path = f"{file_path}.csv"
    
    try:
        # Copy the original file to the backup location
        shutil.copyfile(file_path, bu_file)
        print (f"Back-up file successfully created: {bu_file} ")
    
    except Exception as e:
        print(f"Error creating backup: {e}")
        
def copy_file(source_file, destination_file):
        # File paths
    # these are the final files
    # input_file = 'resources/HistoricalData/StockPricesTodaysDaily.csv'
    # output_file = 'resources/HistoricalData/StockPricesTodaysDailyAllDays.csv'
    
    # append the source file to the destination file
    try:
        # Open the source file in read mode
        with open(source_file, 'r') as source:
            # Read the content of the source file
            lines = source.read()
        
        # Open the destination file in append mode
        with open(destination_file, 'a') as dest:
            # Write all lines except the first one (header)
            dest.writelines(lines[1:])
        
        print(f"File '{source_file}' appended to '{destination_file}' successfully.")
    
    except Exception as e:
        print(f"Error appending file: {e}")
# MAIN
if __name__ == '__main__':

    if function == 'back-up':
        backup_file(file_path)
    if function == 'copy':
        copy_file(source_file,destination_file)