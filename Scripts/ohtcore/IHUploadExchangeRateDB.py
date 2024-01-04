import os
import ujson
from itertools import islice
from openpyxl import load_workbook

from AvenirCommon.Database import GB_upload_file
from AvenirCommon.Logger import log

import SpectrumCommon.Const.GB as gbc
import SpectrumCommon.Const.IH.IHConst as ihc
import SpectrumCommon.Const.IH.IHDatabaseKeys as ihdbk 

# Column tag 'constants' for identifying columns.

IH_ISO_NUMERIC_COUNTRY_CODE = '<ISO Numeric Country Code>'  
IH_ISO_ALPHA_3_COUNTRY_CODE = '<ISO Alpha-3 Country Code>'
IH_COUNTRY_NAME             = '<Country Name>'
IH_DATA                     = '<Data>'
IH_YEARS                    = '<Years>'

def create_exchange_rate_DB_IH(version_str):

    log('Creating Exchange rate IH')
    IH_path = os.getcwd() + '\Tools\DefaultDataManager\IH\\'
    IH_mod_data_FQ_name = IH_path + 'ModData\IHModData.xlsx'

    country_list = []
    wb = load_workbook(IH_mod_data_FQ_name)
    sheet = wb[ihc.IH_EXCHANGE_RATE_DB_NAME]

    num_rows = sheet.max_row
    num_cols = sheet.max_column

    # Establish tag columns.
    col = 1
    #iso_numeric_country_code_col = col
    col += 1    
    #country_name_col = col
    col += 1
    iso_alpha_3_country_code_col = col
    col += 1
    data_col = col

    row = 3
    first_data_row = row

    # Get each row from the sheet and create a dictionary for each each country
    for row in islice(sheet.values, first_data_row - 1, num_rows):

        country_dict = {}
        country_dict[ihdbk.IH_ISO_ALPHA_3_COUNTRY_CODE_KEY_EXDB] = row[iso_alpha_3_country_code_col - 1]
        country_dict[ihdbk.IH_EXCHANGE_RATE_KEY_EXDB] = row[data_col - 1]

        country_list.append(country_dict)

    os.makedirs(IH_path + '\JSON\\' + ihc.IH_EXCHANGE_RATE_DB_DIR + '\\', exist_ok = True)
    
    for country_obj in country_list:    
        iso3 = country_obj[ihdbk.IH_ISO_ALPHA_3_COUNTRY_CODE_KEY_EXDB]
        with open(IH_path + '\JSON\\' + ihc.IH_EXCHANGE_RATE_DB_DIR + '\\' + iso3 + '_' + version_str + '.' + gbc.GB_JSON, 'w') as f:
            ujson.dump(country_obj, f)

    log('Finished Exchange rate IH')

def upload_exchange_rate_DB_IH(version):
    connection =  os.environ[gbc.GB_SPECT_MOD_DATA_CONN_ENV]
    walk_path = os.getcwd() + '\Tools\DefaultDataManager\IH\JSON\\' + ihc.IH_EXCHANGE_RATE_DB_DIR + '\\'

    for subdir, dirs, files in os.walk(walk_path):
        for file in files:
            FQName = os.path.join(subdir, file)
            #log(FQName)
            GB_upload_file(connection, gbc.GB_IH_CORE_CONTAINER, ihc.IH_EXCHANGE_RATE_DB_DIR + '\\' + file, FQName)
            
    log('Uploaded Exchange rate IH')


