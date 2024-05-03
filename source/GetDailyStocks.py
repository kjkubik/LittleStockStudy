################################################################################
# Purpose: Access Polygons API's Daily Data using InputTickers.csv             #
#                                                                              #
# NOTES: Presently, this can only pull up to 2 years of data until I start     #
#        paying for a subscription. It does not pull last day's data.          #
#                                                                              #
# ATTN: Whenever pulling data from an API and/or AWS, you should always        #
#       Attempt to get in and out of the server they are sitting on ASAP.      #
#       Never, ever do any processing while getting data. AWS measures the     #
#       amount of time you spend accessing data                                #
################################################################################    
# DEPENDENCIES
import pandas as pd
import datetime
from AccessPolygon import access_polygon
from File_Sort import sort_file
from File_Compare import find_unique_records
from File_Backup_Copy import copy_file, backup_file
from CRUD_Daily_Stock_Data import insert_into_table
    
######################################################################################
# MAIN                                                                               #
######################################################################################
if __name__ == '__main__':
    
    print('Starting GetDaulyStocks')
    
    # TODO: You are going to want to delete everything but the last back-up files
    
    # INPUT
    tickers_df = pd.read_csv("resources/InputTickersTEST.csv")
    
    # back-up tickers requesting
    backup_file('resources/InputTickersTEST')
    
    # OUTPUT
    output = open("resources/HistoricalData/StockPricesTodaysDailyTEST.csv", "a")
    # TESTED
    # get DAILY stock                                                
    access_polygon(tickers_df,
                  output, 
                  from_ = (datetime.datetime.now() - datetime.timedelta(days=500)).strftime('%Y-%m-%d'),
                  to = datetime.datetime.now().strftime('%Y-%m-%d'), 
                  time_span = "day"
                  )
    
    print('We have all Daily data.')
    
    # back-up all tickers data recieved
    backup_file('resources/HistoricalData/StockPricesTodaysDailyTEST')
    
    # After daily_run completes, run FileFunctions to sort
    sort_file(file_path='resources/HistoricalData/StockPricesTodaysDailyTEST.csv')
    
    sort_file(file_path ='resources/HistoricalData/CombinedStockPricesTEST.csv') 
    
    find_unique_records(old_file_path = 'resources/HistoricalData/CombinedStockPricesTEST.csv', # All stocks that have made it to the database already
                        new_file_path = 'resources/HistoricalData/StockPricesTodaysDailyTEST.csv', # All stocks received running GetAllStocksDatas
                        output_file = 'resources/HistoricalData/SendToDatabaseTEST.csv') # All stocks not in compare_input_old  
    
    # TODO: INSERT RECORDS INTO DAILY TABLE
       
    print("GetDailyStocks has completed.")
    print("Boooo-yaaaaahhhh!\n")