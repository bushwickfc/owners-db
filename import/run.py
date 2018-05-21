# The main app module.
# The basic flow is that we pull data from a Google Sheet, do some reformatting/processing,
# dump it into a .csv, and then upload that .csv to a db.
import import_from_google_sheet
import handle_data
import insert

filename = 'new_owner_onboarding.csv'

def execute():
    raw_data = import_from_google_sheet.execute()
    handle_data.execute(raw_data, filename)
    insert.execute(filename)
    print("Done!")

if __name__ == '__main__':
    execute()
