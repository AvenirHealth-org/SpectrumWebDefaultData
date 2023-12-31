import os
import pandas as pd
import numpy as np
import ujson
from AvenirCommon.Database import GB_upload_json, GB_get_db_json
from AvenirCommon.Logger import log
from AvenirCommon.Util import formatCountryFName, GBRange, getTagRow
from DefaultData.DefaultDataUtil import *

from Tools.DefaultDataManager.GB.Upload.GBUploadModData import getGBModDataDict, getGBModDataDictByISO3

from SpectrumCommon.Const.GB import *
from SpectrumCommon.Const.DP import *

CSAVR_json_path = os.getcwd() + '\\DefaultData\\JSONData\\aim\\CSAVR'
CSAVR_json_country_path = CSAVR_json_path + '\\' + country_dir

def addDataByCountryCode(countryCode, countries, data, subnatCode = 0):

    if not(countryCode in countries):
        countries[countryCode] = {}

    countries[countryCode][subnatCode] = data

def write_CSAVR_db(version, country=''):
    fitTypeRow  = 1
    mstIDRow    = 2
    paramRow    = 4
    startRow    = 5

    startCol    = 11

    FQName = os.getcwd() + '/DefaultData/SourceData/aim/AMModData.xlsx'

    connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']

    countries = {}
    # globalData = {}

    xlsx = pd.ExcelFile(FQName)

    sheet = xlsx.parse('CSAVRParameters', header=None)

    for row in GBRange(5, len(sheet.values) - 1):
        countryCode = int(sheet.values[row][1])
        subnatCode = 0

        rowData = {}
        
        for col in GBRange(startCol, len(sheet.values[row]) - 1):
            fitType = int(sheet.values[fitTypeRow][col])
            param = sheet.values[paramRow][col]

            data = {
                'mstID' : sheet.values[mstIDRow][col],
                'value' : float(sheet.values[row][col])
            }
            if not fitType in rowData:
                rowData[fitType] = {}
            rowData[fitType][param] = data

        addDataByCountryCode(countryCode, countries, rowData, subnatCode)
    

    log('Writing global data')
    data_json = ujson.dumps(countries[0][0])
    FName = formatCountryFName('Global', version)
    os.makedirs(CSAVR_json_path, exist_ok=True)
    with open(os.path.join(CSAVR_json_path, FName), 'w') as f:
        ujson.dump(countries[0][0], f)
    # GB_upload_json(connection, 'aim', FName, data_json)

    GBModData = getGBModDataDictByISO3()
    os.makedirs(CSAVR_json_country_path, exist_ok=True)
    for countryCode in countries:
        ISO3_Alpha = GBModData[countryCode]['ISO3_Alpha'] if countryCode in GBModData else 'notFound'

        if ISO3_Alpha != 'notFound':
            for subnatCode in countries[countryCode]:
                country = countries[countryCode][subnatCode]

                log('Writing ' + GBModData[countryCode]['countryName'] + ' ' + str(subnatCode))
                country_json = ujson.dumps(country)
                FName = formatCountryFName(ISO3_Alpha, version, subnatCode)
                with open(os.path.join(CSAVR_json_country_path, FName), 'w') as f:
                    ujson.dump(country, f)
                # GB_upload_json(connection, 'aim', FName, country_json)
            
def upload_CSAVR_db(version): 
    uploadFilesInDir('aim', CSAVR_json_path, version, pathMod = 'CSAVR/') 