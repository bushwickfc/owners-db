# This module will take the data produced by handle_data and insert it
# into the db.
import psycopg2
import time
import dicts
import util

# Divvy up the data for the data_dict-formatted owner (a row in
# master_date) to reflect the different tables we're inserting into...
def dict_to_tables(master_data):
    current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    owner_data = []
    hour_log_data = []
    owner_owner_type_data = []

    for d in master_data:
        owner_dict = dict(dicts.owner_dict,
                          old_member_id=d['old_member_id'],
                          pos_id=d['pos_id'],
                          seven_shifts_id=d['seven_shifts_id'],
                          email=d['email'],
                          first_name=d['first_name'],
                          last_name=d['last_name'],
                          join_date=d['join_date'],
                          phone=d['phone'],
                          address=d['address'],
                          city=d['city'],
                          state=d['state'],
                          zipcode=d['zipcode'],
                          payment_plan_delinquent=d['payment_plan_delinquent'])
        # In this import script, all hours logged are balance_carryovers...
        # and I assume that the hour_date would just be the date of the import.
        hour_log_dict = dict(dicts.hour_log_dict,
                             email=d['email'],
                             amount=d['amount'],
                             hour_reason='balance_carryover',
                                                  hour_date=current_date)
        # In this case, I assume that start_date is the same as join_date.
        owner_owner_type_dict = dict(
            dicts.owner_owner_type_dict, email=d['email'],
            start_date=d['join_date'],
            owner_type=d['owner_type'])

        owner_data.append(owner_dict)
        hour_log_data.append(hour_log_dict)
        owner_owner_type_data.append(owner_owner_type_dict)

    return owner_data, hour_log_data, owner_owner_type_data

# Create the cols and params from a dict from each table.
def cols_from_dict(d):
    names = list(d.keys())
    params = ', '.join(['%({})s'.format(name) for name in names])
    cols = ', '.join(names)
    return cols, params

# An owner's email address is their unique identifier across
# tables. In order to make this script safe to re-run, check to see
# whether an associated owner record already exists for a particular
# table.
def exists(cursor, table, email):
    query = f'SELECT * FROM {table} WHERE email=\'{email}\''
    cursor.execute(query)
    return False if cursor.fetchone() == None else True

# Handle the data insert.
# We want this script to be idempotent, so before every insert, check
# to see whether or not a record associated with that email address
# already exists for that table.
def bulk_insert(connection, data_query_dicts):
    with connection.cursor() as cursor:
        for dq in data_query_dicts:
            query = f'INSERT INTO {dq["table"]} ({{}}) VALUES({{}})'.format(
                dq['cols'], dq['params'])
            for d in dq['data']:
                table = dq['table']
                email = d['email']
                if not exists(cursor, table, email):
                    try:
                        cursor.execute(query, d)
                    except psycopg2.Error as e:
                        print(f'- error: failed to insert record for \
                        {email} into table {table} with error {e}')
                    else:
                        print(f'- success: inserted record for {email} \
                        into table {table}')

def last_update(conn):
    query = 'select max(join_date) from owner'
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()[0]

def execute(master_data):
    print('Inserting data into database...')
    with util.connection() as connection:

        last_ingest = last_update(connection)
        # >= in case someone joins later in the day that we ran the ingest
        master_data = [d for d in master_data
                       if (not last_ingest) or d['join_date'] >= last_ingest]

        # Split up each owner's master_data into set of related table data
        # to be inserted
        owner_data, hour_log_data, owner_owner_type_data = \
            dict_to_tables(master_data)

        # Using each table dict, turn the keys into cols and params
        owner_cols, owner_params = cols_from_dict(dicts.owner_dict)
        hour_log_cols, hour_log_params = cols_from_dict(dicts.hour_log_dict)
        owner_owner_type_cols, owner_owner_type_params = cols_from_dict(dicts.owner_owner_type_dict)

        # Finally, put each set of data and its associated data for
        # building the query into a list of dicts...
        data_query_dicts = [
            {'data': owner_data, 'cols':
             owner_cols, 'params': owner_params,
             'table': 'owner'},
            {'data': hour_log_data, 'cols': hour_log_cols,
             'params': hour_log_params, 'table': 'hour_log'},
            {'data': owner_owner_type_data,
             'cols': owner_owner_type_cols,
             'params': owner_owner_type_params,
             'table': 'owner_owner_type'}]

        bulk_insert(connection, data_query_dicts)
