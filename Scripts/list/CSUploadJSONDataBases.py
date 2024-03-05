import os
import ujson

from AvenirCommon.Database import GB_upload_json
from AvenirCommon.Logger import log

from SpectrumCommon.Const.CS import *

DIR = os.getcwd() + '\DefaultData\JSONData\list/'

def openDatabaseFile(FQName):
    with open(FQName, 'r') as f:
        result = ujson.load(f)

    return result

def FormatDBName(DBName, post):
    return DBName + '_' + latest_DB_Version[DBName] + post

def uploadDatabaseFile(connection, Dir, FName):
    if os.path.isfile(Dir + FName):
        log('Uploading ' + FName)
        data = openDatabaseFile(Dir + FName)
        data_json = ujson.dumps(data)
        GB_upload_json(connection, 'list', FName, data_json)

def uploadDatabaseDir(connection, Dir, DBName):
    subDir = FormatDBName(DBName, '/')
    directory = Dir + subDir
    if os.path.exists(directory):
        Files = os.listdir(directory)
        for FName in Files:
            uploadDatabaseFile(connection, Dir, subDir + FName)

def uploadDatabaseFiles(DBName = ''):
    connection =  os.environ['AVENIR_SW_DEFAULT_DATA_CONNECTION']

    def processDatabase(DBName):
        if DBName in All_Country_DB_Names:
            uploadDatabaseFile(connection, DIR, FormatDBName(DBName, '.JSON'))
        
        if DBName in DBC_DB_Names:
            uploadDatabaseDir(connection, DIR, DBName)
    
    if DBName == '':
        for DBName in All_Country_DB_Names:
            processDatabase(DBName)
        
        for DBName in DBC_DB_Names:
            processDatabase(DBName)
    else:
        processDatabase(DBName)