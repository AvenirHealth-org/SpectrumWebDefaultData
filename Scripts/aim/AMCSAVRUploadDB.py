import os
import pandas as pd
import numpy as np
import ujson
from AvenirCommon.Database import GB_upload_json, GB_get_db_json
from AvenirCommon.Logger import log
from AvenirCommon.Util import formatCountryFName, GBRange, getTagRow

from Tools.DefaultDataManager.GB.Upload.GBUploadModData import getGBModDataDict, getGBModDataDictByISO3

from SpectrumCommon.Const.GB import *
from SpectrumCommon.Const.DP import *


def addDataByCountryCode(countryCode, countries, data, subnatCode = 0):

    if not(countryCode in countries):
        countries[countryCode] = {}

    countries[countryCode][subnatCode] = data

def upload_CSAVR_db(version, country=''):
    fitTypeRow  = 1
    mstIDRow    = 2
    paramRow    = 4
    startRow    = 5

    startCol    = 11

    AM_Path = os.getcwd()+'\Tools\DefaultDataManager\AM\\'
    FQName = AM_Path + 'ModData\AMModData.xlsx'

    connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']

    countries = {}
    # globalData = {}

    xlsx = pd.ExcelFile(FQName)

    sheet = xlsx.parse('CSAVRParameters', header=None)

    for row in GBRange(5, len(sheet.values) - 1):
        countryCode = int(sheet.values[row][1])
        subnatCode = 0

        rowData = {}
        # for i in GBRange(DP_FitNotCalculated, DP_rLogistic):
        #     rowData.append({})
        
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


    log('Uploading global data')
    data_json = ujson.dumps(countries[0][0])
    FName = 'CSAVR/' + formatCountryFName('Global', version)
    GB_upload_json(connection, 'aim', FName, data_json)

    GBModData = getGBModDataDictByISO3()
    for countryCode in countries:
        ISO3_Alpha = GBModData[countryCode]['ISO3_Alpha'] if countryCode in GBModData else 'notFound'

        if ISO3_Alpha != 'notFound':
            for subnatCode in countries[countryCode]:
                country = countries[countryCode][subnatCode]

                log('Uploading ' + GBModData[countryCode]['countryName'] + ' ' + str(subnatCode))
                country_json = ujson.dumps(country)
                FName = 'CSAVR/' + formatCountryFName(ISO3_Alpha, version, subnatCode)
                GB_upload_json(connection, 'aim', FName, country_json)