import os
import pandas as pd
import numpy as np
import ujson

from AvenirCommon.Database import GB_upload_json, GB_get_db_json, GB_upload_file
from AvenirCommon.Logger import log
from AvenirCommon.Util import formatCountryFName, GBRange
from AvenirCommon.Logger import log

from Tools.DefaultDataManager.GB.Upload.GBUploadModData import getGBModDataDict
from DefaultData.DefaultDataUtil import *

from SpectrumCommon.Const.GB import GB_Nan

easyaim_json_path = os.getcwd() + '\\DefaultData\\JSONData\\aim\\easyAIM'

def addDataByCountryName(countryName, countries, dataName, data, subnatCode = 0):
    if (subnatCode == 0):
        countrySubnatName = countryName + '_' + str(subnatCode)
    else:
        countrySubnatName = countryName

    if not(countrySubnatName in countries):
        countries[countrySubnatName] = {
            'countryName' : countryName,
            'subnatCode' : subnatCode,
        }
    countries[countrySubnatName][dataName] = data

def isValueByYearSheet(sheetName):
    return not (sheetName in ['PercentHIVPopEligible', 'PercNotBFNotRecARVs', 'PercNotBFRecARVs', 'LocalAdjustmentFactor', 'NewARTPatAllocation'])

def getValuesByYear(countries, sheet, sheetName, startRow = 3):
    startCol = 4
    endCol = len(sheet.values[2]) - 1
    startYear = int(sheet.values[2][startCol])
    endYear = int(sheet.values[2][endCol])

    for row in GBRange(startRow, len(sheet.values) - 1):
        countryCode = sheet.values[row][0]
        countryName = sheet.values[row][1]

        if (not pd.isna(countryCode)) and (not pd.isna(countryName)): #if country ID values are valid, add
            values = np.zeros(endYear - startYear + 1)
            i = 0
            for col in GBRange(startCol, endCol):
                values[i] = sheet.values[row][col]
                i += 1
            
            data = {
                'countryName' : countryName,
                'countryCode' : countryCode,
                'startYear' : startYear,
                'endYear' : endYear,
                'values' : values.tolist()
            }

            addDataByCountryName(countryName, countries, sheetName, data)


def getValuesNotByYear(countries, sheet, sheetName):
    startCol = 4
    endCol = len(sheet.values[2]) - 1

    for row in GBRange(3, len(sheet.values) - 1):
        countryCode = sheet.values[row][0]
        countryName = sheet.values[row][1]
      
        if (not pd.isna(countryCode)) and (not pd.isna(countryName)): #if country ID values are valid, add
            data = {
                'countryName' : countryName,
                'countryCode' : countryCode,
            }

            for col in GBRange(startCol, endCol):
                dataName = 'value' if pd.isna(sheet.values[2][col]) else sheet.values[2][col]  
                data[dataName] = 0 if (pd.isna(sheet.values[row][col])) else sheet.values[row][col]

            addDataByCountryName(countryName, countries, sheetName, data)

def write_easyAIM_db(version, country=''):
    
    FQName = os.getcwd() + '/DefaultData/SourceData/aim/EasyAIMData.xlsx'

    countries = {}
    xlsx = pd.ExcelFile(FQName)
    for sheetName in xlsx.sheet_names:

        sheet = xlsx.parse(sheetName, header=None)

        if isValueByYearSheet(sheetName):
            getValuesByYear(countries, sheet, sheetName)
        else:
            getValuesNotByYear(countries, sheet, sheetName)
    
    GBModData = getGBModDataDict()
    os.makedirs(easyaim_json_path, exist_ok=True)
    for countryName in countries:
        country = countries[countryName]
        ISO3_Alpha = GBModData[countries[countryName]['countryName']]['ISO3_Alpha'] if countries[countryName]['countryName'] in GBModData else 'notFound'

        if ISO3_Alpha != 'notFound':
            log('Writing '+ countryName)
            # country_json = ujson.dumps(country)
            FName = formatCountryFName(ISO3_Alpha, version)
            with open(os.path.join(easyaim_json_path, FName), 'w') as f:
                ujson.dump(country, f)
            # GB_upload_json(connection, 'aim', FName, country_json)

def upload_easyAIM_db(version):  
    uploadFilesInDir('aim', easyaim_json_path, version, pathMod = 'easyAIM/') 
    # connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']  

    # for root, dirs, files in os.walk(easyaim_json_path): 
    #     for file in files:
    #         if isCurrentVersion(file, version):
    #             log('Uploading ' + file)
    #             GB_upload_file(connection, 'aim', 'easyAIM/' + file, os.path.join(root, file))

# def get_easyAIM_test(version):
#     FName = 'easyAIM/' + formatCountryFName('BEN', version)
    
#     connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']
    
#     db = GB_get_db_json(connection, 'aim', FName)
#     log(db['Incidence'])

