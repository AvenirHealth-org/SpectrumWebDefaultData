# fmt: off
# import Scripts.globals as globals
# import Scripts.aim as aim
# import Scripts.demproj as demproj
# from Scripts import interventions
# import Scripts.famplan as famplan
# import Scripts.rapid as rapid
# import Scripts.tuberculosis as tuberculosis
# import Scripts.interventions as interventions
# import Scripts.interventioncosting as interventioncosting
# import Scripts.list as list
# import Scripts.ohtcore as ihtcore
# import Scripts.humanresources as humanresources
# import Scripts.infrastructure as infrastructure
# import Scripts.programmecosting as programmecosting
# import Scripts.budgetmapping as budgetmapping
# import Scripts.supplychain as supplychain
# import Scripts.famplan as famplan

from SpectrumCommon.Const.GB import *
from SpectrumCommon.Const.DP.DPConst import *
from SpectrumCommon.Const.FP import *
from SpectrumCommon.Const.RP.RPConst import *
from SpectrumCommon.Const.CS.CSConst import *
from SpectrumCommon.Const.IV.IVConst import *
from SpectrumCommon.Const.IC.ICConst import *
from SpectrumCommon.Const.IH.IHConst import *
from SpectrumCommon.Const.HW.HWConst import *
from SpectrumCommon.Const.IS.ISConst import *
from SpectrumCommon.Const.PC.PCConst import *
from SpectrumCommon.Const.BG.BGConst import *
from SpectrumCommon.Const.LG.LGConst import *

from AvenirCommon.Keys import store_keys_in_env

# from Scripts.globals import GBRunScripts

store_keys_in_env()
from AvenirCommon.Logger import initialise_logger
initialise_logger(
    program="DefaultData",
    env="development"
)

# GBRunScripts()


# aim.AMRunScripts()
# demproj.DPRunScripts()

# famplan.FPRunScripts()


####### Rapid #######
# rapid.create_country_defaults_DB_RP(RP_COUNTRY_DEFAULTS_DB_CURR_VERSION)
# rapid.upload_country_defaults_DB_RP(RP_COUNTRY_DEFAULTS_DB_CURR_VERSION)
# rapid.create_country_defaults_sources_DB_RP(RP_COUNTRY_DEFAULTS_SOURCES_DB_CURR_VERSION)
# rapid.upload_country_defaults_sources_DB_RP(RP_COUNTRY_DEFAULTS_SOURCES_DB_CURR_VERSION)
# rapid.create_contraceptive_use_DBs_RP()
# rapid.upload_contraceptive_use_DBs_RP()
# rapid.create_SSP_temperature_DBs_RP()
# rapid.upload_SSP_temperature_DBs_RP()
# rapid.create_urban_DB_RP(RP_URBAN_DB_CURR_VERSION)
# rapid.upload_urban_DB_RP(RP_URBAN_DB_CURR_VERSION)

# tuberculosis.TBRunScripts()

# interventions.create_intervention_DB_IV(IV_IH_INTERVENTION_DB_CURR_VERSION, GB_IH)
# interventions.upload_intervention_DB_IV(IV_IH_INTERVENTION_DB_CURR_VERSION, GB_IH)
# interventions.create_group_DB_IV(IV_IH_GROUP_DB_CURR_VERSION, GB_IH)
# interventions.upload_group_DB_IV(IV_IH_GROUP_DB_CURR_VERSION, GB_IH)

# interventions.create_intervention_DB_IV(IV_TI_INTERVENTION_DB_CURR_VERSION, GB_TI)
# interventions.upload_intervention_DB_IV(IV_TI_INTERVENTION_DB_CURR_VERSION, GB_TI)
# interventions.create_group_DB_IV(IV_TI_GROUP_DB_CURR_VERSION, GB_TI)
# interventions.upload_group_DB_IV(IV_TI_GROUP_DB_CURR_VERSION, GB_TI)

