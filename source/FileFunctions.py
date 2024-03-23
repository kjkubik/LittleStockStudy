import csv
import psycopg2
from config import dbname, user, password, host, port

def move_csv_to_daily_stock_data(file_date,time_frame):
    
    print(file_date)
    
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(dbname,user,password,host,port)

    # Create a cursor object
    cur = conn.cursor()

    # Open the CSV file for reading
    # INPUT file
    input_file = "resources/HistoricalData/StockPricesTodays" + time_frame + ".csv"
    print(input_file)
    with open(input_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row
    
        # Iterate over each row in the CSV file
        for row in csvreader:
            # Insert the row into the PostgreSQL table
            cur.execute(
                "INSERT INTO daily_stock_data (ticker, date, open, high, low, close, volume, volume_weight, number_of_transactions) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)",
                (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])  
            )

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()         
    

# # Define your SQL statement to insert data into a table
# sql = """
# INSERT INTO daily_stock_data (ticker, date, open, high, low, close, volume, volume_weight, number_of_transactions)
# VALUES (%s, %s, %s)
# """

# # Define the data to be inserted
# data = ('value1', 'value2', 'value3')

# # Execute the SQL statement with the data
# cur.execute(sql, data)

# # Commit the transaction
# conn.commit()

# # Close the cursor and connection
# cur.close()
# conn.close()

# MAIN
# if __name__ == '__main__':
    
#     print('Starting DatatoTables')
    
#     # move_csv_to_daily_stock_data(file_date = (datetime.datetime.now() - datetime.timedelta(days=729)).strftime('%Y-%m-%d'),
#     #                             time_frame = "Minutes")
    
#     move_csv_to_daily_stock_data(file_date = (datetime.datetime.now() - datetime.timedelta(days=729)).strftime('%Y-%m-%d'),
#                                 time_frame = "Daily")