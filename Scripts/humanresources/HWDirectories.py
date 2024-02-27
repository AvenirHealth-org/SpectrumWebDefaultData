import os

from SpectrumCommon.Const.HW.HWConst import *

def create_HW_directories():
    HW_path = os.getcwd()+'\Tools\DefaultDataManager\HW\\'

    dir_list = [HW_path + 'JSON\\' + HW_STAFF_SALARIES_DB_DIR]
    for path in dir_list:
        os.makedirs(path, exist_ok=True)