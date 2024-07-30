import os

from AvenirCommon.Database import GB_upload_file
from AvenirCommon.Logger import log

import DefaultData.DefaultDataUtil as ddu

import SpectrumCommon.Const.GB as gbc

def upload_string_DBs(version):
    # Note: There is no create_string_DBs because we already have them created in json format (one for each language) and just need to upload them.

    JSON_file_name = gbc.GB_ENGLISH_STRINGS_DB_NAME + '_' + version + '.' + gbc.GB_JSON
    GB_upload_file(os.environ[gbc.GB_SPECT_MOD_DATA_CONN_ENV], gbc.GB_GB_CONTAINER, JSON_file_name, ddu.get_JSON_data_path(gbc.GB_GB) + '\Strings\\' + JSON_file_name, encoding='utf-8') 

    JSON_file_name =  gbc.GB_SPANISH_STRINGS_DB_NAME + '_' + version + '.' + gbc.GB_JSON
    GB_upload_file(os.environ[gbc.GB_SPECT_MOD_DATA_CONN_ENV], gbc.GB_GB_CONTAINER, JSON_file_name, ddu.get_JSON_data_path(gbc.GB_GB) + '\Strings\\' + JSON_file_name, encoding='utf-8') 

    JSON_file_name =  gbc.GB_FRENCH_STRINGS_DB_NAME + '_' + version + '.' + gbc.GB_JSON
    GB_upload_file(os.environ[gbc.GB_SPECT_MOD_DATA_CONN_ENV], gbc.GB_GB_CONTAINER, JSON_file_name, ddu.get_JSON_data_path(gbc.GB_GB) + '\Strings\\' + JSON_file_name, encoding='utf-8') 

    JSON_file_name = gbc.GB_UKRANIAN_STRINGS_DB_NAME + '_' + version + '.' + gbc.GB_JSON
    GB_upload_file(os.environ[gbc.GB_SPECT_MOD_DATA_CONN_ENV], gbc.GB_GB_CONTAINER, JSON_file_name, ddu.get_JSON_data_path(gbc.GB_GB) + '\Strings\\' + JSON_file_name, encoding='utf-8') 

    JSON_file_name = gbc.GB_RUSSIAN_STRINGS_DB_NAME + '_' + version + '.' + gbc.GB_JSON
    GB_upload_file(os.environ[gbc.GB_SPECT_MOD_DATA_CONN_ENV], gbc.GB_GB_CONTAINER, JSON_file_name, ddu.get_JSON_data_path(gbc.GB_GB) + '\Strings\\' + JSON_file_name, encoding='utf-8') 

    log('Uploaded GB string DBs')