# Dealing with Google Sheets and its API

import pygsheets

# Check against this column to see if a record needs to be inserted into the DB;
# update this column with the current timestamp as records are inserted.
DATABASE_COL = 'Added to Database (Timestamp inserted by technology)'

# Get a set of sheets, based on the sheet title.
# start and end may be set to None in order to access a range of pages like [:3], etc.
def fetch_sheets(sheet_title, start, end = False):
    gc = pygsheets.authorize(outh_file='client_secret.json', outh_nonlocal=True)
    sheet = gc.open(sheet_title)
    return sheet.worksheets()[start:end] if end != False else [sheet.worksheets()[start]]

# Create a dictionary of headers and their column numbers.
def get_header_map(sheet):
    return dict([(c, i+1) for i, c in
                enumerate(sheet.get_values((1,1), (1,sheet.cols))[0])
                if c])

def update_cell(sheet, row_idx, col_num, val):
    sheet.update_cell((row_idx, col_num), val)
