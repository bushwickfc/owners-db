import pygsheets

def execute():
    # Authorize access to Google Drive/Google Sheet API
    # https://pygsheets.readthedocs.io/en/latest/authorizing.html
    gc = pygsheets.authorize(outh_file='client_secret.json', outh_nonlocal=True)
    # Get the sheet by name
    sh = gc.open("Copy of New Owner Onboarding")
    # Get the specific worksheet
    all_new_owners_sheet = sh.worksheet_by_title("All New Owners")
    # Pull the values from the sheet as a matrix
    return all_new_owners_sheet.get_values(start=(3,1), end=(79,16), returnas='matrix')
