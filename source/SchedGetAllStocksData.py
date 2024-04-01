# scheduler.py
import schedule
import time
from GetAllStocksDatas import daily_run
from config import stock_key

# Schedule the task to run daily at a specific time (e.g., 9:00 AM)
schedule.every().day.at("04:00").do(daily_run)

# Keep the program running to allow scheduled tasks to execute
while True:
    schedule.run_pending()
    time.sleep(1)
    
