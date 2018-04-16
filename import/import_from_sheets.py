import argparse
import csv

import pymysql.cursors



def main():
    parser = argparse.ArgumentParser(description='Ingest from csv')
    parser.add_argument('csv')
    args = parser.parse_args()
    with open(args.csv) as f:
        csv_reader = csv.DictReader(f)
        members = [m for m in csv_reader]

    connection = pymysql.connect(host='localhost',
                                 user='admin',
                                 password='admin',
                                 db='owner_db',
                                 cursorclass=pymysql.cursors.DictCursor)

    


if __name__ == '__main__':
    main()
