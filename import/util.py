# Helper functions
import time

# Lowercase email addresses and remove whitespace.
def normalize_email(email):
    return email.lower().replace(" ", "")

# Convert a Google Sheet timestamp string ('5/1/2018 21:07:52') to basic date string format ('2018-5-1')
def timestamp_to_date(ts):
    dt_tup = time.strptime(ts, "%m/%d/%Y %H:%M:%S")
    return str(dt_tup[0]) + "-" + str(dt_tup[1]) + "-" + str(dt_tup[2])
