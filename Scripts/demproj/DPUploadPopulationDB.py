import os
from re import L, M
import pandas as pd
import numpy as np
import json
import copy
from datetime import datetime
from AvenirCommon.Database.BlobStorage import GB_upload_json, GB_get_db_json
from Calc.GB.GBMain import GBCalculate 
from SpectrumCommon.Const.GB.GBConst import GB_DP, GB_AM, GB_Male, GB_Female
from Tools.DefaultDataManager.GB.Upload.GBUploadModData import getGBModDataDict, getGBModDataDictByISO3
from AvenirCommon.Util import GBRange, formatCountryFName, findTagCol
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Modvars.GB.GBUtil import get_country_ISO3Alpha
from SpectrumCommon.Modvars.GB.GBCreateProjection import *
# from SpectrumCommon.Const.DP import *

def addDataByCountryName(countryName, countries, dataName, data):

    if not(countryName in countries):
        countries[countryName] = {}
    countries[countryName][dataName] = data.copy()


def upload_DP_1970population_db(version):
    GBModData = getGBModDataDictByISO3()
    FQName = os.getcwd() + '\Tools\DefaultDataManager\DP\ModData\DPFirstYearPopInput.xlsx'
    connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']
    cNameCol = 0
    cCodeCol = 1
    yearCol = 2

    sheet = pd.read_excel(FQName, sheet_name='Data', header=None)

    maleStartCol = findTagCol(sheet, 'Male') + 1
    femaleStartCol = findTagCol(sheet, 'Female') + 1

    for row in range(1, len(sheet.values)):
        countryName = sheet.values[row][0]
        countryCode = sheet.values[row][1]
        countryISO3AlphaCode = str(sheet.values[row][2])

        if not (countryISO3AlphaCode in ['', GB_Nan, GB_Nan.lower(), np.nan]):
            data = np.zeros((GB_Female + 1, DP_MaxSingleAges + 1))
            
            maleCol = maleStartCol
            femaleCol = femaleStartCol
            for a in GBRange(0, 79):
                data[GB_Male, a] = (sheet.values[row][maleCol] * 1000) if (type(sheet.values[row][maleCol]) != str) else 0.0
                maleCol += 1
                data[GB_Female, a] = (sheet.values[row][femaleCol] * 1000) if (type(sheet.values[row][femaleCol]) != str) else 0.0
                femaleCol += 1
            for a in GBRange(80, 100):
                data[GB_Male, 80] += (sheet.values[row][maleCol] * 1000) if (type(sheet.values[row][maleCol]) != str) else 0.0
                maleCol += 1
                data[GB_Female, 80] += (sheet.values[row][femaleCol] * 1000) if (type(sheet.values[row][femaleCol]) != str) else 0.0
                femaleCol += 1

        # ISO3_Alpha = GBModData[countryISO3Code]['ISO3_Alpha'] if countryISO3Code in GBModData else 'notFound'

            # if ISO3_Alpha != 'notFound':
            print('Uploading '+ countryName)
            country_json = json.dumps(data.tolist())
            FName = 'UNPopulation1970/' + formatCountryFName(countryISO3AlphaCode, version)
            GB_upload_json(connection, 'demproj', FName, country_json)


def upload_DP_population_db(version):
    GBModData = getGBModDataDict()
    # FQName = os.getcwd() + '\Tools\DefaultDataManager\DP\ModData\DPFirstYearPopInput.xlsx'
    connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']
    for country in GBModData: 
        if not (GBModData[country]['ISO3'] == 5733):

            params = createProjectionParams()
            params.firstYear = 1970
            params.finalYear = 2030
            params.country = GBModData[country]['ISO3_Alpha']
            params.extra['subNatCode'] = 0
            params.modules = [GB_DP, GB_AM]

            projection = GB_CreateProjection(params)
            
            dt = np.dtype(np.float64)  
            for mv in projection:
                    if mv in ['<AM_ChildMortByCD4WithART0to6_V1>', '<AM_ChildMortByCD4WithART0to6Perc_V1>',
                            '<AM_ChildMortByCD4WithART7to12_V1>', '<AM_ChildMortByCD4WithART7to12Perc_V1>',
                            '<AM_ChildMortByCD4WithARTGT12_V1>', '<AM_ChildMortByCD4WithARTGT12Perc_V1>']:
                        #print('meow')
                        pass
                    elif type(projection[mv]) == list:
                        if len(projection[mv])>0 and ((type(projection[mv][0])==dict) or(type(projection[mv][0])==str)) :
                            projection[mv] = np.array(projection[mv], order='C')
                        else:
                            projection[mv] = np.array(projection[mv], order='C', dtype=dt)

            projection[DP_Pop1TempTransportTag] = []

            projection['timings']  = {}
            GBCalculate(projection)

            pop1 = projection[DP_Pop1TempTransportTag]
 
            print('Uploading '+ country)

            now = datetime.utcnow()
            timeStamp = now.strftime("Date: %Y-%m-%d Time: %H:%M:%S")

            country_json = json.dumps(
                {
                    'pop1': pop1.tolist(),
                    'calcVersion': GB_Calc_Version,
                    'PMVersion': GB_PM_Version,
                    'date': timeStamp,
                }        
            )
            FName = 'pop1Default/' + formatCountryFName(params.country, version)
            GB_upload_json(connection, 'demproj', FName, country_json)
