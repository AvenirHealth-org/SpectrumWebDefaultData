import os
import openpyxl
from openpyxl.utils import get_column_letter
import matplotlib.pyplot as plt
from AvenirCommon.Database import GB_upload_json, GB_upload_file, GB_get_db_json
import ujson
import numpy as np
from requests import post

import logging
from AvenirCommon.Util import GBRange
from SpectrumCommon.Const.TB import *
from SpectrumCommon.Const.GB import GB_Nan


def create_TB_fort_outputs(version):
    
    # 
    default_path = os.getcwd()+'\\' + __name__.split('.')[0] 
    if not TB_RUN_DEFAULT_COUNTRIES:
    # if True:
        who_tb_fqname = f'{default_path}\\SourceData\\tuberculosis\\WHO_TB_CountryData2023.xlsx'
        xlsx = openpyxl.load_workbook(who_tb_fqname, read_only=False, keep_vba=False, data_only=False, keep_links=True)
        countries = ['SAMP']
        
        for country_cell in xlsx['Noti_Distribution']['C']:
            iso3=country_cell.value
            if iso3 == 'SSD':
                tXf = xlsx['Noti_Distribution'][f'BQ{country_cell.row}'].value
            countries.append(iso3)
            # iso3=country_cell.value
    else:
        countries = TB_RUN_DEFAULT_COUNTRIES 
    failed_countries = []
    after_stp =True
    # for country_cell in xlsx['Countries']['C']:
    # for country_cell in xlsx['Noti_Distribution']['C']:
    #     # # tXf = xlsx['Noti_Distribution'][f'BQ{country_cell.row}'].value
        # iso3=country_cell.value

    for iso3 in TB_RUN_DEFAULT_COUNTRIES:
    #     tXf = 0.0298
    #     tXp = 0.2450
        # if iso3 == 'STP':
        #     after_stp = True 
        #     continue
        if after_stp:
            try:
                if ((iso3=='iso3') or (iso3==None)):
                    continue
                print(iso3)
                # pages = ['TB_burden_countries']
                fort_inputs = GB_get_db_json(os.environ['AVENIR_SW_DEFAULT_DATA_CONNECTION'], 'tuberculosis', 'fort/inputs/'+iso3+'_V6.JSON') 
                # who_db  = GB_get_db_json(os.environ['AVENIR_SW_DEFAULT_DATA_CONNECTION'], 'tuberculosis', 'countries/'+iso3+'_V3.JSON') 
                # fort_inputs["tXf"]  = [0.035]*num_years

                # null = None

                # with open('BRB_FORT_INPUTS.JSON', "w+") as fp:
                    # ujson.dump(fort_inputs, fp)
                fort_inputs['modelType'] = 'IPn2'
                # fort_inputs['tXf'] = [tXf]*len(fort_inputs['tXf'])
                # fort_inputs['tXp'] = [tXp]*len(fort_inputs['tXf'])
                response = post('https://tbbetastatisticalserver.azurewebsites.net/projection', json=fort_inputs)
                # response = post('http://localhost:8080/projection', json=fort_inputs)
                if response.status_code==500:
                    failed_countries.append({"iso":iso3, "tXf":fort_inputs['tXf']})    
                    with open(default_path+'\\JSONData\\tuberculosis\\fortinputs\\failed\\'+iso3+'_'+version+'.JSON', 'w') as f:
                        ujson.dump(fort_inputs, f)
                fort_IP_outputs = response.json()
                # fort_inputs['modelType'] = 'failsafe
                # response = post('https://tbbetastatisticalserver.azurewebsites.net/projection', json=fort_inputs)
                # # response = post('http://localhost:8080/projection', json=fort_inputs)
                # fort_failsafe_outputs = response.json()

                # plt.plot(fort_IP_outputs['year'], fort_IP_outputs['pMid'])
                # plt.plot(fort_failsafe_outputs['year'], fort_failsafe_outputs['pMid'])
                # plt.la
                # plt.ylabel('prevalence')
                # plt.show()

                # plt.plot(fort_IP_outputs['year'], fort_IP_outputs['iMid'])
                # plt.plot(fort_failsafe_outputs['year'], fort_failsafe_outputs['iMid'])
                # plt.ylabel('incidence')
                # plt.show()
                
                # plt.plot(fort_IP_outputs['year'], fort_IP_outputs['mMid'])
                # plt.plot(fort_failsafe_outputs['year'], fort_failsafe_outputs['mMid'])
                # plt.ylabel('mortality')
                # plt.show()

                # plt.plot(fort_IP_outputs['year'], fort_IP_outputs['nMid'])
                # plt.plot(fort_failsafe_outputs['year'], fort_failsafe_outputs['nMid'])
                # plt.ylabel('notification')
                # plt.show()

                pass
                os.makedirs(default_path+'\\JSONData\\tuberculosis\\fortoutputs\\', exist_ok=True)
                with open(default_path+'\\JSONData\\tuberculosis\\fortoutputs\\'+iso3+'_'+version+'.JSON', 'w') as f:
                    ujson.dump(fort_IP_outputs, f)
                    if iso3 == 'KEN':
                        iso3 = 'SAMP'
                        print(iso3)
                        with open(default_path+'\\JSONData\\tuberculosis\\fortoutputs\\'+iso3+'_'+version+'.JSON', 'w') as f:
                            ujson.dump(fort_IP_outputs, f)
            except:
                print(f'{iso3} exception')
    pass

