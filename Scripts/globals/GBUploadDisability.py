
from os import getcwd, environ, makedirs
import pandas as pd
import ujson

from AvenirCommon.Database import GB_upload_file
from AvenirCommon.Logger import log

def create_disability_json(version):
    log('Creating disability json')
    countries = []

    FQName = getcwd()+'\Tools\DefaultDataManager\GB\ModData\GBModData.xlsx'

    sheet = pd.read_excel(FQName, sheet_name='DisabilityWeights', header=None)

    for r in range(2, sheet.shape[0]):
        #log(sheet.iat[r, 1]) #country name
        
        
        ages = []
        for c in range(2, sheet.shape[0]):
            ages.append(sheet.iat[r, c])
            
        country_jo = {
          'GBD_Name' : sheet.iat[r, 0],
          'Name' : sheet.iat[r, 1],
          'ages' : ages
        }
        
        #dict(zip(list(sheet.columns), list(sheet.values[r])))
        jo_str = ujson.dumps(country_jo)
        countries.append(country_jo)

    #PD_JSON = {"countryDataJSON": {"countryData": countries}}
    makedirs(getcwd()+'\Tools\DefaultDataManager\GB\JSON\\', exist_ok=True)
    with open(getcwd()+'\Tools\DefaultDataManager\GB\JSON\DisabilityWeights_'+version+'.JSON', 'w') as f:
        ujson.dump(countries, f)
    log('Finished creating disability json')
        

def upload_disability_json(version, country=''):
    log('Uploading disability json')
    FQName = getcwd()+'\Tools\DefaultDataManager\GB\JSON\DisabilityWeights_'+version+'.JSON'
    connection = environ['AVENIR_SW_DEFAULT_DATA_CONNECTION']

    GB_upload_file(connection, 'globals', 'DisabilityWeights_'+version+'.JSON', FQName)
    log('Uploaded disability json')