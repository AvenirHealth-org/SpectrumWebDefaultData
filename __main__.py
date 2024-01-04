import DefaultData.Scripts.aim as aim
import DefaultData.Scripts.demproj as demproj
import DefaultData.Scripts.famplan as famplan
import DefaultData.Scripts.tuberculosis as tuberculosis

from SpectrumCommon.Const.DP import *
from SpectrumCommon.Const.FP import *
from AvenirCommon.Keys import store_keys_in_env
store_keys_in_env()
# demproj.upload_UPD_db(DPUPDVersion)

# demproj.write_demproj_db(DPDatabaseVersion)
# demproj.upload_demproj_db(DPDatabaseVersion)

# demproj.upload_DP_population_db(DPFirstYearPopDBVersion)

# aim.write_aim_db(AMDatabaseVersion)
# aim.upload_aim_db(AMDatabaseVersion)
# aim.write_easyAIM_db(AMEasyAIMDatabaseVersion)
# aim.upload_easyAIM_db(AMEasyAIMDatabaseVersion)
# aim.write_CSAVR_db(AMCSAVRDatabaseVersion)
# aim.upload_CSAVR_db(AMCSAVRDatabaseVersion)
# aim.write_CSAVR_db('V1Beta')
# aim.upload_CSAVR_db('V1Beta')

# famplan.create_famplan_db('V5', FP_Interpolated) 
# famplan.create_famplan_db('V3', FP_Uninterpolated)
# famplan.create_famplan_effectiveness('V2')# famplan.create_famplan_db('V5', FP_Interpolated) 
# famplan.create_famplan_db('V3', FP_Uninterpolated)
# famplan.create_famplan_effectiveness('V2')

# tuberculosis.create_TB_WHOCountryData('V2')
# tuberculosis.upload_TB_WHOCountryData('V2')

# tuberculosis.create_TB_fort_input('V2')
# tuberculosis.upload_tb_fort_inputs_db('V2')

# tuberculosis.create_TB_fort_outputs('V3')
# tuberculosis.upload_tb_fort_outputs_db('V3')
