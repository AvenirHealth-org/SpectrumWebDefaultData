import os
import pandas as pd
import numpy as np
import ujson

from AvenirCommon.Database import GB_upload_json, GB_get_db_json
from AvenirCommon.Logger import log
from AvenirCommon.Util import GBRange, GBDownRange

from SpectrumCommon.Const.GB import GB_Male, GB_Female
from SpectrumCommon.Const.DP import *


HIVMortARTSheets = [
    'HIVMortART_Asia',
    'HIVMortART_CentralAfrica',
    'HIVMortART_DevelopedCountries',
    'HIVMortART_EastAfrica',
    'HIVMortART_LatinAmAndCaribbean',
    'HIVMortART_SouthAfrica',
    'HIVMortART_SouthernAfrica',
    'HIVMortART_WestAfrica',
]

AgePatternsSheet = 'AgePatterns'
ProgressionRatesAndHIVMortNoARTSheet = 'ProgressionRatesAndHIVMortNoART'

def readHIVMortART(FQName, sheet):
    StartRow = 4
    LT6mthsStartCol = 1
    From6to12mthsStartCol = 57
    GT12mthsStartCol = 113

    sheet = pd.read_excel(FQName, sheet_name=sheet, header=None)

    HIVMortART0_6  = np.zeros((DPUA_NumFileRuns, GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_LT50 + 1))
    HIVMortART7_12 = np.zeros((DPUA_NumFileRuns, GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_LT50 + 1))
    HIVMortARTGT12 = np.zeros((DPUA_NumFileRuns, GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_LT50 + 1))
    
    row = StartRow
    for r in GBRange(1, DPUA_NumFileRuns):
        col = LT6mthsStartCol
        for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
            for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
                for s in GBRange(GB_Male, GB_Female):
                    HIVMortART0_6[r - 1, s, a, c] = sheet.values[row, col]
                    col += 1
        row += 1
        
    row = StartRow
    for r in GBRange(1, DPUA_NumFileRuns):
        col = From6to12mthsStartCol
        for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
            for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
                for s in GBRange(GB_Male, GB_Female):
                    HIVMortART7_12[r - 1, s, a, c] = sheet.values[row, col]
                    col += 1
        row += 1
        
    row = StartRow
    for r in GBRange(1, DPUA_NumFileRuns):
        col = GT12mthsStartCol
        for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
            for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
                for s in GBRange(GB_Male, GB_Female):
                    HIVMortARTGT12[r - 1, s, a, c] = sheet.values[row, col]
                    col += 1
        row += 1

    return {
        '0_6'   : HIVMortART0_6.tolist(),
        '7_12'  : HIVMortART7_12.tolist(),
        'GT12'  : HIVMortARTGT12.tolist(),
    }

def readAgePatterns(FQName, sheet):
    sheet = pd.read_excel(FQName, sheet_name=sheet, header=None)

    DistOfHIVHiPrev = np.zeros((DPUA_NumDistHIVCurvesHiPrev, DP_MAX_AGE + 1, GB_Female + 1))
    DistOfHIVLoPrev = np.zeros((DPUA_NumDistHIVCurvesLoPrev, DP_MAX_AGE + 1, GB_Female + 1))
    DistOfHIVIDU = np.zeros((DPUA_NumDistHIVCurvesIDU, DP_MAX_AGE + 1, GB_Female + 1))
    
    row = 2
    
    for s in GBDownRange(GB_Female, GB_Male):
        row += 1
        for r in GBRange(1, DPUA_NumDistHIVCurvesHiPrev):
            col = 1
            for a in GBRange(GB_A15_19, GB_A75_79):
                DistOfHIVHiPrev[r - 1, a, s] = sheet.values[row, col]
                col += 1
            row += 1
    
    for s in GBDownRange(GB_Female, GB_Male):
        row += 1
        for r in GBRange(1, DPUA_NumDistHIVCurvesLoPrev):
            col = 1
            for a in GBRange(GB_A15_19, GB_A75_79):
                DistOfHIVLoPrev[r - 1, a, s] = sheet.values[row, col]
                col += 1
            row += 1
    
    for s in GBDownRange(GB_Female, GB_Male):
        row += 1
        for r in GBRange(1, DPUA_NumDistHIVCurvesIDU):
            col = 1
            for a in GBRange(GB_A15_19, GB_A75_79):
                DistOfHIVIDU[r - 1, a, s] = sheet.values[row, col]
                col += 1
            row += 1

    return {
        'HiPrev'    : DistOfHIVHiPrev.tolist(),
        'LoPrev'    : DistOfHIVLoPrev.tolist(),
        'IDU'       : DistOfHIVIDU.tolist(),
    }

def readProgressionRates(FQName, sheet):
    sheet = pd.read_excel(FQName, sheet_name=sheet, header=None)
    
    StartRow = 8
    ProgressRatesStartCol = 1
        
    values = np.zeros((DPUA_NumFileRuns, GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_50_99 + 1))
    
    row = StartRow
    for r in GBRange(1, DPUA_NumFileRuns):
        col = ProgressRatesStartCol
        for s in GBRange(GB_Male, GB_Female):
            for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
                for c in GBRange(DP_CD4_GT500, DP_CD4_50_99):
                    values[r - 1, s, a, c] = sheet.values[row, col]
                    col += 1
        row += 1

    return values.tolist()

def readHIVMortNoART(FQName, sheet):
    sheet = pd.read_excel(FQName, sheet_name=sheet, header=None)
    
    StartRow = 8
    HIVMortNoARTStartCol = 49
        
    values = np.zeros((DPUA_NumFileRuns, GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_LT50 + 1))
    
    row = StartRow
    for r in GBRange(1, DPUA_NumFileRuns):
        col = HIVMortNoARTStartCol
        for s in GBRange(GB_Male, GB_Female):
            for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
                for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                    values[r - 1, s, a, c] = sheet.values[row, col]
                    col += 1
        row += 1

    return values.tolist()


def upload_UA_db(version):
    FQName = os.getcwd() + '\\DefaultData\\SourceData\\aim\\UAModData.xlsx'
    connection =  os.environ[GB_SPECT_MOD_DATA_CONN_ENV]

    UAData = {}

    for sheet in HIVMortARTSheets:
        UAData[sheet] = readHIVMortART(FQName, sheet)
    
    UAData[AgePatternsSheet] = readAgePatterns(FQName, AgePatternsSheet)

    UAData['ProgressionRates'] = readProgressionRates(FQName, ProgressionRatesAndHIVMortNoARTSheet)
    UAData['HIVMortNoART'] = readHIVMortNoART(FQName, ProgressionRatesAndHIVMortNoARTSheet)

    log('Uploading Uncertainty Analysis data')
    UAData_json = ujson.dumps(UAData)
    FName = 'UAData_' + version + '.JSON'
    GB_upload_json(connection, 'uncertaintyanalysis', FName, UAData_json)
    