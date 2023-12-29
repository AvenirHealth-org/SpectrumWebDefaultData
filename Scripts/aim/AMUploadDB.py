import os
import pandas as pd
import numpy as np
import ujson
from AvenirCommon.Database import GB_upload_json, GB_get_db_json
from AvenirCommon.Logger import log
from AvenirCommon.Util import formatCountryFName, GBRange, getTagRow, GBEqual
from DefaultData.DefaultDataUtil import *

from Tools.DefaultDataManager.GB.Upload.GBUploadModData import getGBModDataDict, getGBModDataDictByISO3
from AvenirCommon.Database import GB_upload_json, GB_get_db_json, GB_upload_file

from SpectrumCommon.Const.GB import *
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Modvars.AM.AMUtil import getARTCovSurveyDict

aim_json_path = os.getcwd() + '\\DefaultData\\JSONData\\aim\\moddata'
aim_json_country_path = aim_json_path + '\\' + country_dir


def addDataByCountryName(countryName, countries, dataName, data, subnatCode = 0):

    if not(countryName in countries):
        countries[countryName] = {}

    if not subnatCode in countries[countryName]:
        countries[countryName][subnatCode] = {}

    countries[countryName][subnatCode][dataName] = data

def addDataByCountryCode(countryCode, countries, dataName, data, subnatCode = 0):

    if not(countryCode in countries):
        countries[countryCode] = {}

    if not subnatCode in countries[countryCode]:
        countries[countryCode][subnatCode] = {}

    countries[countryCode][subnatCode][dataName] = data

def isValueByYearSheet(sheetName):
    return sheetName in [
        'ART50PlusPercentFemales', 
        'ART50PlusPercentMales', 
        'ART50PlusPercentTotal', 
        'HIV_15',
        'HIV_15_ART',
        'HIV_50',
        'HIV_50_ART',
    ]
    
def getValuesByYear(countries, sheet, sheetName, startRow = 1):
    startCol = 4
    endCol = len(sheet.values[0]) - 1
    startYear = int(sheet.values[0][startCol])
    endYear = int(sheet.values[0][endCol])

    for row in GBRange(startRow, len(sheet.values) - 1):
        countryCode = sheet.values[row][0]
        countryName = sheet.values[row][1]
        subnatCode = sheet.values[row][2]
        subnatName = sheet.values[row][3]

        values = np.zeros(endYear - startYear + 1)
        i = 0
        for col in GBRange(startCol, endCol):
            values[i] = sheet.values[row][col]
            i += 1
        
        data = {
            'startYear' : startYear,
            'endYear' : endYear,
            'values' : values.tolist()
        }

        addDataByCountryCode(countryCode, countries, sheetName, data, subnatCode)

def readRegions(countries, sheet, sheetName):
    
    for row in GBRange(1, len(sheet.values) - 1):
        countryCode = sheet.values[row][0]
        countryName = sheet.values[row][1]
        region = sheet.values[row][2]
        
        data = {
            'region' : region
        }

        addDataByCountryCode(countryCode, countries, sheetName, data)

def readPercPregAccessAntenatalCare(countries, sheet, sheetName):
    
    for row in GBRange(1, len(sheet.values) - 1):
        countryCode = sheet.values[row][4]
        countryName = sheet.values[row][0]
        value = sheet.values[row][2]
        year = sheet.values[row][3]
        
        data = {
            'value' : value,
            'year' : year,
        }

        addDataByCountryCode(countryCode, countries, sheetName, data)

def readMortalityByAge(countries, sheet, sheetName):
    
    Age0Col = 6
    Age4Col = 10
    Age5_9Col = 11
    Age75_79Col = 25
    Age80_84Col = 26
    Age95PlusCol = 29

    localCountries = {}
    for row in GBRange(1, len(sheet.values) - 1):
        countryCode = sheet.values[row][0]
        countryName = sheet.values[row][1]
        year = sheet.values[row][2]
        cause = sheet.values[row][3]
        sex = sheet.values[row][4]
        values = np.zeros(DP_A80_Up + 1)
        
        for a in GBRange(Age0Col, Age4Col):
            values[DP_A0_4] += 0 if pd.isna(sheet.values[row][a]) else sheet.values[row][a]
        
        age = DP_A5_9
        for a in GBRange(Age5_9Col, Age75_79Col):
            values[age] = 0 if pd.isna(sheet.values[row][a]) else sheet.values[row][a]
            age += 1
            
        for a in GBRange(Age80_84Col, Age95PlusCol):
            values[DP_A80_Up] += 0 if pd.isna(sheet.values[row][a]) else sheet.values[row][a]
        
        data = {
            'year' : year,
            'cause' : cause,
            'sex' : sex,
            'values' : values.tolist(),
        }
        
        if not (countryCode in localCountries):
            localCountries[countryCode] = []
            
        localCountries[countryCode].append(data)

    for countryCode in localCountries:
        addDataByCountryCode(countryCode, countries, sheetName, localCountries[countryCode])

