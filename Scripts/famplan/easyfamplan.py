import os
import pandas as pd
from AvenirCommon.Wrappers import GBSheet
import numpy as np
import ujson

from AvenirCommon.Database import GB_upload_json, GB_upload_file
from AvenirCommon.Util import formatCountryFName
from AvenirCommon.Logger import log

from SpectrumCommon.Const.GB import GB_Nan
from SpectrumCommon.Const.FP import *

from Tools.DefaultDataManager.GB.Upload.GBUploadModData import getGBModDataDict
  
sheet_to_key = {
    'Vaginal Barrier (Diaphragm)':     'vaginalBarrierDiaphragm',
    'Implant(Jadelle 5years Default)': 'implantJadelle5YrDefault',
    'Injectable(Depo3months default)': 'injectableDepo3MoDefault',
    'IUD (Copper T, 10 years)':        'IUD_CopperT10Yr',
    'Condom (Male)':                   'condomMale',
    'Sterilization (Female)':          'sterilizationFemale',
    'Sterilization (Male)':            'sterilizationMale',
    'Other Modern':                    'otherModern',
    'Pill (standard)':                 'pillStandard',
    'Traditional(PeriodicAbstinence)': 'traditionalPeriodicAbstinence',
    'Traditional (Withdrawal)':        'traditionalWithdrawal',
    'Traditional (Other)':             'traditionalOther',
    
    'Childless Women45-49(Sterility)': 'childlessWomen45to49Sterility',
    'PPI Median Duration':             'PPI_MedianDuration',
    
    'TAR':                             'TAR',
    'TF':                              'TF',
    'TFR':                             'TFR',
    'CPR':                             'CPR',
    'In Union':                        'inUnion',
    'Unmet need':                      'unmetNeed',
}

single_year_key = {
    'ProxyNote':'ProxyNote',
    'Group': 'Group',
    'MA<18 & First Birth': 'MA_L18FirstBirth',
    'MA<18 & BO2_3': 'MA_L18_BO2_3',
    'MA<18 & BO>3': 'MA_L18_BO_G3',
    'MA18_34 & First Birth': 'MA18_34FirstBirth',
    'MA18_34 & BO2_3': 'MA18_34BO2_3',
    'MA18_34 & BO>3':'MA18_34BO_G3',
    'MA>35 & First Birth': 'MA_G35FirstBirth',
    'MA>35 & BO2_3':'MA_G35BO2_3',
    'MA>35 & BO>3':'MA_G35BO_G3',
    'FirstBirth Interval': 'firstBirthInterval',
    '<18Months':'L18Months',
    '<24Months':'BO18_24Months',
    '24 monthers or Greater': 'BO_24MonthsOrGreater',
    'Proportion of unintended pregnancies terminated by abortion':'PropUnintendedPregEndInAbort',
    'Ratio Unsafe abortion MMR to MMR': 'mortalityRateUnsafeAbortMMR',
    'Proportion of abortions that are unsafe':'propUnsafeAbort',
    'Deaths related to unsafe abortion per 100000 unsafe abortions':'MortalityRateUnsafeAbort',
    'StartYear':'surveyYear',
    'MMR':'MMR',  
}
        

def create_famplan_db(version, mode, country=''):
    log('Creating famplan json')
    countries = {}
    default_path = os.getcwd()+'\\' + __name__.split('.')[0] 
    easy_famplan_fqname = f'{default_path}\\SourceData\\famplan\\EasyFamPlan.xlsx'
    fp_xlsx = pd.ExcelFile(easy_famplan_fqname)
     
    GBModData = getGBModDataDict()

    #single year data and initial country data setup
    sheet = fp_xlsx.parse('Single Year Data')
    for r in range(0, sheet.shape[0]):
        country_name = sheet.iat[r, 1]
        iso_numeric = int(sheet.iat[r, 0])
      
        iso_alpha = -1
        for key, record in GBModData.items():
            if record['ISO3'] == iso_numeric:
                iso_alpha = record['ISO3_Alpha'] 
        
        #using country name as key since it is used in age data
        countries[country_name] = {'name':country_name, 
                                   'ISO_Numeric':iso_numeric,
                                   'ISO_Alpha': iso_alpha}
        

        for c in range(2, sheet.shape[1]):
            col_name = list(sheet)[c]
            key = single_year_key[col_name]
            value = sheet.iat[r, c]
            if sheet[col_name].dtype == np.int64:
                value = int(value)
            if (str(value).upper() ==GB_Nan): 
                value = 0
            countries[country_name][key] = value 
        
    #Sources
    sheet = fp_xlsx.parse('Sources')
    for r in range(0, sheet.shape[0]):
        country_name = sheet.iat[r, 2]
        note = str(sheet.iat[r, 3])
        proxy_note = str(sheet.iat[r, 4])
        source = ''
        if note!='nan':
            source += note+' '
        if proxy_note!='nan':
            source += proxy_note

        if (country_name in  countries):
            countries[country_name]['mainDataSources'] = source        

    #age data, Uninterpolated data is for Explore LiST 
    sheetName = 'Age Data' if mode == FP_Interpolated else 'Age Data (Uninterpolated)'
    
    sheet = fp_xlsx.parse(sheetName)
    for r in range(0, sheet.shape[0]):
        country_name = sheet.iat[r, 2]
        if not (country_name in  countries):
            #log(country_name +' skipped. No single year data')
            continue
            #raise Exception(country+' country does not exist in FP single year data')
        
        varible_name = sheet.iat[r, 3] 
        key = sheet_to_key[varible_name]
        age_idx = int(sheet.iat[r, 4]) 
        if key == None:
            log(r)
            continue
        if not(key in countries[country_name]):
            countries[country_name][key] = [] 
            
        age_array = []
        for c in range(5, sheet.shape[1]):
            value = sheet.iat[r, c]
            if str(value).upper()==GB_Nan:           
                value = 0 if mode == FP_Interpolated else -1
            age_array.append(value)
        countries[country_name][key].append(age_array)
        
    dir = FP_InterpDir if mode == FP_Interpolated else FP_Uninterp

    famplan_json_path  = default_path +'\\JSONData\\famplan\\'
    for country_name in countries:    
        country = countries[country_name]
        if country['ISO_Alpha']==-1:
            continue
        os.makedirs(famplan_json_path+dir+'\\', exist_ok=True)
        print(country['ISO_Alpha'])
        with open(famplan_json_path+dir+'\\'+country['ISO_Alpha']+'_'+version+'.JSON', 'w') as f:
            ujson.dump(country, f)
    log('Finished famplan json')