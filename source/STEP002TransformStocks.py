# F I R S T   A N D   S E C O N D   T H O U G H T S   C A N   G O   T O G E T H E R
import pandas as pd
import math
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# from plotly.subplots import make_subplots

# Load the stock data into dataframe
stock_df = pd.read_csv('resources/HistoricalData/StockResponse.csv', parse_dates=['date'], low_memory=False)

# Get starting data
stock_df = stock_df[['date', 'ticker','close']]
# print(stock_df) 

# rename close to todays_price
stock_df.rename(columns = {'close':'todays_price'}, inplace=True)
# print(stock_df)

# create new column, 'yesterdays_price' and fill it with yesterday's price for each ticker
stock_df['yesterdays_price'] = stock_df.groupby('ticker')['todays_price'].shift(1)
# print(stock_df)

# remove NaN rows produced when added 'yesterdays_price'
stock_df.dropna(subset=['yesterdays_price'], inplace=True)
# print(stock_df)

# create a new column, 'percent_change', place = (((todays_price/yesterdays_price)*100) - 100) 
stock_df['percent_change'] = (stock_df['todays_price']/stock_df['yesterdays_price'] * 100 - 100)
# print(stock_df.head(50))

# initialize column 'sum_percent_change'
stock_df['sum_percent_change'] = 0.0
print(stock_df.columns)

# iterate over each ticker
for ticker in stock_df['ticker'].unique():
    
    # print(ticker)
    
    # create a dataframe for the current ticker
    tickers_df = stock_df[stock_df['ticker'] == ticker]
    
    # check if there are any record for one of the dataframes you are creating
    if len(tickers_df[tickers_df['ticker'] == 'WSM']) > 0 :
        print(tickers_df)
    
    # Initialize the previous accumulated percent change
    previous_accum = 0.0

    for index, row in tickers_df.iterrows():
        # Add the current percent change to the accumulated sum
        previous_accum += row['percent_change']
        
        # Update the 'sum_percent_change' column in the original DataFrame
        stock_df.loc[index, 'sum_percent_change'] = previous_accum

# Display the final DataFrame with accumulated percent change
print(stock_df.tail(50))

# # # #   E N D   O F   F I R S T   T H O U G H T   # # # 


# # Get starting data
stock_df = stock_df[['date', 'ticker','sum_percent_change']]

# # Get the unique tickers
# tickers_to_plot = stock_df['ticker'].unique()

# # Split tickers into chunks of 15 (you can adjust chunk size as needed)
# chunk_size = 10
# ticker_chunks = [tickers_to_plot[i:i + chunk_size] for i in range(0, len(tickers_to_plot), chunk_size)]

# # Create plots for each chunk of tickers
# for ticker_chunk in ticker_chunks:
#     # Create a new figure for each chunk of tickers
#     fig = go.Figure()

#     # Add a line plot for each ticker in the chunk
#     for ticker in ticker_chunk:
#         # Filter the data for the current ticker
#         ticker_data = stock_df[stock_df['ticker'] == ticker]
        
#         # Add a line plot (scatter plot) for the accumulated percent change
#         fig.add_trace(
#             go.Scatter(
#                 x=ticker_data['date'], 
#                 y=ticker_data['sum_percent_change'], 
#                 mode='lines+markers', 
#                 name=f'{ticker}'  # set the ticker name for the legend
#             )
#         )

#     # Update layout to show grid lines, proper formatting, and legend
#     fig.update_layout(
#         title='Accumulated Percent Change for Stocks',
#         xaxis_title='Date',
#         yaxis_title='Accumulated Percent Change',
#         showlegend=True,  # Enable the legend
#         height=800,  # Adjust the height for the plot
#         width=1800,   # Adjust the width for a wider view
#         xaxis_tickangle=45,  # Rotate date labels for better readability
#         xaxis=dict(
#             showgrid=True,  # Show vertical grid lines
#             zeroline=False,  # Don't show a horizontal line at y=0
#             gridcolor='gray',  # set grid color to gray (you can change this)
#             gridwidth=1       # set grid line width
#         ),
#         yaxis=dict(
#             showgrid=True,  # Show horizontal grid lines
#             zeroline=False,  # Don't show a vertical line at x=0
#             gridcolor='gray',  # set grid color to gray (you can change this)
#             gridwidth=1       # set grid line width
#         ),
#         plot_bgcolor='white'  # set background color to white for cleaner look
#     )

