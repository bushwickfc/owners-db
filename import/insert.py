# This module will take the data produced by handle_data and insert it into the db.
import pymysql.cursors
import credentials # This file is gitignored - you'll need to provide your own copy

# Create the cols and params from a raw data_dict
def cols_from_dict(d):
    names = list(d.keys())
    params = ', '.join(['%({})s'.format(name) for name in names])
    cols = ', '.join(names)
    return cols, params

def bulk_insert(connection, query, data):
    with connection.cursor() as cursor:
        for d in data:
            cursor.execute(query, d)

    connection.commit()
    connection.close()

def execute(owner_data, data_dict):
    print('Inserting data into database...')
    cols, params = cols_from_dict(data_dict)
    connection = pymysql.connect(host=credentials.host,
                                 user=credentials.user,
                                 password=credentials.password,
                                 db=credentials.db,
                                 cursorclass=pymysql.cursors.DictCursor)
    query = 'INSERT INTO owner ({}) VALUES ({})'.format(cols, params)

    bulk_insert(connection, query, owner_data)
