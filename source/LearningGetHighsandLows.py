###########################################################################
# Script: GetHighsandLows                                                 #
# Story: The user needs to be able to visually see the high and low       #
#        prices in a period of  time so that they can identify patterns   #
#        for buying/selling a specific stock                              #
#                                                                         #
#          INPUT: daily_stock_data                                        #
#          OUTPUT: Starting with the first two dates in a period of time, #
#                                                                         #
###########################################################################
#                                                                         #
# Things to learn:                                                        #
# 1) What is psycopg2                                                     #
# 2) Proper way to access a database - Reinforcing config, curser, conn   #
# 3) Writing queries vs. using dataframes (introduce numpy)               #
# 4) Writing multiline queries (no continuation)                          #
# 5) Getting results of a query to to a dataframe                         #
# 7) Referencing a row of a dataframe (loc and iloc)                      #
# 8) Find and change value of a column in a dataframe's row               #
# 9) Why doens't this work?                                               #
# 10) What does this give you?                                            #
# 11) Using forloop with iterrows()                                       # 
# 12) Practice using iterrows() and other forloops (reinforcement)        # 
# 13) About writing to a dataframe:                                       # 
# Pandas documentation on .append(): https://pandas.pydata.org/pandas-docs/version/1.4/reference/api/pandas.DataFrame.append.html
# Stack Overflow discussion on performance of appending rows: https://stackoverflow.com/questions/43771240/appending-rows-to-a-pandas-dataframe
# Remember, readability and maintainability are often more important than squeezing out the last bit of performance. Choose the approach that balances clarity and efficiency for your specific needs.
# 14) Comparing data                                                      #
# 15) Verifying results                                                   #
# 16) How to see all rows                                                 #
# 17) Modifying so that this code is optimize. (only comment out code)    #
# 18) Add notes stating why you did what you did.                         #
# 19) Summary: Comment the pros and cons of using methods vs. positional  #
#     indexing, the factors affecting performance. What are some          #
#     guidelines? Are there any tools you can use for optimization?       # 
# TODO: Extra Credit: Exploring optimization tools.                       #
#                                                                         #
#             GOOD LUCK                                                   #
########################################################################### 


# To keep this relatively simple, we will insert records first. 
# This is the first query to get data into the high_low table: 
import psycopg2
import pandas as pd
from config import dbconnection        

def query_highs_and_lows():
    # TODO: 
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
        # Execute a SELECT query  # <- why?!?!?!?!
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
        # TODO: the right code (in GetHighs and Lows)
        
        high_low_df = pd.read_sql_query(select_query, conn)
        print (high_low_df)
        
        # The first row is 'UNCH', so we must find appropriate value:
        # What is the second row of the dataframe?
        second_row = high_low_df.loc[1, 'high_low_txt']
        print('GetHighandLows:second_row: ' + second_row)
        
        if second_row == 'HIGHEST':
            high_low_df.loc[0, 'high_low_txt'] = "LOWEST"
        else:        
            high_low_df.loc[0, 'high_low_txt'] = "HIGHEST"
            
        #What is the value of the first row now?
        yesterdays_txt = (high_low_df.loc[0, 'high_low_txt'])    
                
        # Initialize DataFrame and write the first row to the dataframe. 
        
        # Why doens't this work?
        # final_df = [] # Initialize an empty DataFrame
        # final_df = final_df.append(high_low_df.iloc[0])
        
        # Why doesn't this work?
        # final_df = pd.DataFrame()  # Initialize an empty DataFrame
        # final_df.append(high_low_df.iloc[0])
        
        # Solution #1 - This does work
        # final_df = pd.DataFrame(columns=high_low_df.columns)  
        # #final_df.append(high_low_df.iloc[0]) <- Why doesn't this work?
        # final_df = final_df.append(high_low_df.iloc[0])
        # #print('Rows in final_df: ' + final_df) #<- Why doesn't this work?
        # print('Rows in final_df: ' + str(len(final_df)))
        # print(final_df) # What does this give you?
        
        # # Starting with the 2nd row, we iterate through all the 
        # # rows to get the lowest lows and the highest highs
        # for i, row in high_low_df.iloc[1:].iterrows():
        #     present_txt = high_low_df.iloc[i]['high_low_txt'] 
        #     if present_txt != yesterdays_txt: 
        #         final_df.loc[len(final_df)] = row # <- This does the same thing as final_df = final_df.append(row). Which should I use?
        #         # final_df = final_df.loc[len(final_df)] = row
        #         yesterdays_txt = present_txt                 

        # Solution #2 - This does work
        final_df = pd.DataFrame()  # Initialize an empty DataFrame
        final_df = final_df.append(high_low_df.iloc[0])  # Append the first row
        print(final_df)
        # Starting with the 2nd row, iterate through all  
        # rows to get lowest lows and the highest highs
        for i, row in high_low_df.iloc[1:].iterrows():
            present_txt = high_low_df.iloc[i]['high_low_txt']
            if present_txt != yesterdays_txt: 
                final_df = final_df.append(row)  # Append rows to the DataFrame
                yesterdays_txt = present_txt
                
        # Test: Is the data frames total count equal to the sum of the 'LOWEST' count and 'HIGHEST' count
        # TODO: Do something if they are not equal
        print (final_df)  
        print ((final_df['high_low_txt'] == 'LOWEST').sum())          
        print ((final_df['high_low_txt'] == 'HIGHEST').sum())          

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