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
#from numpy import record
#from numba import njit
#import csv
#import os
import plotly.graph_objects as go

from config import dbconnection        

def query_highs_and_lows():
    # TODO: 
    # INPUT
    tickers_df = pd.read_csv("resources/InputTickers.csv")

    for record, row in tickers_df.iterrows():
        ticker =  row['ticker']
        print(ticker)
        if record != 'ticker':
    
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
                                where ticker = '{ticker}'
                                and date between '2022-03-31' and '2024-03-31'
                                ''' 
                                #where ticker = '{ticker}';
                # TODO: the right code (in GetHighs and Lows)
                
                high_low_df = pd.read_sql_query(select_query, conn)
                #print (high_low_df)
                
            finally:
                # Close the cursor and connection
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()                    
                
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
        
            final_df = pd.DataFrame()  # Initialize an empty DataFrame
            final_df = final_df.append(high_low_df.iloc[-1])  # Append the last row (reversed order)
            #print(final_df)
            yesterdays_txt = high_low_df.iloc[-1]['high_low_txt']  # Initialize yesterdays_txt with the last row's text

            # Iterate through the rows of high_low_df in reverse order
            for i, row in high_low_df.iloc[::-1].iterrows():
                present_txt = row['high_low_txt']
                if present_txt != yesterdays_txt:
                    final_df = final_df.append(row)  # Append rows to the DataFrame
                    yesterdays_txt = present_txt

            #print(final_df)
            
            # Initialize variables
            low_count = 0  # Initialize variable to count 'LOWEST' occurrences
            prev_low_date = None  # Initialize variable to store the date of the previous 'LOWEST'

            # Iterate through the rows of final_df
            for index, row in final_df.iterrows():
                if row['high_low_txt'] == 'LOWEST':
                    low_count += 1  # Increment the count of 'LOWEST'
                    if low_count > 1:  # Check if this is not the first 'LOWEST'
                        low_distance = abs((row['date'] - prev_low_date).days)  # Calculate the absolute difference in days
                        print(f"{row['date'].strftime('%Y-%m-%d')} - {prev_low_date.strftime('%Y-%m-%d')}: {low_distance}")
                    prev_low_date = row['date']  # Update the previous 'LOWEST' date
            
            # Set display options to show all rows and columns
            # pd.set_option('display.max_rows', None)  # Show all rows
            # print (final_df)  
            # print ((final_df['high_low_txt'] == 'LOWEST').sum())          
            # print ((final_df['high_low_txt'] == 'HIGHEST').sum()) 
            plot_highs_and_lows(ticker,final_df)    
        # TODO: ONCE YOU GET the dataframe right, we will put them in the high_low table and then use the high_low table to plot points on graph. 
        # TODO: put SMA on the same graph too!!! ;)
        
        # Test: Is the data frames total count equal to the sum of the 'LOWEST' count and 'HIGHEST' count
        # TODO: Do something if they are not equal

def plot_highs_and_lows(ticker,final_df):         
        
    # PLOTTING     
    # Create a new DataFrame with 'date' and 'next_days_price' columns
    hl_df = final_df[['date', 'next_days_price']]
    print(hl_df)
    
    # plot_high_df = high_df[['date', 'next_days_price']]
    # print(plot_high_df)
    
    # Create traces for hl_df and high_df
    trace_hl = go.Scatter(x=hl_df['date'], y=hl_df['next_days_price'], mode='markers', name='High/Low')
    #trace_high = go.Scatter(x=plot_high_df['date'], y=plot_high_df['next_days_price'], mode='lines', name='All days')
    trace_points = go.Scatter(x=hl_df['date'], y=hl_df['next_days_price'], mode='lines', name='High/Low')

    # Create a figure and add traces
    fig = go.Figure()
    fig.add_trace(trace_hl)
    #fig.add_trace(trace_high)
    fig.add_trace(trace_points)

    # Update figure layout (optional)
    fig.update_layout(title='High/Low and Prices for ' + ticker, xaxis_title='Date', yaxis_title='Value')

    # Show the figure
    fig.show() 




# MAIN
if __name__ == '__main__':
    
    query_highs_and_lows()
    print ('GetHighsandLows Processing Complete')