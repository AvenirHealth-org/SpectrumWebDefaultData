import os
import pandas as pd
import numpy as np
import ujson

from copy import deepcopy

from AvenirCommon.Logger import log
from AvenirCommon.Util import formatCountryFName, GBRange
from AvenirCommon.Database import GB_get_db_json, GB_file_exists

from SpectrumCommon.Const.CS import *
from SpectrumCommon.Const.IV.IVConst import IV_INTERVENTION_DB_NAME, IV_CS_INTERVENTION_DB_CURR_VERSION
from SpectrumCommon.Const.IV import IVDatabaseKeys as ivdbk
from SpectrumCommon.Const.GB import *

SourceData_DIR = os.getcwd() + '\DefaultData\SourceData\list'
JSONData_DIR = os.getcwd() + '\DefaultData\JSONData\list'

#####################################################################################################################
#                                                                                                                   #
#                                             Trim Dictionaries                                                     #
#                                                                                                                   #
#####################################################################################################################

def trimDict(data, ignoreKeySet = []):  
    popSet = []
    for key in data:
        if type (data[key]) == dict:
            trimDict(data[key], ignoreKeySet)
        
        copy = deepcopy(data[key])
        if type (copy) == dict:
            for ignoreKey in ignoreKeySet:
                if ignoreKey in copy:
                    copy.pop(ignoreKey)
        
        if (copy in [{}, '']):
            popSet.append(key)

    for key in popSet:
        data.pop(key)

#####################################################################################################################
#                                                                                                                   #
#                                              Get Sheet Values                                                     #
#                                                                                                                   #
#####################################################################################################################

def cellIsBlank(sheet, row, col):
    cell_value = sheet.iloc[row, col]
    return (pd.isnull(cell_value)) or (cell_value == "")

def getVal_IfInBounds(sheet, row, col):
    val = ''
    if row < len(sheet.values):
        if col < len(sheet.values[row]):
            val = sheet.values[row][col] 
    return val

def getVal(sheet, row, col):
    val = getVal_IfInBounds(sheet, row, col)    
    if (type(val)) == str:
        val = val.strip()
    if pd.isna(val):
        val = ''
    return val

def getFloat(sheet, row, col):
    val = getVal_IfInBounds(sheet, row, col)  
    if pd.isna(val):
        val = 0
    return val

#####################################################################################################################
#                                                                                                                   #
#                                            File saving functions                                                  #
#                                                                                                                   #
#####################################################################################################################

def createFile(FQName, reportStr, data):
    log('Creating ' + reportStr)         
    with open(FQName, 'w') as f:
        ujson.dump(data, f)    

def createSingleFile(DBName, data):
    reportStr = DBName
    FQName = JSONData_DIR + '/' + DBName + '_' + latest_DB_Version[DBName] + '.JSON'            
    createFile(FQName, reportStr, data)

def createCountryFiles(DBName, countries):    
    path = JSONData_DIR + '/' + DBName + '_' + latest_DB_Version[DBName] + '/'
    if not os.path.exists(path):
        os.makedirs(path)   

    i = 0
    for key, country in countries.items():
        i += 1
        ISO3_Alpha = country.pop('ISO3_Alpha')     
        progress = str(i) + '/' + str(len(countries))
        if not ISO3_Alpha == -1:
            reportStr = DBName + ', country: ' + ISO3_Alpha + ', ' + progress      
            FQName = path + ISO3_Alpha + '.JSON'   
            createFile(FQName, reportStr, country)        

#####################################################################################################################
#                                                                                                                   #
#                                        DefaultData helper functions                                               #
#                                                                                                                   #
#####################################################################################################################

NOCASE = -1
CASE_1 = 0
CASE_2 = 1
CASE_3 = 2
CASE_4 = 3

def createVarsRec(var1, var2, var3, var4, var5, var6, var7, var8 = False, var9 = True):
    return {
        'case'       : var1, 
        'Eff/OR/RR'  : var2, 
        'alpha/mean' : var3, 
        'beta/sd'    : var4, 
        'startCol'   : var5, 
        'finalCol'   : var6, 
        'keyRow'     : var7, 
        'inc_keyCol' : var8, 
        'inclMstID'  : var9
        }

def initVars(tagRecord, dataFinalCol):                    

    result = createVarsRec(NOCASE, '', '', '', 0, 0, 0)
    
    SGA_START_COL = 11
    AGE_START_COL = 11
    PNN_AGE_START_COL = 17

    SGA_END_COL = 27
    AGE_END_COL = dataFinalCol
    
    HEADER_ROW = 0
    
    tag = tagRecord["tag"]
    TAG_HEADER_ROW_1 = tagRecord["firstRow"] - 1  
    TAG_HEADER_ROW_2 = tagRecord["firstRow"] - 2   
    
    if tag == TG_Efficacy            : result = createVarsRec(CASE_1, 'Eff', 'alpha', 'beta', AGE_START_COL, AGE_END_COL, HEADER_ROW)
    if tag == TG_AgeAndBirthOrder    : result = createVarsRec(CASE_2, 'RR', 'n/a', 'n/a', SGA_START_COL, SGA_END_COL, TAG_HEADER_ROW_1)
    if tag == TG_BirthSpacing        : result = createVarsRec(CASE_2, 'Eff', 'mean', 'sd', SGA_START_COL, SGA_END_COL, TAG_HEADER_ROW_1)
    if tag == TG_IntervForBO         : result = createVarsRec(CASE_3, 'Eff', 'alpha', 'beta', SGA_START_COL, SGA_END_COL, TAG_HEADER_ROW_1)
    if tag == TG_ImpactsStunting     : result = createVarsRec(CASE_1, 'OR', 'alpha', 'beta', AGE_START_COL, AGE_END_COL, HEADER_ROW, False, False)
    if tag == TG_ImpactWastingOnMort : result = createVarsRec(CASE_2, 'Eff', 'alpha', 'beta', AGE_START_COL, AGE_END_COL, HEADER_ROW)
    if tag == TG_ImpactOnAnemia      : result = createVarsRec(CASE_2, 'Eff', 'alpha', 'beta', 5, 17, TAG_HEADER_ROW_2)
    if tag == TG_ReducInStunt        : result = createVarsRec(CASE_2, 'Eff', 'n/a', 'n/a', 5, 11, TAG_HEADER_ROW_1)
    if tag == TG_EducAttain          : result = createVarsRec(CASE_2, 'Eff', 'n/a', 'n/a', 5, 11, TAG_HEADER_ROW_1)
    if tag == TG_RelRiskAnemia       : result = createVarsRec(CASE_1, 'OR', 'mean', 'sd', 5, 11, HEADER_ROW)
    if tag == TG_ImpactDiarrInc      : result = createVarsRec(CASE_2, 'Eff', 'alpha', 'beta', AGE_START_COL, AGE_END_COL, HEADER_ROW, True)
    if tag == TG_ImpactPneumInc      : result = createVarsRec(CASE_2, 'Eff', 'alpha', 'beta', AGE_START_COL, AGE_END_COL, HEADER_ROW, True)
    if tag == TG_ImpactMeninInc      : result = createVarsRec(CASE_2, 'Eff', 'alpha', 'beta', AGE_START_COL, AGE_END_COL, HEADER_ROW, True)
    if tag == TG_BFImprovement       : result = createVarsRec(CASE_2, 'OR', 'mean', 'sd', AGE_START_COL, AGE_END_COL, HEADER_ROW, True)
    if tag == TG_RelRiskStunting     : result = createVarsRec(CASE_1, 'RR', 'mean', 'sd', AGE_START_COL, AGE_END_COL, HEADER_ROW)
    if tag == TG_RelRiskWasting      : result = createVarsRec(CASE_1, 'RR', 'mean', 'sd', AGE_START_COL, AGE_END_COL, HEADER_ROW)
    if tag == TG_RelRiskMortBF       : result = createVarsRec(CASE_1, 'RR', 'mean', 'sd', PNN_AGE_START_COL, AGE_END_COL, HEADER_ROW)
    if tag == TG_RelRiskDiarrBF      : result = createVarsRec(CASE_2, 'RR', 'mean', 'sd', AGE_START_COL, AGE_END_COL, HEADER_ROW, True)
    if tag == TG_RelRiskPneumBF      : result = createVarsRec(CASE_2, 'RR', 'mean', 'sd', AGE_START_COL, AGE_END_COL, HEADER_ROW, True)
    if tag == TG_RelRiskMeninBF      : result = createVarsRec(CASE_2, 'RR', 'mean', 'sd', AGE_START_COL, AGE_END_COL, HEADER_ROW, True)
    if tag == TG_DetVaccEff          : result = createVarsRec(CASE_4, 'Eff', 'alpha', 'beta', AGE_START_COL, AGE_END_COL, HEADER_ROW)

    return result

