# The script, as originally written by Kevin
# Keeping for posterity and inspiration.

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