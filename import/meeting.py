import util
import google_sheets

SHEET_TITLE = 'Monthly Co-op Meeting Attendance Tracking'

def import_meeting(conn):
    sheets = google_sheets.fetch_sheets(SHEET_TITLE, 1)
    not_inserted = []
    for s in sheets:
        import_sheet(conn, s)

def import_sheet(conn, sheet):
    rows = sheet.get_all_records()
    for row_idx, row in enumerate(rows):
            [transform(r) for r in rows]
        # [transform(r) for r in rows if r['Timestamp']]


# def last_update(conn):
#     query = "select max(hour_date) from hour_log where \
#                   hour_reason = 'meeting'"
#     with conn.cursor() as cursor:
#         cursor.execute(query)
#         return cursor.fetchone()[0]

def transform(row):
    print(row)
    # return { 'email': util.standardize_email(row['Email']),
    #          'first_name': row['First Name'],
    #          'last_name': row['Last Name'],
    #          'timestamp': util.parse_gs_timestamp(row['Timestamp']),
    #          'date': util.parse_gs_timestamp(row['Timestamp'])}

# mapping = util.read_mapping()

# def import_meeting(conn, meeting_attendance):
#     last = last_update(conn)
#     owners = util.existing(conn, 'owner')
#     log_new = [l for l in meeting_attendance
#                if (not last) or l['timestamp'] > last]
#     log_ins, log_not_ins = \
#                            util.data_email_exists(mapping, log_new, owners)
#     # meetings are 2 hours
#     query = """insert into hour_log(email, amount, hour_date, hour_reason) \
#                values (%(email)s, 2, %(date)s, 'meeting')"""
#     with conn.cursor() as cursor:
#         cursor.executemany(query, log_ins)
#     return log_not_ins
