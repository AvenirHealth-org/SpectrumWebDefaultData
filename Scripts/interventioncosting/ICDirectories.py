import os

from SpectrumCommon.Const.IC.ICConst import *

def create_IC_directories():
    IC_path = os.getcwd()+'\Tools\DefaultDataManager\IC\\'
    dir_list = [IC_path+ 'JSON\\' + IC_NON_IMPACT_COVERAGE_BY_YEAR_DB_DIR ,
                IC_path+ 'JSON\\' + IC_NON_IMPACT_COVERAGE_DB_DIR ,
                IC_path+ 'JSON\\' + IC_PIN_BY_YEAR_DB_DIR ,
                IC_path+ 'JSON\\' + IC_PIN_DB_DIR ,
                IC_path+ 'JSON\\' + IC_TARG_POP_DIRECT_ENTRY_DB_DIR]
    for path in dir_list:
        os.makedirs(path, exist_ok=True)
    
    #os.makedirs(IC_path + '\JSON\\' + icc.IC_TARG_POP_DIRECT_ENTRY_DB_DIR + '\\', exist_ok=True)