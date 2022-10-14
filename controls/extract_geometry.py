### This script reads from the master value sheet ###

from __future__ import print_function
import gspread
import pandas as pd
SPREADSHEET_ID = '1s5P5vXLdzXZgH1rN1ZvnTEgL87FyuiPga2gGJ-t785g'

def get_values(design_element_values):

    """
    design_element_values is a dictionary with all of the geometry variables you want to extract from the spreadsheet. 
    Map variable names to None to start (or a manual value). See example_extract_geometry for an example use case 
    """""
    client = gspread.service_account('credentials_service.json')
    sheet = client.open_by_key(SPREADSHEET_ID)
    configs_sheet = sheet.worksheet('Controls Script Values')
    all_vals = configs_sheet.get_all_values()
    df = pd.DataFrame(all_vals, columns=['Design Element', 'Variable Name', 'Value', 'Source'])

    for key in design_element_values.keys():
        if key in df['Variable Name'].values:
            design_element_values[key] = float(df[df['Variable Name'] == key]['Value'])
        else:
            print(key, 'not in Master Value Sheet')

    return design_element_values