################################################################################
# Purpose: Given the input file's tickers, we access Polygon's API to get each #
# tickers' data for the defined amount of time. "minute" or "day" can be used. #
# 
# NOTE: Whenever pulling data from an API and/or AWS, you should always        #
#       Attempt to get in and out of the server they are sitting on ASAP.      #
#       Never, ever do any processing while getting data. AWS measures the     #
#       amount of time you spend accessing data                                #
################################################################################

from polygon import RESTClient
import pandas as pd
from numpy import record
import datetime
import time
from config import stock_key
from TableFunctions import stocks_to_tables

def daily_run():
    print('Starting GetAllStocksData')
    
    # get stocks daily data
    access_polygon(from_ = (datetime.datetime.now() - datetime.timedelta(days=729)).strftime('%Y-%m-%d'),
                  to = datetime.datetime.now().strftime('%Y-%m-%d'), 
                  time_span = "day", 
                  record_count = 1)
    print('We have all Daily data.')
    
    # preventing client error 429 
    # TURN BACK ON!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!time.sleep(60) 
    
    access_polygon(from_ = (datetime.datetime.now() - datetime.timedelta(days=729)).strftime('%Y-%m-%d'),
                  to = datetime.datetime.now().strftime('%Y-%m-%d'), 
                  time_span = "minute",
                  record_count = 1) # used to eliminate "429 Client Error: Too Many Requests for url"
    print('We have all the minute data.')
    
    print("GetAllStocksData has completed.")
    print("Boooo-yaaaaahhhh!\n")
        
    # # TODO: BACKUP FILES
    #     outputMASTER = open("resources/HistoricalData/StockPricesMinuteMaster.csv", "a")    
    #     outputMASTER = open("resources/HistoricalData/StockPricesDailyMaster.csv", "a")

    stocks_to_tables()
######################################################################################
# Showing the main routine you call doesn't need to be named 'main'.                 #
# This is one way your code can be self documenting. Also, place subroutines in the  #
# order they are called.                                                             #
######################################################################################
def access_polygon(from_, to, time_span,record_count):
    
    # TEST: Are all parameters into AccessPolygon correct?
    # print("AccessPolygon")
    # print("time_span: " + time_span)
    # print("from_: " + from_)
    # print("to: " + to)
        
    # INPUT
    tickers_df = pd.read_csv("resources/InputTickers.csv")
    
    # OUTPUT
    if time_span == "minute": 
        # this file is over written, daily
        output = open("resources/HistoricalData/StockPricesTodaysMinutes.csv", "w")
    else: 
        # this file is over written, daily
        output = open("resources/HistoricalData/StockPricesTodaysDaily.csv", "w")
        
    record = f"Ticker,Date,Open,High,Low,Close,Volume,VolumeWeight,NumberOfTransactions\n" # HEADER RECORD
    output.write(record)
    
    # iterating through input stocks
    for record, row in tickers_df.iterrows():
        ticker =  row['Ticker']
        
        # preventing client error 429 
        if record_count > 5: 
            print(f"Wait one minute before retrieving next five stocks.")
            time.sleep(60) 
            print (ticker)
            get_stock_price(output, stock_key, ticker, time_span, from_, to)
            record_count = 1
        else: 
            print (ticker)
            get_stock_price(output, stock_key, ticker, time_span, from_, to)
            record_count = record_count + 1
            
    output.close()
    
######################################################################################
# This is where the actual access to Polygon's API occurs.                           #
######################################################################################
def get_stock_price(output, client_key, ticker, time_span, from_, to):
    
    # TEST: Are all stocks itterated through?
    # print("In get_stock_price.") 
    # print("ticker: " + ticker)
        
    with RESTClient(client_key) as client:
        
        # for more information on calling this go to Polygon website
        resp = client.stocks_equities_aggregates(ticker, 1, time_span, from_, to, unadjusted=False)
        # print(f"get_stock_price: resp" + resp) 
        
        # write each resulting record to a file
        # TODO: Instead insert records to stock_API_data table    
        for result in resp.results:
            if time_span == "minute":
                ms = int(result["t"])
                timestamp_sec = ms/1000
                dt = datetime.datetime.fromtimestamp(timestamp_sec) # access fromtimestamp method directly - you cannot do what you do in 
                #print(dt)
                record = f"{ticker},{dt},{result['o']},{result['h']},{result['l']},{result['c']},{result['v']}," \
                     f"{result['vw']},{result['n']}\n"
                output.write(record)
            else: 
                dt = ts_to_datetime(result["t"])
                record = f"{ticker},{dt},{result['o']},{result['h']},{result['l']},{result['c']},{result['v']}," \
                     f"{result['vw']},{result['n']}\n"
                output.write(record)
                
            

######################################################################################
# date format YYYY-MM-DD                               .                                #
######################################################################################
def ts_to_datetime(ts) -> str: 
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d')

######################################################################################
# MAIN                                                                               #
######################################################################################
if __name__ == '__main__':
    
    daily_run()
    