import util

def existing(conn, date):
    query = """select 1 from hour_log where reason='monthly_requirement' \
               and hour_date=?"""
    with conn.cursor() as cursor:
        cursor.execute()
        return cursor.fetchone(query, date)[0]

# TODO: we only want to debit people who signed up before the 15 of last mongth
def debit(conn, date):
    if existing(conn, date):
        return
    query = """insert into hour_log (email, amount, hour_reason, hour_date)
               (select cot.email, -ot.work_requirement, 'monthly_requirement', ?
               from current_owner_type cot
               join owner_type ot on cot.owner_type = ot.owner_type)"""
    cursor.execute(query, date)
