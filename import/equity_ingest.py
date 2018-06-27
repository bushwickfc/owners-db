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
        'timestamp': util.timestamp_to_date(row['Timestamp']),
        'equity_type': equity_owed_to_type(
            row['Equity Investment / Inversión de Capital']),
        'name': ' '.join([row['First Name / Nombre'],
                          row['Last Name / Apellido']]) }

def owner_equity_payment(row):
    return {
        'email': util.normalize_email(row['SEARCHKEY']),
        'name': row['NAME'].split('//')[0].strip(),
        'date': datetime.strptime(row['date'], '%Y-%m-%d').date(),
        'amount': row['TOTAL'] }

def existing(conn, table):
    query = "select distinct email from {}".format(table)
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def insert_equity_type(equity_types):
    existing_equity = existing(conn, "owner_equity_type")
