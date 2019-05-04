import util
import google_sheets

SHEET_TITLE = 'Monthly Co-op Meeting Attendance Tracking'

def transform(row, row_idx):
    return { 'email': util.standardize_email(row['Email']),
             'first_name': row['First Name'],
             'last_name': row['Last Name'],
             'timestamp': util.parse_gs_timestamp(row['Timestamp']),
             'date': util.parse_gs_timestamp(row['Timestamp']),
             'database': row.get(google_sheets.DATABASE_COL),
             'row_idx': row_idx }

def import_meeting(conn):
    # We use the second page of the meetings sheet.
    # DON'T FORGET TO CHANGE THIS BACK TO 1 - CURRENTLY USING A TEST SHEET
    sheets = google_sheets.fetch_sheets(SHEET_TITLE, 2)
    for s in sheets:
        result = import_sheet(conn, s)
    return result

def insert_meeting(conn, row):
    # meetings are 2 hours
    query = """insert into hour_log(email, amount, hour_date, hour_reason) \
               values (%(email)s, 2, %(date)s, 'meeting')"""
    with conn.cursor() as cursor:
        cursor.execute(query, row)

def import_sheet(conn, sheet):
    mapping = util.read_mapping()
    header_map = google_sheets.get_header_map(sheet)
    now_str = util.get_now_str()
    rows = google_sheets.get_all_records(sheet)
    transormed_rows = [transform(row, row_idx) for row_idx, row in enumerate(rows)]
    owners = util.existing(conn, 'owner')
    log_ins, log_not_ins = \
                       util.data_email_exists(mapping, transormed_rows, owners)

    for row in log_ins:
        if row['database'] == None:
            insert_meeting(conn, row)
            google_sheets.update_cell(sheet, row['row_idx'] + 2, header_map[google_sheets.DATABASE_COL], now_str)
        else:
            continue

    return log_not_ins
