

def split_file(input_file, output_prefix, max_records=200000):
    # Open the large file for reading
    with open(input_file, 'r') as infile:
        # Read the header of the file (if applicable)
        header = infile.readline()
        
        # Initialize variables for output file handling
        file_count = 1
        record_count = 0
        outfile = None
        
        # Loop through the file line by line
        for line in infile:
            # If it's time to start a new file
            if record_count == 0:
                # Open a new output file
                output_filename = f"{output_prefix}_{file_count}.csv"
                outfile = open(output_filename, 'w')
                # Write the header to each output file
                outfile.write(header)
            
            # Write the current line to the output file
            outfile.write(line)
            record_count += 1
            
            # If we've reached the max number of records, move to the next file
            if record_count == max_records:
                outfile.close()  # Close the current output file
                file_count += 1  # Increment the file count for the next file
                record_count = 0  # Reset record count for the next file
        
        # Ensure the last output file is closed
        if outfile:
            outfile.close()

    print(f"File split complete. {file_count - 1} files created.")

# Example usage
input_file = 'large_file.csv'  # Path to your large input file
output_prefix = 'output'  # Prefix for the smaller files
split_file(input_file, output_prefix)
