from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("PySpark Example") \
    .getOrCreate()

# Create a simple DataFrame
data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
df = spark.createDataFrame(data, ["Name", "Value"])

# Show the DataFrame
df.show()

# Stop the SparkSession
spark.stop()
