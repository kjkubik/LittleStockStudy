import csv
import psycopg2
import datetime
from config import dbconnection

def insert_into_table(input_file, table_name):
    print('Starting DatatoTables')
    
    # move_csv_to_daily_stock_data(file_date = (datetime.datetime.now() - datetime.timedelta(days=729)).strftime('%Y-%m-%d'),
    #                              time_frame = "Minutes")

    move_csv_to_daily_stock_data(input_file,
                                 file_date = (datetime.datetime.now() - datetime.timedelta(days=729)).strftime('%Y-%m-%d'),
                                 time_frame = "Daily")
    
def move_csv_to_daily_stock_data(input_file, file_date, time_frame):
    
    print(file_date)
    print(time_frame)
    
    if time_frame == "Daily":
        
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(dbconnection)

        # Create a cursor object
        cur = conn.cursor()

        # Open the CSV file for reading
        # INPUT file
#       input_file = "resources/HistoricalData/StockPricesTodaysDaily" + time_frame + ".csv"
        
        with open(input_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row 
        # TODO: and by any chance you need to restart the file again, you need to skip any line with 'Ticker,Date,Open,High,Low,Close,Volume,VolumeWeight,NumberOfTransactions' in it
            # Iterate over each row in the CSV file
            for row in csvreader:
                cur.execute(
                    "INSERT INTO daily_stock_data (ticker, date, open, high, low, close, volume, volume_weight, number_of_transactions) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)",
                    (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])  
                )
            # else: # "Minute"
            #         # Insert the row into the PostgreSQL table
            #         cur.execute(
            #             "INSERT INTO minute_stock_data (ticker, date, open, high, low, close, volume, volume_weight, number_of_transactions) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)",
            #             (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])  
            #         )
        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()
    else: # "Minute":
            
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(dbconnection)

        # Create a cursor object
        cur = conn.cursor()


        # Open the CSV file for reading
        # INPUT file
        # input_file = "resources/HistoricalData/Year2010-2020.csv"
        #input_file = "resources/HistoricalData/StockPricesTodays" + time_frame + ".csv"
        print(input_file)
        
        
        with open(input_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row
        
            # Iterate over each row in the CSV file
            for row in csvreader:
                cur.execute(
                    "INSERT INTO minute_stock_data (ticker, date, open, high, low, close, volume, volume_weight, number_of_transactions) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)",
                    (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])  
                )
        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

# MAIN
if __name__ == '__main__':
    
    insert_into_table(input_file = "resources/HistoricalData/SendToDatabase.csv")
    # stocks_to_tables(input_file = "resources/HistoricalData/Year2010-2020.csv")
    print ('All data in tables. Processing Complete')