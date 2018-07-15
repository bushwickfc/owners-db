# Output entries in the old db that did not have a corresponding owner entry
import csv

import util

# Filter function to return owners who have no old_member_id
def old_member_id_filter(processed_data):
    return True if processed_data['old_member_id'] == None else False

def write_to_csv(filename,  data):
    print('Writing data to ' + filename)
    with open("{}.csv".format(filename), 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(data)

def execute(owner_data, member_db_data):
    print('Preparing reports...')
    mapping = util.read_mapping()
    owner_emails = set([o['email'] for o in owner_data])
    not_imported = [m for m in member_db_data.values()
                    if not util.email_in(mapping, owner_emails, m['email'])]
    if not_imported:
        write_to_csv('member_db_review', not_imported)
