from datetime import datetime

import pygsheets

import util

SHEET_TITLE = 'Copy of Committee Work Hours Tracking (2018)'

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

APPROVAL_COL = 'COMMITTEE CHAIR APPROVAL (Please initial below to approve committee member hours. Board liaison should approve chair hours.)'

DATABASE_COL = 'DATABASE'

def committee_title(sheet_title):
    if sheet_title == 'Board of Directors':
        return 'board'
    else:
        return sheet_title.lower()

def fetch_committee_sheets():
    gc = pygsheets.authorize(outh_file='client_secret.json', outh_nonlocal=True)
    sheet = gc.open(SHEET_TITLE)
    # ignore first sheet which contains all responses
    # the filtered sheets contain approvals
    return sheet.worksheets()[1:]

def import_committee(conn):
    sheets = fetch_committee_sheets()
    for s in sheets:
        import_sheet(conn, s)

def month_to_date(month):
    time = datetime.now()
    return time.replace(day=1,month=MONTH_MAP[month])

def transform(committee, row):
    return { 'email': util.normalize_email(row['Email Address']),
             'timestamp': row['Timestamp'],
             'first_name': row['First Name'],
             'last_name': row['Last Name'],
             'month_worked': row['Month worked'],
             'date': month_to_date(row['Month worked']),
             'hours': row['Number of Hours'],
             'committee': committee,
             'database': row.get(DATABASE_COL),
             'approved': row.get(APPROVAL_COL) }

def insert_hour(conn, row):
    query = """insert into hour_log(email, amount, hour_date, hour_reason) \
               values (%(email)s, %(hours)s, %(date)s, %(committee)s)"""
    with conn.cursor() as cursor:
        cursor.execute(query, row)

def import_sheet(conn, sheet):
    committee = committee_title(sheet.title)
    header_map = dict([(c, i+1) for i, c in
                       enumerate(sheet.get_values((1,1), (1,sheet.cols))[0])
                       if c])
    rows = sheet.get_all_records()
    owners = util.existing(conn, 'owner')
    not_inserted = []
    for row_idx, row in enumerate(rows):
        # 1 indexed + account for header
        idx = row_idx + 2
        row = transform(committee, row)
        if row['email'] not in owners:
            not_inserted.append(row)
            continue
        # insert if not blank and not already inserted
        if row['timestamp'] and row['approved'] and not row['database']:
            insert_hour(conn, row)
            sheet.update_cell((idx, header_map[DATABASE_COL]), 'inserted')
