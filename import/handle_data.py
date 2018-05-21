# This module will get data from Google Sheets, format it, and write it to a .csv
import csv
import util

# A dict representing all of the fields in the 'owner' table.
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

# Create a list of dictionaries, with each dictionary containing the data
# to be inserted for that member.
def process_raw_data(raw_data):
    print('Processing raw data...')
    owner_dict_list = []
    for row in raw_data:
        # Create a new 'main' dictionary for the owner...
        owner_dict = dict(data_dict)
        # and a temporary dictionary to help get the data formatted.
        tmp_dict = {
            'join_date': util.timestamp_to_date(row[0]),
            'first_name': row[1],
            'last_name': row[2],
            'email': util.normalize_email(row[3]),
            'display_name': row[1] + ' ' + row[2]      
        }

        # For each key in the owner dictionary, if that key is found in the tmp_dict,
        # update it with that value. Otherwise, return the default.
        for k in owner_dict:
            if k in tmp_dict:
                owner_dict[k] = tmp_dict[k]

        owner_dict_list.append(owner_dict)

    return owner_dict_list

# Write the data to a .csv file
def write_data_to_csv(data, filename):
    print(f'Writing data to {filename}...')
    with open(filename, 'w') as new_owner_csv:
        dict_writer = csv.DictWriter(new_owner_csv, data_dict.keys())
        dict_writer.writeheader()
        dict_writer.writerows(data)

def execute(raw_data, filename):
    processed_data = process_raw_data(raw_data)
    write_data_to_csv(processed_data, filename)







# import argparse
# import csv
# from datetime import date, datetime
# from dateutil.parser import parse

# import pymysql.cursors

# MAPPING = {'MEMBER ID':'old_member_id',
#            'POS ID':'pos_id',
#            'FIRST NAME':'first_name',
#            'LAST NAME':'last_name',
#            'EMAIL ADDRESS':'email',
#            'PHONE NUMBER':'phone',
#            'JOIN DATE':'join_date'}

# def cols_from_dict(d):
#     names = list(d.keys())
#     params = ', '.join(['%({})s'.format(name) for name in names])
#     cols = ', '.join(names)
#     return cols, params

# def csv_to_sql(member):
#     row = {}
#     for k, v in MAPPING.items():
#         row[v] = member[k]
#     row['owner_type'] = 'standard'
#     if row['join_date']:
#         row['join_date'] = parse(row['join_date'])\
#                            .strftime('%Y-%m-%d')
#     else:
#         row['join_date'] = '2000-01-01'
#     row['phone'] = row['phone'].replace('.','').replace('-','')
#     return row

# def bulk_insert(connection, query, data):
#     print(data)
#     with connection.cursor() as cursor:
#         for d in data:
#             cursor.execute(query, d)
#         connection.commit()

# def main():
#     parser = argparse.ArgumentParser(description='Ingest from csv')
#     parser.add_argument('csv')
#     args = parser.parse_args()
#     with open(args.csv) as f:
#         csv_reader = csv.DictReader(f)
#         members = list(csv_reader)

#     connection = pymysql.connect(host='localhost',
#                                  user='admin',
#                                  password='admin',
#                                  db='owner_db',
#                                  cursorclass=pymysql.cursors.DictCursor)
#     owners = [csv_to_sql(m) for m in members]
#     cols, params = cols_from_dict(owners[0])
#     query = 'INSERT INTO owner ({}) VALUES ({})'.format(cols, params)
#     bulk_insert(connection, query, owners[2:4])



# if __name__ == '__main__':
#     main()
