import csv

def file_operations(from_script, file_path, mode, data=None, has_header=False):
    try:
        if mode not in ['r', 'w', 'a']:
            data = "Invalid mode. Supported modes are 'r', 'w', and 'a'."
            print(data)  # Print data value after return
            return data

        if mode == 'r':
            # Read mode
            with open(file_path, 'r', newline='') as file:
                if file_path.endswith('.csv'):
                    reader = csv.reader(file)
                    if has_header:
                        next(reader)  # Skip header row
                    data = list(reader)
                else:
                    data = file.read()
        elif mode == 'w':
            # Write mode
            with open(file_path, 'w', newline='') as file:
                if file_path.endswith('.csv'):
                    writer = csv.writer(file)
                    if has_header:
                        writer.writerow(data[0])  # Write header row
                        writer.writerows(data[1:])  # Write data rows
                    else:
                        writer.writerows(data)
                else:
                    file.write(data)
            data = "Data written successfully. "
        elif mode == 'a':
            # Append mode
            with open(file_path, 'a', newline='') as file:
                if file_path.endswith('.csv'):
                    writer = csv.writer(file)
                    if has_header:
                        writer.writerows(data[1:])  # Append data rows only
                    else:
                        writer.writerows(data)
                else:
                    file.write(data)
            data = "Data appended successfully. "
            
        print(f'{from_script}: Result: {data}, Mode: {mode}')  # Print data value after return
        return data
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"


# TEST ALL SCENARIOS

# Attempt using wrong mode - PASS
# output = [['Name', 'Age'], ['Alice', 25], ['Bob', 30], ['Charlie', 35]]
# file_operations('calling_script', 'resources/data_with_header.csv', 'v', output, has_header=True)
# # Expected results: "Invalid mode. Supported modes are 'r', 'w', and 'a'."

# # Attempt to read file when no file is present - PASS
# data_read_csv_with_header = file_operations('calling_script', 'resources/data_with_header.csv', 'r', has_header=True)
# print("Message when reading a file when it doesn't exist:")
# print(data_read_csv_with_header)

# # Create a CSV file with header record, writing output - PASS
# output = [['Name', 'Age'], ['Alice', 25], ['Bob', 30], ['Charlie', 35]]
# file_operations('calling_script', 'resources/data_with_header.csv', 'w', output, True)
# file_operations('calling_script', 'resources/data_with_header.csv', 'w') # empties file just created.

# # Append to a file with headers included - PASS
# output = [['Name', 'Age'], ['Alice', 25], ['Bob', 30], ['Charlie', 35]]
# file_operations('calling_script', 'resources/data_without_header_append.csv', 'a', output, has_header=False)

# Append to a file without headers included - doesn't work!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
output = [['Name', 'Age'], ['Alice', 25], ['Bob', 30], ['Charlie', 35]]
file_operations('calling_script', 'resources/data_without_header_append.csv', 'a', output, has_header=True)


# # Create a CSV file without header record using WRITE
# output = [['Name', 'Age'], ['Alice', 25], ['Bob', 30], ['Charlie', 35]]
# file_operations('resources/data_without_header_write.csv', 'w', output, has_header=False)


# # Read from the CSV file with header record
# data_read_csv_with_header = file_operations('resources/data_with_header.csv', 'r', has_header=True)
# print("Data read from CSV file with header record:")
# print(data_read_csv_with_header)
# # Expected Results: 
# # Data read from CSV file with header record:
# # [['Alice', '25'], ['Bob', '30'], ['Charlie', '35']]

# # Read from the CSV file without header record
# data_read_csv_without_header = file_operations('resources/data_with_header.csv', 'r', has_header=False)
# print("\nData read from CSV file without header record:")
# print(data_read_csv_without_header)
# # Expected Results: 
# # Data read from CSV file without header record:
# # [['Name', 'Age'], ['Alice', '25'], ['Bob', '30'], ['Charlie', '35']]