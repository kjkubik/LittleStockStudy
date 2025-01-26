from config import stock_key        
from polygon import RESTClient  

client = RESTClient(stock_key)

# Get aggregate bars for Apple (AAPL)
aggs = client.list_aggs("PLTR", 1, "day", "2024-01-01", "2024-01-05")

for agg in aggs:
    print(agg)