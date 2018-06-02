# This module will take the data produced by handle_data and insert it into the db.
import pymysql.cursors
import time
import credentials # This file is gitignored - you'll need to provide your own copy

# Divvy up the data in the data_dict to reflect the different tables we're inserting into...
def parse_dict(data):
    owner_data = []
    hour_log_data = []
    owner_owner_type_data = []

    for d in data:
        current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        owner_dict = {
            'old_member_id': d['old_member_id'],
            'pos_id': d['pos_id'],
            'seven_shifts_id': d['seven_shifts_id'],
            'email': d['email'],
            'first_name': d['first_name'],
            'last_name': d['last_name'],
            'display_name': d['display_name'],
            'join_date': d['join_date'],
            'phone': d['phone'],
            'address': d['address'],
            'city': d['city'],
            'state': d['state'],
            'zipcode': d['zipcode'],
            'payment_plan_delinquent': d['payment_plan_delinquent']
        }
        # In this import script, all hours logged are balance_carryovers...
        # and I presume that the hour_date would just be the date of the import.
        hour_log_dict = {
            'email': d['email'],
            'amount': d['amount'],
            'hour_reason': 'balance_carryover',
            'hour_date': current_date
        }
        owner_owner_type_dict = {
            'email': d['email'],
            'start_date': d['join_date'],
            'owner_type': d['owner_type']
        }

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

def bulk_insert(connection, data_query):
    with connection.cursor() as cursor:
        for dq in data_query:
            for d in dq['data']:
                cursor.execute(dq['query'], d)

    connection.commit()
    connection.close()

def execute(all_data):
    print('Inserting data into database...')
    connection = pymysql.connect(host=credentials.host,
                             user=credentials.user,
                             password=credentials.password,
                             db=credentials.db,
                             cursorclass=pymysql.cursors.DictCursor)

    owner_data, hour_log_data, owner_owner_type_data = parse_dict(all_data)

    owner_cols, owner_params = cols_from_dict(owner_data[0])
    hour_log_cols, hour_log_params = cols_from_dict(hour_log_data[0])
    owner_owner_type_cols, owner_owner_type_params = cols_from_dict(owner_owner_type_data[0])

    owner_query = 'INSERT INTO owner ({}) VALUES ({})'.format(owner_cols, owner_params)
    hour_log_query = 'INSERT INTO hour_log ({}) VALUES ({})'.format(hour_log_cols, hour_log_params)
    owner_owner_type_query = 'INSERT INTO owner_owner_type ({}) VALUES ({})'.format(owner_owner_type_cols, owner_owner_type_params)

    data_query = [{'data': owner_data, 'query': owner_query},
                  {'data': hour_log_data, 'query': hour_log_query},
                  {'data': owner_owner_type_data, 'query': owner_owner_type_query}]

    bulk_insert(connection, data_query)
