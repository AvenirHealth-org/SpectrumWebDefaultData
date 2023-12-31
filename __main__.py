import DefaultData.Scripts.globals as globals
import DefaultData.Scripts.aim as aim
import DefaultData.Scripts.demproj as demproj
import DefaultData.Scripts.famplan as famplan
import DefaultData.Scripts.tuberculosis as tuberculosis
import DefaultData.Scripts.interventions as interventions
import DefaultData.Scripts.interventioncosting as interventioncosting
import DefaultData.Scripts.ohtcore as ihtcore
import DefaultData.Scripts.infrastructure as infrastructure
import DefaultData.Scripts.programmecosting as programmecosting
import DefaultData.Scripts.budgetmapping as budgetmapping

from SpectrumCommon.Const.GB import *
from SpectrumCommon.Const.DP.DPConst import *
from SpectrumCommon.Const.FP import *
from SpectrumCommon.Const.CS.CSConst import *
from SpectrumCommon.Const.IV.IVConst import *
from SpectrumCommon.Const.IC.ICConst import *
from SpectrumCommon.Const.IH.IHConst import *
from SpectrumCommon.Const.IS.ISConst import *
from SpectrumCommon.Const.PC.PCConst import *
from SpectrumCommon.Const.BG.BGConst import *

from AvenirCommon.Keys import store_keys_in_env

store_keys_in_env()

# globals.create_disability_json('V1')
# globals.upload_disability_json('V1')
# globals.createGBCountryListMaster(GBDatabaseVersion)
# globals.uploadGBCountryListMaster(GBDatabaseVersion)
# globals.upload_string_DBs(GB_STRING_DB_CURR_VERSION)

####### DemProj #######
# demproj.upload_UPD_db(DPUPDVersion)

# demproj.write_demproj_db(DPDatabaseVersion)
# demproj.upload_demproj_db(DPDatabaseVersion)

# demproj.upload_DP_population_db(DPFirstYearPopDBVersion)

####### AIM #######
# aim.write_aim_db(AMDatabaseVersion)
# aim.upload_aim_db(AMDatabaseVersion)
# aim.write_easyAIM_db(AMEasyAIMDatabaseVersion)
# aim.upload_easyAIM_db(AMEasyAIMDatabaseVersion)
# aim.write_CSAVR_db(AMCSAVRDatabaseVersion)
# aim.upload_CSAVR_db(AMCSAVRDatabaseVersion)
# aim.write_CSAVR_db('V1Beta')
# aim.upload_CSAVR_db('V1Beta')


####### FamPlan #######
# famplan.create_famplan_db('V5', FP_Interpolated) 
# famplan.create_famplan_db('V3', FP_Uninterpolated)
# famplan.create_famplan_effectiveness('V2')# famplan.create_famplan_db('V5', FP_Interpolated) 
# famplan.create_famplan_db('V3', FP_Uninterpolated)
# famplan.create_famplan_effectiveness('V2')

####### Tuberculosis #######
# tuberculosis.create_TB_WHOCountryData('V2')
# tuberculosis.upload_TB_WHOCountryData('V2')

# tuberculosis.create_TB_fort_input('V2')
# tuberculosis.upload_tb_fort_inputs_db('V2')

# tuberculosis.create_TB_fort_outputs('V3')
# tuberculosis.upload_tb_fort_outputs_db('V3')

# interventions.create_intervention_DB_IV(IV_IH_INTERVENTION_DB_CURR_VERSION, GB_IH)
# interventions.upload_intervention_DB_IV(IV_IH_INTERVENTION_DB_CURR_VERSION, GB_IH)
# interventions.create_group_DB_IV(IV_IH_GROUP_DB_CURR_VERSION, GB_IH)
# interventions.upload_group_DB_IV(IV_IH_GROUP_DB_CURR_VERSION, GB_IH)

# interventions.create_intervention_DB_IV(IV_TI_INTERVENTION_DB_CURR_VERSION, GB_TI)
# interventions.upload_intervention_DB_IV(IV_TI_INTERVENTION_DB_CURR_VERSION, GB_TI)
# interventions.create_group_DB_IV(IV_TI_GROUP_DB_CURR_VERSION, GB_TI)
# interventions.upload_group_DB_IV(IV_TI_GROUP_DB_CURR_VERSION, GB_TI)

# interventions.create_intervention_DB_IV(IV_CS_INTERVENTION_DB_CURR_VERSION, GB_CS)
# interventions.upload_intervention_DB_IV(IV_CS_INTERVENTION_DB_CURR_VERSION, GB_CS)
# interventions.create_group_DB_IV(IV_CS_GROUP_DB_CURR_VERSION, GB_CS)
# interventions.upload_group_DB_IV(IV_CS_GROUP_DB_CURR_VERSION, GB_CS)

# ihtcore.create_exchange_rate_DB_IH(IH_EXCHANGE_RATE_DB_CURR_VERSION) 
# ihtcore.upload_exchange_rate_DB_IH(IH_EXCHANGE_RATE_DB_CURR_VERSION)

