# TODO: use this for final write of GetHighandLows
# TODO: Explain why you don't use the least complex SELECT statement when accessing databases (in general)
# TODO: AWS - How they make money

import pandas as pd

# Read your daily stock data into a DataFrame
daily_stock_data = pd.read_csv("your_data.csv")  # Replace with your data source

# Filter for the desired ticker
df = daily_stock_data[daily_stock_data["ticker"] == "ADP"]

# Efficient calculation using vectorized operations
df["prev_price"] = df.groupby("ticker")["high"].shift(1)
df["next_days_price"] = df["high"]
conditions = [df["prev_price"] < df["high"], df["prev_price"] > df["high"]]
choices = ["HIGHEST", "LOWEST"]
df["high_low_txt"] = np.select(conditions, choices, default="UNCH")

# Display the resulting DataFrame
print(df)
#--
import pandas as pd
import numpy as np  # Import NumPy for np.select

# Read your daily stock data into a DataFrame
daily_stock_data = pd.read_csv("your_data.csv")  # Replace with your data source

# Filter for the desired ticker
df = daily_stock_data[daily_stock_data["ticker"] == "ADP"]

# Efficient calculation using vectorized operations
df["prev_price"] = df.groupby("ticker")["high"].shift(1)
df["next_days_price"] = df["high"]
conditions = [df["prev_price"] < df["high"], df["prev_price"] > df["high"]]
choices = ["HIGHEST", "LOWEST"]
df["high_low_txt"] = np.select(conditions, choices, default="UNCH")

# Display the resulting DataFrame
print(df)