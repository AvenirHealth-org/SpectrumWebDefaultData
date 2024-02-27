import os
from io import BytesIO
import pandas as pd
from DefaultData.DefaultDataUtil import *
from AvenirCommon.Database.BlobStorage import *

FQPath = os.getcwd() + '\\DefaultData\\SourceData\\aim\\UNAIDSSummaryTemplate'

def upload_aim_UNAIDSSummaryTemplate_db(version): 

    connection =  os.environ[GB_SPECT_MOD_DATA_CONN_ENV]
    for root, dirs, files in os.walk(FQPath): 
        for file in files:
            if isCurrentVersion(file, version):
                log('Uploading ' + file)
                fileName = os.path.join(root.replace(FQPath, '').replace('\\', ''), file)   # strips root directory off of root, so subdirectory is added.  
                                                                                            # might need recursive strategy if you want to go more than one directory deep
                GB_upload_excel_file(connection, 'aim', os.path.join('UNAIDSSummaryTemplate', fileName), os.path.join(root, file))
