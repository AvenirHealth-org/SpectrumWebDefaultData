import os
import pandas as pd
import numpy as np
import ujson

from AvenirCommon.Database import GB_upload_json, GB_get_db_json
from AvenirCommon.Util import formatCountryFName
from AvenirCommon.Logger import log

from Tools.DefaultDataManager.GB.Upload.GBUploadModData  import getGBModDataDict
from SpectrumCommon.Const.GB import GB_Male, GB_Female

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

def upload_demproj_db(version):
    FQName = os.path.dirname(__file__) + '/DPModData.xlsx'
    connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']
    
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

    log('Uploading global data')
    DPModDataGlobal_json = ujson.dumps(DPModDataGlobal)
    FName = 'DP_Global_' + version + '.JSON'
    GB_upload_json(connection, 'demproj', FName, DPModDataGlobal_json)


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
 
    GBModData = getGBModDataDict()
    for countryName in countries:
        country = countries[countryName] 
        ISO3_Alpha = GBModData[countryName]['ISO3_Alpha'] if countryName in GBModData else 'notFound'

        if ISO3_Alpha != 'notFound':
            log('Uploading '+ countryName)
            country_json = ujson.dumps(country)
            FName = 'country/' + formatCountryFName(ISO3_Alpha, version)
            GB_upload_json(connection, 'demproj', FName, country_json)









