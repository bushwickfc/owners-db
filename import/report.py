# We'll want to output some of our data to a hard copy -
# i.e. a list of owners who are missing a POS ID.
import csv

# Filter function to return owners who have no assigned POS ID
def pos_id_filter(processed_data):
    return True if processed_data['pos_id'] == None else False

def write_to_csv(filename, keys, data):
    file = filename + '.csv'
    print('Writing data to ' + file)
    with open(file, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def execute(owner_data, data_dict):
    print('Preparing reports...')
    keys = list(data_dict.keys())
    no_pos_id = filter(pos_id_filter, owner_data)
    write_to_csv('no_pos_id', keys, no_pos_id)