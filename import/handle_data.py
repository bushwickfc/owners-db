# This module will get data from Google Sheets and format it as a list of dicts
import time

# Lowercase email addresses and remove whitespace.
def normalize_email(email):
    return email.lower().replace(" ", "")

def create_display_name(first_name, last_name):
    return first_name + ' ' + last_name

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

# Pull some important values out of each line of the master db - POS IDs (rd[0]) and banked hours (rd[14]).
# Old member accounts will be associated with new owner accounts by email, so make a dict with the email as the key and [POS ID, banked hours] as the value
def process_master_db_data(master_db_raw_data):
    master_db_dict = {}
    for rd in master_db_raw_data:
        master_db_dict[normalize_email(rd[4])] = [rd[0], convert_hours(rd[14])]

    return master_db_dict

# From the master db data, attempt to find the matching record from the new owner signup
# by matching on (normalized) email address. If there's a match, return the pos_id for that record.
def get_pos_id_by_email(master_db_data, email):
    return master_db_data[email][0] if email in master_db_data and master_db_data[email] != '' else None

# From the master db data, attempt to find the matching record from the new owner signup
# and return the banked_hours, or 0.0 if there are none.
def get_amount_by_email(master_db_data, email):
    return master_db_data[email][1] if email in master_db_data and master_db_data[email] != '' else float(0)

# From each row and the data_dict, create a dictionary for each owner
def process_raw_data(owner, processed_master_db_data, data_dict):
    email = normalize_email(owner[3])

    return dict(data_dict, join_date=timestamp_to_date(owner[0]),
                           pos_id=get_pos_id_by_email(processed_master_db_data, email),
                           first_name=owner[1],
                           last_name=owner[2],
                           email=email,
                           display_name=create_display_name(owner[1], owner[2]),
                           phone=owner[4],
                           address=format_address(owner[7], owner[8], owner[9]),
                           city=owner[10],
                           state=owner[11],
                           zipcode=owner[12],
                           amount=get_amount_by_email(processed_master_db_data, email))

def execute(new_owner_raw_data, master_db_raw_data, data_dict):
    print("Processing raw data...")
    processed_master_db_data = process_master_db_data(master_db_raw_data)
    return [process_raw_data(rd, processed_master_db_data, data_dict) for rd in new_owner_raw_data]
