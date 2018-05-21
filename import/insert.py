# This module will take the .csv produced by handle_data and insert it into the db.
import pymysql.cursors
import csv
import credentials # This file is gitignored - you'll need to provide your own copy

data_dict = {
    'old_member_id': None,
    'pos_id': None,
    'seven_shifts_id': None,
    'email': None,
    'first_name': None,
    'last_name': None,
    'display_name': None,
    'join_date': '2000-01-01',
    'phone': None,
    'address': None,
    'city': None,
    'country': None,
    'zipcode': None,
    'payment_plan_delinquent': None
}

def cols_from_dict(d):
    names = list(d.keys())
    params = ', '.join(['%({})s'.format(name) for name in names])
    cols = ', '.join(names)
    return cols, params


# THIS IS MESSY...
def csv_to_sql(owner):
    owner = {
        'join_date': owner[7],
        'first_name': owner[4],
        'last_name': owner[5],
        'display_name': owner[6],
        'email': owner[3]
    }
    # row = {}

    # for k, v in data_dict.items():
    #     row[k] = owner[k]
    # return row
    return owner

def bulk_insert(connection, query, data):
    with connection.cursor() as cursor:
        for d in data:
            cursor.execute(query, d)

    connection.commit()
    connection.close()

def execute(filename):
    print('Inserting data into database...')
    with open(filename) as file:
        csvfile = csv.reader(file)
        owners_list = list(csvfile)

    owners = [csv_to_sql(o) for o in owners_list]
    cols, params = cols_from_dict(owners[0])
    connection = pymysql.connect(host=credentials.host,
                                 user=credentials.user,
                                 password=credentials.password,
                                 db=credentials.db,
                                 cursorclass=pymysql.cursors.DictCursor)
    query = 'INSERT INTO owner ({}) VALUES ({})'.format(cols, params)

    bulk_insert(connection, query, owners[1:])
