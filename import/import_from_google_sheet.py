import pygsheets

# Get the raw data as a matrix
def execute():
    print('Fetching data from Google Sheets...')
    # Authorize access to Google Drive/Google Sheet API - https://pygsheets.readthedocs.io/en/latest/authorizing.html
    gc = pygsheets.authorize(outh_file='client_secret.json', outh_nonlocal=True)
    # Get the sheets by name - the new owner sheet for most of the info, older member db for additional info (POS ID, banked hours...)
    new_owner_sheet = gc.open('Copy of New Owner Onboarding')
    member_database = gc.open('Copy of BFC Member Database (ACTIVE)')
    # Get the specific worksheets from each sheet
    new_owner_worksheet = new_owner_sheet.worksheet_by_title('All New Owners')
    master_db_worksheet = member_database.worksheet_by_title('MASTER DB')
    # Pull the values from the sheets as a matrix
    new_owner_data = new_owner_worksheet.get_values(start=(3,1), end=(79,16), returnas='matrix')
    master_db_data = master_db_worksheet.get_values(start=(2,2), end=(408,16), returnas='matrix')

    return new_owner_data, master_db_data
