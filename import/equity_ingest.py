import util

from datetime import datetime

def equity_owed_to_type(owed):
    if owed == '$100':
        return 'legacy'
    elif owed == '$150':
        return 'full'
    elif owed == '$15':
        return 'reduced'
    else:
        raise ValueError('unknown equity amount')

def owner_equity_type(row):
    return {
        'email': util.normalize_email(
            row['Email Address / Correo Electrónico']),
        'start_date': util.parse_gs_timestamp(row['Timestamp']),
        'equity_type': equity_owed_to_type(
            row['Equity Investment / Inversión de Capital']),
        'name': ' '.join([row['First Name / Nombre'],
                          row['Last Name / Apellido']]) }

def owner_equity_payment(row):
    return {
        'email': util.normalize_email(row['SEARCHKEY']),
        'name': row['NAME'].split('//')[0].strip(),
        'transaction_date': datetime.strptime(row['date'], '%Y-%m-%d').date(),
        'amount': row['TOTAL'] }

mapping = util.read_mapping()

def insert_equity_type(conn, equity_types):
    existing_equity = util.existing(conn, "owner_equity_type")
    owners = util.existing(conn, 'owner')
    equity_types = util.dedupe(equity_types, lambda x: x['email'])
    equity_types_new = [e for e in equity_types
                        if not util.email_in(mapping, existing_equity,
                                             e['email'])]
    equity_types_ins, equity_types_not_ins = \
     util.data_email_exists(mapping, equity_types_new, owners)
    query = """insert into owner_equity_type(email, equity_type, start_date) \
               values (%(email)s, %(equity_type)s, %(start_date)s)"""
    with conn.cursor() as cursor:
        cursor.executemany(query, equity_types_ins)
    return equity_types_not_ins

def last_update(conn):
    query = 'select max(transaction_date) from equity_log'
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()[0]

def insert_payment(conn, equity_payments):
    last = last_update(conn)
    owners = util.existing(conn, 'owner')
    equity_payments_new = [p for p in equity_payments if
                           (not last) or p['transaction_date'] > last]
    equity_payments_ins, equity_payments_not_ins = \
     util.data_email_exists(mapping, equity_payments_new, owners)
    query = """insert into equity_log(email, amount, transaction_date) \
               values (%(email)s, %(amount)s, %(transaction_date)s)"""
    with conn.cursor() as cursor:
        cursor.executemany(query, equity_payments_ins)
    return equity_payments_not_ins
