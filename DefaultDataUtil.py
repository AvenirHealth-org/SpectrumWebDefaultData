import os
from AvenirCommon.Logger import log
from AvenirCommon.Database import GB_upload_json, GB_get_db_json, GB_upload_file

from SpectrumCommon.Const.GB import *


country_dir = 'country'


def isCurrentVersion(file, version):
    return os.path.splitext(file)[0].split('_')[-1] == version


# # this should safely upload any file in the given directory, given that it is the right version number
# def uploadFilesInDir(container, directory, version): 
#     connection =  os.environ['AVENIR_SPEC_DEFAULT_DATA_CONNECTION']  
#     # global
#     for root, dirs, files in os.walk(directory): 
#         if (root == directory):
#             for file in files:
#                 if isCurrentVersion(file, version):
#                     log('Uploading ' + file)
#                     GB_upload_file(connection, container, os.path.join(root.replace(directory, '').replace('\\', ''), file), os.path.join(root, file))

# this should safely upload any file in the given directory, given that it is the right version number, 
# and will also safely work up to one directory 'deep'.  will probably break if things are nested more than one level.
# pathMod is used for uploading from a directory into a 'subdirectory' of a blob - see easyAIM upload as an example
def uploadFilesInDir(container, directory, version, pathMod = ''): 
    connection =  os.environ[GB_SPECT_MOD_DATA_CONN_ENV]
    for root, dirs, files in os.walk(directory): 
        for file in files:
            if isCurrentVersion(file, version):
                log('Uploading ' + file)
                fileName = os.path.join(root.replace(directory, '').replace('\\', ''), file)    # strips root directory off of root, so subdirectory is added.  
                                                                                                # might need recursive strategy if you want to go more than one directory deep
                GB_upload_file(connection, container, os.path.join(pathMod, fileName), os.path.join(root, file))

def get_source_data_path(mod_ID = int):
    return os.getcwd() + '\DefaultData\SourceData\\' + GB_CONTAINERS[mod_ID]

def get_JSON_data_path(mod_ID = int, file_name = ''):
    return os.getcwd() + '\DefaultData\JSONData\\' + GB_CONTAINERS[mod_ID]

def addDataByCountryCode(countryCode, countries, dataName, data, subnatCode = 0):
    if (subnatCode == 0):
        countrySubnatCode = countryCode + '_' + str(subnatCode)
    else:
        countrySubnatCode = countryCode

    if not(countrySubnatCode in countries):
        countries[countrySubnatCode] = {
            'countryCode' : countryCode,
            'subnatCode' : subnatCode,
        }
    countries[countrySubnatCode][dataName] = data