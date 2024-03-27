###########################################################################
# Script: GetHighsandLows                                                 #
# Purpose: The user needs to be able to visually see the high and low     #
#          prices in a period of  time so that they can identify patterns #
#          for buying/selling a specific stock                            #
#
#          INPUT: SMA
#          OUTPUT: Starting with the first two dates in a period of time, #

# Query having columns ticker, date, high, and a column named high_low. 
# The column high_low should start with the previous date's price and 
# compare it with next date's price. If the previous date's prices is 
# lower than next date's price assign 'HIGHER THAN YESTERDAY' to next 
# day's high_low column.  If the previous date's prices is higher than 
# next date's put 'LOWER THAN YESTERDAY' in next day's high_low column. 
# If the previous date's prices is equal to next date's put 'UNCH FROM 
# YESTERDAY' in high_low column.  Then, iterate through the captured 
# data and update the high_low column so that it compares the high_low 
# column as such: If the previous day is 'LOWER THAN YESTERDAY' and the 
# next day is 'LOWER THAN YESTERDAY' , change previouse day's high_low 
# column to 'NEXT DAY IS LOWER'. If previous day is 'LOWER THAN YESTERDAY' 
# and next day is 'HIGHER THAN YESTERDAY' or vice-versa, do nothing. If 
# previous day is 'HIGHER THAN YESTERDAY' and next day is 'HIGHER THAN 
# YESTERDAY', update previous day to 'NEXT DAY IS HIGHER'.

# To keep this relatively simple, we will insert records first. 
# This is the first query to get data into the high_low table: 
import psycopg2
import pandas as pd
from config import dbconnection        

def query_highs_and_lows():
    # INPUT
    #tickers_df = pd.read_csv("resources/InputTickers.csv")

    # for record, row in tickers_df.iterrows():
    #     ticker =  row['Ticker']
    #    print(ticker)
    # if record != 'Ticker':
    try:
        # Connect to the database
        conn = psycopg2.connect(dbconnection)
        print("Connected to the database!")

        # Create a cursor object
        cursor = conn.cursor()
#TODO: once I add sma to the daily table, I will change this so that the 20 day and the 50 day SMA is used instead of the high
        # Execute a SELECT query
        select_query = f'''
                        SELECT ticker, 
                        date, 
                        LAG(high) OVER (PARTITION BY ticker ORDER BY date) AS prev_price,
                        high AS next_days_price,
                        CASE WHEN LAG(high) OVER (PARTITION BY ticker ORDER BY date) < high THEN 'HIGHEST' 
                            WHEN LAG(high) OVER (PARTITION BY ticker ORDER BY date) > high THEN 'LOWEST' 
                            ELSE 'UNCH' 
                        END AS high_low_txt
                        FROM daily_stock_data
                        where ticker = 'ADP';
                        ''' 
                        #where ticker = '{ticker}';
        
        high_low_df = pd.read_sql_query(select_query, conn)
        print (high_low_df)

                
        # The first row is 'UNCH', so we must find appropriate value:
        # What is the second row of the dataframe?
        second_row = high_low_df.loc[1, 'high_low_txt']
        print(second_row)
        
        if second_row == 'HIGHEST':
            high_low_df.loc[0, 'high_low_txt'] = "LOWEST"
        else:        
            high_low_df.loc[0, 'high_low_txt'] = "HIGHEST"
            
        #What is the value of the first row now?
        yesterdays_txt = (high_low_df.loc[0, 'high_low_txt'])    

                
        # Initialize DataFrame
        final_df = pd.DataFrame(columns=high_low_df.columns)  
        final_df = final_df.append(high_low_df.iloc[0])
        # The first row will always be written to the dataframe.
        
        # Starting with the 2nd row, we iterate through all the 
        # rows to get the lowest lows and the highest highs
        for i, row in high_low_df.iloc[1:].iterrows():
            present_txt = high_low_df.iloc[i]['high_low_txt'] 
            #print(present_txt)               
            # check if high = high or low = low
            if present_txt != yesterdays_txt: 
                
                final_df.loc[len(final_df)] = row 
                
                # assign yesterday's text the text present in this row           
                yesterdays_txt = present_txt
        print (final_df)  
        print (final_df[final_df['high_low_txt'] == 'UNCH'])          

        # Set display options to show all rows and columns
        pd.set_option('display.max_rows', None)  # Show all rows

# TODO: ONCE YOU GET the dataframe right, we will put them in the high_low table and then use the high_low table to plot points on graph. 
# TODO: put SMA on the same graph too!!! ;)
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
# MAIN
if __name__ == '__main__':
    
    query_highs_and_lows()
    print ('GetHighsandLows Processing Complete')