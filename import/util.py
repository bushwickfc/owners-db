from datetime import datetime
import psycopg2

# This file is gitignored - you'll need to provide your own copy
import credentials

# Lowercase email addresses and remove whitespace.
def normalize_email(email):
    return email.lower().replace(' ', '').strip()

# Convert a Google Sheet timestamp string ('5/1/2018 21:07:52') to
# basic date string format ('2018-5-1')
def timestamp_to_date(ts):
    dt = datetime.strptime(ts, '%m/%d/%Y %H:%M:%S')
    return dt.date()

def dedupe(seq, selector=None):
    seen = set()
    seen_add = seen.add
    if not selector:
        selector = lambda x: x
    return [x for x in seq
            if not (selector(x) in seen or seen_add(selector(x)))]

def connection():
    return psycopg2.connect(f'''host={credentials.host}
    user={credentials.user}
    password={credentials.password}
    dbname={credentials.dbname}''')
