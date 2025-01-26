import numpy as np
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def calculate_volatility_with_numpy(data, window_size=30):
    """
    This function calculates the rolling volatility using NumPy.
    It operates on a Pandas DataFrame or a small subset of data in a Spark DataFrame.
    """
    # Convert stock price column to NumPy array
    prices = data['close'].values

    # Calculate daily returns using NumPy
    daily_returns = np.diff(prices) / prices[:-1]

    # Calculate rolling standard deviation (volatility) using NumPy
    volatility = np.array([np.nan] * (window_size - 1))  # First (window_size-1) days will be NaN
    for i in range(window_size - 1, len(daily_returns)):
        volatility = np.append(volatility, np.std(daily_returns[i-window_size+1:i]))

    # Return the volatility array
    return volatility

# Example usage with PySpark:
def add_volatility_column(data, window_size=30):
    """
    Apply the volatility calculation function (using NumPy) to PySpark DataFrame
    and add it as a new column.
    """
    # Apply the function to the Pandas DataFrame subset (use Pandas for each group)
    def calculate_volatility_pandas(pdf):
        return calculate_volatility_with_numpy(pdf, window_size)

    # Use PySpark's `groupBy().applyInPandas` to apply NumPy calculations per group (ticker)
    window_spec = Window.partitionBy("ticker").orderBy("date")
    
    # Apply custom function
    result_df = data.groupby('ticker').applyInPandas(calculate_volatility_pandas, schema=data.schema)
    
    return result_df
