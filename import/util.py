import csv
from datetime import datetime

import psycopg2

# This file is gitignored - you'll need to provide your own copy
import credentials

# Lowercase email addresses and remove whitespace.
def normalize_email(email):
    email = email.lower().replace(' ', '').strip()
    email_parts = email.split("@", 1)
    return email_parts[0].replace('.','') + "@" + email_parts[1]

# Parse a Google Sheet timestamp string ('5/1/2018 21:07:52') to
def parse_gs_timestamp(ts):
    return datetime.strptime(ts, '%m/%d/%Y %H:%M:%S')

def parse_iso_date(date):
    return datetime.strptime(date, '%Y-%m-%d')

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

def existing(conn, table):
    query = "select distinct email from {}".format(table)
    with conn.cursor() as cursor:
        cursor.execute(query)
        return set([normalize_email(e[0]) for e in cursor.fetchall()])

def last_hour_update(conn, reason):
    query = "select max(hour_date) from hour_log where \
                  hour_reason = '{}'".format(reason)
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()[0]

def write_review_file(to_review, review_type, hum_name):
    if to_review:
        print("Some {} not inserted".format(hum_name))
        with open('{}_review.csv'.format(review_type),
                  'w', newline='') as f:
            fieldnames = list(to_review[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(to_review)
