#!/usr/bin/env python3
# The main app module.
# The basic flow is that we pull data from a Google Sheet, do some reformatting/processing,
# then insert that into the db.
import argparse
import csv
from datetime import date
from datetime import timedelta
from datetime import datetime

import dicts
import import_from_google_sheet
import handle_data
import insert
import report
import equity_ingest
import util
import seven_shifts
import meeting
import committee

def owner_import(args):
    new_owner_csv = args.new_owner
    master_db_csv = args.master_sheet
    if not new_owner_csv:
        new_owner_raw_data = import_from_google_sheet.fetch(
            'Copy of New Owner Onboarding',
            'All New Owners')
    else:
        with open(new_owner_csv) as f:
            csv_reader = csv.DictReader(f)
            new_owner_raw_data = list(csv_reader)
    # skip the test row
    new_owner_raw_data = new_owner_raw_data[1:]
    if not master_db_csv:
        master_db_raw_data = import_from_google_sheet.fetch(
            'Copy of BFC Member Database (ACTIVE)',
            'MASTER DB')
    else:
        with open(master_db_csv) as f:
            csv_reader = csv.DictReader(f)
            master_db_raw_data = list(csv_reader)
    master_data = handle_data.execute(new_owner_raw_data,
                                      master_db_raw_data,
                                      dicts.master_data_dict)
    insert.execute(master_data)
    report.execute(master_data,
                   handle_data.process_master_db_data(master_db_raw_data))

def equity_import(args):
    equity_csv = args.equity_payments
    equity_type_csv = args.payment_agreement
    with open(equity_csv) as f:
        csv_reader = csv.DictReader(f)
        equity_payments = list(csv_reader)

    with open(equity_type_csv) as f:
        csv_reader = csv.DictReader(f)
        equity_types = list(csv_reader)

    equity_types = [equity_ingest.owner_equity_type(r) for r in equity_types]
    equity_payments = [equity_ingest.owner_equity_payment(r)
                       for r in equity_payments]

    with util.connection() as conn:
        et_review = equity_ingest.insert_equity_type(conn, equity_types)
        ep_review = equity_ingest.insert_payment(conn, equity_payments)
    util.write_review_file(et_review, 'equity_type', 'equity types')
    util.write_review_file(ep_review, 'equity_payment', 'equity payments')

def seven_shifts_import(args):
    start_date, end_date = args.start_date, args.end_date
    with util.connection() as conn:
        if not start_date:
            last = util.last_hour_update(conn, 'shift')
            if last:
                # add one day becuase seven shifts api only supports greater
                # than
                last = (last + timedelta(days=1)).isoformat()
            # if we have no shift data, this is where the old db stops
            start_date = last or '2018-06-01'
        if not end_date:
            end_date = date.today().isoformat()
        responses = seven_shifts.fetch_shifts(start_date, end_date)
        user_shifts = [seven_shifts.transform(r) for r in responses]
        ss_review = seven_shifts.insert(conn, user_shifts)
    util.write_review_file(ss_review, 'shift_data', 'shift data')

def meeting_import(args):
    with open(args.attendance_csv) as f:
        csv_reader = csv.DictReader(f)
        meeting_csv = list(csv_reader)
    # need to check cell because there is a blank line at the beginning of
    # the file
    meeting_attendance = [meeting.transform(m) for m in meeting_csv
                          if m['Timestamp']]
    with util.connection() as conn:
        m_review = meeting.import_meeting(conn, meeting_attendance)
    util.write_review_file(m_review, 'meeting_attendance',
                           'meeting attendance entries')

def committee_import(args):
    with util.connection() as conn:
        commitee_review = committee.import_committee(conn)
    util.write_review_file(commitee_review, 'commitee_hour',
                           'commitee work reports')

def hours_debit(args):
    debit_date = args.debit_date
    if not debit_date:
        raise ValueError
    debit_date = util.parse_iso_date(args.debit_date)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    owner_parser = subparsers.add_parser('owner-import')
    owner_parser.add_argument("--new-owner",
                              help="new owner csv - \
                              downloaded from sheets if None")
    owner_parser.add_argument("--master-sheet",
                              help="master csv - \
                              downloaded from sheets if None")
    owner_parser.set_defaults(func=owner_import)

    equity_parser = subparsers.add_parser('equity-import')
    equity_parser.add_argument("--equity-payments",
                               help="equity payment csv")
    equity_parser.add_argument("--payment-agreement",
                               help="payment plan agreement")
    equity_parser.set_defaults(func=equity_import)

    shifts_parser = subparsers.add_parser('seven-shifts')
    shifts_parser.add_argument("--start-date")
    shifts_parser.add_argument("--end-date")
    shifts_parser.set_defaults(func=seven_shifts_import)

    meeting_parser = subparsers.add_parser('meeting-attendance')
    meeting_parser.add_argument("attendance_csv")
    meeting_parser.set_defaults(func=meeting_import)

    committee_parser = subparsers.add_parser('committee')
    committee_parser.set_defaults(func=committee_import)

    hours_debit_parser = subparsers.add_parser('hours_debit')
    shifts_parser.add_argument("--debit-date")
    hours_debit_parser.set_defaults(func=hours_debit)

    args = parser.parse_args()
    args.func(args)