def createDataRec(sheet, row, col, vars):
    
    key1 = vars['Eff/OR/RR']
    key5 = vars['alpha/mean']
    key6 = vars['beta/sd']

    return {
        key1  : getVal(sheet, row, col),
        'Aff' : getVal(sheet, row, col + 1),
        'Min' : getVal(sheet, row, col + 2),
        'Max' : getVal(sheet, row, col + 3),
        key5  : getVal(sheet, row, col + 4), 
        key6  : getVal(sheet, row, col + 5) 
        }

#####################################################################################################################
#                                                                                                                   #
#                                             Create DefaultData                                                    #
#                                                                                                                   #
#####################################################################################################################

def create_DefaultData():
    xlsx = pd.ExcelFile(SourceData_DIR + '\CSModData.xlsx')

    for sheetName in xlsx.sheet_names:     
        if sheetName in ['DefaultData']:
            sheet = xlsx.parse(sheetName, header=None)

            dataFirstRow = 2
            dataFinalRow = len(sheet.values) - 1

            sourceCol = 4
            dataFinalCol = len(sheet.values[2])

            data = {}  
            
            tagRecords = []
            
            for row in GBRange(dataFirstRow, dataFinalRow):
                cellVal = getVal(sheet, row, 0)
                if '<' in cellVal:
                    tagRecords.append({"tag" : cellVal, "firstRow" : row + 2})
            
            finalTagIndex = len(tagRecords) - 1
            for i in GBRange(0, finalTagIndex - 1):
                tagRecords[i]["finalRow"] = tagRecords[i + 1]["firstRow"] - 4    
            tagRecords[finalTagIndex]["finalRow"] = dataFinalRow            

            for tagRecord in tagRecords:
                
                tag = tagRecord["tag"]
                firstRow = tagRecord["firstRow"]  
                finalRow = tagRecord["finalRow"]     

                vars = initVars(tagRecord, dataFinalCol)       

                data[tag] = {}
                
                row = firstRow

                if vars['case'] == CASE_1:
                    
                    while row <= finalRow:                    
                        
                        key = getVal(sheet, row, 2)                    
                        mstID = getVal(sheet, row, 1)
                        row += 1                                   
                        
                        if not key == '':                            
                                   
                            key2 = getVal(sheet, row, 3)                  
                            mstID2 = getVal(sheet, row, 2)                             
                            
                            while not key2 == '':
                                
                                if not(key in data[tag]):
                                    data[tag][key] = {}                                
                                    if vars['inclMstID']:
                                        data[tag][key]['mstID'] = mstID                                                             
                                
                                data[tag][key][key2] = {}
                                
                                if tag in [TG_Efficacy]:
                                    data[tag][key][key2]['mstID'] = mstID2                                 
                                
                                source = getVal(sheet, row, sourceCol)
                                data[tag][key][key2]['source'] = source                                                    
                                
                                if (tag in [TG_RelRiskMortBF]) and 'Neonatal' in key:
                                    vars['startCol'] = 5
                                    vars['keyRow'] = 299

                                col = vars['startCol']                   
                                while col < vars['finalCol']:       
                                    record = createDataRec(sheet, row, col, vars)                                                                                                        
                                    if tag in [TG_RelRiskAnemia]:
                                        for key3 in record:
                                            data[tag][key][key2][key3] = record[key3]                                                                      
                                    else:   
                                        key3 = getVal(sheet, vars['keyRow'], col)                                                   
                                        data[tag][key][key2][key3] = record                                  
                                    col += 6                                                           
                                
                                row += 1
                                key2 = getVal(sheet, row, 3)              
                                mstID2 = getVal(sheet, row, 2) 

                if vars['case'] == CASE_2:
                    
                    ImpactCompFeedOnWasting = False

                    while row <= finalRow:
                        
                        if not ImpactCompFeedOnWasting:
                            key = getVal(sheet, row, 2)                                         
                            if vars['inc_keyCol']:
                                key = getVal(sheet, row, 3)    
                        
                        ImpactCompFeedOnWasting = key == 'Impact of complementary feeding on wasting'

                        if ImpactCompFeedOnWasting:
                            row += 1
                            if row > finalRow:
                                break
                            key2 = getVal(sheet, row, 3) 

                        sourceRec = {'source' : getVal(sheet, row, sourceCol)}                        
                        
                        if tag in [TG_ReducInStunt, TG_EducAttain]:
                            data[tag] = sourceRec                       
                        elif ImpactCompFeedOnWasting:
                            if not key in data[tag]:
                                data[tag][key] = {}   
                            data[tag][key][key2] = sourceRec
                        else:
                            data[tag][key] = sourceRec                                      
                        
                        col = vars['startCol']                   
                        while col < vars['finalCol'] :     
                            record = createDataRec(sheet, row, col, vars)                                                  
                            if tag in [TG_ReducInStunt, TG_EducAttain]:
                                for key in record:
                                    data[tag][key] = record[key]                        
                            elif ImpactCompFeedOnWasting:
                                key3 = getVal(sheet, vars['keyRow'], col) 
                                data[tag][key][key2][key3] = record   
                            else:
                                key2 = getVal(sheet, vars['keyRow'], col) 
                                data[tag][key][key2] = record                                                       
                            col += 6                                                   
                        
                        if not ImpactCompFeedOnWasting:
                            row += 1
                
                if vars['case'] == CASE_3:
                    
                    while row <= finalRow:
                        key = getVal(sheet, row, 2)                      
                        source = getVal(sheet, row, sourceCol) 
                        
                        if not(key in data[tag]):
                            data[tag][key] = {
                                'mstID'  : getVal(sheet, row, 1),
                                'source' : source
                                }                                        
                        
                        col = 5                      
                        while col < 11:       
                            key2 = getVal(sheet, vars['keyRow'], col)               
                            data[tag][key][key2] = getVal(sheet, row, col)                            
                            col += 3                               
                        
                        col = 11
                        while col < 27:       
                            key2 = getVal(sheet, vars['keyRow'], col)                               
                            data[tag][key][key2] = createDataRec(sheet, row, col, vars)              
                            col += 6                                            
                        
                        row += 1
                
                if vars['case'] == CASE_4:
                    
                    while row <= finalRow:                   
                            
                        key = getVal(sheet, row, 2)                    
                        mstID = getVal(sheet, row, 1)                            
                        
                        if not key == '':                            
                            
                            row += 1              
                            key2 = getVal(sheet, row, 3)                  
                            mstID2 = getVal(sheet, row, 2)                             
                            
                            while not key2 == '':                          
                                
                                row += 1              
                                key3 = getVal(sheet, row, 3)                           
                                
                                while not key3 == '':
                                    
                                    if not(key in data[tag]):
                                        data[tag][key] = {'mstID' : mstID}                                                         
                                    
                                    if not(key2 in data[tag][key]):
                                        data[tag][key][key2] = {'mstID' : mstID2}                             

                                    sourceRec = {'source' : getVal(sheet, row, sourceCol)}                        
                                    data[tag][key][key2][key3] = sourceRec                                               
                                    
                                    col = vars['startCol']                   
                                    while col < vars['finalCol']:       
                                        record = createDataRec(sheet, row, col, vars)                                                                                                        
                                        key4 = getVal(sheet, vars['keyRow'], col)                                                   
                                        data[tag][key][key2][key3][key4] = record                                  
                                        col += 6                                                           
                                    
                                    row += 1                                    
                                    
                                    key3 = getVal(sheet, row, 3)                                        
                                    mstID2 = getVal(sheet, row, 2)                                            
                                    
                                    if key3 == '':
                                        key2 = ''                                    
                                    elif (not (mstID2 == '') and (type(mstID2) == int)):
                                        key2 = getVal(sheet, row, 3)
                                        key3 = ''
            
            trimDict(data, ['mstID'])
            createSingleFile(DefaultData, data)