def readDHSPrevalenceByAge(countries, sheet, sheetName):

    PointEstMaleCol   = 6
    LBoundMaleCol     = 19
    UBoundMaleCol     = 32
    WeightMaleCol     = 45
    PointEstFemaleCol = 58
    LBoundFemaleCol   = 71
    UBoundFemaleCol   = 84
    WeightFemaleCol   = 97

    localCountries = {}
    for row in GBRange(2, len(sheet.values) - 1):
        countryCode = sheet.values[row][0]
        subnatCode = sheet.values[row][1]
        countryName = sheet.values[row][2]
        surveyYear = sheet.values[row][4]
        surveyName = sheet.values[row][5]

        values = np.zeros((GB_Female + 1, DP_WeightedSampleSize + 1, DP_A55_59 + 1))
        col = 0
        for a in GBRange(DP_A0_4, DP_A55_59): 
            values[GB_Male][DP_Percent][a] = sheet.values[row][PointEstMaleCol + col]
            values[GB_Male][DP_LowerBound][a] = sheet.values[row][LBoundMaleCol + col]
            values[GB_Male][DP_UpperBound][a] = sheet.values[row][UBoundMaleCol + col]
            values[GB_Male][DP_WeightedSampleSize][a] = sheet.values[row][WeightMaleCol + col]
            values[GB_Female][DP_Percent][a] = sheet.values[row][PointEstFemaleCol + col]
            values[GB_Female][DP_LowerBound][a] = sheet.values[row][LBoundFemaleCol + col]
            values[GB_Female][DP_UpperBound][a] = sheet.values[row][UBoundFemaleCol + col]
            values[GB_Female][DP_WeightedSampleSize][a] = sheet.values[row][WeightFemaleCol + col]
            col += 1

        data = {
            'surveyYear' : surveyYear,
            'surveyName' : surveyName,
            'values' : values.tolist(),
        }

        if not (countryCode in localCountries):
            localCountries[countryCode] = {}

        if not subnatCode in localCountries[countryCode]:
            localCountries[countryCode][subnatCode] = []
            
        localCountries[countryCode][subnatCode].append(data)

    for countryCode in localCountries:
        for subnatCode in localCountries[countryCode]:
            addDataByCountryCode(countryCode, countries, sheetName, localCountries[countryCode][subnatCode], subnatCode)


def getValuesNotByYear(countries, sheet, sheetName, headerRow = 0, startRow = 1):
    startCol = 4 
    endCol = len(sheet.values[2]) - 1

    endRow = len(sheet.values) - 1

    for row in GBRange(startRow, endRow):
        countryCode = sheet.values[row][0]
        countryName = sheet.values[row][1]
        subnatCode = sheet.values[row][2]
        subnatCode = 0 if pd.isna(subnatCode) else subnatCode 
      
        data = {
            # 'countryName' : countryName,
            # 'countryCode' : countryCode,
            # 'subnatCode' : subnatCode,
        }

        for col in GBRange(startCol, endCol):
            dataName = 'value' if pd.isna(sheet.values[headerRow][col]) else str(sheet.values[headerRow][col])
            # dataName = str(sheet.values[headerRow][col])
            # dataName = 'value' if dataName in ['', GB_Nan] else dataName    
            #   
            data[dataName] = sheet.values[row][col]

        addDataByCountryCode(countryCode, countries, sheetName, data, subnatCode)

def getValuesNotByYearNoSubnatCols(countries, sheet, sheetName):
    
    headerRow = 0
    startRow = 1
    endRow = len(sheet.values) - 1

    startCol = 2 
    endCol = len(sheet.values[headerRow]) - 1

    subnatCode = 0

    for row in GBRange(startRow, endRow):
        countryCode = sheet.values[row][0]
        countryName = sheet.values[row][1]
      
        data = {
        }

        for col in GBRange(startCol, endCol):
            dataName = 'value' if pd.isna(sheet.values[headerRow][col]) else str(sheet.values[headerRow][col])
            # dataName = str(sheet.values[headerRow][col])
            # dataName = 'value' if dataName in ['', GB_Nan] else dataName      
            data[dataName] = sheet.values[row][col]

        addDataByCountryCode(countryCode, countries, sheetName, data, subnatCode)

def readInfantFeedingData(countries, sheet, sheetName):

    localCountries = {}
    subnatCode = 0
    for row in GBRange(1, len(sheet.values) - 1):
        countryCode = sheet.values[row][0]
        countryName = sheet.values[row][1]
        year = sheet.values[row][2]

        values = np.zeros(DP_InfantFeedingMths + 1)

        col = 3
        for m in GBRange(1, DP_InfantFeedingMths):
          values[m] = sheet.values[row][col]
          col += 1

        data = {
            'year' : year,
            'values' : values.tolist(),
        }

        if not (countryCode in localCountries):
            localCountries[countryCode] = {}

        if not subnatCode in localCountries[countryCode]:
            localCountries[countryCode][subnatCode] = []
            
        localCountries[countryCode][subnatCode].append(data)

    for countryName in localCountries:
        for subnatCode in localCountries[countryCode]:
            addDataByCountryCode(countryCode, countries, sheetName, localCountries[countryCode][subnatCode], subnatCode)

