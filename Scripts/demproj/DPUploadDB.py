import os
import pandas as pd
import numpy as np
import ujson

from AvenirCommon.Database import GB_upload_json, GB_get_db_json, GB_upload_file
from AvenirCommon.Util import formatCountryFName
from AvenirCommon.Logger import log
from DefaultData.DefaultDataUtil import *

from Tools.DefaultDataManager.GB.Upload.GBUploadModData  import getGBModDataDict
from SpectrumCommon.Const.GB import GB_Male, GB_Female

demproj_json_path = os.getcwd() + '\\DefaultData\\JSONData\\demproj\\moddata'
# demproj_country_dir = 'country'
demproj_json_country_path = demproj_json_path + '\\' + country_dir

def addDataByCountryName(countryName, countries, dataName, data):

    if not(countryName in countries):
        countries[countryName] = {}
    countries[countryName][dataName] = data

def getLifeTableNameRoots():
    return [
        'CDWest',
        'CDNorth',
        'CDEast',
        'CDSouth',
        'UNGen',
        'UNLA',
        'UNChile',
        'UNSA',
        'UNEA',
    ]

def getASFRTableNames():
    return [
        'ASFR_AFR',
        'ASFR_ARB',
        'ASFR_ASA',
        'ASFR_AVG',
    ]

def write_demproj_db(version):
    FQName = os.getcwd() + '\DefaultData\SourceData\demproj\ModData\DPModData.xlsx'
    # connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']
    
    #non-country-specific data

    ModelLifeTables = {}
    for sheetNameRoot in getLifeTableNameRoots():       
        for sex in [GB_Male, GB_Female]:
            suffix = '_m' if sex == GB_Male else '_f'
            sheetName = sheetNameRoot + suffix
            ModelLifeTables[sheetName] = {}
            sheet = pd.read_excel(FQName, sheet_name=sheetName, header=None)
            
            for row in range(1, len(sheet.values)):
                ModelLifeTables[sheetName][str(sheet.values[row][0])] = {}
                for col in range(2, len(sheet.values[row])):
                    ModelLifeTables[sheetName][str(sheet.values[row][0])][str(int(sheet.values[0][col]))] = sheet.values[row][col]

    ASFRTables = {}
    for sheetName in getASFRTableNames():
        sheet = pd.read_excel(FQName, sheet_name=sheetName, header=None)
        result = sheet.values.tolist()

        ASFRTables[sheetName] = sheet.values.tolist()

    DPModDataGlobal = {
        'ModelLifeTables' : ModelLifeTables,
        'ASFRTables' : ASFRTables,
    }

    log('Writing global data')
    FName = 'DP_Global_' + version + '.JSON'
    os.makedirs(demproj_json_path, exist_ok=True)
    with open(os.path.join(demproj_json_path, FName), 'w') as f:
        ujson.dump(DPModDataGlobal, f)

    #country-specific data

    countries = {}
    sheet = pd.read_excel(FQName, sheet_name='LifeTable10', header=None)
    for row in range(1, len(sheet.values)):
        countryCode = sheet.values[row][0]
        countryName = sheet.values[row][1]  
        lifeTableName = sheet.values[row][2]
        lifeTableNum = sheet.values[row][3]
        data = {
            'lifeTableName' : lifeTableName,
            'lifeTableNum' : lifeTableNum,
            'countryName' : countryName,
            'countryCode' : countryCode,
        }
        addDataByCountryName(countryName, countries, 'LifeTable', data)
 
 
    os.makedirs(demproj_json_country_path, exist_ok=True)
    GBModData = getGBModDataDict()
    for countryName in countries:
        country = countries[countryName] 
        ISO3_Alpha = GBModData[countryName]['ISO3_Alpha'] if countryName in GBModData else 'notFound'

        if (ISO3_Alpha != 'notFound') and (isinstance(GBModData[countryName]['ISO3_Alpha'], str)):
            log('Writing '+ countryName)
            FName = formatCountryFName(ISO3_Alpha, version)
            with open(os.path.join(demproj_json_country_path, FName), 'w') as f:
                ujson.dump(country, f)

def upload_demproj_db(version):  
    uploadFilesInDir('demproj', demproj_json_path, version)
    # connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']  
    # # global
    # for root, dirs, files in os.walk(demproj_json_path): 
    #     for file in files:
    #         if isCurrentVersion(file, version):
    #             GB_upload_file(connection, 'demproj', file, os.path.join(root, file))

    # # country
    # for root, dirs, files in os.walk(demproj_json_country_path): 
    #     for file in files:
    #         if isCurrentVersion(file, version):
    #             GB_upload_file(connection, 'demproj', os.path.join(country_dir, file), os.path.join(root, file))