#     # Show the plot
#     fig.show()
    
# # # #   T H I S   I S   T H E   E N D   O F   T H E    S E C O N D   T H O U G H T   # # #   


### BEGINNING OF THIRD THOUGHT. RUN WITH FIRST THOUGHT   
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#Assuming stock_df is your original dataframe with the columns: date, ticker, and sum_percent_change
# Get the unique tickers
tickers_to_plot = stock_df['ticker'].unique()

# Filter data for all tickers
filtered_df = stock_df[stock_df['ticker'].isin(tickers_to_plot)]

# Pivot the dataframe to have each ticker's 'sum_percent_change' as a separate column
stock_pct_change_pivot = filtered_df.pivot(index='date', columns='ticker', values='sum_percent_change')

# Calculate the correlation matrix for all tickers
correlation_matrix = stock_pct_change_pivot.corr()

# Mask correlations less than 0.95 by setting them to NaN
correlation_matrix_masked = correlation_matrix.where(correlation_matrix >= 0.95, other=None)

# Print the masked correlation matrix
print("Masked Correlation Matrix (correlations >= 0.95):")
print(correlation_matrix_masked)

# Visualize the masked correlation matrix using a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix_masked, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
plt.title("Correlation Matrix of Stock Percentage Changes (>= 0.95)")
plt.show()
### END OF THIRD

### BEGINNING OF FOURTH


# Assuming stock_df is your original dataframe with the columns: date, ticker, and sum_percent_change
# Get the unique tickers
tickers_to_plot = stock_df['ticker'].unique()

# Filter data for all tickers
filtered_df = stock_df[stock_df['ticker'].isin(tickers_to_plot)]

# Pivot the dataframe to have each ticker's 'sum_percent_change' as a separate column
stock_pct_change_pivot = filtered_df.pivot(index='date', columns='ticker', values='sum_percent_change')

# Calculate the correlation matrix for all tickers
correlation_matrix = stock_pct_change_pivot.corr()

# Mask correlations that are not exactly 0.95
correlation_matrix_masked = correlation_matrix.where(correlation_matrix >= 0.95, other=None)

# Print the filtered correlation matrix
print("Correlation List:")

# Create a list to store the results
correlation_pairs = []

# Iterate through the correlation matrix and collect pairs with correlation exactly 0.95
for col in correlation_matrix_masked.columns:
    for row in correlation_matrix_masked.index:
        # Skip self-correlations (diagonal elements) and NaN values
        if col != row and not pd.isna(correlation_matrix_masked.loc[row, col]):
            correlation_pairs.append((row, col, correlation_matrix_masked.loc[row, col]))

# Display the pairs that have a correlation of exactly 0.95
for pair in correlation_pairs:
    print(f"{pair[0]} | {pair[1]} | {pair[2]:.2f}")

# # import matplotlib.pyplot as plt
# # from matplotlib_venn import venn2, venn3
# # import pandas as pd
# # from upsetplot import UpSet

