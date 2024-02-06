from os import getcwd, environ, makedirs, path
from AvenirCommon.Util import formatCountryFName
import pandas as pd
import ujson

from SpectrumCommon.Const.GB import *
from AvenirCommon.Database import GB_upload_file
from AvenirCommon.Logger  import log


countryList_json_path = getcwd() + '\\DefaultData\\JSONData\\globals\\'

def writeGBCountryListMaster(version):
    log('Creating country list master json ')
    FQName = getcwd() + '\\DefaultData\\SourceData\\globals\\GBModData.xlsx'
    
    gb_xlsx = pd.ExcelFile(FQName)
    sheet = gb_xlsx.parse('CountryMaster')

    def MapDefaultColToModID(col):
        cases = {
            10: GB_AM,
            11: GB_FP,
            12: GB_CS,
            13: GB_HV,
            14: GB_RN,
            15: GB_TB,
            16: GB_NC,
            17: GB_MA,
            18: GB_SI,
            19: GB_GC,
        }
        return cases[col]

    def getCell(row, col):
        if pd.isnull(sheet.values[row][col]):
            return ''
        else:
            return sheet.values[row][col]
        
    countries = []
    for row in range(0, len(sheet.values)):
        if (getCell(row, 3) == 0):
            countries.append({
                    'name':         getCell(row, 1),
                    'ISO3_Numeric': getCell(row, 0),
                    'ISO3_Alpha':   getCell(row, 2),
                    'subNatCode':   getCell(row, 3),
                    'subNatName':   getCell(row, 4),
                    'subNats':      [],
                    'currency':     getCell(row, 5),
                    'exchangeRate': getCell(row, 6),
                    'currencyName': getCell(row, 7),
                    'UPDFileName':  getCell(row, 8),
                    'EPPFileName':  getCell(row, 9),
                    'modsWithDefaultData': [MapDefaultColToModID(c) for c in range(10, 20) if getCell(row, c) == 1]+[GB_GB, GB_DP],
                    'sources': {
                        'DPSource': getCell(row, 20),
                        'AMSource': getCell(row, 21),
                        'FPSource': getCell(row, 22),
                        'CSSource': getCell(row, 23),
                        'HVSource': getCell(row, 24),
                        'RNSource': getCell(row, 25),
                        'TBSource': getCell(row, 26),
                        'NCSource': getCell(row, 27),
                        'MASource': getCell(row, 28),
                        'SISource': getCell(row, 29),
                        'GCSource': getCell(row, 30),
                    },
                    'NCRegionCode': getCell(row, 31),
                    'equityTool':   getCell(row, 32)
            })
        else:
            if (countries[-1]['ISO3_Alpha'] == getCell(row, 2)):
                countries[-1]['subNats'].append({
                    'subNatCode':   getCell(row, 3),
                    'subNatName':   getCell(row, 4),
                    })
                
    countries = sorted(countries, key=lambda d: d['name']) 

    makedirs(countryList_json_path, exist_ok=True)
    with open(path.join(countryList_json_path, formatCountryFName(GBCountryListDBName, version)), 'w') as f:
        ujson.dump(countries, f)
    log('Finished country list master json ')

    
def uploadGBCountryListMaster(version):
    FQName = path.join(countryList_json_path, formatCountryFName(GBCountryListDBName, version))
    connection = environ['AVENIR_SW_DEFAULT_DATA_CONNECTION']
    
    GB_upload_file(connection, 'globals', formatCountryFName(GBCountryListDBName, version), FQName) 
    log('Uploaded country list master json ')
