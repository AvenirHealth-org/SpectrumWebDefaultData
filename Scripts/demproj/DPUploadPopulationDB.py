import os
import numpy as np
from datetime import datetime, timezone
from AvenirCommon.Database.BlobStorage import GB_get_db_json
from Calc.GB.GBMain import GBCalculate 
from SpectrumCommon.Const.GB.GBConst import GB_DP, GB_AM
from AvenirCommon.Util import formatCountryFName
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Const.AM import *
from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Modvars.GB.GBCreateProjection import *
from DefaultData.DefaultDataUtil import *
from Calc.DP.Transfer_DLL.x64.Release.SWCalcTransfer import DemProj
from Calc.CS.Transfer_DLL.x64.Release.SWCalcTransfer import LiSTCalc

initialConditions_json_path = os.getcwd() + '\\DefaultData\\JSONData\\demproj\\initialConditions'

def write_DP_population_db(version):
    GBModData = GB_get_db_json(os.environ[GB_SPECT_MOD_DATA_CONN_ENV], "globals", formatCountryFName(GBCountryListDBName, GBDatabaseVersion))

    for country in GBModData: 
        # if not (country['ISO3_Numeric'] == 5733):

        params = createProjectionParams()
        params.firstYear = 1970
        params.finalYear = 2030
        params.country = country['ISO3_Alpha']
        params.extra['subNatCode'] = 0
        params.modules = [GB_DP, GB_AM]

        projection = GB_CreateProjection(params)
        
        dt = np.dtype(np.float64)  
        for mv in projection:
            if type(projection[mv]) == list:
                if len(projection[mv])>0 and ((type(projection[mv][0])==dict) or(type(projection[mv][0])==str)) :
                    projection[mv] = np.array(projection[mv], order='C')
                else:
                    projection[mv] = np.array(projection[mv], order='C', dtype=dt)

        projection[DP_InitialConditionsTempTransportTag] = {}

        projection['timings']  = {}
        projection['dp_dll']  = DemProj()
        projection['cs_dll']  = LiSTCalc()
        GBCalculate(projection)

        pop1 = projection[DP_InitialConditionsTempTransportTag]['pop1']
        births = projection[DP_InitialConditionsTempTransportTag]['births']
        deaths = projection[DP_InitialConditionsTempTransportTag]['deaths']
        hiv_infections = projection[DP_InitialConditionsTempTransportTag]['hiv_infections']
        hiv_deaths = projection[DP_InitialConditionsTempTransportTag]['hiv_deaths']
        pmtct_need_15_49 = projection[DP_InitialConditionsTempTransportTag]['pmtct_need_15_49']
        pmtct_need_15_24 = projection[DP_InitialConditionsTempTransportTag]['pmtct_need_15_24']
        cotrim_need = projection[DP_InitialConditionsTempTransportTag]['cotrim_need']

        print('Writing '+ country['name'])

        now = datetime.datetime.now(timezone.utc)
        timeStamp = now.strftime("Date: " + GB_DateTime_Format)

        country_data = {
                'pop1': pop1.tolist(),
                'births': births.tolist(),
                'deaths': deaths.tolist(),
                'hiv_infections': hiv_infections.tolist(),
                'hiv_deaths': hiv_deaths.tolist(),
                'pmtct_need_15_49': pmtct_need_15_49.tolist(),
                'pmtct_need_15_24': pmtct_need_15_24.tolist(),
                'cotrim_need': cotrim_need.tolist(),
                'calcVersion': GB_Calc_Version,
                'PMVersion': GB_PM_Version,
                'date': timeStamp,
            }        
        
        os.makedirs(initialConditions_json_path, exist_ok=True)
        with open(os.path.join(initialConditions_json_path, formatCountryFName(params.country, version)), 'w') as f:
            ujson.dump(country_data, f)

def upload_DP_population_db(version):  
    uploadFilesInDir('demproj', initialConditions_json_path, version, pathMod = DPInitialConditionsDBSubDir)