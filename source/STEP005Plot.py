# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta

import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta

# Assuming you already have a DataFrame `df` with columns ['ticker', 'date', 'percent_change']
df = pd.read_csv('resources/HistoricalData/extremesGone.csv')
# Step 1: Ensure 'date' is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Step 2: Filter the DataFrame to only include the last 30 days
end_date = df['date'].max()  # Get the latest date in the dataset
start_date = end_date - timedelta(days=30)  # Calculate the date 30 days ago

df_last_30_days = df[df['date'] >= start_date].copy()  # Create a copy to avoid warnings

# Step 3: Group tickers into chunks of 10 for plotting
tickers = df_last_30_days['ticker'].unique()
ticker_groups = [tickers[i:i + 5] for i in range(0, len(tickers), 10)]  # Group tickers into chunks of 10

# Step 4: Create a plot for each group of 10 tickers
for group_idx, group in enumerate(ticker_groups, 1):
    fig = go.Figure()

    # Add a scatter trace for each ticker in the group
    for ticker in group:
        ticker_data = df_last_30_days[df_last_30_days['ticker'] == ticker]
        
        # Color the points: Green for positive, Red for negative
        color = ticker_data['direction'].apply(lambda x: 'green' if x == 'positive' else 'red')

        fig.add_trace(go.Scatter(
            x=ticker_data['date'],
            y=ticker_data['accum_prcnt_chg_close'],  # Using your accumulated sum
            mode='lines+markers',  # Connect the dots with lines
            name=ticker,
            marker=dict(color=color),  # Color based on direction
            hovertemplate=(
                'Ticker: %{text}<br>' +
                'Date: %{x}<br>' +  # Display the date on hover
                'Accumulated Price Change: %{y}<br>' +  # Display the accumulated price change
                'Days Up or Down: %{customdata}<br>' +  # Display the days up or down
                '<extra></extra>'
            ),
            text=[ticker] * len(ticker_data),  # Add ticker name for hover info
            customdata=ticker_data['days_up_or_down']  # Pass 'days_up_or_down' directly
        ))

    # Step 5: Customize the layout for each ticker plot
    fig.update_layout(
        title=f'Accumulated Price Changes for Tickers (Last 30 Days) - Group {group_idx}',
        xaxis_title='Date',
        yaxis_title='Accumulated Price Change',
        hovermode='closest',
        xaxis=dict(
            tickformat='%Y-%m-%d',  # Format x-axis as Date
            showgrid=True
        ),
        yaxis=dict(
            showgrid=True
        ),
    )

    # Show the plot for this group of 10 tickers
    fig.show()