from notify import notify_dates
from login import fmel_navigate
import time
from datetime import date

error_count = 0

todays_date = date.today()

while True:

    if todays_date != date.today():
        notify_dates(f"Today: {error_count} errors",["recap info"])
        error_count = 0
        todays_date = date.today()

    try:
        dates = fmel_navigate()
    except:
        error_count += 1

    try:
        if len(dates) != 0:
            notify_dates("Available!!!", dates)
        else:
            notify_dates("No Housing",["No available housing"])
    except:
        error_count += 1

    print(f"Cumulative error count: {error_count}")
    print(f"Available dates: {dates}")
    # Sleep 30 minutes
    time.sleep(60*30)