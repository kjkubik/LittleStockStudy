from config import stock_key        
from polygon import RESTClient  
import schedule
import time
import datetime
import pandas as pd


def get_stock_data():
    # Set client 
    client = RESTClient(stock_key)

    # INPUT - tickers
    tickers_df = pd.read_csv("resources/InputTickers.csv")

    # OUTPUT - appending data onto the end of whatever is present in this file.
    output = open("resources/HistoricalData/StockResponse1.csv", "w")

    # request is called as follows: 
    from_ = (datetime.datetime.now() - datetime.timedelta(days=400)).strftime('%Y-%m-%d')
    to = datetime.datetime.now().strftime('%Y-%m-%d')
    time_span = "day"

    # HEADER    
    record = f"ticker,date,open,high,low,close,volume,volume_weight,number_of_transactions\n" # HEADER RECORD
    output.write(record)

    count_tickers_processed = 0
    record_count = 1

    print('Starting GetStocks')

    # for each stock ticker in InputTickers.csv, get stock prices
    for record, row in tickers_df.iterrows():
        ticker =  row['ticker']
        print(record_count)
        print("ticker is:" + str(ticker))
        
        # preventing client error 429 - You are limited to 5 stocks a minute
        if record_count >= 5: 
            record_count = 1
            time.sleep(60)  # Wait for a minute
        else: 
            record_count +=  1
        
        aggs = client.list_aggs(ticker, 1, time_span, from_, to)
            
        # Write each day to output
        for agg in aggs:
            # Extract the timestamp (in milliseconds)
            timestamp_ms = agg.timestamp

            # Convert to seconds
            timestamp_sec = timestamp_ms / 1000

            # Convert to a datetime object
            dt_object = datetime.datetime.fromtimestamp(timestamp_sec)

            # Format the datetime as yyyymmdd
            formatted_date = dt_object.strftime('%Y%m%d')
            
            record = f"{ticker},{formatted_date},{agg.open},{agg.high},{agg.low},{agg.close},{agg.volume},{agg.vwap},{agg.transactions}\n" # HEADER RECORD
            output.write(record)

    print("Extraction complete")


# Schedule the script to run every day
schedule.every().day.at("01:00").do(get_stock_data)

# Keep the script running and execute scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute if it's time to run the task