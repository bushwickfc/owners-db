import util
from dateutil.relativedelta import *

def existing(conn, date):
    query = """select 1 from hour_log where hour_reason='monthly_requirement' \
               and hour_date=%s"""
    with conn.cursor() as cursor:
        cursor.execute(query, (date,))
        return cursor.fetchone()

# TODO: we only want to debit people who signed up before the 15 of last mongth
def debit(conn, date):
    if existing(conn, date):
        print('Hour debit already run for date, skipping')
        return
    cutoff = (date - relativedelta(months=1, day=14))
    query = """insert into hour_log (email, amount, hour_reason, hour_date)
               (select cot.email, -ot.work_requirement, 'monthly_requirement',
                %s
               from current_owner_type cot
               join owner_type ot on cot.owner_type = ot.owner_type
               join owner_equity_type oet on oet.email = cot.email
               where oet.start_date < %s)"""
    with conn.cursor() as cursor:
        cursor.execute(query, (date, cutoff))
        print('Hours debited')
