import os
from re import L, M
import pandas as pd
import numpy as np
import json
import copy
from datetime import datetime
from AvenirCommon.Database.BlobStorage import GB_upload_json, GB_get_db_json
from Calc.GB.GBMain import GBCalculate 
from SpectrumCommon.Const.GB.GBConst import GB_DP, GB_AM
from Tools.DefaultDataManager.GB.Upload.GBUploadModData import getGBModDataDict, getGBModDataDictByISO3
from AvenirCommon.Util import GBRange, formatCountryFName, findTagCol
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Const.AM import *
from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Modvars.GB.GBUtil import get_country_ISO3Alpha
from SpectrumCommon.Modvars.GB.GBCreateProjection import *
# from SpectrumCommon.Const.DP import *
from DefaultData.DefaultDataUtil import *

pop1Default_json_path = os.getcwd() + '\\DefaultData\\JSONData\\demproj\\pop1Default'

def addDataByCountryName(countryName, countries, dataName, data):

    if not(countryName in countries):
        countries[countryName] = {}
    countries[countryName][dataName] = data.copy()

def upload_DP_population_db(version):
    GBModData = getGBModDataDict()
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
                    if mv in [AM_ChildMortByCD4WithART0to6Tag, AM_ChildMortByCD4WithART0to6PercTag,
                            AM_ChildMortByCD4WithART7to12Tag, AM_ChildMortByCD4WithART7to12PercTag,
                            AM_ChildMortByCD4WithARTGT12Tag, AM_ChildMortByCD4WithARTGT12PercTag]:
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

            country_data = {
                    'pop1': pop1.tolist(),
                    'calcVersion': GB_Calc_Version,
                    'PMVersion': GB_PM_Version,
                    'date': timeStamp,
                }        
            
            # FName = 'pop1Default/' + formatCountryFName(params.country, version)
            # GB_upload_json(connection, 'demproj', FName, country_json)
        with open(os.path.join(pop1Default_json_path, formatCountryFName(params.country, version)), 'w') as f:
            ujson.dump(country_data, f)

def upload_DP_population_db(version):  
    uploadFilesInDir('demproj', pop1Default_json_path, version, pathMod = 'pop1Default/')