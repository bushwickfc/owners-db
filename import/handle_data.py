# This module will get data from Google Sheets and format it as a list of dicts
import util

# From each row and the data_dict, create a dictionary for each owner
def process_raw_data(owner, data_dict):
    return dict(data_dict, join_date=util.timestamp_to_date(owner[0]),
                           first_name=owner[1],
                           last_name=owner[2],
                           email=util.normalize_email(owner[3]),
                           display_name=util.create_display_name(owner[1], owner[2]),
                           phone=owner[4],
                           address=util.format_address(owner[7], owner[8], owner[9]),
                           city=owner[10],
                           state=owner[11],
                           zipcode=owner[12])


def execute(raw_data, data_dict):
    print("Processing raw data...")
    return [process_raw_data(rd, data_dict) for rd in raw_data]
