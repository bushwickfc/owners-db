# Dealing with Google Sheets API

import pygsheets

def fetch_sheets(sheet_title, start, end = False):
    gc = pygsheets.authorize(outh_file='client_secret.json', outh_nonlocal=True)
    sheet = gc.open(sheet_title)
    return sheet.worksheets()[start:end] if end != False else [sheet.worksheets()[start]]
