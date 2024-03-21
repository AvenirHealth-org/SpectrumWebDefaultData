import os
import numpy as np
from datetime import datetime
from AvenirCommon.Database.BlobStorage import GB_get_db_json
from Calc.GB.GBMain import GBCalculate 
from SpectrumCommon.Const.GB.GBConst import GB_DP, GB_AM
from AvenirCommon.Util import formatCountryFName
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Const.AM import *
from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Modvars.GB.GBCreateProjection import *
from DefaultData.DefaultDataUtil import *

initialConditions_json_path = os.getcwd() + '\\DefaultData\\JSONData\\demproj\\initialConditions'

def write_DP_population_db(version):
    GBModData = GB_get_db_json(os.environ[GB_SPECT_MOD_DATA_CONN_ENV], "globals", formatCountryFName(GBCountryListDBName, GBDatabaseVersion))

    for country in GBModData: 
        if not (country['ISO3_Numeric'] == 5733):

            params = createProjectionParams()
            params.firstYear = 1970
            params.finalYear = 2030
            params.country = country['ISO3_Alpha']
            params.extra['subNatCode'] = 0
            params.modules = [GB_DP, GB_AM]

            projection = GB_CreateProjection(params)
            
            dt = np.dtype(np.float64)  
            for mv in projection:
                    # if mv in [AM_ChildMortByCD4WithART0to6Tag, AM_ChildMortByCD4WithART0to6PercTag,
                    #         AM_ChildMortByCD4WithART7to12Tag, AM_ChildMortByCD4WithART7to12PercTag,
                    #         AM_ChildMortByCD4WithARTGT12Tag, AM_ChildMortByCD4WithARTGT12PercTag]:
                    #     #print('meow')
                    #     pass
                if type(projection[mv]) == list:
                    if len(projection[mv])>0 and ((type(projection[mv][0])==dict) or(type(projection[mv][0])==str)) :
                        projection[mv] = np.array(projection[mv], order='C')
                    else:
                        projection[mv] = np.array(projection[mv], order='C', dtype=dt)

            projection[DP_InitialConditionsTempTransportTag] = {}

            projection['timings']  = {}
            GBCalculate(projection)

            pop1 = projection[DP_InitialConditionsTempTransportTag]['pop1']
            births = projection[DP_InitialConditionsTempTransportTag]['births']
            hiv_infections = projection[DP_InitialConditionsTempTransportTag]['hiv_infections']
            hiv_deaths = projection[DP_InitialConditionsTempTransportTag]['hiv_deaths']

 
            print('Writing '+ country['name'])

            now = datetime.utcnow()
            timeStamp = now.strftime("Date: %Y-%m-%d Time: %H:%M:%S")

            country_data = {
                    'pop1': pop1.tolist(),
                    'births': births.tolist(),
                    'hiv_infections': hiv_infections.tolist(),
                    'hiv_deaths': hiv_deaths.tolist(),
                    'calcVersion': GB_Calc_Version,
                    'PMVersion': GB_PM_Version,
                    'date': timeStamp,
                }        
            
        os.makedirs(initialConditions_json_path, exist_ok=True)
        with open(os.path.join(initialConditions_json_path, formatCountryFName(params.country, version)), 'w') as f:
            ujson.dump(country_data, f)

def upload_DP_population_db(version):  
    uploadFilesInDir('demproj', initialConditions_json_path, version, pathMod = DPInitialConditionsDBSubDir)