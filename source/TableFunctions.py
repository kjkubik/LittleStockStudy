import csv
import psycopg2

def move_csv_to_daily_stock_data(file_date,time_frame):
    
    print(file_date)
    
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="Stock_Data",
        user="postgres",
        password="P05t1n9!",
        host="localhost",
        port="5432"
    )

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
    