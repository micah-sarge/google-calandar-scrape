# for sheets api
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from os import path

# The name of the sheet to print the info to
SHEET_NAME = "<specific google sheets name>"


def recordIncome(year, month, lessons):
    """
    Finds the total income from lessons and adds it to  a new row in google sheets.
    The new row contains the year, month, and total income for that month
    @params year The year of the month being analized
    @params month The month being analized
    @params lessons A list of strings. If the stirng is an integer then it it added to the total
    income.
    """
    # use creds to create a client to interact with the Google Drive API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    sheets_drive_creds = path.expanduser("<full path to google sheets credentials .json file>")
    creds = ServiceAccountCredentials.from_json_keyfile_name(sheets_drive_creds, scope)
    client = gspread.authorize(creds)

    # Finds a workbook by name and open the first sheet
    sheet = client.open(SHEET_NAME).sheet1
    # Finds the next available row in the sheet
    next_available_row = len(sheet.get_all_values()) + 1
    # the total income for the month
    income = 0
    # Adds all the integers in lessons to get the total income for the month
    for item in lessons:
        try:
            income += int(item)
        except ValueError:
            continue

    row = [year, month, income]

    sheet.insert_row(row, next_available_row)