#####################################################################################################################
#                                                                                                                   #
#                                       Create InterventionDefaultData                                              #
#                                                                                                                   #
#####################################################################################################################

def create_IVDefaultData():
    xlsx = pd.ExcelFile(SourceData_DIR + '\CSModData.xlsx')

    for sheetName in xlsx.sheet_names:      
        if sheetName in ['InterventionDefaultData']:
            sheet = xlsx.parse(sheetName, header=None)

            dataFirstRow = 4
            dataFinalRow = len(sheet.values) - 1

            matDataStartCol = 3
            SB_DataStartCol = 58
            dataFinalCol = len(sheet.values[2]) - 4
            
            data = {}

            for row in GBRange(dataFirstRow, dataFinalRow):

                interventionName = getVal(sheet, row, 1)
                
                data[interventionName] = {
                    'mstID' : getVal(sheet, row, 0),
                    'MatSource' : getVal(sheet, row, matDataStartCol - 1),
                    'SB_Source' : getVal(sheet, row, SB_DataStartCol - 1)
                }
                
                col = matDataStartCol
                while col < SB_DataStartCol - 1:                    
                    causeOfDeath = getVal(sheet, 1, col)       
                    if not 'matDeathCauses' in data[interventionName]:
                        data[interventionName]['matDeathCauses'] = {}    
                    data[interventionName]['matDeathCauses'][causeOfDeath] = {
                        'mstID' : getVal(sheet, 2, col),
                        'Eff' : getVal(sheet, row, col),
                        'Aff' : getVal(sheet, row, col + 1),
                        'Min' : getVal(sheet, row, col + 2),
                        'Max' : getVal(sheet, row, col + 3),
                        'alpha' : getVal(sheet, row, col + 4),
                        'beta' : getVal(sheet, row, col + 5),
                        }
                    col += 6
                
                col = SB_DataStartCol
                while col <= dataFinalCol:
                    causeOfDeath = getVal(sheet, 1, col)       
                    if not 'SB_DeathCauses' in data[interventionName]:
                        data[interventionName]['SB_DeathCauses'] = {}    
                    data[interventionName]['SB_DeathCauses'][causeOfDeath] = {
                        'mstID' : getVal(sheet, 2, col),
                        'Eff' : getVal(sheet, row, col),
                        'Aff' : getVal(sheet, row, col + 1),
                        'aRR' : getVal(sheet, row, col + 2),
                        'Min' : getVal(sheet, row, col + 3),
                        'Max' : getVal(sheet, row, col + 4),
                        'alpha' : getVal(sheet, row, col + 5),
                        'beta' : getVal(sheet, row, col + 6),
                        }
                    col += 7

            trimDict(data, ['mstID'])
            createSingleFile(IVDefaultData, data)      
        
#####################################################################################################################
#                                                                                                                   #
#                                            Create GNI per capita                                                  #
#                                                                                                                   #
#####################################################################################################################

def create_GNI_Per_Cap():
    xlsx = pd.ExcelFile(SourceData_DIR + '\CSModData.xlsx')

    GBModData = GB_get_db_json(os.environ[GB_SPECT_MOD_DATA_CONN_ENV], "globals", formatCountryFName(GBCountryListDBName, GBDatabaseVersion))

    for sheetName in xlsx.sheet_names:      
        if sheetName in ['GNI per capita growth rate']:
            sheet = xlsx.parse(sheetName, header=None)
            
            dataFirstRow = 1
            dataFinalRow = len(sheet.values) - 1

            dataStartCol = 4
            dataFinalCol = len(sheet.values[2]) - 1
            
            countries = {}
            
            for row in GBRange(dataFirstRow, dataFinalRow):
                
                ISO3 = getVal(sheet, row, 0)
                
                ISO3_Alpha = -1
                for i in GBRange(0, len(GBModData)-1):
                    if GBModData[i]['ISO3_Numeric'] == int(ISO3):
                        ISO3_Alpha = GBModData[i]['ISO3_Alpha']               
                
                countries[ISO3_Alpha] = {'ISO3_Alpha' : ISO3_Alpha}

                i = 0
                for col in GBRange(dataStartCol, dataFinalCol):
                    years = getVal(sheet, 0, col)
                    countries[ISO3_Alpha][years] = getVal(sheet, row, col)
                    i += 1         

            createCountryFiles(GNI_Per_Cap, countries)
            
