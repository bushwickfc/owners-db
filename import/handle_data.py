# This module will get data from Google Sheets and format it as a list of dicts
import time
import difflib

# Lowercase email addresses and remove whitespace.
def normalize_email(email):
    return email.lower().replace(" ", "")

# Convert a Google Sheet timestamp string ('5/1/2018 21:07:52') to basic date string format ('2018-5-1')
def timestamp_to_date(ts):
    dt_tup = time.strptime(ts, "%m/%d/%Y %H:%M:%S")
    return str(dt_tup[0]) + "-" + str(dt_tup[1]) + "-" + str(dt_tup[2])

# Clean up the building/street/unit number fields so we have a cohesive address.
def format_address(building, street, unit):
    building_street = building + ' ' + street
    return building_street if unit == '' else building_street + ', ' + unit

# Convert banked hours to a float.
def convert_hours(hours):
    if hours == '#NUM!' or hours == '':
        return float(0)
    else:
        return float(hours)

# Convert the string from the new owner sheet into a category matching the types in the owner_type table.
def convert_owner_type(owner_type):
    types = ['disability', 'family_leave', 'hold', 'inactive', 'parental', 'pregnancy', 'senior', 'standard']
    # For at least 'Standard / Estander', 'Parent/Guardian - Padre/Guardián', and 'Senior (65+) / Adulto Mayor (65+)',
    # these settings for difflib.get_close_matches() returns the correct type.
    # https://docs.python.org/3/library/difflib.html#difflib.get_close_matches
    return difflib.get_close_matches(owner_type, types, 1, 0.2)[0]

# Pull some important values out of each line of the master db - old member ID (rd[0]) POS IDs (rd[1]) and banked hours (rd[15]).
def process_master_db_data(master_db_raw_data):
    master_db_dict = {}
    for rd in master_db_raw_data:
        master_db_dict[normalize_email(rd[5])] = [rd[0], rd[1], convert_hours(rd[15])]

    return master_db_dict

# Get the old member id...
def get_old_member_id_by_email(master_db_data, email):
  return master_db_data[email][0] if email in master_db_data and master_db_data[email] != '' else None

# From the master db data, attempt to find the matching record from the new owner signup
# by matching on (normalized) email address. If there's a match, return the pos_id for that record.
def get_pos_id_by_email(master_db_data, email):
    return master_db_data[email][1] if email in master_db_data and master_db_data[email] != '' else None

# From the master db data, attempt to find the matching record from the new owner signup
# and return the banked_hours, or 0.0 if there are none.
def get_amount_by_email(master_db_data, email):
    return master_db_data[email][2] if email in master_db_data and master_db_data[email] != '' else float(0)

# From each row and the data_dict, create a dictionary for each owner
def process_raw_data(owner, processed_master_db_data, data_dict):
    email = normalize_email(owner[3])

    return dict(data_dict, join_date=timestamp_to_date(owner[0]),
                           pos_id=get_pos_id_by_email(processed_master_db_data, email),
                           first_name=owner[1],
                           last_name=owner[2],
                           email=email,
                           phone=owner[4],
                           address=format_address(owner[7], owner[8], owner[9]),
                           city=owner[10],
                           state=owner[11],
                           zipcode=owner[12],
                           amount=get_amount_by_email(processed_master_db_data, email),
                           owner_type=convert_owner_type(owner[14]),
                           old_member_id=get_old_member_id_by_email(processed_master_db_data, email))

def execute(new_owner_raw_data, master_db_raw_data, data_dict):
    print("Processing raw data...")
    processed_master_db_data = process_master_db_data(master_db_raw_data)
    return [process_raw_data(rd, processed_master_db_data, data_dict) for rd in new_owner_raw_data]
