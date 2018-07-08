import util

def last_update(conn):
    query = "select max(hour_date) from hour_log where \
                  hour_reason = 'meeting'"
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()[0]

def transform(log):
    return { 'email': util.normalize_email(log['Email']),
             'first_name': log['First Name'],
             'last_name': log['Last Name'],
             'timestamp': log['Timestamp'],
             'date': util.timestamp_to_date(log['Timestamp'])}

def import_meeting(conn, meeting_attendance):
    last = last_update(conn)
    owners = util.existing(conn, 'owner')
    log_new = [l for l in meeting_attendance
               if (not last) or l['timestamp'] > last]
    log_ins = [l for l in log_new if l['email'] in owners]
    log_not_ins = [l for l in log_new if l['email'] in owners]
    # meetings are 2 hours
    query = """insert into hour_log(email, amount, hour_date, reason) \
               values (%(email)s, 2, %(date)s, 'meeting')"""
    with conn.cursor() as cursor:
        cursor.executemany(query, log_ins)
    return log_not_ins
