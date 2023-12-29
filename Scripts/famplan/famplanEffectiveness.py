import os
import pandas as pd
import ujson

from AvenirCommon.Database import GB_upload_json, GB_upload_file
from AvenirCommon.Logger import log


def create_famplan_effectiveness(version):
    log('Creating FP effectiveness json')
    
    default_path = os.getcwd()+'\\' + __name__.split('.')[0] 
    fp_moddata_fqname = f'{default_path}\\SourceData\\famplan\\FPModData.xlsx'
    FPmoddata=pd.read_excel(fp_moddata_fqname,"Effectiveness", header=None) # Read the excel sheet_name "Effectiveness" and exclude the headers
    df_FPmoddata= pd.DataFrame(FPmoddata) #Converts the excel data format into pandas DataFrame

    FP_est_list=[] #Main FP estimates list to store multiple dictionary data
    sdict={}    # Stores excel row values
    values1=[] # Stores values of each FP methods

    for r in range(1,df_FPmoddata.shape[0]):
        name1=df_FPmoddata.iat[r,0]
        sdict["name"]=name1
        sdict["mstID"]=int(FPmoddata.iat[r,1])     # r's value starts from 1 and mstID should start from 0 hence r-1
        values1=list(df_FPmoddata.iloc[r,2:]) #store data from excel's column 1 till the end, for each row
        values_rounded = values1.copy() # [round(num, 3) for num in values1] #we're rounding by 3 here since there appears to be junk at the end of the floating values
        sdict["values"]=values_rounded #Store list of values in a dictionary
        sdict_copy=sdict.copy() #Create a copy of the dictionary
        FP_est_list.append(sdict_copy) #Append the values of the new copied dictionary into the main FP estimates list
    
    famplan_json_path  = f'{default_path}\\JSONData\\famplan\\'
    os.makedirs(famplan_json_path, exist_ok=True)
    with open(f'{famplan_json_path}\\FPEffectiveness_{version}.JSON', 'w') as f:
        ujson.dump(FP_est_list, f)
    log('Finished FP effectiveness json')
    
    
def upload_FP_effectiveness(version):
    FQName = os.getcwd()+'\Tools\DefaultDataManager\FP\JSON\FPEffectiveness_'+version+'.JSON'
    connection = os.environ['AVENIR_SW_DEFAULT_DATA_CONNECTION']
    
    GB_upload_file(connection, 'famplan', 'FPEffectiveness_'+version+'.JSON', FQName) 
    log('Uploaded FP effectiveness json')

