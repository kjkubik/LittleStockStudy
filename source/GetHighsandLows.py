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
        print (final_df[final_df['high_low_txt'] == 'LOWEST'])          
        # # First, capture the first record in new dataframe
        # final_high_low_df = high_low_df.append(high_low_df.iloc[0], ignore_index=True)
        # print(final_high_low_df)
        
        
                
        # for i, row in high_low_df.iterrows():
        #     if i == 
        # 
        # print(f"previous: {previous_txt}")
        
        # previous_txt = high_low_df.iloc[0]['high_low_txt'] 
        #         # Iterate through each row #TODO this is still not right, this needs to be updated right. sometime when get high,' ',high or low,' ',low! 
        #         for i in range(1, len(high_low_df)):
        #             current_txt = high_low_df.iloc[i]['high_low_txt']
        #             if previous_txt == current_txt:
        #                 print(f"No change detected from {previous_txt} to {current_txt} at row {i+1}")
        #                 # update previous_txt to ' '
        #                 previous_txt = current_txt
        #             if previous_txt != current_txt:
        #                 print(f"Change detected from {previous_txt} to {current_txt} at row {i+1}")
        #                 previous_txt = current_txt
                
            
                     
                
                
                
                
                
                        # Set display options to show all rows and columns
        pd.set_option('display.max_rows', None)  # Show all rows

        #print (high_low_df)
                # # Fetch the result
                # rows = cursor.fetchall()
                # print(rows)
                # # Process the fetched rows
                # for row in rows:
                #     continue
                #     # Process each row as needed
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
#  INSERT INTO high_low (ticker, date, prev_price, next_days_price, high_low_txt)
# SELECT
#     ticker,
#     date,
#     LAG(high) OVER (PARTITION BY ticker ORDER BY date) AS prev_price,
#     high AS next_days_price,
#     CASE
#         WHEN LAG(high) OVER (PARTITION BY ticker ORDER BY date) < high THEN 'HIGHEST'
#         WHEN LAG(high) OVER (PARTITION BY ticker ORDER BY date) > high THEN 'LOWEST'
#         ELSE 'UNCH'
#     END AS high_low
# FROM
#     daily_stock_data       
# Then, an update will be done to the table to elim 

# def SMA_highs_and_lows(): 
#     with open ("resources/StockPricesTodaysDaily, 'r'"):
#         if previous_price > present_price:
#             higher_price
#         else
#         if previous_price < pre
#          For instance, say the user is attempting to discover patterns  #
#          in Microsoft stock. The user will be able to enter wants to see the 5 highest prices   #
#          between March 21st 2023 and March 21st 2024 for each month     #
#          ticker 'MSFT'. 

# this one give ranking of highs and lows 
# WITH ranked_data AS (
#     SELECT 
#         ticker,
#         date,
#         high,
#         low,
#         RANK() OVER (PARTITION BY ticker ORDER BY high DESC NULLS LAST) AS high_rank,
#         RANK() OVER (PARTITION BY ticker ORDER BY low ASC NULLS LAST) AS low_rank
#     FROM daily_stock_data
#     WHERE ticker = 'MSFT'
#         AND date BETWEEN '2023-03-21' AND '2023-05-21'
# )
# SELECT 
#     date,
#     high,
#     high_rank,
#     low,
#     low_rank
# FROM ranked_data
# WHERE high_rank <= 5 OR low_rank <= 5
# ORDER BY date;

# I kind of like this one, too!
# WITH ranked_highs AS (
#     SELECT 
#         date,
#         high,
#         ROW_NUMBER() OVER (PARTITION BY date_trunc('month', date) ORDER BY high DESC) AS high_rank
#     FROM daily_stock_data
#     WHERE ticker = 'MSFT' AND date BETWEEN '2023-03-21' AND '2024-03-21'
# ),
# ranked_lows AS (
#     SELECT 
#         date,
#         low,
#         ROW_NUMBER() OVER (PARTITION BY date_trunc('month', date) ORDER BY low ASC) AS low_rank
#     FROM daily_stock_data
#     WHERE ticker = 'MSFT' AND date BETWEEN '2023-03-21' AND '2024-03-21'
# )
# SELECT category, date, 
#  CASE
#            WHEN high IS NULL THEN COALESCE(low, 'NAN')  -- If high is NULL, use low or 'NAN' if low is also NULL
#            ELSE high  -- Otherwise, use high
#        END AS price
# FROM (
#     SELECT 'High' AS category, date, high, NULL AS low
#     FROM ranked_highs
#     WHERE high_rank <= 5
#     UNION ALL
#     SELECT 'Low' AS category, date, NULL AS high, low
#     FROM ranked_lows
#     WHERE low_rank <= 5
# ) subquery
# ORDER BY date ASC;

