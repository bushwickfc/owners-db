# This module will ingest the data from Google Sheets, do some processing, and format it as a list of dicts.
import time
import difflib

# Lowercase email addresses and remove whitespace.
def normalize_email(email):
    return email.lower().replace(' ', '')

# Convert a Google Sheet timestamp string ('5/1/2018 21:07:52') to basic date string format ('2018-5-1')
def timestamp_to_date(ts):
    dt_tup = time.strptime(ts, '%m/%d/%Y %H:%M:%S')
    return str(dt_tup[0]) + '-' + str(dt_tup[1]) + '-' + str(dt_tup[2])

# Clean up the building/street/unit number fields so we have a cohesive address.
def format_address(building, street, unit):
    building_street = building + ' ' + street
    return building_street if unit == '' else building_street + ', ' + unit

# Determine if a string value could be converted to a float.
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Convert the string from the new owner sheet into a category matching the types in the owner_type table.
def convert_owner_type(owner_type):
    types = ['disability', 'family_leave', 'hold', 'inactive', 'parental', 'pregnancy', 'senior', 'standard']
    # For at least 'Standard / Estander', 'Parent/Guardian - Padre/Guardián', and 'Senior (65+) / Adulto Mayor (65+)',
    # these settings for difflib.get_close_matches() returns the correct type.
    # https://docs.python.org/3/library/difflib.html#difflib.get_close_matches
    return difflib.get_close_matches(owner_type, types, 1, 0.2)[0]

# Convert banked hours to a float.
# Any incorrectly typed or empty string values should be zeroed out,
# and any valid negative values should be zeroed out.
def convert_hours(hours):
    if not isfloat(hours) or hours == '' or float(hours) < 0:
        return float(0)
    else:
        return float(hours)

# Pull some important values out of each line of the master db and put them in a dict with the email as the key.
def process_master_db_data(master_db_raw_data):
    master_db_dict = {}
    for rd in master_db_raw_data:
        master_db_dict[normalize_email(rd[5])] = {'old_member_id': rd[0],
                                                  'pos_id': rd[1],
                                                  'time_balance': convert_hours(rd[14])}

    return master_db_dict

# Based on the attr argument, get the value from the dicts of master_db data.
def get_val_from_master_by_email(master_db_data, email, attr):
    default_val = float(0) if attr == 'time_balance' else None
    return master_db_data[email][attr] if email in master_db_data and master_db_data[email][attr] != '' else default_val

# From each row and the data_dict, create a dictionary for each owner
def process_raw_data(owner, processed_master_db_data, data_dict):
    # Grab the email here, as it is also used as a reference key against the master_db data.
    email = normalize_email(owner[3])

    return dict(data_dict, join_date=timestamp_to_date(owner[0]),
                           pos_id=get_val_from_master_by_email(processed_master_db_data, email, 'pos_id'),
                           first_name=owner[1],
                           last_name=owner[2],
                           email=email,
                           phone=owner[4],
                           address=format_address(owner[7], owner[8], owner[9]),
                           city=owner[10],
                           state=owner[11],
                           zipcode=owner[12],
                           amount=get_val_from_master_by_email(processed_master_db_data, email, 'time_balance'),
                           owner_type=convert_owner_type(owner[14]),
                           old_member_id=get_val_from_master_by_email(processed_master_db_data, email, 'old_member_id'))

def execute(new_owner_raw_data, master_db_raw_data, data_dict):
    print('Processing raw data...')
    processed_master_db_data = process_master_db_data(master_db_raw_data)
    return [process_raw_data(rd, processed_master_db_data, data_dict) for rd in new_owner_raw_data]
