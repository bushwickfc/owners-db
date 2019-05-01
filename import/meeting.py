import util
import google_sheets

SHEET_TITLE = 'Monthly Co-op Meeting Attendance Tracking'
DATABASE_COL = 'DATABASE (Place an X when hours have been added to database by hours@)'
mapping = util.read_mapping()

def transform(row):
    return { 'email': util.standardize_email(row['Email']),
             'first_name': row['First Name'],
             'last_name': row['Last Name'],
             'timestamp': util.parse_gs_timestamp(row['Timestamp']),
             'date': util.parse_gs_timestamp(row['Timestamp']),
             'database': row.get(DATABASE_COL) }

def import_meeting(conn):
    # Get the second page of the sheet.
    sheets = google_sheets.fetch_sheets(SHEET_TITLE, 1)
    for s in sheets:
        result = import_sheet(conn, s)
    return result

def insert_meeting(conn, row):
    print(row)
    # # meetings are 2 hours
    # query = """insert into hour_log(email, amount, hour_date, hour_reason) \
    #            values (%(email)s, 2, %(date)s, 'meeting')"""
    # with conn.cursor() as cursor:
    #     cursor.execute(query, row)

def import_sheet(conn, sheet):
    rows = sheet.get_all_records()
    # Skip any empty row, likely the first
    transormed_rows = [transform(row) for row in rows if len(list(row.keys())) > 0]
    owners = util.existing(conn, 'owner')
    log_ins, log_not_ins = \
                       util.data_email_exists(mapping, transormed_rows, owners)

    for row in log_ins:
        if row['database'] == None:
            insert_meeting(conn, row)
        else:
            continue

    return log_not_ins






# def last_update(conn):
#     query = "select max(hour_date) from hour_log where \
#                   hour_reason = 'meeting'"
#     with conn.cursor() as cursor:
#         cursor.execute(query)
#         return cursor.fetchone()[0]

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
