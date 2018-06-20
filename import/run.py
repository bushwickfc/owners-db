#!/usr/bin/env python3
# The main app module.
# The basic flow is that we pull data from a Google Sheet, do some reformatting/processing,
# then insert that into the db.
import argparse
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
            'All New Owners',
            # skip the header and test rows
            (3,1))
    if not master_db_raw_data:
        master_db_raw_data = import_from_google_sheet.fetch(
            'Copy of BFC Member Database (ACTIVE)',
            'MASTER DB',
            # skip the header
            (2,1))

    master_data = handle_data.execute(new_owner_raw_data,
                                      master_db_raw_data,
                                      dicts.master_data_dict)
    insert.execute(master_data)
    report.execute(master_data, dicts.master_data_dict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    owner_parser = subparsers.add_parser('owner_import')
    owner_parser.parse_args("--new_owner",
                            help="new owner csv -
                            downloaded from sheets if None")
    owner_parser.parse_args("--master_sheet",
                            help="master csv -
                            downloaded from sheets if None")
    owner_parser.set_defaults(func=owner_import)
    parser.parse_args()