def readInfantFeedingModel(countries, AMModDataGlobal, sheet, sheetName):

#   // country table
    col_isocode = 1
    col_cregion = 2
    col_bgn     = 3
    col_med     = 4
    col_shp     = 5

    localCountries = {}
    subnatCode = 0
    
    for row in GBRange(1, len(sheet.values) - 1):
        countryName = sheet.values[row][0]
        countryCode = sheet.values[row][1]
        data = {
            'region' : sheet.values[row][2],
            'bgn' : sheet.values[row][col_bgn],
            'med' : sheet.values[row][col_med],
            'shp' : sheet.values[row][col_shp],
        }

        if not (countryCode in localCountries):
            localCountries[countryCode] = {}

        if not subnatCode in localCountries[countryCode]:
            localCountries[countryCode][subnatCode] = []
            
        localCountries[countryCode][subnatCode].append(data)

    for countryCode in localCountries:
        for subnatCode in localCountries[countryCode]:
            addDataByCountryCode(countryCode, countries, sheetName, localCountries[countryCode][subnatCode], subnatCode)


#   // region table
    col_rregion  =  7
    col_bgn_time =  8
    col_bgn_hiv  =  9
    col_bgn_both = 10
    col_med_time = 11
    col_med_hiv  = 12
    col_med_both = 13
    col_shp_time = 14
    col_year_base = 15
    col_year_start = 16
    col_year_final = 17

    values = {}
    for row in GBRange(1, 4):
        data = {}
        for col in GBRange(col_bgn_time, col_year_final):
            data[sheet.values[0][col]] = sheet.values[row][col]
        values[sheet.values[row][col_rregion]] = data

    AMModDataGlobal[sheetName] = values


def readFRRbyLocation(countries, sheet, sheetName):
    headerRow = 1
    startRow = 2
    endRow = len(sheet.values) - 1

    startCol = 2 
    endCol = len(sheet.values[headerRow]) - 1

    subnatCode = 0

    for row in GBRange(startRow, endRow):
        countryCode = sheet.values[row][1]
        countryName = sheet.values[row][0]
      
        data = {}

        for col in GBRange(startCol, endCol):
            dataName = 'value' if pd.isna(sheet.values[headerRow][col]) else str(sheet.values[headerRow][col])
            # dataName = str(sheet.values[headerRow][col])
            # dataName = 'value' if dataName in ['', GB_Nan] else dataName      
            data[dataName] = sheet.values[row][col]

        addDataByCountryCode(countryCode, countries, sheetName, data, subnatCode)

def readChildARTDistByRegion(AMModDataGlobal, sheet, sheetName):
    startYear = 2004
    endYear = 2020
    startAge = 0
    endAge = 14

    values = np.zeros(DP_MaxNumRegions, dtype = list)

    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            row += 1
            yearVals = {}
            for year in GBRange(startYear, endYear):
                yearVals[str(year)] = np.zeros(endAge + 1).tolist()
                col = 1
                for age in GBRange(startAge, endAge):
                    yearVals[str(year)][age] = sheet.values[row][col]
                    col += 1
                row += 1
            values[DP_GlobalRegions[region]] = yearVals
                
    AMModDataGlobal[sheetName] = values.tolist()

def readChildMortCD4CountARTByRegion(AMModDataGlobal, sheet, sheetName):

    ChildMortByCD4WithART0to6 = np.zeros(DP_MaxNumRegions, dtype = list)
    ChildMortByCD4WithART7to12 = np.zeros(DP_MaxNumRegions, dtype = list)
    ChildMortByCD4WithARTGT12 = np.zeros(DP_MaxNumRegions, dtype = list)

    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            ART1T6M_row = row + 4
            ART7T12M_row = row + 11
            ARTGT12M_row = row + 18

            ART1T6M_values = np.zeros((GB_Female + 1, DP_A10t14 + 1, DP_CD4_Ped_LT200 + 1))
            ART7T12M_values = np.zeros((GB_Female + 1, DP_A10t14 + 1, DP_CD4_Ped_LT200 + 1))
            ARTGT12M_values = np.zeros((GB_Female + 1, DP_A10t14 + 1, DP_CD4_Ped_LT200 + 1))
            for c in GBRange(DP_CD4_Ped_GT1000, DP_CD4_Ped_LT200):
                col = 1
                for a in GBRange(DP_A5t9, DP_A10t14):
                    ART1T6M_values[GB_Male][a][c] = sheet.values[ART1T6M_row][col]
                    ART1T6M_values[GB_Female][a][c] = sheet.values[ART1T6M_row][col + 2]

                    ART7T12M_values[GB_Male][a][c] = sheet.values[ART7T12M_row][col]
                    ART7T12M_values[GB_Female][a][c] = sheet.values[ART7T12M_row][col + 2]

                    ARTGT12M_values[GB_Male][a][c] = sheet.values[ARTGT12M_row][col]
                    ARTGT12M_values[GB_Female][a][c] = sheet.values[ARTGT12M_row][col + 2]

                    col += 1
                ART1T6M_row += 1
                ART7T12M_row += 1
                ARTGT12M_row += 1

            ChildMortByCD4WithART0to6[DP_GlobalRegions[region]] = ART1T6M_values.tolist()
            ChildMortByCD4WithART7to12[DP_GlobalRegions[region]] = ART7T12M_values.tolist()
            ChildMortByCD4WithARTGT12[DP_GlobalRegions[region]] = ARTGT12M_values.tolist()
    
    AMModDataGlobal['ChildMortByCD4WithART0to6Count'] = ChildMortByCD4WithART0to6.tolist()
    AMModDataGlobal['ChildMortByCD4WithART7to12Count'] = ChildMortByCD4WithART7to12.tolist()
    AMModDataGlobal['ChildMortByCD4WithARTGT12Count'] = ChildMortByCD4WithARTGT12.tolist()

