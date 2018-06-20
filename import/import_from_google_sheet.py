# This module will retrieve the data from the Google Sheets via pygsheets.
import pygsheets

# Get the raw data as a matrix
def fetch(sheet_name, worksheet_name, start):
    print('Fetching {} from Google Sheets...'.format(sheet_name))
    # Authorize access to Google Drive/Google Sheet API - https://pygsheets.readthedocs.io/en/latest/authorizing.html
    gc = pygsheets.authorize(outh_file='client_secret.json', outh_nonlocal=True)
    sheet = gc.open(sheet_name)
    # Get the specific worksheet from sheet.
    worksheet = sheet.worksheet_by_title(worksheet_name)
    data = new_owner_worksheet.get_values(start=start, returnas='matrix')

    return data
