################################################################################
# Purpose: Request stock data from Polygon using from date, to date, & either  #
# "minute" or "day" for time span.                                             #
#                                                                              #
# ATTN: Whenever pulling data from an API and/or AWS, you should always        #
#       Attempt to get in and out of the server they are sitting on ASAP.      #
#       Never, ever do any processing while getting data. AWS measures the     #
#       amount of time you spend accessing data                                #
################################################################################
from config import stock_key
from polygon import RESTClient

import pandas as pd
import csv
from numpy import record
import datetime
import time

#from TableFunctions import stocks_to_tables

#from source.FileFunctions import backup_input_tickers
#from source.FileFunctions import backup_daily

# TODO: THIS PROCESS CANNOT STOP EVER WHILE IT IS RUNNING OR WE HAVE A 
#       MESS THAT WE ARE NOT EQUIPT TO HANDLE!
# TODO: We need to write some code that says if we get "AttributeError: 
# 'StocksEquitiesAggregatesApiResponse' object has no attribute 'results'" then name 
# the stock and continue through the list...or something like that
# TODO: when access_polygon fails, we need write something to that either skips the 
# input record and continues (and writes the failed ticker to a file) OR
# as it is failing, captures failed ticker in FailedTickers.csv and moves 
# all tickers completed to SuccessTickers.csv (deleting them from InputTicker.csv)
# and tries to restart with the next ticker.


#def access_polygon(tickers_df, output, from_, to, time_span):
# def access_polygon(tickers_df, output, from_, to, time_span):        
    

######################################################################################
# This is where the actual access to Polygon's API occurs.                           #
######################################################################################
# def get_stock_price(stock_key, output, ticker, time_span, from_, to):
    
    
                
######################################################################################
# date format YYYY-MM-DD                                                             #
######################################################################################
def ts_to_datetime(ts) -> str: 
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d')

if __name__ == '__main__':

    # INPUT
    tickers_df = pd.read_csv("resources/InputTickers.csv")
    
    # OUTPUT
    # NOTE: IF THIS EVER STOPS, back up the stock tickers, remove the ones that have already run successfully, change the below open statements to append ('a') and restart
    # OUTPUT   
    # # TODO: move a ticker that has completed into InputTickersCompleted file.
    # if time_span == "minute": 
    #     # this file is over written, daily
    #     output = open("resources/HistoricalData/StockPricesTodaysMinutes.csv", "w")
    # else: 
    #     # this file is over written, daily
    output = open("resources/HistoricalData/StockResponse.csv", "a")
    from_ = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime('%Y-%m-%d')
    to = datetime.datetime.now().strftime('%Y-%m-%d')
    time_span = "day"
    
    # HEADER    
    record = f"ticker,date,open,high,low,close,volume,volume_weight,number_of_transactions\n" # HEADER RECORD
    output.write(record)
    count_tickers_processed = 0
    record_count = 1
    # iterating through input stocks
    for record, row in tickers_df.iterrows():
        ticker =  row['ticker']
        count_tickers_processed += 1        
        # preventing client error 429 
        if record_count > 4: 
            print(f"Wait one minute before retrieving next five stocks.")
            time.sleep(60) 
            print (ticker)
            with RESTClient(stock_key) as client:
        
                # for more information on calling this go to Polygon website
                resp = client.stocks_equities_aggregates(ticker, 1, time_span, from_, to, unadjusted=False)
                # print(f"get_stock_price: resp" + resp) 
            
                # write each resulting record to a file 
                for result in resp.results:
                    if time_span == "minute":
                        ms = int(result["t"])
                        timestamp_sec = ms/1000
                        dt = datetime.datetime.fromtimestamp(timestamp_sec) # access fromtimestamp method directly - you cannot do what you do in 
                        #print(dt)
                        record = f"{ticker},{dt},{result['o']},{result['h']},{result['l']},{result['c']},{result['v']}," \
                            f"{result['vw']},{result['n']}\n"
                        output.write(record)
                    else: # time_span == daily
                        dt = ts_to_datetime(result["t"])
                        record = f"{ticker},{dt},{result['o']},{result['h']},{result['l']},{result['c']},{result['v']}," \
                            f"{result['vw']},{result['n']}\n"
                        output.write(record)
                    # TODO: some way I got this in the middle of processing: 
                    #AttributeError: 'StocksEquitiesAggregatesApiResponse' object has no attribute 'results'
                    record_count = 1
        else: 
            print (ticker)
            with RESTClient(stock_key) as client:
        
                # for more information on calling this go to Polygon website
                resp = client.stocks_equities_aggregates(ticker, 1, time_span, from_, to, unadjusted=False)
                # print(f"get_stock_price: resp" + resp) 
                
                # write each resulting record to a file 
                for result in resp.results:
                    if time_span == "minute":
                        ms = int(result["t"])
                        timestamp_sec = ms/1000
                        dt = datetime.datetime.fromtimestamp(timestamp_sec) # access fromtimestamp method directly - you cannot do what you do in 
                        #print(dt)
                        record = f"{ticker},{dt},{result['o']},{result['h']},{result['l']},{result['c']},{result['v']}," \
                            f"{result['vw']},{result['n']}\n"
                        output.write(record)
                    else: # time_span == daily
                        dt = ts_to_datetime(result["t"])
                        record = f"{ticker},{dt},{result['o']},{result['h']},{result['l']},{result['c']},{result['v']}," \
                            f"{result['vw']},{result['n']}\n"
                        output.write(record)
                    record_count = record_count + 1
    output.close()
    print(f'count_tickers_processed: {count_tickers_processed}') 