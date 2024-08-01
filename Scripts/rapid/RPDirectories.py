import os

from SpectrumCommon.Const.RP.RPConst import *

def create_RP_directories():
    RP_path = os.getcwd()+'\Tools\DefaultDataManager\RP\\'
    dir_list = [
        RP_path+ 'JSON\\' + RP_COUNTRY_DEFAULTS_DB_DIR
    ]
    for path in dir_list:
        os.makedirs(path, exist_ok=True)
