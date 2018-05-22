# This module will get data from Google Sheets and format it as a list of dicts
import util

# Pull some important values out of each line of the master db
def process_master_db_data(rd):
    return dict({}, pos_id=rd[1], email=util.normalize_email(rd[5]))

# From each row and the data_dict, create a dictionary for each owner
def process_raw_data(owner, processed_master_db_data, data_dict):
    email = util.normalize_email(owner[3])

    return dict(data_dict, join_date=util.timestamp_to_date(owner[0]),
                           pos_id=util.get_pos_id_by_email(processed_master_db_data, email),
                           first_name=owner[1],
                           last_name=owner[2],
                           email=email,
                           display_name=util.create_display_name(owner[1], owner[2]),
                           phone=owner[4],
                           address=util.format_address(owner[7], owner[8], owner[9]),
                           city=owner[10],
                           state=owner[11],
                           zipcode=owner[12])

def execute(new_owner_raw_data, master_db_raw_data, data_dict):
    print("Processing raw data...")
    processed_master_db_data = [process_master_db_data(rd) for rd in master_db_raw_data]
    return [process_raw_data(rd, processed_master_db_data, data_dict) for rd in new_owner_raw_data]
