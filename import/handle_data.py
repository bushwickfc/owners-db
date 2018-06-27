# This module will ingest the data from Google Sheets, do some processing, and format it as a list of dicts.
from datetime import datetime
import difflib

# new owners sheet
FIRST_NAME = "First Name / Nombre"
LAST_NAME = "Last Name / Apellido"
EMAIL = "Email Address / Correo Electrónico"
PHONE = "Phone Number / Teléfono"
BUILDING = "Building Number / Número de Edificio"
STREET = "Street / Calle"
UNIT = "Unit Number / Número de unidad"
CITY = "City / Ciudad"
STATE = "State / Estado"
ZIP = "Zip Code / Código Postal"
O_TYPE = "Ownership Category / Categoría de Propietario"
TIME = "Timestamp"

# old members db
OLD_ID = "MEMBER NUMBER"
POS_ID = "POS ID"
TIME_BALANCE = "TIME BALANCE"

# Lowercase email addresses and remove whitespace.
def normalize_email(email):
    return email.lower().replace(' ', '')

# Convert a Google Sheet timestamp string ('5/1/2018 21:07:52') to
# basic date string format ('2018-5-1')
def timestamp_to_date(ts):
    dt = datetime.strptime(ts, '%m/%d/%Y %H:%M:%S')
    return dt.date()

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

# Pull some important values out of each line of the master db, put them
# in a dict, and nest them in a parent dict with the email as the key.
def process_master_db_data(master_db_raw_data):
    master_db_dict = {}
    for rd in master_db_raw_data:
        master_db_dict[normalize_email(rd["EMAIL ADDRESS"])] = {'old_member_id': rd[OLD_ID],
                                                  'pos_id': rd[POS_ID],
                                                  'time_balance': rd[TIME_BALANCE]}

    return master_db_dict

# Based on the attr argument, get the value from the dicts of master_db data.
# If we're dealing with 'time_balance', make sure to zero out any negative or invalid values.
def get_val_from_master_by_email(master_db_data, email, attr):
    default_val = float(0) if attr == 'time_balance' else None
    return_val = master_db_data[email][attr] if email in master_db_data and master_db_data[email][attr] != '' else default_val
    return convert_hours(return_val) if attr == 'time_balance' else return_val

# Strip any leading or trailing whitespace from each value.
def strip_whitespace(owner_prop):
    return owner_prop.strip()

# From each row and the master_data_dict, create a dictionary for each owner
def process_raw_data(owner, processed_master_db_data, master_data_dict):
    owner = {k: strip_whitespace(v) for k, v in owner.items()}
    # Grab the email here, as it is also used as a reference key
    # against the master_db data.
    email = normalize_email(owner[EMAIL])
    return dict(master_data_dict, join_date=timestamp_to_date(owner[TIME]),
                                  pos_id=get_val_from_master_by_email(processed_master_db_data, email, 'pos_id'),
                                  first_name=owner[FIRST_NAME],
                                  last_name=owner[LAST_NAME],
                                  email=email,
                                  phone=owner[PHONE],
                                  address=format_address(owner[BUILDING], owner[STREET], owner[UNIT]),
                                  city=owner[CITY],
                                  state=owner[STATE],
                                  zipcode=owner[ZIP],
                                  amount=get_val_from_master_by_email(processed_master_db_data, email, 'time_balance'),
                                  owner_type=convert_owner_type(owner[O_TYPE]),
                                  old_member_id=get_val_from_master_by_email(processed_master_db_data, email, 'old_member_id'))

def execute(new_owner_raw_data, master_db_raw_data, master_data_dict):
    print('Processing raw data...')
    processed_master_db_data = process_master_db_data(master_db_raw_data)
    return [process_raw_data(rd, processed_master_db_data, master_data_dict)
            for rd in new_owner_raw_data]
