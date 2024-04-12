import os
import ujson
from itertools import islice
from openpyxl import load_workbook

# from AvenirCommon.Database import GB_upload_file
from AvenirCommon.Logger import log

import DefaultData.DefaultDataUtil as ddu

import SpectrumCommon.Const.GB as gbc

import SpectrumCommon.Const.PC.PCConst as pcc
import SpectrumCommon.Const.PC.PCDatabaseKeys as pcdbk 

# Column tag 'constants' for identifying columns.

PC_ISO_NUMERIC_COUNTRY_CODE = '<ISO Numeric Country Code>'  
PC_ISO_ALPHA_3_COUNTRY_CODE = '<ISO Alpha-3 Country Code>'
PC_COUNTRY_NAME             = '<Country Name>'
PC_PHASE_INTENSITY_ROW_ID   = '<Phase and Intensity Row ID>'
PC_PHASE_INTENSITY_ROW_NAME = '<Phase and Intensity Row Name>'
PC_PHASE_ID                 = '<Phase ID>'
PC_PHASE_NAME               = '<Phase Name>'

def create_PPLI_phase_DB_PC(version = str):

    log('Creating PPLI phase DB PC')

    country_list = []
    wb = load_workbook(ddu.get_source_data_path(gbc.GB_PC) + '\PCModData.xlsx')
    sheet = wb[pcc.PC_PPLI_PHASE_DB_NAME]

    num_rows = sheet.max_row
    # num_cols = sheet.max_column

    # Establish tag columns.
    col = 1
    #iso_numeric_country_code_col = col
    col += 1    
    #country_name_col = col
    col += 1
    iso_alpha_3_country_code_col = col
    col += 1
    phase_intensity_row_ID_col = col
    col += 1
    # phase_intensity_row_name_col = col
    col += 1
    phase_ID_col = col
    # col += 1
    # phase_ID_name_col = col

    row = 2
    first_data_row = row

    # Get each row from the sheet and create a dictionary for each each country
    for row in islice(sheet.values, first_data_row - 1, num_rows):

        country_dict = {}
        country_dict[pcdbk.PC_ISO_ALPHA_3_COUNTRY_CODE_KEY_PPLIPDB] = row[iso_alpha_3_country_code_col - 1]
        country_dict[pcdbk.PC_PHASE_INTENSITY_ROW_ID_KEY_PPLIPDB] = row[phase_intensity_row_ID_col - 1]
        country_dict[pcdbk.PC_PHASE_ID_KEY_PPLIPDB] = row[phase_ID_col - 1]

        country_list.append(country_dict)

    PC_JSON_data_path = ddu.get_JSON_data_path(gbc.GB_PC) + '\\' + pcc.PC_PPLI_PHASES_DB_DIR
    os.makedirs(PC_JSON_data_path + '\\', exist_ok = True)
    
    for country_obj in country_list:    
        iso3 = country_obj[pcdbk.PC_ISO_ALPHA_3_COUNTRY_CODE_KEY_PPLIPDB]
        with open(PC_JSON_data_path + '\\' + iso3 + '_' + version + '.' + gbc.GB_JSON, 'w') as f:
            ujson.dump(country_obj, f)

    log('Finished PPLI phase DB PC')

def upload_PPLI_phase_DB_PC(version):
    walk_path = ddu.get_JSON_data_path(gbc.GB_PC) + '\\' + pcc.PC_PPLI_PHASES_DB_DIR + '\\'
    ddu.uploadFilesInDir(gbc.GB_PC_CONTAINER, walk_path, version, pcc.PC_PPLI_PHASES_DB_DIR + '\\')
    log('Uploaded PPLI phase DB PC')


