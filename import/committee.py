import pygsheets

import util

SHEET_TITLE = 'Copy of Committee Work Hours Tracking (2018)'

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
    import_sheet(conn, sheets[0])

def transform(row):
    return { 'email': util.normalize_email(row['Email Address']),
             'timestamp': row['Timestamp'],
             'first_name': row['First Name'],
             'last_name': row['Last Name'],
             'month_worked': row['Month worked'],
             'hours': row['Number of Hours'],
             'database': row['DATABASE'],
             'approved': row['COMMITTEE CHAIR APPROVAL (Please initial below to approve committee member hours. Board liaison should approve chair hours.)'] }

def import_sheet(conn, sheet):
    committee = committee_title(sheet.title)
    import pdb; pdb.set_trace()
