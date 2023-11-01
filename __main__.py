import DefaultData.Scripts.famplan as famplan
from SpectrumCommon.Const.FP import *

famplan.create_famplan_db('V5', FP_Interpolated) 
famplan.create_famplan_db('V3', FP_Uninterpolated)
famplan.create_famplan_effectiveness('V2')