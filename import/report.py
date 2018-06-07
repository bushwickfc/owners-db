# We'll want to output some of our data to a hard copy - these are owners who do not have
# an old_member_id. That'll be for two reasons: either they're totally new to BFC, or they
# were a member but provided a non-matching email address when they registered as an owner.
#
# This module will output a .csv file to the root directory named 'no_old_member_id.csv'.
# It will need to be reviewed for two things:
#
# 1. Any owner who was previously a member will need to have their old_member_id, pos_id,
#    and banked_hours manually copied from the old MemberDB Google Sheet and inserted into
#    the new database as 'old_member_id' and 'pos_id' fields on the 'owner' table, and 'amount'
#    on the 'hour_log' table, respectively, based on that owner's new email address.
#
# 2. Any owner who is totally new to BFC will need to have a pos_id created and inserted into
#    the 'pos_id' field on the 'owner' table.
import csv

# Filter function to return owners who have no old_member_id
def old_member_id_filter(processed_data):
    return True if processed_data['old_member_id'] == None else False

def write_to_csv(filename, keys, data):
    file = filename + '.csv'
    print('Writing data to ' + file)
    with open(file, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def execute(owner_data, master_data_dict):
    print('Preparing reports...')
    keys = list(master_data_dict.keys())
    no_old_member_id = filter(old_member_id_filter, owner_data)
    write_to_csv('no_old_member_id', keys, no_old_member_id)