#####################################################################################################################
#                                                                                                                   #
#                                               Create Readiness                                                    #
#                                                                                                                   #
#####################################################################################################################

def create_Readiness():
    xlsx = pd.ExcelFile(SourceData_DIR + '\CSModData.xlsx')

    GBModData = GB_get_db_json(os.environ[GB_SPECT_MOD_DATA_CONN_ENV], "globals", formatCountryFName(GBCountryListDBName, GBDatabaseVersion))

    for sheetName in xlsx.sheet_names:     
        if sheetName in ['Readiness']:
            sheet = xlsx.parse(sheetName, header=None)
            
            dataFirstRow = 7
            dataFinalRow = len(sheet.values) - 1
                 
            dataFirstCol = 6
            dataFinalCol = len(sheet.values[2]) - 1
                        
            countries = {}
            
            for row in GBRange(dataFirstRow, dataFinalRow): 
                
                ISO3 = getVal(sheet, row, 1)
                
                ISO3_Alpha = -1
                for i in GBRange(0, len(GBModData)-1):
                    if GBModData[i]['ISO3_Numeric'] == int(ISO3):
                        ISO3_Alpha = GBModData[i]['ISO3_Alpha']               
                
                countries[ISO3_Alpha] = {
                    'ISO3_Alpha' : getVal(sheet, row, 0),
                    'anchorYear' : getVal(sheet, row, 2),
                    'anc' : getVal(sheet, row, 3),
                    'cb' : getVal(sheet, row, 4)
                    } 
                
                for col in GBRange(dataFirstCol, dataFinalCol): 
                    name = getVal(sheet, 3, col)
                    if not name == '':
                        countries[ISO3_Alpha][name] = {
                            'mstID': getVal(sheet, 4, col),
                            'anchor' : getVal(sheet, row, col)
                        }                 
    
            trimDict(countries, ['mstID'])
            createCountryFiles(Readiness, countries)            

#####################################################################################################################
#                                                                                                                   #
#                                           Create CSection coverage                                                #
#                                                                                                                   #
#####################################################################################################################

def create_CSection_Cov():
    xlsx = pd.ExcelFile(SourceData_DIR + '\CSModData.xlsx')

    GBModData = GB_get_db_json(os.environ[GB_SPECT_MOD_DATA_CONN_ENV], "globals", formatCountryFName(GBCountryListDBName, GBDatabaseVersion))

    for sheetName in xlsx.sheet_names:     
        if sheetName in ['CSection coverage']:
            sheet = xlsx.parse(sheetName, header=None)

            dataFirstRow = 2
            dataFinalRow = len(sheet.values) - 1
                        
            countries = {}
            
            for row in GBRange(dataFirstRow, dataFinalRow):                            

                ISO3 = getVal(sheet, row, 1)
                
                ISO3_Alpha = -1
                for i in GBRange(0, len(GBModData)-1):
                    if GBModData[i]['ISO3_Numeric'] == int(ISO3):
                        ISO3_Alpha = GBModData[i]['ISO3_Alpha']               
                
                year = getVal(sheet, row, 2)
                
                if not(ISO3_Alpha in countries):
                    countries[ISO3_Alpha] = {
                        'ISO3_Alpha' : getVal(sheet, row, 0)
                        }
                
                countries[ISO3_Alpha][year] = {
                    '<Csect>' : getVal(sheet, row, 3),
                    '<Urine>' : getVal(sheet, row, 4),
                    '<Blood>' : getVal(sheet, row, 5),
                    '<BP>' : getVal(sheet, row, 6)
                    }
    
            trimDict(countries, ['mstID'])
            createCountryFiles(CSection_Cov, countries) 
    
#####################################################################################################################
#                                                                                                                   #
#                                     Create Diarrhea shigella distribution                                         #
#                                                                                                                   #
#####################################################################################################################

def create_DiarrShigella():
    xlsx = pd.ExcelFile(SourceData_DIR + '\CSModData.xlsx')

    GBModData = GB_get_db_json(os.environ[GB_SPECT_MOD_DATA_CONN_ENV], "globals", formatCountryFName(GBCountryListDBName, GBDatabaseVersion))

    for sheetName in xlsx.sheet_names:     
        if sheetName in ['Diarrhea shigella distribution']:
            sheet = xlsx.parse(sheetName, header=None)

            dataFirstRow = 2
            dataFinalRow = len(sheet.values) - 1
                        
            countries = {}
            
            dataStartCol = 3
            dataFinalCol = len(sheet.values[2]) - 1
            
            for row in GBRange(dataFirstRow, dataFinalRow):                            

                ISO3 = getVal(sheet, row, 0)
            
                ISO3_Alpha = -1
                for i in GBRange(0, len(GBModData)-1):
                    if GBModData[i]['ISO3_Numeric'] == int(ISO3):
                        ISO3_Alpha = GBModData[i]['ISO3_Alpha']               
                
                
                if not(ISO3_Alpha in countries):
                    countries[ISO3_Alpha] = {
                        'ISO3_Alpha' : ISO3_Alpha
                        }

                tagRecords = []
                
                for col in GBRange(dataStartCol, dataFinalCol):
                    cellVal = getVal(sheet, 0, col)
                    if '<' in cellVal:
                        tagRecords.append({"tag" : cellVal, "firstCol" : col})
                        
                finalTagIndex = len(tagRecords) - 1
                for i in GBRange(0, finalTagIndex - 1):
                    tagRecords[i]["finalCol"] = tagRecords[i + 1]["firstCol"] - 1      
                tagRecords[finalTagIndex]["finalCol"] = dataFinalCol            

                for tagRecord in tagRecords:
                    
                    tag = tagRecord["tag"]
                    firstCol = tagRecord["firstCol"]  
                    finalCol = tagRecord["finalCol"]             

                    key1 = ''

                    countries[ISO3_Alpha][tag] = {}
                    
                    for col in GBRange(firstCol, finalCol):
                        value = getFloat(sheet, row, col)
                        key1 = getVal(sheet, 1, col)
                        countries[ISO3_Alpha][tag][key1] = value
        
            trimDict(countries)
            createCountryFiles(DiarrShigella, countries) 
    
#####################################################################################################################
#                                                                                                                   #
#                                            DBC helper functions                                                   #
#                                                                                                                   #
#####################################################################################################################

