# The main app module.
# The basic flow is that we pull data from a Google Sheet, do some reformatting/processing,
# then insert that into the db.
import import_from_google_sheet
import handle_data
import insert
import write_to_console
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
# The following three dicts are specific to the tables that data will be inserted into.
# Data from the list of data_dicts (as master_data) will be used to populate these dicts in insert.py.
owner_dict = {
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
    'payment_plan_delinquent': None
}
hour_log_dict = {
    'email': None,
    'amount': None,
    'hour_reason': None,
    'hour_date': None
} 
owner_owner_type_dict = {
    'email': None,
    'start_date': None,
    'owner_type': None
}


def execute():
    new_owner_raw_data, master_db_raw_data = import_from_google_sheet.execute()
    master_data = handle_data.execute(new_owner_raw_data, master_db_raw_data, data_dict)
    success, error = insert.execute(master_data, {'owner_dict': owner_dict,
                                                  'hour_log_dict': hour_log_dict,
                                                  'owner_owner_type_dict': owner_owner_type_dict})
    write_to_console.execute([success, error])
    report.execute(master_data, data_dict)
    print("Done!")

if __name__ == '__main__':
    execute()
