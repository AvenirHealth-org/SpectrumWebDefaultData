import DefaultData.Scripts.aim as aim
import DefaultData.Scripts.demproj as demproj
import DefaultData.Scripts.famplan as famplan

from SpectrumCommon.Const.DP import *
from SpectrumCommon.Const.FP import *

demproj.upload_UPD_db(DPUPDVersion)
# demproj.upload_demproj_db(DPDatabaseVersion)
# demproj.upload_DP_population_db(DPFirstYearPopDBVersion)

# aim.upload_aim_db(AMDatabaseVersion)
# aim.upload_easyAIM_db(AMEasyAIMDatabaseVersion)
# aim.upload_CSAVR_db(AMCSAVRDatabaseVersion)

# famplan.create_famplan_db('V5', FP_Interpolated) 
# famplan.create_famplan_db('V3', FP_Uninterpolated)
# famplan.create_famplan_effectiveness('V2')