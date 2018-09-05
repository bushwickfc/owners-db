import csv
import copy
from datetime import datetime

import psycopg2

# This file is gitignored - you'll need to provide your own copy
import credentials

#TODO: put this in google sheet and have it optionally read
#      from sheet or file.
MAPPING_FILE = 'mapping.csv'

# Lowercase email addresses and remove whitespace.
def standardize_email(email):
    return email.lower().replace(' ', '').strip()

# also remove . from emails. This should be used for comparisons only
# and emails stored in db should use `standardize_email`
def normalize_email(email):
    email = standardize_email(email)
    email_parts = email.split("@", 1)
    if len(email_parts) > 1:
        return email_parts[0].replace('.','') + "@" + email_parts[1]
    else:
        return email

# generate mapping of equivalent emails
def email_mapping(mapping_file):
    email_list = [l.split(",") for l in mapping_file]
    mapping = {}
    for e in email_list:
        normalized = [normalize_email(em) for em in e]
        for email in normalized:
            mapping[email] = normalized
    return mapping

def read_mapping(name=MAPPING_FILE):
    with open(name) as f:
        return email_mapping(f.readlines())

# check if email and it's mappings are in iterable
def email_in(mapping, iterable, email):
    mapped = mapping.get(email) or [email]
    mapped.append(normalize_email(email))
    acc = None
    for e in mapped:
        found = e in iterable
        if found:
            acc = acc or e
    return acc

# get mapped email from dicts
def email_lookup(mapping, dictionary, email):
    mapped = mapping.get(email) or [email]
    for e in mapped:
        item = dictionary.get(e)
        if item:
            return item
    return None

def data_email_exists(mapping, data, owners):
    data_copy = [copy.copy(d) for d in data]
    for d in data_copy:
        d['email'] = email_in(mapping, owners, d['email'])
    transformed = [d for d in data_copy if d['email']]
    not_found = [d for d in data if not email_in(mapping, owners,
                                                 d['email'])]
    return transformed, not_found

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
        return set([e[0] for e in cursor.fetchall()])

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
