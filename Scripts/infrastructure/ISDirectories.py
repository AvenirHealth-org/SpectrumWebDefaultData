import os

from SpectrumCommon.Const.IS.ISConst import *


def create_IS_directories():
    IS_path = os.getcwd()+'\Tools\DefaultDataManager\IS\\'
    #dir_list = [IS_path+ 'JSON\\' + IC_NON_IMPACT_COVERAGE_BY_YEAR_DB_DIR ,
    #for path in dir_list:
    #    os.makedirs(path, exist_ok=True)
    
    #os.makedirs(IC_path + '\JSON\\' + icc.IC_TARG_POP_DIRECT_ENTRY_DB_DIR + '\\', exist_ok=True)