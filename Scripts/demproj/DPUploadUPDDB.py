import os
import pandas as pd
import numpy as np
import ujson

from AvenirCommon.Database import  GB_upload_json, GB_get_db_json
from AvenirCommon.Util import GBRange, formatCountryFName, getTagRow
from AvenirCommon.Logger import log
from SpectrumCommon.Const.DP import *

from Tools.DefaultDataManager.GB.Upload.GBUploadModData  import getGBModDataDict
from DefaultData.DefaultDataUtil import *

UPD_json_path = os.getcwd() + '\\DefaultData\\JSONData\\demproj\\UPD'

headerStartTag = '<header>'
headerEndTag = '</header>'

basepopStartTag = '<basepop>'
basepopEndTag = '</basepop>'

lftsStartTag = '<lfts>'
lftsEndTag = '</lfts>'

tfrStartTag = '<tfr>'
tfrEndTag = '</tfr>'

srbStartTag = '<srb>'
srbEndTag = '</srb>'

pasfrsStartTag = '<pasfrs>'
pasfrsEndTag = '</pasfrs>'

migrationStartTag = '<migration>'
migrationEndTag = '</migration>'

sourceStartTag = '<source>'
sourceEndTag = '</source>'

generalStartTag = '<general>'
generalEndTag = '</general>'

def getYearSexAgeYearData(sheet, row, yearStr):
    result = np.zeros((DP_MaxSingleAges + 1, GB_Female + 1))

    while (yearStr == sheet.values[row][0]):
        sex = int(sheet.values[row][1])
        age = int(sheet.values[row][2])
        result[age][sex] = float(sheet.values[row][3])
        row += 1
    return result.tolist(), row

def getYearSexAgeData(sheet, startTagRow, endTagRow):
    result = {}

    row = startTagRow + 2
    while (row < endTagRow):
        result[sheet.values[row][0]], row = getYearSexAgeYearData(sheet, row, sheet.values[row][0])
    return result


def getYearData(sheet, startTagRow, endTagRow):
    result = {}

    row = startTagRow + 2
    while (row < endTagRow):
        result[sheet.values[row][0]] = float(sheet.values[row][1])
        row += 1
    return result


def getpasfrsYearData(sheet, row, yearStr):
    result = np.zeros(49 + 1)

    while (yearStr == sheet.values[row][0]):
        age = int(sheet.values[row][1])
        result[age] = float(sheet.values[row][2])
        row += 1
    return result.tolist(), row

def getpasfrsData(sheet, startTagRow, endTagRow):
    result = {}

    row = startTagRow + 2
    while (row < endTagRow):
        result[sheet.values[row][0]], row = getpasfrsYearData(sheet, row, sheet.values[row][0])
    return result


def getlftsYearData(sheet, row, yearStr):
    result = np.zeros((DP_MaxSingleAges + 2, GB_Female + 1), dtype = list)

    while (yearStr == sheet.values[row][0]):
        sex = int(sheet.values[row][1])
        age = int(sheet.values[row][2])
        result[age][sex] = {
            'lx' : float(sheet.values[row][3]),
            'ex' : float(sheet.values[row][4]),
            'sx' : float(sheet.values[row][5]),
        }

        row += 1
    return result.tolist(), row

def getlftsData(sheet, startTagRow, endTagRow):
    result = {}

    row = startTagRow + 2
    while (row < endTagRow):
        result[sheet.values[row][0]], row = getlftsYearData(sheet, row, sheet.values[row][0])
    return result

def getsourceData(sheet, startTagRow, endTagRow):
    result = []

    row = startTagRow + 2
    for src in GBRange(DP_UPD_Pop, DP_UPD_Migration):
        result.append({
            'Name'      : '' if pd.isna(sheet.values[row][0]) else sheet.values[row][0],
            'Summary'   : '' if pd.isna(sheet.values[row][1]) else sheet.values[row][1],
            'Source'    : '' if pd.isna(sheet.values[row][2]) else sheet.values[row][2],
            'RefDate'   : '' if pd.isna(sheet.values[row][3]) else sheet.values[row][3],
        })
        row += 1
    return result

def getgeneralData(sheet, startTagRow, endTagRow):
    return {
        'Provider' : sheet.values[startTagRow + 1][1],
        'Version'  : sheet.values[startTagRow + 2][1],
    }

