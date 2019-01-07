# This module will ingest the data from Google Sheets, do some
# processing, and format it as a list of dicts.
import util

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
OLD_EMAIL = "EMAIL ADDRESS"
POS_ID = "POS ID"
TIME_BALANCE = "TIME BALANCE"

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

# Convert the string from the new owner sheet into a category matching
# the types in the owner_type table.
def convert_owner_type(owner_type):
    types = ['disability', 'family_leave', 'hold', 'inactive', 'parental',
             'pregnancy', 'senior', 'standard']
    # For at least 'Standard / Estander', 'Parent/Guardian -
    # Padre/Guardián', and 'Senior (65+) / Adulto Mayor (65+)', these
    # settings for difflib.get_close_matches() returns the correct
    # type.
    # https://docs.python.org/3/library/difflib.html#difflib.get_close_matches
    return difflib.get_close_matches(owner_type, types, 1, 0.2)[0]

mapping = util.read_mapping()

# Strip any leading or trailing whitespace from each value.
def strip_whitespace(owner_prop):
    return owner_prop.strip()

# From each row and the master_data_dict, create a dictionary for each owner
def process_raw_data(owner, master_data_dict):
    owner = {k: strip_whitespace(v) for k, v in owner.items()}
    # Grab the email here, as it is also used as a reference key
    # against the master_db data.
    email = util.normalize_email(owner[EMAIL])
    db_email = util.standardize_email(owner[EMAIL])
    return dict(master_data_dict,
                join_date=util.parse_gs_timestamp(owner[TIME]),
                first_name=owner[FIRST_NAME],
                last_name=owner[LAST_NAME],
                email=db_email,
                phone=owner[PHONE],
                address=format_address(owner[BUILDING],
                                       owner[STREET],
                                       owner[UNIT]),
                city=owner[CITY],
                state=owner[STATE],
                zipcode=owner[ZIP],
                owner_type=convert_owner_type(owner[O_TYPE]))

def execute(new_owner_raw_data, master_data_dict):
    print('Processing raw data...')
    return [process_raw_data(rd, master_data_dict)
            for rd in new_owner_raw_data]