# # # Example stock data - Replace with your actual stock relationships
# # set1={'APH','FRPT','NTRA','NVDA'}
# # set2={'CAVA','FTAI'}
# # set3={'CEG','VST'}
# # set4={'CLS','MSTR','VRT','MOD'}
# # set5={'DRS','SFM'}
# # set6={'EAT','SFM'}
# # set7={'ERJ','FTAI','NTRA','PHIN'}
# # set8={'FICO','KKR'}
# # set9={'FRPT','APH','NTRA'}
# # set10={'FTAI','CAVA','ERJ'}
# # set11={'GDDY','KKR'}
# # set12={'KKR','FICO','GDDY','MOD','PRCT'}
# # set13={'MOD','CSL','KKR','NTRA'}
# # set14={'MSTR','CLS'}
# # set15={'NTRA','APH','ERJ','FRPT','MOD'}
# # set16={'NVDA','APH'}
# # set17={'PHIN','ERJ'}
# # set18={'PRCT','KKR'}
# # set19={'SFM','DRS','EAT','TRGP'}
# # set20={'STRL','VST'}
# # set21={'TRGP','SFM'}
# # set22={'VRT','CLS','VST'}
# # set23={'VST','CEG','STRL','VRT'}
# # set24={'FTAI','SFM'}
# # set25={'SFM','FTAI'}

# # # Create a Venn diagram with 3 sets
# # venn = venn3([set1,set2,set3,set4,set5,set6,set7,set8,set9,set10,set11,set12,set13,set14,set15,set16,set17,set18,set19,set20,set21,set22,set23,set24,set25], set_labels=('set1','set2','set3','set4','set5','set6','set7','set8','set9','set10','set11','set12','set13','set14','set15','set16','set17','set18','set19','set20','set21','set22','set23','set24','set25'))

# # # # Customizing the Venn Diagram (Optional)
# # # venn.get_label_by_id('100').set_text('APH, CAVA, ERJ')  # Only in set 1
# # # venn.get_label_by_id('010').set_text('FRPT, NVDA, NTRA')  # Only in set 2
# # # venn.get_label_by_id('001').set_text('FTAI, SFM')  # Only in set 3

# # # Display the Venn diagram
# # plt.title("Venn Diagram of Stock Relationships")
# # plt.show()

# # import pandas as pd
# # from upsetplot import UpSet
# # import matplotlib.pyplot as plt

# # # Example data
# # data = {
# #     'set1': {'APH', 'FRPT', 'NTRA', 'NVDA'},
# #     'set2': {'CAVA','FTAI'},
# #     'set3': {'CEG','VST'},
# #     'set4': {'CLS','MSTR','VRT','MOD'},
# #     'set5': {'DRS','SFM'},
# #     'set6': {'EAT','SFM'},
# #     'set7': {'ERJ','FTAI','NTRA','PHIN'},
# #     'set8': {'FICO','KKR'},
# #     'set9': {'FRPT','APH','NTRA'},
# #     'set10': {'FTAI','CAVA','ERJ'},
# #     'set11': {'GDDY','KKR'},
# #     'set12': {'KKR','FICO','GDDY','MOD','PRCT'},
# #     'set13': {'MOD','CSL','KKR','NTRA'},
# #     'set14': {'MSTR','CLS'},
# #     'set15': {'NTRA','APH','ERJ','FRPT','MOD'},
# #     'set16': {'NVDA','APH'},
# #     'set17': {'PHIN','ERJ'},
# #     'set18': {'PRCT','KKR'},
# #     'set19': {'SFM','DRS','EAT','TRGP'},
# #     'set20': {'STRL','VST'},
# #     'set21': {'TRGP','SFM'},
# #     'set22': {'VRT','CLS','VST'},
# #     'set23': {'VST', 'CEG', 'STRL', 'VRT'},
# #     'set24': {'FTAI', 'SFM'},
# #     'set25': {'SFM', 'FTAI'}
# #     }
# # # Convert the data into a format that can be plotted
# # # We need to count how many times each element appears across all sets
# # set_names = data.keys()
# # combinations = []

# # # Loop over sets and store stock and corresponding set
# # for set_name in set_names:
# #     for stock in data[set_name]:
# #         combinations.append((stock, set_name))

# # # Create the DataFrame with combinations
# # df = pd.DataFrame(combinations, columns=['stock', 'set'])

