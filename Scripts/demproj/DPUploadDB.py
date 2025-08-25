import os
import pandas as pd
import numpy as np
import ujson

from AvenirCommon.Database import GB_upload_json, GB_get_db_json, GB_upload_file
from AvenirCommon.Util import formatCountryFName
from AvenirCommon.Logger import log
from DefaultData.DefaultDataUtil import *

from SpectrumCommon.Const.GB import GB_Male, GB_Female
from SpectrumCommon.Modvars.GB.GBUtil import get_country_ISO3Alpha, get_country_details

demproj_json_path = os.getcwd() + '\\DefaultData\\JSONData\\demproj\\moddata'
demproj_json_country_path = demproj_json_path + '\\' + country_dir

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
    FQName = os.getcwd() + '\\DefaultData\\SourceData\\demproj\\ModData\\DPModData.xlsx'
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
        addDataByCountryCode(countryCode, countries, 'LifeTable', data)
 
    os.makedirs(demproj_json_country_path, exist_ok=True)
    for countryCode in countries:
        countryData = countries[countryCode] 
        ISO3_Alpha = get_country_ISO3Alpha(countryCode) 

        if (ISO3_Alpha != 'notFound') and (isinstance(ISO3_Alpha, str)):
            log('Writing '+ get_country_details(ISO3_Alpha)['name'])
            FName = formatCountryFName(ISO3_Alpha, version)
            with open(os.path.join(demproj_json_country_path, FName), 'w') as f:
                ujson.dump(countryData, f)

def upload_demproj_db(version):  
    uploadFilesInDir('demproj', demproj_json_path, version)




