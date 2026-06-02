import os
from io import BytesIO
import pandas as pd
from DefaultDataUtil import *
from AvenirCommon.Database.BlobStorage import *
from Scripts.aim.AMVersions import aim_live_db_versions

FQPath = os.getcwd() + '\\DefaultData\\SourceData\\aim\\UNAIDSSummaryTemplate'

def upload_aim_UNAIDSSummaryTemplate_db(version): 
    if aim_live_db_versions['UNAIDSSummaryTemplate'] == version:
        user_input = input("You are uploading LIVE UNAIDSSummaryTemplate. Are you sure? (y/n)  ")
        if user_input.lower() not in ['y', 'yes']:
            print("Operation cancelled by user.")
            return
        
    connection =  os.environ[GB_SPECT_MOD_DATA_CONN_ENV]
    for root, dirs, files in os.walk(FQPath): 
        for file in files:
            if isCurrentVersion(file, version):
                log('Uploading ' + file)
                fileName = os.path.join(root.replace(FQPath, '').replace('\\', ''), file)   # strips root directory off of root, so subdirectory is added.  
                                                                                            # might need recursive strategy if you want to go more than one directory deep
                GB_upload_excel_file(connection, 'aim', os.path.join('UNAIDSSummaryTemplate', fileName), os.path.join(root, file))