# # # Create a MultiIndex from the 'stock' and 'set' columns
# # df_multi_index = df.set_index(['stock', 'set'])

# # # Pivot the data to create a binary indicator matrix (0 or 1)
# # # Each row will represent a stock, and each column will represent a set
# # df_pivot = df_multi_index.groupby(['stock', 'set']).size().unstack(fill_value=0)

# # # Now, `df_pivot` will contain a matrix where the index is stock, and columns are sets.
# # # Each entry will be 1 if the stock is in the set, 0 otherwise.

# # # Use `upsetplot` to plot
# # upset = UpSet(df_pivot, subset_size='count')

# # # Plot the UpSet diagram
# # upset.plot()

# # # Display the plot
# # plt.title("UpSet Plot of Stock Relationships")
# # plt.show()

# # import pandas as pd
# # from upsetplot import UpSet
# # import matplotlib.pyplot as plt

# # # Example data
# # data = {
# #     'set1': {'APH', 'FRPT', 'NTRA', 'NVDA'},
# #     'set2': {'CAVA', 'FTAI'},
# #     'set3': {'CEG', 'VST'},
# #     'set4': {'CLS', 'MSTR', 'VRT', 'MOD'},
# #     'set5': {'DRS', 'SFM'},
# #     'set6': {'EAT', 'SFM'},
# #     'set7': {'ERJ', 'FTAI', 'NTRA', 'PHIN'},
# #     'set8': {'FICO', 'KKR'},
# #     'set9': {'FRPT', 'APH', 'NTRA'},
# #     'set10': {'FTAI', 'CAVA', 'ERJ'},
# #     'set11': {'GDDY', 'KKR'},
# #     'set12': {'KKR', 'FICO', 'GDDY', 'MOD', 'PRCT'},
# #     'set13': {'MOD', 'CSL', 'KKR', 'NTRA'},
# #     'set14': {'MSTR', 'CLS'},
# #     'set15': {'NTRA', 'APH', 'ERJ', 'FRPT', 'MOD'},
# #     'set16': {'NVDA', 'APH'},
# #     'set17': {'PHIN', 'ERJ'},
# #     'set18': {'PRCT', 'KKR'},
# #     'set19': {'SFM', 'DRS', 'EAT', 'TRGP'},
# #     'set20': {'STRL', 'VST'},
# #     'set21': {'TRGP', 'SFM'},
# #     'set22': {'VRT', 'CLS', 'VST'},
# #     'set23': {'VST', 'CEG', 'STRL', 'VRT'},
# #     'set24': {'FTAI', 'SFM'},
# #     'set25': {'SFM', 'FTAI'}
# # }

# # # Convert the data into a format that can be plotted
# # combinations = []

# # # Loop through the data to create stock-set pairs
# # for set_name, stocks in data.items():
# #     for stock in stocks:
# #         combinations.append((stock, set_name))

# # # Create a DataFrame with stock-set pairs
# # df = pd.DataFrame(combinations, columns=['stock', 'set'])

# # # Create a MultiIndex from the stock and set columns
# # df_multi_index = df.set_index(['stock', 'set'])

# # # Create a binary matrix by unstacking (filling missing values with 0)
# # df_pivot = df_multi_index.groupby(['stock', 'set']).size().unstack(fill_value=0)

# # # Verify that the DataFrame has the right structure
# # print(df_pivot.head())

# # # Now `df_pivot` should be in the correct format for the UpSet plot.
# # # Pass the DataFrame to UpSet and plot
# # upset = UpSet(df_pivot, subset_size='count')
# # upset.plot()

# # # Display the plot
# # plt.title("UpSet Plot of Stock Relationships")
# # plt.show()

# # import matplotlib.pyplot as plt
# # from matplotlib_venn import venn2, venn3
# # import numpy as np

