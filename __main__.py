import DefaultData.Scripts.famplan as famplan
import DefaultData.Scripts.tuberculosis as tuberculosis
from SpectrumCommon.Const.FP import *
from AvenirCommon.Keys import store_keys_in_env
store_keys_in_env()
# famplan.create_famplan_db('V5', FP_Interpolated) 
# famplan.create_famplan_db('V3', FP_Uninterpolated)
# famplan.create_famplan_effectiveness('V2')

# tuberculosis.create_TB_WHOCountryData('V2')
# tuberculosis.upload_TB_WHOCountryData('V2')

# tuberculosis.create_TB_fort_input('V2')
# tuberculosis.upload_tb_fort_inputs_db('V2')

tuberculosis.create_TB_fort_outputs('V3')
# tuberculosis.upload_tb_fort_outputs_db('V3')