def upload_tb_fort_outputs_db(version):
    connection =  os.environ['AVENIR_SW_DEFAULT_DATA_CONNECTION']
    countries = []
    
    default_path = os.getcwd()+'\\' + __name__.split('.')[0] 
    json_path= default_path+'\\JSONData\\tuberculosis\\fortoutputs\\'
    for subdir, dirs, files in os.walk(json_path):
        # for file in files:
        for iso3 in TB_RUN_DEFAULT_COUNTRIES:
            file = iso3+'_'+version+'.JSON'
            FQName = os.path.join(subdir, file)
            if os.path.isfile(FQName):
                if version in FQName:
                    print(FQName)
                    GB_upload_file(connection, 'tuberculosis', 'fort\\outputs\\'+file, FQName)
        
    logging.debug('Uploaded fort outputs db json')
   

######## Static data that works ######
# fort_inputs = {}
# fort_inputs["year"] = [
#                     2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011,
#                     2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023,
#                     2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035,
#                     2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047,
#                     2048, 2049, 2050
#                 ]
# fort_inputs["iHat"] = [
#         37000,
#         37000,
#         40000,
#         43000,
#         44000,
#         46000,
#         48000,
#         49000,
#         50000,
#         52000,
#         53000,
#         55000,
#         58000,
#         60000,
#         62000,
#         64000,
#         65000,
#         67000,
#         69000,
#         71000,
#         71000,
#         74000,
#         76000,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null,
#         null
#     ]
# fort_inputs["sEi"] = [
#     7397.95918367347,
#     7397.95918367347,
#     7908.163265306122,
#     8418.367346938776,
#     8928.57142857143,
#     9183.673469387755,
#     9693.877551020409,
#     9693.877551020409,
#     10204.081632653062,
#     10204.081632653062,
#     10714.285714285714,
#     10969.387755102041,
#     11479.591836734695,
#     11734.69387755102,
#     12244.897959183674,
#     12755.102040816328,
#     13010.204081632653,
#     13265.30612244898,
#     13775.510204081633,
#     14285.714285714286,
#     14030.612244897959,
#     14285.714285714286,
#     14540.816326530612,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null
# ]
# fort_inputs["nHat"] = [
#     7107,
#     10139,
#     13794,
#     13808,
#     18404,
#     21844,
#     25475,
#     28769,
#     28301,
#     26150,
#     28029,
#     27983,
#     28679,
#     30507,
#     31746,
#     35878,
#     41954,
#     46847,
#     48625,
#     52518,
#     45887,
#     50386,
#     51855,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null
# ]
# fort_inputs["sEn"] = [
#     543.9030612244896,
#     775.9438775510201,
#     1055.6632653061222,
#     1056.7346938775509,
#     1408.4693877551017,
#     1671.7346938775513,
#     1949.6173469387745,
#     2201.7091836734694,
#     2165.892857142857,
#     2001.2755102040808,
#     2145.0765306122453,
#     2141.5561224489793,
#     2194.821428571429,
#     2334.719387755101,
#     2429.5408163265297,
#     2745.7653061224487,
#     3210.7653061224482,
#     3585.2295918367345,
#     3721.3010204081615,
#     4019.2346938775513,
#     3511.7602040816323,
#     3856.0714285714275,
#     3968.494897959182,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null
# ]
# fort_inputs["mHat"] = [
#     13000,
#     12000,
#     12000,
#     13000,
#     12000,
#     12000,
#     11000,
#     10000,
#     11000,
#     12000,
#     12000,
#     13000,
#     14000,
#     14000,
#     14000,
#     13000,
#     12000,
#     11000,
#     11000,
#     9900,
#     10000,
#     10000,
#     9900,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null
# ]
# fort_inputs["sEm"] = [
#     3163.265306122449,
#     3010.204081632653,
#     2806.122448979592,
#     3163.265306122449,
#     2780.612244897959,
#     2857.1428571428573,
#     2678.5714285714284,
#     2295.918367346939,
#     2448.979591836735,
#     2984.6938775510203,
#     2755.1020408163267,
#     3137.7551020408164,
#     3290.8163265306125,
#     3265.3061224489797,
#     3214.285714285714,
#     3061.2244897959185,
#     2806.122448979592,
#     2448.979591836735,
#     2448.979591836735,
#     2321.4285714285716,
#     2193.877551020408,
#     2193.877551020408,
#     2295.918367346939,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null
# ]
# fort_inputs["pHat"] = [
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null
# ]
# fort_inputs["sEp"] = [
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null,
#     null
# ]
# fort_inputs["modelType"] = "IP"
# fort_inputs["tXf"] = [
#     0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035,
#     0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035,
#     0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035,
#     0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035,
#     0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035
# ]
# fort_inputs["hRd"] = [
#     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
# ]
# fort_inputs["hRi"] = [
#     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
# ]
# fort_inputs["oRt"] = [
#     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
# ]