# # using these two queries to keep lows and highs separate. 
# WITH ranked_highs AS (
#     SELECT 
# 	    ticker,
#         date,
#         high,
#         RANK() OVER (ORDER BY high DESC NULLS LAST) AS high_rank
#     FROM daily_stock_data
#     WHERE ticker = 'MSFT'
# 	and date BETWEEN '2023-03-21' AND '2023-05-21'
# )
# SELECT 
#     date,
#     high,
#     high_rank
# FROM ranked_highs
# limit 5;
# --
# WITH ranked_lows AS (
#     SELECT 
# 	    ticker,
#         date,
#         low,
#         RANK() OVER (ORDER BY low DESC NULLS LAST) AS low_rank
#     FROM daily_stock_data
#     WHERE ticker = 'MSFT'
# 	and date BETWEEN '2023-03-21' AND '2023-05-21'
# )
# SELECT 
#     date,
#     low,
#     low_rank
# FROM ranked_lows
# limit 5;



# # # this is closer but no cookies

# WITH ranked_highs AS (
#     SELECT 
#         date,
#         high,
#         ROW_NUMBER() OVER (PARTITION BY date_trunc('month', date) ORDER BY high DESC) AS high_rank
#     FROM daily_stock_data
#     WHERE ticker = 'MSFT' AND date BETWEEN '2023-03-21' AND '2024-03-21'
# ),
# ranked_lows AS (
#     SELECT 
#         date,
#         low,
#         ROW_NUMBER() OVER (PARTITION BY date_trunc('month', date) ORDER BY low ASC) AS low_rank
#     FROM daily_stock_data
#     WHERE ticker = 'MSFT' AND date BETWEEN '2023-03-21' AND '2024-03-21'
# )
# SELECT category, date, 
#  CASE
#            WHEN high IS NULL THEN COALESCE(low, 'NAN')  -- If high is NULL, use low or 'NAN' if low is also NULL
#            ELSE high  -- Otherwise, use high
#        END AS price
# FROM (
#     SELECT 'High' AS category, date, high, NULL AS low
#     FROM ranked_highs
#     WHERE high_rank <= 5
#     UNION ALL
#     SELECT 'Low' AS category, date, NULL AS high, low
#     FROM ranked_lows
#     WHERE low_rank <= 5
# ) subquery
# ORDER BY date ASC;

# # The query below will give us data like this: 
# # -- "Lows"	"2023-03-21"	NaN	272.18
# # -- "Lows"	"2023-03-22"	NaN	275.2
# # -- "Highs"	"2023-03-22"	281.06	NaN
# # -- "Lows"	"2023-03-23"	NaN	275.28
# # -- "Lows"	"2023-03-26"	NaN	275.52
# # -- "Highs"	"2023-03-26"	281.4589	NaN
# # -- "Lows"	"2023-03-27"	NaN	272.0451
# # -- "Highs"	"2023-03-28"	281.1398	NaN
# # -- "Highs"	"2023-03-29"	284.46	NaN
# # -- "Highs"	"2023-03-30"	289.27	NaN

# # # I don't necessarily like its format

# WITH ranked_highs AS (
#     SELECT 
#         date,
#         high,
#         ROW_NUMBER() OVER (PARTITION BY date_trunc('month', date) ORDER BY high DESC) AS high_rank
#     FROM daily_stock_data
#     WHERE ticker = 'MSFT' AND date BETWEEN '2023-03-21' AND '2024-03-21'
# ),
# ranked_lows AS (
#     SELECT 
#         date,
#         low,
#         ROW_NUMBER() OVER (PARTITION BY date_trunc('month', date) ORDER BY low ASC) AS low_rank
#     FROM daily_stock_data
#     WHERE ticker = 'MSFT' AND date BETWEEN '2023-03-21' AND '2024-03-21'
# )
# SELECT category, date, COALESCE(high, 'NAN') AS high, COALESCE(low, 'NAN') AS low
# FROM (
#     SELECT 'Highs' AS category, date, high, NULL AS low
#     FROM ranked_highs
#     WHERE high_rank <= 5
#     UNION ALL
#     SELECT 'Lows' AS category, date, NULL AS high, low
#     FROM ranked_lows
#     WHERE low_rank <= 5
# ) subquery
# ORDER BY date ASC, category DESC, high DESC, low ASC;

