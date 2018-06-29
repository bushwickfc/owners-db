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
        'start_date': util.timestamp_to_date(row['Timestamp']),
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

def existing(conn, table):
    query = "select distinct email from {}".format(table)
    with conn.cursor() as cursor:
        cursor.execute(query)
        return set([util.normalize_email(e[0]) for e in cursor.fetchall()])

def insert_equity_type(conn, equity_types):
    existing_equity = existing(conn, "owner_equity_type")
    owners = existing(conn, 'owner')
    equity_types = util.dedupe(equity_types, lambda x: x['email'])
    equity_types = [e for e in equity_types
                    if e['email'] not in existing_equity
                    and e['email'] in owners]
    query = """insert into owner_equity_type(email, equity_type, start_date) \
               values (%(email)s, %(equity_type)s, %(start_date)s)"""
    with conn.cursor() as cursor:
        cursor.executemany(query, equity_types)

def last_update(conn):
    query = 'select max(transaction_date) from equity_log'
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()[0]

def insert_payment(conn, equity_payments):
    last = last_update(conn)
    owners = existing(conn, 'owner')
    equity_payments = [p for p in equity_payments
                       if p['email'] in owners
                       and ((not last) or p['transaction_date'] > last)]
    query = """insert into equity_log(email, amount, transaction_date) \
               values (%(email)s, %(amount)s, %(transaction_date)s)"""
    with conn.cursor() as cursor:
        cursor.executemany(query, equity_payments)
