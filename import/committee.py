import copy
from datetime import datetime

import google_sheets
import util

SHEET_TITLE = 'Committee Work Hours Tracking (2018)'

MONTH_MAP = {'January': 1,
             'February': 2,
             'March': 3,
             'April': 4,
             'May': 5,
             'June': 6,
             'July': 7,
             'August': 8,
             'September': 9,
             'October': 10,
             'November': 11,
             'December': 12}

def committee_title(sheet_title):
    if sheet_title == 'Board of Directors':
        return 'board'
    else:
        return sheet_title.lower()

def import_committee(conn, dry_run):
    # Grab all of the pages, except for the first one.
    sheets = google_sheets.fetch_sheets(SHEET_TITLE, 1, None)
    not_inserted = []
    for s in sheets:
        result = import_sheet(conn, s, dry_run)
        not_inserted.append(result)
    # flatten the list of uninserted commmittee hours
    return [item for sublist in not_inserted for item in sublist]

def month_and_year_to_date(month, year):
    return datetime(day=1,month=MONTH_MAP[month],year=year)

def transform(committee, row):
    # if no row['Year worked'] or row['Year worked'] is '', sub in the current year...
    # likely to only be an issue the first time we run this script
    year = datetime.now().year if 'Year worked' not in row or row['Year worked'] == '' else row['Year worked']
    return { 'email': util.normalize_email(row['Email Address']),
             'timestamp': row['Timestamp'],
             'first_name': row['First Name'], # still in use?
             'last_name': row['Last Name'], # still in use?
             'month_worked': row['Month worked'], # still in use?
             'date': month_and_year_to_date(row['Month worked'], year),
             'hours': row['Number of Hours'],
             'committee': committee,
             'database': row.get(google_sheets.DATABASE_COL) }

def insert_hour(conn, row):
    query = """insert into hour_log(email, amount, hour_date, hour_reason) \
               values (%(email)s, %(hours)s, %(date)s, %(committee)s)"""
    with conn.cursor() as cursor:
        cursor.execute(query, row)

mapping = util.read_mapping()

def import_sheet(conn, sheet, dry_run):
    now_str = util.get_now_str()
    committee = committee_title(sheet.title)
    header_map = google_sheets.get_header_map(sheet)
    rows = google_sheets.get_all_records(sheet)
    owners = util.existing(conn, 'owner')
    not_inserted = []
    for row_idx, row in enumerate(rows):
        # 1 indexed + account for header
        idx = row_idx + 2
        row = transform(committee, row)

        # skip if blank or already inserted
        if not row['timestamp'] or row['database']:
            continue
        if not util.email_in(mapping, owners, row['email']):
            not_inserted.append(row)
            continue

        row = copy.copy(row)
        row['email'] = util.email_in(mapping, owners, row['email'])
        insert_hour(conn, row)
        google_sheets.update_cell(sheet, idx, header_map[google_sheets.DATABASE_COL], now_str, dry_run)

    return not_inserted