def readChildMortCD4PercARTByRegion(AMModDataGlobal, sheet, sheetName):

    ChildMortByCD4WithART0to6 = np.zeros(DP_MaxNumRegions, dtype = list)
    ChildMortByCD4WithART7to12 = np.zeros(DP_MaxNumRegions, dtype = list)
    ChildMortByCD4WithARTGT12 = np.zeros(DP_MaxNumRegions, dtype = list)

    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            ART1T6M_row = row + 4
            ART7T12M_row = row + 12
            ARTGT12M_row = row + 20

            ART1T6M_values = np.zeros((GB_Female + 1, DP_A3t4 + 1, DP_CD4_Per_LT5 + 1))
            ART7T12M_values = np.zeros((GB_Female + 1, DP_A3t4 + 1, DP_CD4_Per_LT5 + 1))
            ARTGT12M_values = np.zeros((GB_Female + 1, DP_A3t4 + 1, DP_CD4_Per_LT5 + 1))
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
                col = 1
                for a in GBRange(DP_A0, DP_A3t4):
                    ART1T6M_values[GB_Male][a][c] = sheet.values[ART1T6M_row][col]
                    ART1T6M_values[GB_Female][a][c] = sheet.values[ART1T6M_row][col + 3]

                    ART7T12M_values[GB_Male][a][c] = sheet.values[ART7T12M_row][col]
                    ART7T12M_values[GB_Female][a][c] = sheet.values[ART7T12M_row][col + 3]

                    ARTGT12M_values[GB_Male][a][c] = sheet.values[ARTGT12M_row][col]
                    ARTGT12M_values[GB_Female][a][c] = sheet.values[ARTGT12M_row][col + 3]

                    col += 1
                ART1T6M_row += 1
                ART7T12M_row += 1
                ARTGT12M_row += 1

            ChildMortByCD4WithART0to6[DP_GlobalRegions[region]] = ART1T6M_values.tolist()
            ChildMortByCD4WithART7to12[DP_GlobalRegions[region]] = ART7T12M_values.tolist()
            ChildMortByCD4WithARTGT12[DP_GlobalRegions[region]] = ARTGT12M_values.tolist()
    
    AMModDataGlobal['ChildMortByCD4WithART0to6Perc'] = ChildMortByCD4WithART0to6.tolist()
    AMModDataGlobal['ChildMortByCD4WithART7to12Perc'] = ChildMortByCD4WithART7to12.tolist()
    AMModDataGlobal['ChildMortByCD4WithARTGT12Perc'] = ChildMortByCD4WithARTGT12.tolist()

def readMortalityNoARTByRegion(AMModDataGlobal, sheet, sheetName):
    
    MortalityNoART = np.zeros(DP_MaxNumRegions, dtype = list)

    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            row = row + 3

            values = np.zeros((GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_LT50 + 1))
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                col = 1
                for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
                    values[GB_Male][a][c] = sheet.values[row][col]
                    values[GB_Female][a][c] = sheet.values[row][col + 4]

                    col += 1
                row += 1

            MortalityNoART[DP_GlobalRegions[region]] = values.tolist()
    
    AMModDataGlobal[sheetName] = MortalityNoART.tolist()
    
