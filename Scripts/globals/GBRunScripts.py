
import Scripts.globals  as globals

from SpectrumCommon.Const.GB import *

def GBRunScripts():
    user_input = input("Would you like to run GB scripts?  ")
    if user_input.lower() in ['y', 'yes']:
        try:
            ####### GB #######
            # globals.writeGBCountryListMaster('V18')
            globals.uploadGBCountryListMaster('V18')

            # globals.create_disability_json()
            # globals.upload_disability_json()

            # globals.upload_string_DBs()
        except Exception as e:
            print(f"An error occurred while running GB scripts: {e}")
    else:
        print("Operation cancelled by user.")