import os
import pandas as pd
import numpy as np
import ujson

from AvenirCommon.Database import GB_upload_json, GB_get_db_json
from AvenirCommon.Logger import log
from AvenirCommon.Util import formatCountryFName, GBRange
from AvenirCommon.Logger import log

from Tools.DefaultDataManager.GB.Upload.GBUploadModData import getGBModDataDict

from SpectrumCommon.Const.GB import GB_Nan

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
    return not (sheetName in ['PercentHIVPopEligible', 'PercNotBFNotRecARVs', 'PercNotBFRecARVs', 'LocalAdjustmentFactor'])

def getValuesByYear(countries, sheet, sheetName, startRow = 3):
    startCol = 4
    endCol = len(sheet.values[2]) - 1
    startYear = int(sheet.values[2][startCol])
    endYear = int(sheet.values[2][endCol])

    for row in GBRange(startRow, len(sheet.values) - 1):
        countryCode = sheet.values[row][0]
        countryName = sheet.values[row][1]

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
      
        data = {
            'countryName' : countryName,
            'countryCode' : countryCode,
        }

        for col in GBRange(startCol, endCol):
            dataName = str(sheet.values[2][col])
            dataName = 'value' if dataName in ['', GB_Nan, 'nan'] else dataName      #for LocalAdjustmentFactor
            data[dataName] = sheet.values[row][col]

        addDataByCountryName(countryName, countries, sheetName, data)

def upload_easyAIM_db(version, country=''):
    AM_Path = os.getcwd()+'\Tools\DefaultDataManager\AM\\'
    FQName = AM_Path + 'ModData\EasyAIMData.xlsx'
    # FQName = os.path.dirname(__file__) + '/EasyAIMData.xlsx'
    connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']

    countries = {}
    xlsx = pd.ExcelFile(FQName)
    for sheetName in xlsx.sheet_names:

        sheet = xlsx.parse(sheetName, header=None)

        if isValueByYearSheet(sheetName):
            getValuesByYear(countries, sheet, sheetName)
        else:
            getValuesNotByYear(countries, sheet, sheetName)
    
    GBModData = getGBModDataDict()
    for countryName in countries:
        country = countries[countryName]
        ISO3_Alpha = GBModData[countries[countryName]['countryName']]['ISO3_Alpha'] if countries[countryName]['countryName'] in GBModData else 'notFound'

        if ISO3_Alpha != 'notFound':
            log('Uploading '+ countryName)
            country_json = ujson.dumps(country)
            FName = 'easyAIM/' + formatCountryFName(ISO3_Alpha, version)
            GB_upload_json(connection, 'aim', FName, country_json)


def get_easyAIM_test(version):
    FName = 'easyAIM/' + formatCountryFName('BEN', version)
    
    connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']
    
    db = GB_get_db_json(connection, 'aim', FName)
    log(db['Incidence'])

