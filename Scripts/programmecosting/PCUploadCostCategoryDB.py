import os
import ujson
from itertools import islice
from openpyxl import load_workbook

from AvenirCommon.Util import GBRange
from AvenirCommon.Database import GB_upload_file
from AvenirCommon.Logger import log

import SpectrumCommon.Const.GB as gbc

import SpectrumCommon.Const.PC.PCConst as pcc
import SpectrumCommon.Const.PC.PCDatabaseKeys as pcdbk 

# Column tag 'constants' for identifying columns.

PC_COST_CAT_ID        = '<Cost Category ID>'  
PC_COST_CAT_NAME      = '<Cost Category Name>'  
PC_COST_CAT_STR_CONST = '<Cost Category String Constant>' 

def create_cost_category_DB_PC(version_str):
    log('Creating PC cost category DB')
    PC_path = os.getcwd() + '\Tools\DefaultDataManager\PC\\'
    PC_mod_data_FQ_name = PC_path + 'ModData\PCModData.xlsx'

    cost_cat_list = []
    wb = load_workbook(PC_mod_data_FQ_name)
    sheet = wb[pcc.PC_COST_CAT_DB_NAME]
    
    '''
        IMPORTANT: Max cost category master ID: xxx

        New cost category must have a master ID greater than this. Please update this maximum if you add a new one.
    '''

    # first row of data after col descriptions and col tags
    tag_row = 1
    first_data_row = 2
    first_data_col = 1
    num_rows = sheet.max_row
    num_cols = sheet.max_column

    cost_cat_ID_col = gbc.GB_NOT_FOUND
    cost_cat_name_col = gbc.GB_NOT_FOUND
    cost_cat_str_const = gbc.GB_NOT_FOUND

    for c in GBRange(first_data_col, num_cols):
        tag = sheet.cell(tag_row, c).value

        if tag == PC_COST_CAT_ID:
            cost_cat_ID_col = c

        elif tag == PC_COST_CAT_NAME:
            cost_cat_name_col = c

        elif tag == PC_COST_CAT_STR_CONST:
            cost_cat_str_const = c

    for row in islice(sheet.values, first_data_row - 1, num_rows):

        cost_cat_dict = {}

        cost_cat_dict[pcdbk.PC_COST_CAT_ID_KEY_CCDB] = row[cost_cat_ID_col - 1]
        cost_cat_dict[pcdbk.PC_COST_CAT_NAME_KEY_CCDB] = row[cost_cat_name_col - 1]
        cost_cat_dict[pcdbk.PC_COST_CAT_STR_CONST_KEY_CCDB] = row[cost_cat_str_const - 1]

        cost_cat_list.append(cost_cat_dict)

    j = ujson.dumps(cost_cat_list)
    # for debugging
    # for i, obj in enumerate(activity_list):
    #     log(obj)
    os.makedirs(PC_path + 'JSON\\', exist_ok = True)
    with open(PC_path + 'JSON\\' + pcc.PC_COST_CAT_DB_NAME + '_' + version_str + '.' + gbc.GB_JSON, 'w') as f:
        f.write(j)
    log('Finished PC cost category DB')

def upload_cost_category_DB_PC(version):
    connection =  os.environ[gbc.GB_SPECT_MOD_DATA_CONN_ENV]
    FQName = os.getcwd() + '\Tools\DefaultDataManager\PC\JSON\\' + pcc.PC_COST_CAT_DB_NAME + '_' + version + '.' + gbc.GB_JSON
    container_name = gbc.GB_PC_CONTAINER
    GB_upload_file(connection, container_name, pcc.PC_COST_CAT_DB_NAME + '_' + version + '.' + gbc.GB_JSON, FQName) 
    log('Uploaded PC cost category DB')
            