# # # Example data (25 sets of tickers)
# # data = {
# #     'set1': {'APH', 'FRPT', 'NTRA', 'NVDA'},
# #     'set2': {'CAVA', 'FTAI'},
# #     'set3': {'CEG', 'VST'},
# #     'set4': {'CLS', 'MSTR', 'VRT', 'MOD'},
# #     'set5': {'DRS', 'SFM'},
# #     'set6': {'EAT', 'SFM'},
# #     'set7': {'ERJ', 'FTAI', 'NTRA', 'PHIN'},
# #     'set8': {'FICO', 'KKR'},
# #     'set9': {'FRPT', 'APH', 'NTRA'},
# #     'set10': {'FTAI', 'CAVA', 'ERJ'},
# #     'set11': {'GDDY', 'KKR'},
# #     'set12': {'KKR', 'FICO', 'GDDY', 'MOD', 'PRCT'},
# #     'set13': {'MOD', 'CSL', 'KKR', 'NTRA'},
# #     'set14': {'MSTR', 'CLS'},
# #     'set15': {'NTRA', 'APH', 'ERJ', 'FRPT', 'MOD'},
# #     'set16': {'NVDA', 'APH'},
# #     'set17': {'PHIN', 'ERJ'},
# #     'set18': {'PRCT', 'KKR'},
# #     'set19': {'SFM', 'DRS', 'EAT', 'TRGP'},
# #     'set20': {'STRL', 'VST'},
# #     'set21': {'TRGP', 'SFM'},
# #     'set22': {'VRT', 'CLS', 'VST'},
# #     'set23': {'VST', 'CEG', 'STRL', 'VRT'},
# #     'set24': {'FTAI', 'SFM'},
# #     'set25': {'SFM', 'FTAI'}
# # }

# # # Function to create a custom Venn diagram
# # def plot_custom_venn(data):
# #     # Set up the plot
# #     fig, ax = plt.subplots(figsize=(10, 10))

# #     # Define the position and size of each circle manually
# #     circle_positions = [
# #         (0, 1), (2, 1), (1, 2), (3, 3), (4, 1), (1, 4), (3, 5), (5, 2),
# #         (2, 5), (4, 3), (3, 1), (1, 3), (4, 4), (5, 1), (2, 2), (3, 2),
# #         (1, 1), (4, 2), (2, 3), (1, 5), (0, 3), (5, 3), (0, 2), (4, 5),
# #         (3, 4)
# #     ]

# #     # Iterate over each set and plot a circle at the given position
# #     for i, (set_name, tickers) in enumerate(data.items()):
# #         x, y = circle_positions[i]
# #         circle = plt.Circle((x, y), 0.5, color=np.random.rand(3,), alpha=0.6)
# #         ax.add_artist(circle)
        
# #         # Label the circle with tickers
# #         ticker_names = ', '.join(tickers)
# #         ax.text(x, y, ticker_names, ha='center', va='center', fontsize=8, color='black')

# #     # Set the limits and remove axis labels
# #     ax.set_xlim(-1, 6)
# #     ax.set_ylim(-1, 6)
# #     ax.set_aspect('equal', 'box')
# #     ax.axis('off')

# #     # Title
# #     plt.title("Venn Diagram for 25 Sets of Stock Tickers", fontsize=16)
    
# #     # Show the plot
# #     plt.show()

# # # Call the function to create the custom Venn diagram
# plot_custom_venn(data)
import networkx as nx
import matplotlib.pyplot as plt

