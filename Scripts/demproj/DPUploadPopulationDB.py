import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime, timezone
import ujson

from AvenirCommon.Database.BlobStorage import GB_get_db_json
from AvenirCommon.Util import formatCountryFName

from SpectrumCommon.Const.GB.GBConst import GB_DP, GB_AM
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Const.AM import *
from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Modvars.GB.GBCreateProjection import *

import Calc
from Calc.GB.GBMain import GBCalculate 
from Calc.DP.Transfer_DLL.x64.Release.SWCalcTransfer import DemProj
from Calc.CS.Transfer_DLL.x64.Release.SWCalcTransfer import LiSTCalc

from DefaultDataUtil import *

initialConditions_json_path = os.getcwd() + '\\JSONData\\demproj\\initialConditions'


def _get_calc_runtime_root():
    # The native transfer DLLs load with a relative path like .\\Calc\\...,
    # so the process cwd must be the parent folder that contains Calc.
    calc_paths = list(getattr(Calc, '__path__', []))
    if calc_paths:
        return os.path.dirname(os.path.abspath(calc_paths[0]))

    calc_file = getattr(Calc, '__file__', None)
    if calc_file:
        return os.path.dirname(os.path.dirname(os.path.abspath(calc_file)))

    return os.getcwd()


@contextmanager
def _calc_runtime_cwd():
    original_cwd = os.getcwd()
    try:
        os.chdir(_get_calc_runtime_root())
        yield
    finally:
        os.chdir(original_cwd)


def _process_country_population(country, version):
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
            if len(projection[mv]) > 0 and ((type(projection[mv][0]) == dict) or (type(projection[mv][0]) == str)):
                projection[mv] = np.array(projection[mv], order='C')
            else:
                projection[mv] = np.array(projection[mv], order='C', dtype=dt)

    projection[DP_InitialConditionsTempTransportTag] = {}
    projection['timings'] = {}

    with _calc_runtime_cwd():
        projection['dp_dll'] = DemProj()
        projection['cs_dll'] = LiSTCalc()
        GBCalculate(projection)

    pop1 = projection[DP_InitialConditionsTempTransportTag]['pop1']
    births = projection[DP_InitialConditionsTempTransportTag]['births']
    deaths = projection[DP_InitialConditionsTempTransportTag]['deaths']
    hiv_infections = projection[DP_InitialConditionsTempTransportTag]['hiv_infections']
    hiv_deaths = projection[DP_InitialConditionsTempTransportTag]['hiv_deaths']
    pmtct_need_15_49 = projection[DP_InitialConditionsTempTransportTag]['pmtct_need_15_49']
    pmtct_need_15_24 = projection[DP_InitialConditionsTempTransportTag]['pmtct_need_15_24']
    cotrim_need = projection[DP_InitialConditionsTempTransportTag]['cotrim_need']
    art_need = projection[DP_InitialConditionsTempTransportTag]['art_need']

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
        'art_need': art_need.tolist(),
        'calcVersion': GB_Calc_Version,
        'PMVersion': GB_PM_Version,
        'date': timeStamp,
    }

    os.makedirs(initialConditions_json_path, exist_ok=True)
    with open(os.path.join(initialConditions_json_path, formatCountryFName(params.country, version)), 'w') as f:
        ujson.dump(country_data, f)

    return country['name']


def write_DP_population_db(version, max_workers=None):
    start_time = datetime.datetime.now()
    print(f"Starting DP population database generation at {start_time}")
    GBModData = GB_get_db_json(os.environ[GB_SPECT_MOD_DATA_CONN_ENV], "globals", formatCountryFName(GBCountryListDBName, GBDatabaseVersion))
    failed_countries = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_country = {
            executor.submit(_process_country_population, country, version): country
            for country in GBModData
        }

        for future in as_completed(future_to_country):
            country = future_to_country[future]
            try:
                finished_country = future.result()
                print('Writing ' + finished_country)
            except Exception as e:
                failed_countries.append(country['name'])
                print(f"Error processing country {country['name']}: {e}")   
    end_time = datetime.datetime.now()
    print(f"Finished DP population database generation at {end_time}")
    print(f"Total time taken: {end_time - start_time}")

    print("Failed countries:", failed_countries)

    
def upload_DP_population_db(version):  
    uploadFilesInDir('demproj', initialConditions_json_path, version, pathMod = DPInitialConditionsDBSubDir)