def get_DBC_Key(sheet, row, col, oldkey = ''):
    result = oldkey
    newKey = getVal(sheet, row, col)
    if not newKey == '':
        result = newKey
    if type(result) == str:
        if '\xa0' in result:
            result = result.replace('\xa0', ' ')
    return result
     
#####################################################################################################################
#                                                                                                                   #
#                                              Create DBC Files                                                     #
#                                                                                                                   #
#####################################################################################################################
   
def create_dataByCountry(mode):
    if mode == CS_Interpolated:
        FQName = SourceData_DIR + '\CSDataByCountry.xlsx'
    
    if mode == CS_Uninterpolated:
        FQName = SourceData_DIR + '\CSDataByCountry_uninterpolated.xlsx'
    
    countries = {}

    xlsx = pd.ExcelFile(FQName)

    GBModData = GB_get_db_json(os.environ[GB_SPECT_MOD_DATA_CONN_ENV], "globals", formatCountryFName(GBCountryListDBName, GBDatabaseVersion))

    for sheetName in xlsx.sheet_names:
        if sheetName not in ['DataByCountry_Countries', 'Regional_values']:
            sheet = xlsx.parse(sheetName, header=None)

            dataFirstRow = 7
            dataFinalRow = len(sheet.values) - 1

            dataStartCol = 7
            dataFinalCol = len(sheet.values[2]) - 1
            
            code = getVal(sheet, dataFirstRow, 0)
            name = getVal(sheet, dataFirstRow, 1)
            region = getVal(sheet, dataFirstRow, 3)
            
            log('Creating DBC record for ' + name)     

            ISO3_Alpha = -1
            for i in GBRange(0, len(GBModData)-1):
                if GBModData[i]['ISO3_Numeric'] == int(code):
                    ISO3_Alpha = GBModData[i]['ISO3_Alpha']  
            
            firstYear = int(sheet.values[dataFirstRow][2])
            finalYear = int(sheet.values[dataFinalRow][2])

            tagRecords = []
            
            for col in GBRange(dataStartCol, dataFinalCol):
                cellVal = getVal(sheet, 0, col)
                if '<' in cellVal:
                    tagRecords.append({"tag" : cellVal, "firstCol" : col})
                    
            finalTagIndex = len(tagRecords) - 1
            for i in GBRange(0, finalTagIndex - 1):
                tagRecords[i]["finalCol"] = tagRecords[i + 1]["firstCol"] - 1      
            tagRecords[finalTagIndex]["finalCol"] = dataFinalCol            

            for tagRecord in tagRecords:
                
                tag = tagRecord["tag"]
                firstCol = tagRecord["firstCol"]  
                finalCol = tagRecord["finalCol"]             
                    
                key1Row = 2
                key2Row = 3

                if tag in [TG_DeathsByCause, 
                           TG_AdolDeathByCause,
                           TG_MatDeathByCause, 
                           TG_SBCauses, 
                           TG_Coverage, 
                           TG_ImpactBirthOutcomesOnMort, 
                           TG_HerdEff]:                        
                    key1Row = 1
                    key2Row = 2

                data = {}  
                sources = {}

                key1 = ''
                key2 = ''

                for col in GBRange(firstCol, finalCol):
                    
                    values = np.zeros(dataFinalRow - dataFirstRow + 1)        
                
                    i = 0
                    nonZeroValueFound = False
                    for row in GBRange(dataFirstRow, dataFinalRow):
                        value = getFloat(sheet, row, col)
                        values[i] = value
                        if not float(value) == 0.0:
                            nonZeroValueFound = True
                        i += 1
                    
                    values = values.tolist()
                    if not nonZeroValueFound:
                        values = CS_TG_Zeros
                    
                    key1 = get_DBC_Key(sheet, key1Row, col, key1)
                    
                    if not key1 == '':                        
                        key2 = get_DBC_Key(sheet, key2Row, col)  

                        if not(key1 in data):
                            data[key1] = {}
                            
                            if tag in [TG_NutritionalDeficiencies]:
                                data[key1] = {'mstID' : getVal(sheet, 5, col)}                                      
                            
                            if tag in [TG_DeathsByCause, 
                                       TG_MatDeathByCause, 
                                       TG_SBCauses, 
                                       TG_Coverage, 
                                       TG_HerdEff]:
                                data[key1] = {'mstID' : getVal(sheet, 3, col)}                                      
                        
                        if not key2 == '':
                            if not(key2 in data[key1]):
                                data[key1][key2] = values
                                if tag in [TG_AdolDeathByCause, TG_ImpactBirthOutcomesOnMort]:
                                    data[key1][key2] = {
                                        'mstID' : getVal(sheet, 3, col),
                                        'values' : values
                                    }

                        else:
                            if 'mstID' in data[key1]:
                                data[key1]['values'] = values
                            else:
                                data[key1] = values
                    
                    else:
                        data = values                     
                    
                    ID = getVal(sheet, 5, col)
                    source = getVal(sheet, 6, col)

                    if not (ID == '') and not (source == '') and not (ID in sources):
                        sources[ID] = source                         
                
                if not sources == {}:                        
                    if type(data) in [str, list]:
                        data = {'values' : data}
                    data['sources'] = sources

                if not(name in countries):
                    countries[name] = {
                        'ISO3_Alpha' : ISO3_Alpha,
                        'firstYear' : firstYear,
                        'finalYear' : finalYear,
                        'Region' : region
                    }
                
                countries[name][tag] = data
    
    if mode == CS_Interpolated:
        createCountryFiles(DataByCountry, countries)
    
    if mode == CS_Uninterpolated:
        createCountryFiles(DBC_DataPoints, countries)

#####################################################################################################################
#                                                                                                                   #
#                                             Create Regional Files                                                 #
#                                                                                                                   #
#####################################################################################################################