def findCountryInDirs(root, dirs, file):
    result = False
    for dir in dirs:     
        for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):                                  
            for file2 in files2:
                if (str.lower(file[file.find('_') : file.find('_', file.find('_') + 1)]) == 
                str.lower(file2[file2.find('_') : file2.find('_', file2.find('_') + 1)])):                  # find duplicate countries by country code
                    result = True                        

    return result

def write_UPD_db(version):
    os.makedirs(UPD_json_path, exist_ok=True)
    
    for root, dirs, files in os.walk(os.getcwd() + '\\DefaultData\\SourceData\\demproj\\UNPopDataByCountry'):  # get all year dirs
        dirs.sort()                                                                                         # and sort them, just in case

        for dir in dirs:                                                                                   # upload  files 
            for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):                                  # loop through directories oldest to newest 
                for file in files2:
                    if str.lower(file).endswith('.upd'):
                        if not findCountryInDirs(root, dirs[dirs.index(dir)+1:], file):                     # for each file, check if newer version exists
                            writeUPD(version, root2, file)                                                 # if not, upload it



def writeUPD(version, root, file):
    connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']
    GBModData = getGBModDataDict()

    sheet = pd.read_csv(os.path.join(root, file), header=None)

    # headerStartTagRow = getTagRow(sheet, headerStartTag)
    countryName = file[0 : file.find('_')]
    ISO3_Alpha = GBModData[countryName]['ISO3_Alpha'] if countryName in GBModData else 'notFound'

    UPDData = {}

    basepopStartTagRow = getTagRow(sheet, basepopStartTag)
    # basepopEndTagRow = getTagRow(sheet, basepopEndTag)
    basepop, row = getYearSexAgeYearData(sheet, basepopStartTagRow + 2, '1970')
    # basepop = getYearSexAgeData(sheet, basepopStartTagRow, basepopEndTagRow)
    UPDData['basepop'] = basepop

    lftsStartTagRow = getTagRow(sheet, lftsStartTag)
    lftsEndTagRow = getTagRow(sheet, lftsEndTag)
    lfts = getlftsData(sheet, lftsStartTagRow, lftsEndTagRow)
    UPDData['lfts'] = lfts

    tfrStartTagRow = getTagRow(sheet, tfrStartTag)
    tfrEndTagRow = getTagRow(sheet, tfrEndTag)
    tfr = getYearData(sheet, tfrStartTagRow, tfrEndTagRow)
    UPDData['tfr'] = tfr

    srbStartTagRow = getTagRow(sheet, srbStartTag)
    srbEndTagRow = getTagRow(sheet, srbEndTag)
    srb = getYearData(sheet, srbStartTagRow, srbEndTagRow)
    UPDData['srb'] = srb

    pasfrsStartTagRow = getTagRow(sheet, pasfrsStartTag)
    pasfrsEndTagRow = getTagRow(sheet, pasfrsEndTag)
    pasfrs = getpasfrsData(sheet, pasfrsStartTagRow, pasfrsEndTagRow)
    UPDData['pasfrs'] = pasfrs

    migrationStartTagRow = getTagRow(sheet, migrationStartTag)
    migrationEndTagRow = getTagRow(sheet, migrationEndTag)
    migration = getYearSexAgeData(sheet, migrationStartTagRow, migrationEndTagRow)
    UPDData['migration'] = migration

    sourceStartTagRow = getTagRow(sheet, sourceStartTag)
    sourceEndTagRow = getTagRow(sheet, sourceEndTag)
    if type(sourceStartTagRow) == int:
        source = getsourceData(sheet, sourceStartTagRow, sourceEndTagRow)
        UPDData['source'] = source

    generalStartTagRow = getTagRow(sheet, generalStartTag)
    generalEndTagRow = getTagRow(sheet, generalEndTag)
    if type(generalStartTagRow) == int:
        general = getgeneralData(sheet, generalStartTagRow, generalEndTagRow)
        UPDData['general'] = general

    if ISO3_Alpha != 'notFound':
        log('Writing '+ countryName)
        with open(os.path.join(UPD_json_path, formatCountryFName(ISO3_Alpha, version)), 'w') as f:
            ujson.dump(UPDData, f)

def upload_UPD_db(version):  
    uploadFilesInDir('demproj', UPD_json_path, version, pathMod = 'UPD/')

def get_UPD_test(version):
    FName = 'UPD/' + formatCountryFName('BEN', version)
    
    connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']
    
    db = GB_get_db_json(connection, 'demproj', FName)
    log(db['general'])




    