# interventions.create_intervention_DB_IV("V23", GB_CS)
# interventions.upload_intervention_DB_IV("V23", GB_CS)
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

# supplychain.LGRunScripts()

####### LiST  #######
# list.create_DefaultData() 
# list.create_DefaultWHOData() 
# list.create_IVDefaultData() 
# list.create_IVDefaultWHOData() 
# list.create_GNI_Per_Cap()
# list.create_Readiness() 
# list.create_CSection_Cov() 
# list.create_DiarrShigella() 
# list.create_dataByCountry(CS_Interpolated)
# list.create_dataByCountry(CS_Uninterpolated)
# list.create_regionalValues()
# list.create_SubnatData()
# list.create_MissOpData()
# list.uploadDatabaseFiles(DefaultData)
# list.uploadDatabaseFiles(DefaultWHOData)
# list.uploadDatabaseFiles(IVDefaultData)
# list.uploadDatabaseFiles(IVDefaultWHOData)
# list.uploadDatabaseFiles(GNI_Per_Cap)
# list.uploadDatabaseFiles(Readiness)
# list.uploadDatabaseFiles(CSection_Cov)
# list.uploadDatabaseFiles(DiarrShigella)
# list.uploadDatabaseFiles(DataByCountry)
# list.uploadDatabaseFiles(DBC_DataPoints)
# list.uploadDatabaseFiles(RegionData)
# list.uploadDatabaseFiles(SubnatData)
# list.uploadDatabaseFiles(SubnatMetaData)
# list.uploadDatabaseFiles(MissOpData)

# humanresources.create_staff_salaries_DB_HW(HW_STAFF_SALARIES_DB_CURR_VERSION)
# humanresources.upload_staff_salaries_DB_HW(HW_STAFF_SALARIES_DB_CURR_VERSION)

# infrastructure.create_facility_equipment_and_group_DBs_IS(IS_FACILITY_EQUIP_DB_CURR_VERSION)
# infrastructure.upload_facility_equipment_and_group_DBs_IS(IS_FACILITY_EQUIP_DB_CURR_VERSION)

# programmecosting.create_cost_category_DB_PC(PC_COST_CAT_DB_CURR_VERSION)
# programmecosting.upload_cost_category_DB_PC(PC_COST_CAT_DB_CURR_VERSION)
# programmecosting.create_cost_input_DB_PC() #('Testing')
# programmecosting.upload_cost_input_DB_PC() #('Testing')
# programmecosting.create_costing_section_DB_PC(PC_COSTING_SECT_DB_CURR_VERSION)
# programmecosting.upload_costing_section_DB_PC(PC_COSTING_SECT_DB_CURR_VERSION)
# programmecosting.create_activity_DB_PC(PC_ACTIVITY_DB_CURR_VERSION)
# programmecosting.upload_activity_DB_PC(PC_ACTIVITY_DB_CURR_VERSION)
# programmecosting.create_activity_line_item_DB_PC() #('Testing')
# programmecosting.upload_activity_line_item_DB_PC() #('Testing')
# programmecosting.create_PPLI_activity_line_item_DB_PC(PC_PPLI_ACTIVITY_LINE_ITEM_DB_CURR_VERSION)
# programmecosting.upload_PPLI_activity_line_item_DB_PC(PC_PPLI_ACTIVITY_LINE_ITEM_DB_CURR_VERSION)
# programmecosting.create_PPLI_phase_DB_PC(PC_PPLI_PHASE_DB_CURR_VERSION)
# programmecosting.upload_PPLI_phase_DB_PC(PC_PPLI_PHASE_DB_CURR_VERSION)
# programmecosting.create_PPLI_taxation_DB_PC(PC_PPLI_TAXATION_DB_CURR_VERSION)
# programmecosting.upload_PPLI_taxation_DB_PC(PC_PPLI_TAXATION_DB_CURR_VERSION)

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