def readMortalityWithARTByRegion(AMModDataGlobal, sheet, sheetName):

    MortByCD4WithART0to6 = np.zeros(DP_MaxNumRegions, dtype = list)
    MortByCD4WithART7to12 = np.zeros(DP_MaxNumRegions, dtype = list)
    MortByCD4WithARTGT12 = np.zeros(DP_MaxNumRegions, dtype = list)

    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            ART1T6M_row = row + 4
            ART7T12M_row = row + 12
            ARTGT12M_row = row + 20

            ART1T6M_values = np.zeros((GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_LT50 + 1))
            ART7T12M_values = np.zeros((GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_LT50 + 1))
            ARTGT12M_values = np.zeros((GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_LT50 + 1))
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                col = 1
                for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
                    ART1T6M_values[GB_Male][a][c] = sheet.values[ART1T6M_row][col]
                    ART1T6M_values[GB_Female][a][c] = sheet.values[ART1T6M_row][col + 4]

                    ART7T12M_values[GB_Male][a][c] = sheet.values[ART7T12M_row][col]
                    ART7T12M_values[GB_Female][a][c] = sheet.values[ART7T12M_row][col + 4]

                    ARTGT12M_values[GB_Male][a][c] = sheet.values[ARTGT12M_row][col]
                    ARTGT12M_values[GB_Female][a][c] = sheet.values[ARTGT12M_row][col + 4]

                    col += 1
                ART1T6M_row += 1
                ART7T12M_row += 1
                ARTGT12M_row += 1

            MortByCD4WithART0to6[DP_GlobalRegions[region]] = ART1T6M_values.tolist()
            MortByCD4WithART7to12[DP_GlobalRegions[region]] = ART7T12M_values.tolist()
            MortByCD4WithARTGT12[DP_GlobalRegions[region]] = ARTGT12M_values.tolist()
    
    AMModDataGlobal['AdultMortByCD4WithART0to6'] = MortByCD4WithART0to6.tolist()
    AMModDataGlobal['AdultMortByCD4WithART7to12'] = MortByCD4WithART7to12.tolist()
    AMModDataGlobal['AdultMortByCD4WithARTGT12'] = MortByCD4WithARTGT12.tolist()

def readARTmortalityTrends(AMModDataGlobal, sheet, sheetName): 
    startCol = 2
    endCol = len(sheet.values[0]) - 1
    startYear = int(sheet.values[0][startCol])
    endYear = int(sheet.values[0][endCol])

    ARTmortalityTrends = np.zeros(DP_MaxNumRegions, dtype = list)

    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            values = np.zeros((DP_MortRates_GT12Mo + 1, endYear - startYear + 1))
            
            i = 0
            for col in GBRange(startCol, endCol):
                values[DP_MortRates_LT12Mo][i] = sheet.values[row][col]
                values[DP_MortRates_GT12Mo][i] = sheet.values[row + 1][col]
                i += 1
         
            data = {
                'startYear' : startYear,
                'endYear' : endYear,
                'values' : values.tolist()
            }

            ARTmortalityTrends[DP_GlobalRegions[region]] = data
    
    AMModDataGlobal[sheetName] = ARTmortalityTrends.tolist()


def readAgeRatioPatternsIncidence(AMModDataGlobal, sheet, sheetName):
    IncidenceStartRow = 2
    SexRatioStartRow = 17
    AnnualChangeRow  = 48

    values = np.zeros((DP_Concentrated2_Patt + 1, GB_Female + 1, DP_A75_Up + 1))

    row = IncidenceStartRow
    for a in GBRange(DP_A15_19, DP_A75_Up):
        col = 1
        for id in GBRange(DP_Generalized_Patt, DP_Concentrated2_Patt):
            for s in GBRange(GB_Male, GB_Female):
                values[id][s][a] = sheet.values[row][col]
                col += 1
        row += 1

    AMModDataGlobal['AgeRatioPatternsIncidence'] = values.tolist()

    values = np.zeros((DP_Concentrated2_Patt + 1, DP_AgeRatioMaxYear + 1))

    row = SexRatioStartRow
    for t in GBRange(DP_AgeRatioMinYear, DP_AgeRatioMaxYear):
        col = 1
        for id in GBRange(DP_Generalized_Patt, DP_Concentrated2_Patt):
            values[id][t] = sheet.values[row][col]
            col += 1
        row += 1

        data = {
            'startYear' : DP_AgeRatioMinYear,
            'endYear' : DP_AgeRatioMaxYear,
            'values' : values.tolist()
        }

    AMModDataGlobal['AgeRatioPatternsSexRatio'] = values.tolist()

    AMModDataGlobal['AgeRatioPatternsAnnualChange'] = sheet.values[AnnualChangeRow][1]


def readPediatricTransitionParameters(AMModDataGlobal, sheet, sheetName):
    
    perValues = np.zeros((GB_Female + 1, DP_A3t4 + 1, DP_CD4_Per_5_10 + 1))   
    row = 3
    for sd in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_5_10):
        col = 1
        for s in GBRange(GB_Male, GB_Female):
            for a in GBRange(DP_A0t2, DP_A3t4):
                perValues[s][a][sd] = sheet.values[row][col]
            col += 1
        row += 1
    AMModDataGlobal['PedTransParamsPercent'] = perValues.tolist()

    countValues = np.zeros((GB_Female + 1, DP_CD4_Ped_200_349 + 1))    
    row = 14
    for sd in GBRange(DP_CD4_Ped_GT1000, DP_CD4_Ped_200_349):
        col = 1
        for s in GBRange(GB_Male, GB_Female):
            countValues[s][sd] = sheet.values[row][col]
            col += 1
        row += 1
    AMModDataGlobal['PedTransParamsCount'] = countValues.tolist()
    
