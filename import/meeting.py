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
             'row_idx': row_idx } # Store the row's index as well, used for updating the GSheet

def import_meeting(conn, dry_run):
    # We use the second page of the meetings sheet.
    sheets = google_sheets.fetch_sheets(SHEET_TITLE, 1)
    for s in sheets:
        result = import_sheet(conn, s, dry_run)
    return result

def insert_meeting(conn, row):
    # meetings are 2 hours
    query = """insert into hour_log(email, amount, hour_date, hour_reason) \
               values (%(email)s, 2, %(date)s, 'meeting')"""
    with conn.cursor() as cursor:
        cursor.execute(query, row)

def import_sheet(conn, sheet, dry_run):
    mapping = util.read_mapping()
    header_map = google_sheets.get_header_map(sheet)
    now_str = util.get_now_str()
    rows = google_sheets.get_all_records(sheet)
    transformed_rows = [transform(row, row_idx) for row_idx, row in enumerate(rows)]
    owners = util.existing(conn, 'owner')
    log_ins, log_not_ins = \
                       util.data_email_exists(mapping, transformed_rows, owners)

    for row in log_ins:
        # The actual row index in the GSheet will be two more than the row's position in the list.
        idx = row['row_idx'] + 2

        if row['database'] == None:
            insert_meeting(conn, row)
            google_sheets.update_cell(sheet, idx, header_map[google_sheets.DATABASE_COL], now_str, dry_run)
        else:
            continue

    return log_not_ins
