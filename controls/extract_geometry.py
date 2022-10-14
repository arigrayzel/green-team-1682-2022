### This script reads from the master value sheet ###

from __future__ import print_function
import gspread
SAMPLE_SPREADSHEET_ID = '1s5P5vXLdzXZgH1rN1ZvnTEgL87FyuiPga2gGJ-t785g'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    client = gspread.service_account('credentials_service.json')
    sheet = client.open_by_key(SAMPLE_SPREADSHEET_ID)
    configs_sheet = sheet.worksheet('Configurations')
    all_vals = configs_sheet.get_all_values()

    print(all_vals)


if __name__ == '__main__':
    main()