def readChildWeightBands(AMModDataGlobal, sheet, sheetName):

    values = np.zeros((GB_Female + 1, DP_A14 + 1, DP_Kgs_35_Plus + 1)) 
    
    row = 5
    for a in GBRange(DP_A6Months, DP_A14):
        col = 1
        for b in GBRange(DP_Kgs_3_5pt9, DP_Kgs_35_Plus):
            values[GB_Male][a][b] = sheet.values[row][col]
            col += 1
        row += 1

    row = 24
    for a in GBRange(DP_A6Months, DP_A14):
        col = 1
        for b in GBRange(DP_Kgs_3_5pt9, DP_Kgs_35_Plus):
            values[GB_Female][a][b] = sheet.values[row][col]
            col += 1
        row += 1

    AMModDataGlobal[sheetName] = values.tolist()


def readFertilityRatio(AMModDataGlobal, sheet, sheetName):

    values = np.zeros((DP_MaxNumRegions, DP_A45_49 + 1))
    
    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            col = 1
            for age in GBRange(DP_A15_19, DP_A45_49):
                values[DP_GlobalRegions[region]][age] = sheet.values[row][col]
                col += 1

    AMModDataGlobal[sheetName] = values.tolist()
    
def readFRRByCD4Category(AMModDataGlobal, sheet, sheetName):

    values = np.zeros((DP_MaxNumRegions, DP_CD4_LT50 + 1))
    
    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            col = 1
            for age in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                values[DP_GlobalRegions[region]][age] = sheet.values[row][col]
                col += 1

    AMModDataGlobal[sheetName] = values.tolist()

def readRatioWomenOnART(AMModDataGlobal, sheet, sheetName):

    values = np.zeros((DP_MaxNumRegions, DP_A45_49 + 1))
    
    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            col = 1
            for age in GBRange(DP_A15_19, DP_A45_49):
                values[DP_GlobalRegions[region]][age] = sheet.values[row][col]
                col += 1

    AMModDataGlobal[sheetName] = values.tolist()
    
def readFRR15_19Coefs(AMModDataGlobal, sheet, sheetName):

    values = np.zeros(DP_MaxNumRegions, dtype = list)

    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            values[DP_GlobalRegions[region]] = {
                sheet.values[0][1] : sheet.values[row][1],
                sheet.values[0][2] : sheet.values[row][2],
            }

    AMModDataGlobal[sheetName] = values.tolist()
       
def readViralSupprPhiByRegion(AMModDataGlobal, sheet, sheetName):
    numberCol = 1
    LBCol     = 2
    UBCol     = 3

    values = np.zeros(DP_MaxNumRegions, dtype = list)

    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            values[DP_GlobalRegions[region]] = {
                sheet.values[0][numberCol] : sheet.values[row][numberCol],
                sheet.values[0][LBCol] : sheet.values[row][LBCol],
                sheet.values[0][UBCol] : sheet.values[row][UBCol],
            }

    AMModDataGlobal[sheetName] = values.tolist()

def readChildCD4TransitionMatrix(AMModDataGlobal, sheet, sheetName):

    values = np.zeros((DP_CD4_Per_LT5 + 1, DP_CD4_Ped_LT200 + 1))

    row = 2
    for cd4Count in GBRange(DP_CD4_Ped_LT200, DP_CD4_Ped_GT1000, -1):
        col = 1
        for cd4Percent in GBRange(DP_CD4_Per_LT5, DP_CD4_Per_GT30, -1):
            values[cd4Percent][cd4Count] = sheet.values[row][col]
            col += 1
        row += 1

    AMModDataGlobal[sheetName] = values.tolist()

def readProgressionRatesByRegion(AMModDataGlobal, sheet, sheetName):
    
    ProgressionRates = np.zeros(DP_MaxNumRegions, dtype = list)

    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            row = row + 3

            values = np.zeros((GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_50_99 + 1))
            for c in GBRange(DP_CD4_GT500, DP_CD4_50_99):
                col = 1
                for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
                    values[GB_Male][a][c] = sheet.values[row][col]
                    values[GB_Female][a][c] = sheet.values[row][col + 4]

                    col += 1
                row += 1

            ProgressionRates[DP_GlobalRegions[region]] = values.tolist()
    
    AMModDataGlobal[sheetName] = ProgressionRates.tolist()

def readInitialCD4CountByRegion(AMModDataGlobal, sheet, sheetName):
    
    InitialCD4Count = np.zeros(DP_MaxNumRegions, dtype = list)

    for region in DP_GlobalRegions:
        row = getTagRow(sheet, region)
        if not (row == GB_Nan):
            row = row + 3

            values = np.zeros((GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_LT50 + 1))
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                col = 1
                for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
                    values[GB_Male][a][c] = sheet.values[row][col]
                    values[GB_Female][a][c] = sheet.values[row][col + 4]

                    col += 1
                row += 1

            InitialCD4Count[DP_GlobalRegions[region]] = values.tolist()
    
    AMModDataGlobal[sheetName] = InitialCD4Count.tolist()

