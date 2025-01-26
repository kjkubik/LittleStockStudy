from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag, when, lit
from pyspark.sql.window import Window

# Initialize a Spark session
spark = SparkSession.builder.appName("Accumulate Low Percent Change").getOrCreate()

# Read the CSV into a PySpark DataFrame
df = spark.read.option("header", "true").csv('resources/HistoricalData/accumulated_data.csv')

# Cast columns to the appropriate types (e.g., 'low' column to float)
df = df.withColumn("low", col("low").cast("float"))

# Define a window spec partitioned by ticker and ordered by date or time
window_spec = Window.partitionBy("ticker").orderBy("date")  # Assuming there's a 'date' column in your data

# Get the previous day's low using the `lag` function
df = df.withColumn("prev_low", lag("low").over(window_spec))

# Get today's low as a column
df = df.withColumn("todays_low", col("low"))

# Calculate percent change from previous day's low to today's low
df = df.withColumn("percent_change_low", 
                   (col("todays_low") - col("prev_low")) / col("prev_low") * 100)

# Initialize columns for accumulation and flag tracking
df = df.withColumn("accumulated_percent_chg_low", lit(0.0)) \
       .withColumn("days_count_low", lit(1))

# We need to track the accumulation process using a user-defined function (UDF) or using row-by-row logic.
# To simulate this, we use a simple approach that works in a windowed aggregation.

# Define a windowed approach to accumulate the values
# Note: PySpark doesn't support direct row-wise iteration, so we will approximate this with additional columns.

df_with_accumulation = df.withColumn("sign", when(col("percent_change_low") >= 0, "positive").otherwise("negative"))

# Define a window specification for the sign tracking and accumulation
accumulation_window = Window.partitionBy("ticker").orderBy("date").rowsBetween(Window.unboundedPreceding, Window.currentRow)

# Use `lag` and `sum` over the window to calculate accumulated values and days count
df_accumulated = df_with_accumulation \
    .withColumn("accumulated_percent_chg_low", 
                when(col("sign") == lag("sign", 1).over(accumulation_window), 
                     sum("percent_change_low").over(accumulation_window))
                .otherwise(col("percent_change_low"))) \
    .withColumn("days_count_low", 
                when(col("sign") == lag("sign", 1).over(accumulation_window), 
                     sum(lit(1)).over(accumulation_window))
                .otherwise(lit(1)))

# Save the resulting DataFrame to a new CSV file
df_accumulated.write.option("header", "true").csv("resources/HistoricalData/accumulated_dataSTEP004.csv")

print("DataFrame has been saved to resources/HistoricalData/accumulated_dataSTEP004.csv")
