import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from datetime import timedelta

# Get today's date (start date)
start_date = pd.to_datetime('today')

# Calculate the date 365 days ago (end date)
end_date = start_date - timedelta(days=365)

# Generate a list of U.S. federal holidays between today and 365 days ago
cal = USFederalHolidayCalendar()
holidays = cal.holidays(start=end_date, end=start_date).to_pydatetime()

# Convert holidays list to a set of datetime objects for faster lookup
holiday_set = set(holidays)

# Generate a list of all weekdays in the range (Monday=0, Sunday=6)
all_weekdays = pd.date_range(start=end_date, end=start_date, freq='B')

# Now count how many of the weekdays are not in the holidays set
valid_weekdays = [date for date in all_weekdays if date not in holiday_set]

# The number of valid weekdays is the length of valid_weekdays
print(f"Number of weekdays excluding weekends and holidays: {len(valid_weekdays)}")