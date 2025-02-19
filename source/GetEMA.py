from polygon import RESTClient
import pandas as pd
from numpy import record
from numba import njit
import csv
import datetime
import time

# before running program, user must assign smoothing and days and TupleIndex = 0
tupleIndex = 0
smoothing = 2
firstEMADays = 2
secondEMADays = 5

# INPUT tickers
tickers_df = pd.read_csv("resources/InputTickers.csv")
print(tickers_df)
# isolate ticker, date, and closing prices in dataframe
stock_prices_df = pd.read_csv("C:/Users/kkubi/LittleStockStudy/resources/StockPrices.csv", usecols=['ticker','date','close'])
print(stock_prices_df)   
ticker_close_prices_df = stock_prices_df.groupby(["ticker"]).mean()["close"]
print (ticker_close_prices_df)

# # OUTPUT
# output = open(f"resources/OutputEMAs.csv", "w")




# # try this next...I think it will work but it is going to have to be put in a forloop 
# #df_head = df.head()
# #df_last_3 = df.tail(3) 
    
# def main():
#     # move closing prices to a list
#     close_prices_df = pd.read_csv("C:/Users/kkubi/LittleStockStudy/resources/StockPrices.csv", usecols=['Close'])
#     print(close_prices_df)
    
#     # iterating through input stocks
#     for record, row in tickers_df.iterrows():
        
#         present_ticker = row['ticker']
#         #print (present_ticker)
#         #print('first forloop:', present_ticker)
        
#         sma_flag = True
        
#         # count the number of occurances having the present ticker
#         #count_present_tickers_rows = stock_prices_df['ticker'].value_counts()[present_ticker]
#         #print(count_present_tickers_rows)
        
#         #print(stock_prices_df)
        
#         # # based on present ticker, create df
#         # present_ticker_df = stock_prices_df.loc[stock_prices_df['ticker']] == present_ticker
#         # print (present_ticker_df)
            
#         for record, row in stock_prices_df.iterrows():
            
#             if sma_flag == True:
#                 # get ticker
#                 ticker = stock_prices_df.iloc[0,0]
#                 #print (ticker)
#                 get_SMA(firstEMADays, secondEMADays, present_ticker, stock_prices_df)            
#                 sma_flag = False
#             #else:
            
            
#             # if present_ticker != ticker:
#             #    present_ticker = ticker 
#             #    print('second forloop:', ticker)
# #                 if present_ticker == ticker: 

                    
# #  THIS IS THE EMA!!!!!!!!
# # to calculate EMA(yesterday), we need to find the SMA for each given number of days
# def get_SMA(firstEMADays, secondEMADays, present_ticker, stock_prices_df):
    
#     firstSMA = stock_prices_df.iloc[0:firstEMADays,2].sum()/firstEMADays
#     print(firstSMA)

#     secondSMA = stock_prices_df.iloc[0:secondEMADays,2].sum()/secondEMADays
#     print(secondSMA)

    
    
#     # ticker_held =  row['ticker']
#     # print(ticker_held)
    
#     # if stock_df['ticker'].value_counts()[ticker_held]
    
        
        
    

#     # # get start date
#     # startDate = df.iloc[0,1]
#     # print(startDate)

    

# # # create a df for first stock ticker
# # ticker_df = df[df["ticker"].str.contains(ticker)]
# # print(ticker_df)

# # # how many rows are there?
# # ticker_df_size = len(ticker_df)
# # print(ticker_df_size)


# # for each ticker create add to a df 
# #if ticker is the same as previous ticker or if today's date is the same as yesterday, you are done with this ticker





# # the formula for EMA is this:
# # For days = n take n day's prices and divide them by n. This gives you the SMA (Simple Moving Average) - THIS IS THE FIRST EMA FOR YESTERDAY.
# # EMA(today) = (value(today) * (smoothing/(1+days)) + EMA(yesterday) * (1 - (smothing/(1+days)))
# # Do some algebra based stuff:  (smoothing/(1+days) (value(today) +)

# # Example: Say you want the EMA for days = 5 with a smoothing factor of 2 
# # and the closing price of stock ABC is {(20240105,87.00), (20240106,90.00), (20240107,91.00), (20240108,88.00), (20240109,92.00)} <-- concern dates are needed for visualization!
# # SMA = (87 + 90 + 91 + 88 + 92)/5 = 89.6 => EMA(yesterday)
# # Assign day 2 to day 1, day 3 to day 2, day 4 to day 3, day 5 to day 4. (you have to do this before reading the next closing price.)


# # Read the next record. (closing price is (20240110,90.00)
# # Assign next record's closing price to day 5.
# # Calculate EMA(today) = (90 * (2/6) + 89.6 * (1 - (2/6))) = 89.73
# # move date and EMA(today) to tuple (immutable!!!). EMATuple = ((date,EMA)) t[0] = ((20240110,89.73))
# # add 1 to the TupleIndex
# # Assign day 2 to day 1, day 3 to day 2, day 4 to day 3, day 5 to day 4. (you have to do this before reading the next closing price.)
# # What about inflation? how do you account for inflation?

# MAIN
if __name__ == '__main__':
    main()
    
    
#    	Mission to Mars - Utilized tools for scraping data from Mars websites, storing it in MongoDB, and presenting it on web page.
#Tools: BeautifulSoup, Splinter, MongoDB, Flask, HTML, CSS, ChromeDriverManager, Chrome Developer Tools, Python
