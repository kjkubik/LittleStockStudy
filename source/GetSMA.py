# This module will be used to get the SMA for every
import pandas as pd
from numpy import record
from numba import njit
import csv
import datetime
import time
from pandas.core.indexes.datetimes import date_range
import plotly.graph_objects as go



def get_SMA():
    ticker = 'SMRT'
    start_date = '2022-03-31'
    end_date = '2024-03-31'
    # INPUT tickers
    #tickers_df = pd.read_csv("resources/InputTickers.csv")
    #print(tickers_df)

    # INPUT: we are isolate columns ticker, date, and closing price into a dataframe
    stock_prices_df = pd.read_csv("resources/HistoricalData/CombinedStockPrices.csv", usecols=['ticker','date','close'])
    print(stock_prices_df)   

    single_stock_df = stock_prices_df[(stock_prices_df['ticker'] == ticker) &
                                      (stock_prices_df['date'] >= start_date) & 
                                      (stock_prices_df['date'] <= end_date)]
    
    # Convert 'date' column to datetime format
    single_stock_df['date'] = pd.to_datetime(single_stock_df['date'])

    # TODO: When getting all stocks you want to grab 

    # Calculate SMA for a specified window size (e.g., 3 days)
    window_size1 = 10
    window_size_txt1 = '10'
    single_stock_df['SMA1'] = single_stock_df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=window_size1).mean())

    window_size2 = 20
    window_size_txt2 = '20'
    single_stock_df['SMA2'] = single_stock_df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=window_size2).mean())
    
    window_size3 = 30
    window_size_txt3 = '30'
    single_stock_df['SMA3'] = single_stock_df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=window_size3).mean())
    print(single_stock_df)
    
    window_size4 = 40
    window_size_txt4 = '40'
    single_stock_df['SMA4'] = single_stock_df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=window_size4).mean())
    print(single_stock_df)
    
    window_size5 = 50
    window_size_txt5 = '50'
    single_stock_df['SMA5'] = single_stock_df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=window_size5).mean())
    print(single_stock_df)
    
    window_size6 = 50
    window_size_txt6 = '50'
    single_stock_df['SMA6'] = single_stock_df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=window_size6).mean())
    print(single_stock_df)
    
    window_size7 = 70
    window_size_txt7 = '70'
    single_stock_df['SMA7'] = single_stock_df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=window_size7).mean())
    print(single_stock_df)
    
    # PLOTTING
    close_df = single_stock_df[['date', 'close']]
    SMA1_df = single_stock_df[['date', 'SMA1']]
    SMA2_df = single_stock_df[['date', 'SMA2']]
    SMA3_df = single_stock_df[['date', 'SMA3']]
    SMA4_df = single_stock_df[['date', 'SMA4']]
    SMA5_df = single_stock_df[['date', 'SMA5']]
    SMA6_df = single_stock_df[['date', 'SMA6']]
    SMA7_df = single_stock_df[['date', 'SMA7']]
    
    trace_close = go.Scatter(x=close_df['date'], y=close_df['close'], mode='lines', name='close', line=dict(color='black', width=3))
    trace_SMA1 = go.Scatter(x=SMA1_df['date'], y=SMA1_df['SMA1'], mode='lines', name='SMA' + window_size_txt1, line=dict(color='red', width=2))
    trace_SMA2 = go.Scatter(x=SMA2_df['date'], y=SMA2_df['SMA2'], mode='lines', name='SMA' + window_size_txt2, line=dict(color='yellow', width=2))
    trace_SMA3 = go.Scatter(x=SMA3_df['date'], y=SMA3_df['SMA3'], mode='lines', name='SMA' + window_size_txt3, line=dict(color='blue', width=2))
    trace_SMA4 = go.Scatter(x=SMA4_df['date'], y=SMA4_df['SMA4'], mode='lines', name='SMA' + window_size_txt4, line=dict(color='green', width=2))
    trace_SMA5 = go.Scatter(x=SMA5_df['date'], y=SMA5_df['SMA5'], mode='lines', name='SMA' + window_size_txt5, line=dict(color='olive', width=2))
    trace_SMA6 = go.Scatter(x=SMA6_df['date'], y=SMA6_df['SMA6'], mode='lines', name='SMA' + window_size_txt6, line=dict(width=2))
    trace_SMA7 = go.Scatter(x=SMA7_df['date'], y=SMA7_df['SMA7'], mode='lines', name='SMA' + window_size_txt7, line=dict(width=2))
    
    # Create a figure and add traces
    fig = go.Figure()
    fig.add_trace(trace_close)
    fig.add_trace(trace_SMA1)
    fig.add_trace(trace_SMA2)
    fig.add_trace(trace_SMA3)
    fig.add_trace(trace_SMA4)
    fig.add_trace(trace_SMA5)
    #fig.add_trace(trace_SMA6)
    #fig.add_trace(trace_SMA7)
    
    # Update figure layout (optional)
    fig.update_layout(title='SMA for ' + ticker, xaxis_title='Date', yaxis_title='Simple Moving Averages')

        # Show the figure
    fig.show() 
    
# MAIN
if __name__ == '__main__':
    get_SMA()