def create_regionalValues():
    FQName = SourceData_DIR + '\CSDataByCountry.xlsx'
    
    regions = {}

    xlsx = pd.ExcelFile(FQName)

    for sheetName in xlsx.sheet_names:
        if sheetName in ['Regional_values']:
            sheet = xlsx.parse(sheetName, header=None)

            dataFirstRow = 6
            dataFinalRow = len(sheet.values) - 2

            dataStartCol = 7
            dataFinalCol = len(sheet.values[2]) - 1
            
            tagRecords = []
                        
            for col in GBRange(dataStartCol, dataFinalCol):
                cellVal = getVal(sheet, 0, col)
                if '<' in cellVal:
                    tagRecords.append({"tag" : cellVal, "firstCol" : col})
                    
            finalTagIndex = len(tagRecords) - 1
            for i in GBRange(0, finalTagIndex - 1):
                tagRecords[i]["finalCol"] = tagRecords[i + 1]["firstCol"] - 1      
            tagRecords[finalTagIndex]["finalCol"] = dataFinalCol            

            for row in GBRange(dataFirstRow, dataFinalRow): 
                region = getVal(sheet, row, 3)            
                
                for tagRecord in tagRecords:
                    
                    tag = tagRecord["tag"]
                    firstCol = tagRecord["firstCol"]  
                    finalCol = tagRecord["finalCol"]             
                        
                    key1Row = 2
                    key2Row = 3

                    if tag in [TG_DeathsByCause, 
                            TG_MatDeathByCause, 
                            TG_SBCauses, 
                            TG_Coverage, 
                            TG_ImpactBirthOutcomesOnMort, 
                            TG_HerdEff]:                        
                        key1Row = 1
                        key2Row = 2

                    data = {}  
                    sources = {}

                    key1 = ''
                    key2 = ''

                    for col in GBRange(firstCol, finalCol):
                        
                        value = getFloat(sheet, row, col)
                    
                        key1 = get_DBC_Key(sheet, key1Row, col, key1)
                        
                        if not key1 == '':                        
                            key2 = get_DBC_Key(sheet, key2Row, col)

                            if not(key1 in data):
                                data[key1] = {}
                                
                                if tag in [TG_NutritionalDeficiencies]:
                                    data[key1] = {'mstID' : getVal(sheet, 5, col)}                                      
                                
                                if tag in [TG_DeathsByCause, 
                                        TG_MatDeathByCause, 
                                        TG_SBCauses, 
                                        TG_Coverage, 
                                        TG_HerdEff]:
                                    data[key1] = {'mstID' : getVal(sheet, 3, col)}                                      
                            
                            if not key2 == '':
                                if not(key2 in data[key1]):
                                    data[key1][key2] = value
                                    if tag in [TG_ImpactBirthOutcomesOnMort]:
                                        data[key1][key2] = {
                                            'mstID' : getVal(sheet, 3, col),
                                            'value' : value
                                        }

                            else:
                                if type(data[key1]) == dict and 'mstID' in data[key1]:
                                    data[key1]['value'] = value
                                else:
                                    data[key1] = value
                        
                        else:
                            data = value                     
                        
                        ID = getVal(sheet, 5, col)
                        source = getVal(sheet, dataFinalRow + 1, col)

                        if not (ID == '') and not (source == '') and not (ID in sources):
                            sources[ID] = source                         
                    
                    if not sources == {}:                        
                        if type(data) in [str, int]:
                            data = {'value' : data}
                        data['sources'] = sources

                    if not(region in regions):
                        regions[region] = {
                            'ISO3_Alpha' : region
                        }
                    
                    regions[region][tag] = data
    
    createCountryFiles(RegionData, regions)

#####################################################################################################################
#                                                                                                                   #
#                                              Create Subnational                                                   #
#                                                                                                                   #
#####################################################################################################################

def processSubnatData(GBModData, countries, regions, FName, key):
    xlsx = pd.ExcelFile(SourceData_DIR + '\Subnational/' + FName + '.xlsx')

    for sheetName in xlsx.sheet_names:     
        sheet = xlsx.parse(sheetName, header=None)

        dataFirstRow = 4
        dataFinalRow = len(sheet.values) - 1

        dataStartCol = 6
        dataFinalCol = len(sheet.values[2]) - 1
                    
        for row in GBRange(dataFirstRow, dataFinalRow):                            

            ISO3 = getVal(sheet, row, 0)
            level = getVal(sheet, row, 5)
            year = getVal(sheet, row, 3)
            source = getVal(sheet, row, 4)
            
            ISO3_Alpha = -1
            for i in GBRange(0, len(GBModData)-1):
                if GBModData[i]['ISO3_Numeric'] == int(ISO3):
                    ISO3_Alpha = GBModData[i]['ISO3_Alpha']               
            
            # Country stuff            
            
            if not(ISO3_Alpha in countries):
                countries[ISO3_Alpha] = {'ISO3_Alpha' : ISO3_Alpha}
            
            if not (level in countries[ISO3_Alpha]):
                countries[ISO3_Alpha][level] = {}

            if not (year in countries[ISO3_Alpha][level]):
                countries[ISO3_Alpha][level][year] = {}

            if not (source in countries[ISO3_Alpha][level][year]):
                countries[ISO3_Alpha][level][year][source] = {}            
            
            for col in GBRange(dataStartCol, dataFinalCol): 
                mstID =  getVal(sheet, 2, col)

                if not cellIsBlank(sheet, row, col):
                
                    if not (mstID in countries[ISO3_Alpha][level][year][source]):
                        countries[ISO3_Alpha][level][year][source][mstID] = {'name' : getVal(sheet, 3, col)}
                
                    if key == 'flag':
                        countries[ISO3_Alpha][level][year][source][mstID][key] = getVal(sheet, row, col)
            
                    if key == 'value':
                        countries[ISO3_Alpha][level][year][source][mstID][key] = getFloat(sheet, row, col)    

            # Region stuff

            if not(ISO3_Alpha in regions):
                regions[ISO3_Alpha] = []           
            
            foundLevel = False
            for l in GBRange(0, len(regions[ISO3_Alpha])-1):
                record = regions[ISO3_Alpha][l]
                if level == record['region']:
                    foundLevel = True
                                
            if not foundLevel:
                regions[ISO3_Alpha].append({'region' : level, 'surveys' : []})
                        
            for l in GBRange(0, len(regions[ISO3_Alpha])-1):
                record = regions[ISO3_Alpha][l]
                if level == record['region']:
                    foundSurvey = False
                    for s in GBRange(0, len(record['surveys'])-1):
                        survey = record['surveys'][s]
                        if source == survey['source'] and year == survey['year']:
                            foundSurvey = True
            
                    if not foundSurvey:
                        record['surveys'].append({'source' : source, 'year' : year})
            
def processPercPop(GBModData, countries, FName):
    xlsx = pd.ExcelFile(SourceData_DIR + '\Subnational/' + FName + '.xlsx')

    for sheetName in xlsx.sheet_names:     
        sheet = xlsx.parse(sheetName, header=None)

        dataFirstRow = 4
        dataFinalRow = len(sheet.values) - 1

        for row in GBRange(dataFirstRow, dataFinalRow):                            

            ISO3 = getVal(sheet, row, 0)
            level = getVal(sheet, row, 5)
            year = getVal(sheet, row, 3)
            
            ISO3_Alpha = -1
            for i in GBRange(0, len(GBModData)-1):
                if GBModData[i]['ISO3_Numeric'] == int(ISO3):
                    ISO3_Alpha = GBModData[i]['ISO3_Alpha']               
            
            if not(ISO3_Alpha in countries):
                countries[ISO3_Alpha] = {
                    'ISO3_Alpha' : getVal(sheet, row, 1)
                    }
            
            if not (level in countries[ISO3_Alpha]):
                countries[ISO3_Alpha][level] = {}

            if not (year in countries[ISO3_Alpha][level]):
                countries[ISO3_Alpha][level][year] = {}
            
            countries[ISO3_Alpha][level][year]['PercPop'] = getFloat(sheet, row, 6)

