import os
import pandas as pd
import numpy as np
import ujson
from AvenirCommon.Database import GB_upload_json, GB_get_db_json
from AvenirCommon.Logger import log
from AvenirCommon.Util import formatCountryFName, GBRange, getTagRow
from DefaultData.DefaultDataUtil import *

from SpectrumCommon.Const.GB import *
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Modvars.GB.GBUtil import get_country_ISO3Alpha, get_country_details

CSAVR_json_path = os.getcwd() + '\\DefaultData\\JSONData\\aim\\CSAVR'
CSAVR_json_country_path = CSAVR_json_path + '\\' + country_dir

def write_CSAVR_db(version, country=''):
    fitTypeRow  = 1
    mstIDRow    = 2
    paramRow    = 4

    startCol    = 11

    FQName = os.getcwd() + '/DefaultData/SourceData/aim/AMModData.xlsx'

    countries = {}

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
    FName = formatCountryFName('Global', version)
    os.makedirs(CSAVR_json_path, exist_ok=True)
    with open(os.path.join(CSAVR_json_path, FName), 'w') as f:
        ujson.dump(countries[0][0], f)

    os.makedirs(CSAVR_json_country_path, exist_ok=True)
    for countryCode in countries:
        ISO3_Alpha = get_country_ISO3Alpha(countryCode)

        if ISO3_Alpha != 'notFound':
            for subnatCode in countries[countryCode]:
                country = countries[countryCode][subnatCode]

                log('Writing ' + get_country_details(ISO3_Alpha)['name'] + ' ' + str(subnatCode))
                FName = formatCountryFName(ISO3_Alpha, version, subnatCode)
                with open(os.path.join(CSAVR_json_country_path, FName), 'w') as f:
                    ujson.dump(country, f)
            
def upload_CSAVR_db(version): 
    uploadFilesInDir('aim', CSAVR_json_path, version, pathMod = 'CSAVR/') 