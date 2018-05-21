# The main app module.
# The basic flow is that we pull data from a Google Sheet, do some reformatting/processing,
# then insert that into the db.
import import_from_google_sheet
import handle_data
import insert

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
    'state': None,
    'zipcode': None,
    'payment_plan_delinquent': None
}

def execute():
    raw_data = import_from_google_sheet.execute()
    processed_data = handle_data.execute(raw_data, data_dict)
    insert.execute(processed_data, data_dict)
    print("Done!")

if __name__ == '__main__':
    execute()