def create_SubnatData():
    countries = {}
    regions = {}
    
    GBModData = GB_get_db_json(os.environ[GB_SPECT_MOD_DATA_CONN_ENV], "globals", formatCountryFName(GBCountryListDBName, GBDatabaseVersion))

    processSubnatData(GBModData, countries, regions, 'CSSubnatDB', 'value')
    processSubnatData(GBModData, countries, regions, 'CSSubnatFlagDB', 'flag')
    processSubnatData(GBModData, countries, regions, 'CSSubnatUrbanRural', 'value')
    processSubnatData(GBModData, countries, regions, 'CSSubnatFlagUrbanRural', 'flag')
   
    for key, record in regions.items():
        for i in GBRange(0, len(record)-1):
            record[i]['surveys'] = sorted(record[i]['surveys'], key=lambda x: x['year'], reverse=True)

    processPercPop(GBModData, countries, 'CSSubnatPercPop')
    processPercPop(GBModData, countries, 'CSSubnatPercPopUrbanRural')

    trimDict(countries)
    createCountryFiles(SubnatData, countries)
    createSingleFile(SubnatMetaData, regions)      
    
#####################################################################################################################
#                                                                                                                   #
#                                          Create Missed Oportunities                                               #
#                                                                                                                   #
#####################################################################################################################

# def create_MissOpData():
#     xlsx = pd.ExcelFile(DIR + '\ModData\CSMissOpData.xlsx')

#     GBModData = getGBModDataDict()
    
#     countries = {}
    
#     for sheetName in xlsx.sheet_names:     
#         sheet = xlsx.parse(sheetName, header=None)
        
#         dateCreated = getVal(sheet, 0, 0)
#         UseInflation = getVal(sheet, 0, 5)
    
#         ISO3_Alpha = -1
#         for key, record in GBModData.items():
#             if record['ISO3'] == int(sheetName):
#                 ISO3_Alpha = record['ISO3_Alpha']          

#         dataFirstRow = 2
#         dataFinalRow = len(sheet.values) - 1
                
#         if dataFinalRow > 1:
        
#             dataStartCol = 0
#             dataFinalCol = len(sheet.values[2]) - 1
                        
#             for row in GBRange(dataFirstRow, dataFinalRow):                            
#                 for col in GBRange(dataStartCol, dataFinalCol):                            
#                     tag = getVal(sheet, 1, col)
#                     value = getVal(sheet, row, col)                
                    
#                     if tag == MO_InterventionTag: intervName = value
#                     if tag == MO_InterventionMstIDTag: intervMstID = value
#                     if tag == MO_DelivPointTag: delivPointName = value
#                     if tag == MO_DelivPointMstIDTag: delivPointMstID = value
#                     if tag == MO_DeathCauseTypeTag: deathCauseTypeName = value
#                     if tag == MO_DeathCauseTypeMstIDTag: deathCauseTypeMstID = value
#                     if tag == MO_DeathCauseTag: deathCauseName = value
#                     if tag == MO_DeathCauseMstIDTag: deathCauseMstID = value
#                     if tag == MO_LivesSavedTag: livesSaved = value
#                     if tag == MO_DeathsTag: deaths = value
#                     if tag == MO_TotDeathsTag: totalDeaths = value
#                     if tag == MO_StuntingAvertedTag: stuntAverted = value
#                     if tag == MO_InterventionCostTag: intervCost = value
#                     if tag == MO_BaselineCoverageTag: baselineCov = value
#                     if tag == MO_ScaleupCoverageTag: scaleupCov = value

#                 def doThing33(value):
#                     if not value == '':
#                         value = int(value)
#                     return value
                
#                 def doThing34(value):
#                     if not value == '':
#                         value = float(value)
#                     return value
                    
#                 if not intervMstID == '105':
#                     intervMstID = intervMstID[4:7]
                
#                 intervMstID = doThing33(intervMstID)
#                 delivPointMstID = doThing33(delivPointMstID)
#                 deathCauseTypeMstID = doThing33(deathCauseTypeMstID)
#                 deathCauseMstID = doThing33(deathCauseMstID)
#                 deaths = doThing33(deaths)
#                 totalDeaths = doThing33(totalDeaths)
#                 stuntAverted = doThing33(stuntAverted)
                
#                 livesSaved = doThing34(livesSaved)
#                 intervCost = doThing34(intervCost)
#                 baselineCov = doThing34(baselineCov)
#                 scaleupCov = doThing34(scaleupCov)
                
#                 if delivPointMstID == 7: 
#                     delivPointMstID = 1
#                     delivPointName = 'Periconceptual'
                    
#                 ref = countries
                
#                 def doThing500(ref, key, name = ''):
#                     if not key in ref:
#                         ref[key] = {}
#                         if not name == '': 
#                             ref[key]['name'] = name

#                     return ref[key]
                
#                 def doThing3(key, value):
#                     if value == '':
#                         value = 0
#                     ref[key] = value

#                 ref = doThing500(ref, ISO3_Alpha)
#                 doThing3('ISO3_Alpha', ISO3_Alpha)
#                 doThing3('dateCreated', dateCreated)

#                 if not delivPointMstID == 0:
#                     ref = doThing500(ref, 'LiST intervention delivery points')
#                     ref = doThing500(ref, delivPointMstID, delivPointName)
#                     ref = doThing500(ref, 'Interventions')
#                     ref = doThing500(ref, intervMstID, intervName)
                    
#                     doThing3('intervCost', intervCost)
#                     doThing3('stuntAverted', stuntAverted)                
                
#                 else:
#                     ref = doThing500(ref, intervName)                       
                
#                 doThing3('baselineCov', baselineCov)
#                 doThing3('scaleupCov', scaleupCov)
                
#                 ref = doThing500(ref, 'Outcomes')
#                 ref = doThing500(ref, deathCauseTypeMstID, deathCauseTypeName)

#                 if not delivPointMstID == 0:
#                     doThing3('totalDeaths', totalDeaths)

#                 if not deathCauseMstID == 0:
#                     ref = doThing500(ref, 'Death causes')
#                     ref = doThing500(ref, deathCauseMstID, deathCauseName)
                
#                 if not delivPointMstID == 0:
#                     doThing3('deaths', deaths)
                
#                 doThing3('livesSaved', livesSaved)

#     createCountryFiles(MissOpData, countries)