def readChildARTMortalityTrends(AMModDataGlobal, sheet, sheetName):
    startRow = 1
    startCol = 2
    endCol = len(sheet.values[0]) - 1
    startYear = int(sheet.values[0][startCol])
    endYear = int(sheet.values[0][endCol])

    values = np.zeros((DP_WAfrica + 1, DP_CD4_5t14 + 1, DP_MortRates_GT12Mo + 1, endYear - startYear + 1))
    
    row = startRow
    for region in GBRange(DP_Asia, DP_WAfrica):
        for age in GBRange(DP_CD4_0t4, DP_CD4_5t14):
            for timePeriod in GBRange(DP_MortRates_LT12Mo, DP_MortRates_GT12Mo):
                i = 0
                for col in GBRange(startCol, endCol):
                    values[region][age][timePeriod][i] = sheet.values[row][col]
                    i += 1
                row += 1
            
    data = {
        'startYear' : startYear,
        'endYear' : endYear,
        'values' : values.tolist()
    }

    AMModDataGlobal[sheetName] = data

def getSexStartIdx(sex):   #first column of a selected sexes' data
    result = 6
    if sex == GB_BothSexes: 
        result = 6
    elif sex == GB_Male: 
        result = 90
    elif sex == GB_Female: 
        result = 174
    return result

def getDataTypeStartIdx(dt):   #column offset of a selected data type
    result = 0
    if dt == DP_Percent: 
        result = 0
    elif dt == DP_LowerBound: 
        result = 21
    elif dt == DP_UpperBound: 
        result = 42
    elif dt == DP_WeightedSampleSize: 
        result = 63
    return result

def getAgeIdx(age):   #column offset of a selected age
    result = 0
    if age == DP_Val_A0_14: 
        result = 0
    elif age == DP_Val_A15_49: 
        result = 1
    elif age == DP_Val_A50Plus: 
        result = 2
    elif age == GBRange(DP_A0_4, DP_A80_Up): 
        result = age + 3
    return result

def readARTCoverageSurveys(countries, sheet, sheetName):
    localCountries = {}

    for row in GBRange(2, len(sheet.values) - 1):
        countryCode = sheet.values[row][0]
        subnatCode = sheet.values[row][1]
        year = int(sheet.values[row][4])
        survey = getARTCovSurveyDict(year)
        survey['name'] = sheet.values[row][5]
        survey['used'] = True

        for s in GBRange(GB_BothSexes, GB_Female):
            for n in GBRange(DP_Percent, DP_WeightedSampleSize):
                for a in GBRange(DP_A0_4, DP_Val_A50Plus):
                    value = float(sheet.values[row, getSexStartIdx(s) + getDataTypeStartIdx(n) + getAgeIdx(a)])

                    if ((n == DP_WeightedSampleSize) or GBEqual(value, DPNotAvail)):
                        survey['data'][s][n][a] = value
                    else:
                        survey['data'][s][n][a] = value * 100

        if not (countryCode in localCountries):
            localCountries[countryCode] = {}

        if not subnatCode in localCountries[countryCode]:
            localCountries[countryCode][subnatCode] = []
            
        localCountries[countryCode][subnatCode].append(survey)

    for countryCode in localCountries:
        for subnatCode in localCountries[countryCode]:
            addDataByCountryCode(countryCode, countries, sheetName, localCountries[countryCode][subnatCode], subnatCode)
    

