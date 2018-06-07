# The main app module.
# The basic flow is that we pull data from a Google Sheet, do some reformatting/processing,
# then insert that into the db.
import dicts
import import_from_google_sheet
import handle_data
import insert
import report

def execute():
    new_owner_raw_data, master_db_raw_data = import_from_google_sheet.execute()
    master_data = handle_data.execute(new_owner_raw_data, master_db_raw_data, dicts.master_data_dict)
    insert.execute(master_data)
    report.execute(master_data, dicts.master_data_dict)
    print('Done!')

if __name__ == '__main__':
    execute()
