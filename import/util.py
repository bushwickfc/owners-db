# Helper functions
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