# Define the relationships between tickers (edges between nodes)
relationships = [
      ('CLS', 'APH'),
    ('CSL', 'APH'),
    ('ERJ', 'APH'),
    ('MOD', 'APH'),
    ('PHIN', 'APH'),
    ('VRT', 'APH'),
    ('KKR', 'BLFS'),
    ('PRCT', 'BLFS'),
    ('ERJ', 'CAVA'),
    ('FRPT', 'CAVA'),
    ('MOD', 'CAVA'),
    ('NTRA', 'CAVA'),
    ('NVDA', 'CAVA'),
    ('PHIN', 'CAVA'),
    ('SFM', 'CAVA'),
    ('SG', 'CAVA'),
    ('VST', 'CAVA'),
    ('VRT', 'CEG'),
    ('APH', 'CLS'),
    ('NFLX', 'CLS'),
    ('VST', 'CLS'),
    ('APH', 'CSL'),
    ('FRPT', 'CSL'),
    ('NVDA', 'CSL'),
    ('VRT', 'CSL'),
    ('EAT', 'DRS'),
    ('FICO', 'DRS'),
    ('FTAI', 'DRS'),
    ('TRGP', 'DRS'),
    ('DRS', 'EAT'),
    ('FTAI', 'EAT'),
    ('NGVC', 'EAT'),
    ('TRGP', 'EAT'),
    ('VST', 'EAT'),
    ('APH', 'ERJ'),
    ('CAVA', 'ERJ'),
    ('FRPT', 'ERJ'),
    ('GDDY', 'ERJ'),
    ('MOD', 'ERJ'),
    ('SFM', 'ERJ'),
    ('VST', 'ERJ'),
    ('DRS', 'FICO'),
    ('FTAI', 'FICO'),
    ('GDDY', 'FICO'),
    ('SFM', 'FICO'),
    ('CAVA', 'FRPT'),
    ('CSL', 'FRPT'),
    ('ERJ', 'FRPT'),
    ('MOD', 'FRPT'),
    ('NVDA', 'FRPT'),
    ('PHIN', 'FRPT'),
    ('DRS', 'FTAI'),
    ('EAT', 'FTAI'),
    ('FICO', 'FTAI'),
    ('KKR', 'FTAI'),
    ('MOD', 'FTAI'),
    ('NVDA', 'FTAI'),
    ('PHIN', 'FTAI'),
    ('PRCT', 'FTAI'),
    ('TRGP', 'FTAI'),
    ('VST', 'FTAI'),
    ('ZETA', 'FTAI'),
    ('ERJ', 'GDDY'),
    ('FICO', 'GDDY'),
    ('MOD', 'GDDY'),
    ('NFLX', 'GDDY'),
    ('NTRA', 'GDDY'),
    ('PRCT', 'GDDY'),
    ('BLFS', 'KKR'),
    ('FTAI', 'KKR'),
    ('NFLX', 'KKR'),
    ('NTRA', 'KKR'),
    ('APH', 'MOD'),
    ('CAVA', 'MOD'),
    ('ERJ', 'MOD'),
    ('FRPT', 'MOD'),
    ('FTAI', 'MOD'),
    ('GDDY', 'MOD'),
    ('NVDA', 'MOD'),
    ('PHIN', 'MOD'),
    ('VRT', 'MOD'),
    ('NTRA', 'MSTR'),
    ('VRT', 'MSTR'),
    ('VST', 'MSTR'),
    ('CLS', 'NFLX'),
    ('GDDY', 'NFLX'),
    ('KKR', 'NFLX'),
    ('NTRA', 'NFLX'),
    ('EAT', 'NGVC'),
    ('SFM', 'NGVC'),
    ('CAVA', 'NTRA'),
    ('GDDY', 'NTRA'),
    ('KKR', 'NTRA'),
    ('MSTR', 'NTRA'),
    ('NFLX', 'NTRA'),
    ('NVDA', 'NTRA'),
    ('PHIN', 'NTRA'),
    ('PRCT', 'NTRA'),
    ('VRT', 'NTRA'),
    ('VST', 'NTRA'),
    ('CAVA', 'NVDA'),
    ('CSL', 'NVDA'),
    ('FRPT', 'NVDA'),
    ('FTAI', 'NVDA'),
    ('MOD', 'NVDA'),
    ('NTRA', 'NVDA'),
    ('PHIN', 'NVDA'),
    ('APH', 'PHIN'),
    ('CAVA', 'PHIN'),
    ('FRPT', 'PHIN'),
    ('FTAI', 'PHIN'),
    ('MOD', 'PHIN'),
    ('NTRA', 'PHIN'),
    ('NVDA', 'PHIN'),
    ('SFM', 'PHIN'),
    ('SG', 'PHIN'),
    ('VST', 'PHIN'),
    ('BLFS', 'PRCT'),
    ('FTAI', 'PRCT'),
    ('GDDY', 'PRCT'),
    ('NTRA', 'PRCT'),
    ('SFM', 'PRCT'),
    ('CAVA', 'SFM'),
    ('ERJ', 'SFM'),
    ('FICO', 'SFM'),
    ('NGVC', 'SFM'),
    ('PHIN', 'SFM'),
    ('PRCT', 'SFM'),
    ('STRL', 'SFM'),
    ('VST', 'SFM'),
    ('ZETA', 'SFM'),
    ('CAVA', 'SG'),
    ('PHIN', 'SG'),
    ('SFM', 'STRL'),
    ('DRS', 'TRGP'),
    ('EAT', 'TRGP'),
    ('FTAI', 'TRGP'),
    ('APH', 'VRT'),
    ('CEG', 'VRT'),
    ('CSL', 'VRT'),
    ('MOD', 'VRT'),
    ('MSTR', 'VRT'),
    ('NTRA', 'VRT'),
    ('CAVA', 'VST'),
    ('CLS', 'VST'),
    ('EAT', 'VST'),
    ('ERJ', 'VST'),
    ('FTAI', 'VST'),
    ('MSTR', 'VST'),
    ('NTRA', 'VST'),
    ('PHIN', 'VST'),
    ('SFM', 'VST'),
    ('FTAI', 'ZETA'),
    ('SFM', 'ZETA'),
    ('FRPT', 'APH'),
    ('NTRA', 'APH'),
    ('NVDA', 'APH'),
    ('FTAI', 'CAVA'),
    ('VST', 'CEG'),
    ('MSTR', 'CLS'),
    ('VRT', 'CLS'),
    ('MOD', 'CSL'),
    ('SFM', 'DRS'),
    ('SFM', 'EAT'),
    ('FTAI', 'ERJ'),
    ('NTRA', 'ERJ'),
    ('PHIN', 'ERJ'),
    ('KKR', 'FICO'),
    ('APH', 'FRPT'),
    ('NTRA', 'FRPT'),
    ('CAVA', 'FTAI'),
    ('ERJ', 'FTAI'),
    ('KKR', 'GDDY'),
    ('FICO', 'KKR'),
    ('GDDY', 'KKR'),
    ('MOD', 'KKR'),
    ('PRCT', 'KKR'),
    ('CSL', 'MOD'),
    ('KKR', 'MOD'),
    ('NTRA', 'MOD'),
    ('CLS', 'MSTR'),
    ('APH', 'NTRA'),
    ('ERJ', 'NTRA'),
    ('FRPT', 'NTRA'),
    ('MOD', 'NTRA'),
    ('APH', 'NVDA'),
    ('ERJ', 'PHIN'),
    ('KKR', 'PRCT'),
    ('DRS', 'SFM'),
    ('EAT', 'SFM'),
    ('TRGP', 'SFM'),
    ('VST', 'STRL'),
    ('SFM', 'TRGP'),
    ('CLS', 'VRT'),
    ('VST', 'VRT'),
    ('CEG', 'VST'),
    ('STRL', 'VST'),
    ('VRT', 'VST'),
    ('SFM', 'FTAI'),
    ('FTAI', 'SFM')
]


# Create a graph object
G = nx.Graph()

# Add edges to the graph based on the relationships
G.add_edges_from(relationships)

# Plot the graph
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.15, iterations=20)  # Layout for better visualization
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')

# Title
plt.title("Relational Model of Ticker Connections", fontsize=16)
plt.show()