# interventioncosting.create_drug_supply_DB_IC(IC_DRUG_SUPPLY_DB_CURR_VERSION)
# interventioncosting.upload_drug_supply_DB_IC(IC_DRUG_SUPPLY_DB_CURR_VERSION)
# interventioncosting.create_treatment_input_and_group_DBs_IC(IC_TREATMENT_INPUT_DB_CURR_VERSION)
# interventioncosting.upload_treatment_input_and_group_DBs_IC(IC_TREATMENT_INPUT_DB_CURR_VERSION)
# interventioncosting.create_PIN_DB_IC(IC_PIN_DB_CURR_VERSION)
# interventioncosting.upload_PIN_DB_IC(IC_PIN_DB_CURR_VERSION)
# interventioncosting.create_PIN_by_year_DB_IC(IC_PIN_BY_YEAR_DB_CURR_VERSION)
# interventioncosting.upload_PIN_by_year_DB_IC(IC_PIN_BY_YEAR_DB_CURR_VERSION)
# interventioncosting.create_non_impact_coverage_DB_IC(IC_NON_IMPACT_COVERAGE_DB_CURR_VERSION)
# interventioncosting.upload_non_impact_coverage_DB_IC(IC_NON_IMPACT_COVERAGE_DB_CURR_VERSION)
# interventioncosting.create_non_impact_coverage_by_year_DB_IC(IC_NON_IMPACT_COVERAGE_DB_CURR_VERSION)
# interventioncosting.upload_non_impact_coverage_by_year_DB_IC(IC_NON_IMPACT_COVERAGE_DB_CURR_VERSION)
# interventioncosting.create_targ_pop_DB_IC(IC_TARG_POP_DB_CURR_VERSION)
# interventioncosting.upload_targ_pop_DB_IC(IC_TARG_POP_DB_CURR_VERSION)
# interventioncosting.create_targ_pop_direct_entry_DB_IC(IC_TARG_POP_DIRECT_ENTRY_DB_CURR_VERSION)
# interventioncosting.upload_targ_pop_direct_entry_DB_IC(IC_TARG_POP_DIRECT_ENTRY_DB_CURR_VERSION)
# interventioncosting.create_health_system_costs_DB_IC(IC_HEALTH_SYSTEM_COSTS_DB_CURR_VERSION)
# interventioncosting.upload_health_system_costs_DB_IC(IC_HEALTH_SYSTEM_COSTS_DB_CURR_VERSION)
# interventioncosting.create_outpat_visit_inpat_day_costs_TB_DB_IC(IC_OUTPAT_VISIT_INPAT_DAY_COSTS_TB_DB_CURR_VERSION)
# interventioncosting.upload_outpat_visit_inpat_day_costs_TB_DB_IC(IC_OUTPAT_VISIT_INPAT_DAY_COSTS_TB_DB_CURR_VERSION)
# interventioncosting.create_outpat_visit_inpat_day_costs_CS_DB_IC(IC_OUTPAT_VISIT_INPAT_DAY_COSTS_CS_DB_CURR_VERSION)
# interventioncosting.upload_outpat_visit_inpat_day_costs_CS_DB_IC(IC_OUTPAT_VISIT_INPAT_DAY_COSTS_CS_DB_CURR_VERSION)

# infrastructure.create_facility_equipment_and_group_DBs_IS(IS_FACILITY_EQUIP_DB_CURR_VERSION)
# infrastructure.upload_facility_equipment_and_group_DBs_IS(IS_FACILITY_EQUIP_DB_CURR_VERSION)

# programmecosting.create_cost_category_DB_PC(PC_COST_CAT_DB_CURR_VERSION)
# programmecosting.upload_cost_category_DB_PC(PC_COST_CAT_DB_CURR_VERSION)
# programmecosting.create_cost_input_DB_PC(PC_COST_INPUT_DB_CURR_VERSION)
# programmecosting.upload_cost_input_DB_PC(PC_COST_INPUT_DB_CURR_VERSION)
# programmecosting.create_costing_section_DB_PC(PC_COSTING_SECT_DB_CURR_VERSION)
# programmecosting.upload_costing_section_DB_PC(PC_COSTING_SECT_DB_CURR_VERSION)
# programmecosting.create_activity_DB_PC(PC_ACTIVITY_DB_CURR_VERSION)
# programmecosting.upload_activity_DB_PC(PC_ACTIVITY_DB_CURR_VERSION)
# programmecosting.create_activity_line_item_DB_PC(PC_ACTIVITY_LINE_ITEM_DB_CURR_VERSION)
# programmecosting.upload_activity_line_item_DB_PC(PC_ACTIVITY_LINE_ITEM_DB_CURR_VERSION)

# budgetmapping.create_budget_DB_BG(BG_BUDGET_DB_CURR_VERSION)
# budgetmapping.upload_budget_DB_BG(BG_BUDGET_DB_CURR_VERSION)
# budgetmapping.create_budget_category_DB_BG(BG_BUDGET_CAT_DB_CURR_VERSION)
# budgetmapping.upload_budget_category_DB_BG(BG_BUDGET_CAT_DB_CURR_VERSION)
# budgetmapping.create_funding_framework_DB_BG(BG_FUND_FW_DB_CURR_VERSION)
# budgetmapping.upload_funding_framework_DB_BG(BG_FUND_FW_DB_CURR_VERSION)
# budgetmapping.create_funding_source_DB_BG(BG_FUND_SOURCE_DB_CURR_VERSION)
# budgetmapping.upload_funding_source_DB_BG(BG_FUND_SOURCE_DB_CURR_VERSION)
# budgetmapping.create_indicator_mapping_DB_BG(BG_INDICATOR_MAPPING_DB_CURR_VERSION)
# budgetmapping.upload_indicator_mapping_DB_BG(BG_INDICATOR_MAPPING_DB_CURR_VERSION)