def write_aim_db(version, country=''):
    FQName = os.getcwd() + '/DefaultData/SourceData/aim/AMModData.xlsx'

    countries = {}
    AMModDataGlobal = {}

    xlsx = pd.ExcelFile(FQName)
    for sheetName in xlsx.sheet_names:

        sheet = xlsx.parse(sheetName, header=None)

        if isValueByYearSheet(sheetName):
            getValuesByYear(countries, sheet, sheetName)
        elif (sheetName == 'Regions'):
            readRegions(countries, sheet, sheetName)
        elif (sheetName == 'ChildARTDistByRegion'):
            readChildARTDistByRegion(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'ChildMortCD4CountARTByRegion'):
            readChildMortCD4CountARTByRegion(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'ChildMortCD4PercARTByRegion'):
            readChildMortCD4PercARTByRegion(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'PercPregAccessAntenatalCare'):
            readPercPregAccessAntenatalCare(countries, sheet, sheetName)
        elif (sheetName == 'MortalityByAge'):
            readMortalityByAge(countries, sheet, sheetName)
        elif (sheetName == 'MortalityNoARTByRegion'):
            readMortalityNoARTByRegion(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'MortalityWithARTByRegion'):
            readMortalityWithARTByRegion(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'ARTmortalityTrends'):
            readARTmortalityTrends(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'DHSPrevalenceByAge'):
            readDHSPrevalenceByAge(countries, sheet, sheetName)
        elif (sheetName == '45q15WPP'):
            getValuesNotByYear(countries, sheet, sheetName)
        elif (sheetName == 'AgeRatioPatternsIncidence'):
            readAgeRatioPatternsIncidence(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'InfantFeedingData'):
            readInfantFeedingData(countries, sheet, sheetName)
        elif (sheetName == 'InfantFeedingModel'):
            readInfantFeedingModel(countries, AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'EpidemicStartYear'):
            getValuesNotByYearNoSubnatCols(countries, sheet, sheetName)
        elif (sheetName == 'EpidemicType'):
            getValuesNotByYearNoSubnatCols(countries, sheet, sheetName)
        elif (sheetName == 'SexualActivity15-19'):
            getValuesNotByYear(countries, sheet, sheetName, 0, 2)
        elif (sheetName == 'Preg_woman_prev'):
            getValuesNotByYearNoSubnatCols(countries, sheet, sheetName)
        elif (sheetName == 'PediatricTransitionParameters'):
            readPediatricTransitionParameters(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'ChildWeightBands'):
            readChildWeightBands(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'FertilityRatio'):
            readFertilityRatio(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'FRRByCD4Category'):
            readFRRByCD4Category(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'RatioWomenOnART'):
            readRatioWomenOnART(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'FRR15_19Coefs'):
            readFRR15_19Coefs(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'FRRbyLocation'):
            readFRRbyLocation(countries, sheet, sheetName)
        elif (sheetName == 'ViralSupprPhiByRegion'):
            readViralSupprPhiByRegion(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'ChildCD4TransitionMatrix'):
            readChildCD4TransitionMatrix(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'ProgressionRatesByRegion'):
            readProgressionRatesByRegion(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'InitialCD4CountByRegion'):
            readInitialCD4CountByRegion(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'ChildARTMortalityTrends'):
            readChildARTMortalityTrends(AMModDataGlobal, sheet, sheetName)
        elif (sheetName == 'ARTCoverageSurveys'):
            readARTCoverageSurveys(countries, sheet, sheetName)

    # log('Uploading global data')
    # AMModDataGlobal_json = ujson.dumps(AMModDataGlobal)
    # FName = 'AM_Global_' + version + '.JSON'
    # GB_upload_json(connection, 'aim', FName, AMModDataGlobal_json)
    log('Writing global data')
    FName = 'AM_Global_' + version + '.JSON'
    os.makedirs(aim_json_path, exist_ok=True)
    with open(os.path.join(aim_json_path, FName), 'w') as f:
        ujson.dump(AMModDataGlobal, f)


    # GBModData = getGBModDataDictByISO3()
    # for countryCode in countries:
    #     ISO3_Alpha = GBModData[countryCode]['ISO3_Alpha'] if countryCode in GBModData else 'notFound'

    #     if ISO3_Alpha != 'notFound':
    #         for subnatCode in countries[countryCode]:
    #             country = countries[countryCode][subnatCode]

    #             log('Uploading ' + GBModData[countryCode]['countryName'] + ' ' + str(subnatCode))
    #             country_json = ujson.dumps(country)
    #             FName = 'country/' + formatCountryFName(ISO3_Alpha, version, subnatCode)
    #             GB_upload_json(connection, 'aim', FName, country_json)os.makedirs(demproj_json_country_path, exist_ok=True)

    
    GBModData = getGBModDataDictByISO3()
    os.makedirs(aim_json_country_path, exist_ok=True)
    for countryCode in countries:
        # country = countries[countryCode] 
        ISO3_Alpha = GBModData[countryCode]['ISO3_Alpha'] if countryCode in GBModData else 'notFound'

        if ISO3_Alpha != 'notFound':
            for subnatCode in countries[countryCode]:                
                country = countries[countryCode][subnatCode] 
                log('Uploading ' + GBModData[countryCode]['countryName'] + ' ' + str(subnatCode))
                FName = formatCountryFName(ISO3_Alpha, version, subnatCode)
                with open(os.path.join(aim_json_country_path, FName), 'w') as f:
                    ujson.dump(country, f)

    # GBModData = getGBModDataDict()
    # for countryName in countries:
    #     country = countries[countryName] 
    #     ISO3_Alpha = GBModData[countryName]['ISO3_Alpha'] if countryName in GBModData else 'notFound'

    #     if ISO3_Alpha != 'notFound':
    #         log('Writing '+ countryName)
    #         FName = 'country/' + formatCountryFName(ISO3_Alpha, version)
    #         with open(os.path.join(aim_json_country_path, FName), 'w') as f:
    #             ujson.dump(country, f)

def upload_aim_db(version): 
    uploadFilesInDir('aim', aim_json_path, version) 
    # connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']  
    # # global
    # for root, dirs, files in os.walk(aim_json_path, followlinks=False): 
    #     if (root == aim_json_path):
    #         for file in files:
    #             if isCurrentVersion(file, version):
    #                 log('Uploading ' + file)
    #                 GB_upload_file(connection, 'aim', file, os.path.join(root, file))

    # # country
    # for root, dirs, files in os.walk(aim_json_country_path): 
    #     for file in files:
    #         if isCurrentVersion(file, version):
    #             log('Uploading ' + file)
    #             GB_upload_file(connection, 'aim', os.path.join(aim_country_dir, file), os.path.join(root, file))


            

    

