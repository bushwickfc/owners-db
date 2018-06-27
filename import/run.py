#!/usr/bin/env python3
# The main app module.
# The basic flow is that we pull data from a Google Sheet, do some reformatting/processing,
# then insert that into the db.
import argparse
import csv

import dicts
import import_from_google_sheet
import handle_data
import insert
import report

def owner_import(args):
    new_owner_raw_data = args.new_owner
    master_db_raw_data = args.master_sheet
    if not new_owner_raw_data:
        new_owner_raw_data = import_from_google_sheet.fetch(
            'Copy of New Owner Onboarding',
            'All New Owners')
        # skip the test row
    else:
        with open(new_owner_raw_data) as f:
            csv_reader = csv.DictReader(f)
            new_owner_raw_data = list(csv_reader)
    new_owner_raw_data = new_owner_raw_data[1:]
    if not master_db_raw_data:
        master_db_raw_data = import_from_google_sheet.fetch(
            'Copy of BFC Member Database (ACTIVE)',
            'MASTER DB')
    else:
        with open(master_db_raw_data) as f:
            csv_reader = csv.DictReader(f)
            master_db_raw_data = list(csv_reader)
    master_data = handle_data.execute(new_owner_raw_data,
                                      master_db_raw_data,
                                      dicts.master_data_dict)
    insert.execute(master_data)
    #report.execute(master_data, dicts.master_data_dict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    owner_parser = subparsers.add_parser('owner_import')
    owner_parser.add_argument("--new_owner",
                              help="new owner csv - \
                              downloaded from sheets if None")
    owner_parser.add_argument("--master_sheet",
                              help="master csv - \
                              downloaded from sheets if None")
    owner_parser.set_defaults(func=owner_import)
    args = parser.parse_args()
    args.func(args)