def create_MissOpData():
    
    # ========================================================================
    #                             
    # ========================================================================
       
    connection = os.environ[GB_SPECT_MOD_DATA_CONN_ENV]       
    FName = IV_INTERVENTION_DB_NAME + '_' + IV_CS_INTERVENTION_DB_CURR_VERSION + '.JSON'       
    IV_DB = {}
    if GB_file_exists(connection, 'list', FName):
        IV_DB = GB_get_db_json(connection, 'list', FName)    
    
    IVInfo = {}

    for i in GBRange(0, len(IV_DB)-1):        
        record = IV_DB[i]        
        key = str(record[ivdbk.IV_MST_ID_KEY_IDB])
        IVInfo[key] = {}                
        for key2 in [ivdbk.IV_STRING_CONSTANT_KEY_IDB, ivdbk.IV_NUTRITION_CS_KEY_IDB, ivdbk.IV_BIRTH_OUTCOME_CS_KEY_IDB]:
            IVInfo[key][key2] = IV_DB[i][key2]  
                 
    # ========================================================================
    #                             
    # ========================================================================
       
    xlsx = pd.ExcelFile(SourceData_DIR + '\CSMissOpData.xlsx')

    GBModData = GB_get_db_json(os.environ[GB_SPECT_MOD_DATA_CONN_ENV], "globals", formatCountryFName(GBCountryListDBName, GBDatabaseVersion))
    
    countries = {}
    
    for sheetName in xlsx.sheet_names:     
        sheet = xlsx.parse(sheetName, header=None)
        
        monthCreated = getVal(sheet, 0, 1)
        yearCreated = getVal(sheet, 0, 2)
        UseInflation = getVal(sheet, 0, 5)        

        ISO3_Alpha = -1
        for i in GBRange(0, len(GBModData)-1):
            if GBModData[i]['ISO3_Numeric'] == int(sheetName):
                ISO3_Alpha = GBModData[i]['ISO3_Alpha']               
        
        countries[ISO3_Alpha] = {
            'ISO3_Alpha' : ISO3_Alpha,
            'monthCreated' : monthCreated,
            'yearCreated' : yearCreated,
            'UseInflation' : UseInflation,
            'data' : []
            }
        
        dataFirstRow = 2
        dataFinalRow = len(sheet.values) - 1
                
        if dataFinalRow > 1:
        
            dataStartCol = 0
            dataFinalCol = len(sheet.values[2]) - 1
                        
            for row in GBRange(dataFirstRow, dataFinalRow):                            
                for col in GBRange(dataStartCol, dataFinalCol):                            
                    tag = getVal(sheet, 1, col)
                    value = getVal(sheet, row, col)                
                    
                    if tag == MO_InterventionTag: intervName = value
                    if tag == MO_InterventionMstIDTag: intervMstID = value
                    if tag == MO_DelivPointMstIDTag: delivPointMstID = value
                    if tag == MO_DeathCauseTypeMstIDTag: deathCauseTypeMstID = value
                    if tag == MO_DeathCauseMstIDTag: deathCauseMstID = value
                    if tag == MO_LivesSavedTag: livesSaved = value
                    if tag == MO_DeathsTag: deaths = value
                    if tag == MO_TotDeathsTag: totalDeaths = value
                    if tag == MO_StuntingAvertedTag: stuntAverted = value
                    if tag == MO_StuntingAvertedIDTag: stuntAvertedID = value
                    if tag == MO_InterventionCostTag: intervCost = value
                    if tag == MO_BOPreTermSGATag: BOPreTermSGA = value
                    if tag == MO_BOPreTermAGATag: BOPreTermAGA = value
                    if tag == MO_BOTermSGATag: BOTermSGA = value
                    if tag == MO_BOLowBirthWeightTag: BOLowBirthWeight = value
                    if tag == MO_BaselineCoverageTag: baselineCov = value
                    if tag == MO_ScaleupCoverageTag: scaleupCov = value

                def parseInt(value):
                    if not value == '':
                        value = int(value)
                    return value
                
                def parseFloat(value):
                    if not value == '':
                        value = float(value)
                    return value
                    
                stringConst = ''                  
                isNutritionIV = 0
                isBirthOutcomeIV = 0
              
                if intervMstID == '105':
                    intervMstID = str(CS_MstCPR)     
                    intervName = 'Reducing unmet need for family planning'  
                    stringConst = 'GB_stReducUnmetNeed'
                    isNutritionIV = 1
                else:
                    intervMstID = intervMstID[4:7]
                
                if intervMstID == '017':
                    intervMstID = str(CS_MstBFPromotion)          
                    intervName = 'Breastfeeding promotion'  
                    stringConst = 'GB_stBFPromo'
                    isNutritionIV = 1
                
                intervMstID = parseInt(intervMstID)
                delivPointMstID = parseInt(delivPointMstID)
                deathCauseTypeMstID = parseInt(deathCauseTypeMstID)
                deathCauseMstID = parseInt(deathCauseMstID)
                deaths = parseInt(deaths)
                totalDeaths = parseInt(totalDeaths)
                stuntAverted = parseInt(stuntAverted)
                stuntAvertedID = parseInt(stuntAvertedID)
                
                livesSaved = parseFloat(livesSaved)
                intervCost = parseFloat(intervCost)
                BOPreTermSGA = parseFloat(BOPreTermSGA)
                BOPreTermAGA = parseFloat(BOPreTermAGA)
                BOTermSGA = parseFloat(BOTermSGA)
                BOLowBirthWeight = parseFloat(BOLowBirthWeight)
                baselineCov = parseFloat(baselineCov)
                scaleupCov = parseFloat(scaleupCov)
                
                if delivPointMstID == 7: 
                    delivPointMstID = 1
                    
                if str(intervMstID) in IVInfo:
                    stringConst = IVInfo[str(intervMstID)][ivdbk.IV_STRING_CONSTANT_KEY_IDB]
                    isNutritionIV = IVInfo[str(intervMstID)][ivdbk.IV_NUTRITION_CS_KEY_IDB]
                    isBirthOutcomeIV = IVInfo[str(intervMstID)][ivdbk.IV_BIRTH_OUTCOME_CS_KEY_IDB]
                
                countries[ISO3_Alpha]['data'].append({
                    'ClassType' : 'MO_TDataObj',
                    'Outcome' : deathCauseTypeMstID,
                    "CauseOfDeath" : deathCauseMstID,
                    "DeathsAverted" : livesSaved,
                    "Deaths" : deaths,
                    "TotDeaths" : totalDeaths,
                    "name" : intervName,
                    "stringConst" : stringConst,
                    "IntervMstID" : intervMstID,
                    "delivPoint" : delivPointMstID,
                    "baseCov" : baselineCov,
                    "scaleUpCov" : scaleupCov,
                    "stuntingAverted" : stuntAverted,
                    "stuntingAvertedID" : stuntAvertedID,
                    "IVCost" : intervCost,
                    "BOPreTermSGA" : BOPreTermSGA,
                    "BOPreTermAGA" : BOPreTermAGA,
                    "BOTermSGA" : BOTermSGA,
                    "BOLowBirthWeight" : BOLowBirthWeight,
                    "isNutritionIV" : isNutritionIV,
                    "isBirthOutcomeIV" : isBirthOutcomeIV
                })

    createCountryFiles(MissOpData, countries)