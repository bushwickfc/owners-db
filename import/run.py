# The main app module.
# The basic flow is that we pull data from a Google Sheet, do some reformatting/processing,
# then insert that into the db.
import import_from_google_sheet
import handle_data
import insert
import report

# A dict representing all of the fields of interest.
# This will get split off as needed into different tables by insert.py.
data_dict = {
    'old_member_id': None,
    'pos_id': None,
    'seven_shifts_id': None,
    'email': None,
    'first_name': None,
    'last_name': None,
    'join_date': None,
    'phone': None,
    'address': None,
    'city': None,
    'state': None,
    'zipcode': None,
    'payment_plan_delinquent': None,
    'amount': None,
    'owner_type': None
}

def execute():
    new_owner_raw_data, master_db_raw_data = import_from_google_sheet.execute()
    master_data = handle_data.execute(new_owner_raw_data, master_db_raw_data, data_dict)
    insert.execute(master_data)
    report.execute(master_data, data_dict)
    print("Done!")

if __name__ == '__main__':
    execute()
