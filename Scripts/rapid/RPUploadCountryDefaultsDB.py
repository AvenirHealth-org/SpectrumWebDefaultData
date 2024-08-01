import os
import ujson
from itertools import islice
from openpyxl import load_workbook

from AvenirCommon.Database import GB_upload_file
from AvenirCommon.Logger import log

import DefaultData.DefaultDataUtil as ddu

import SpectrumCommon.Const.GB as gbc
import SpectrumCommon.Const.RP.RPConst as rpc
import SpectrumCommon.Const.RP.RPDatabaseConst as rpdbc 

# Column tag 'constants' for identifying columns.

RP_ISO_NUMERIC_COUNTRY_CODE        = '<ISO Numeric Country Code>'
RP_ISO_ALPHA_3_COUNTRY_CODE        = '<ISO Alpha-3 Country Code>'
RP_COUNTRY_NAME                    = '<Country Name>'
RP_CLASSIFICATION                  = '<Classification>'
RP_REGION                          = '<Region>'
RP_EXCH_RATE                       = '<Exchange Rate to USD>'
RP_HH_SIZE                         = '<Household Size (Overall)>'
RP_PERC_URBAN_INFORMAL             = '<Percent Urban Informal>'
RP_COST_STERILIZATION              = '<Cost Sterilization>'
RP_COST_IUD                        = '<Cost IUD>'
RP_COST_IMPLANT                    = '<Cost Implant>'
RP_COST_INJECTIONS                 = '<Cost Injections>'
RP_COST_PILL                       = '<Cost Pill>'
RP_COST_CONDOMS                    = '<Cost Condoms>'
RP_COST_INDIRECTS                  = '<Indirects>'
RP_AGE_START_PRIM                  = '<Age Start Primary>'
RP_AGE_END_PRIM                    = '<Age End Primary>'
RP_AGE_START_SEC                   = '<Age Start Secondary>'
RP_AGE_END_SEC                     = '<Age End Secondary>'
RP_PERC_ENROLL_PRIM                = '<Percent Enrollment (Primary)>'
RP_PRIM_ENROLL_FEMALES             = '<Primary Enrollment (Females)>'
RP_PRIM_ENROLL_MALES               = '<Primary Enrollment (Males)>'
RP_PERC_ENROLL_SEC                 = '<Percent Enrollment (Secondary)>'
RP_SEC_ENROLL_FEMALES              = '<Secondary Enrollment (Females)>'
RP_SEC_ENROLL_MALES                = '<Secondary Enrollment (Males)>'
RP_TEACHER_RATIO_PRIM              = '<Teacher Ratio (Primary)>'
RP_TEACHER_RATIO_SEC               = '<Teacher Ratio (Secondary)>'
RP_PRIM_COSTS                      = '<Primary Costs>'
RP_SEC_COSTS                       = '<Secondary Costs>'
RP_PRIM_TEACHER_SALARY             = '<Primary Teacher Salary>'
RP_SEC_TEACHER_SALARY              = '<Secondary Teacher Salary>'
RP_SKILLED_BIRTHS                  = '<Skilled Births>'
RP_ANC_4_PLUS                      = '<ANC 4 Plus>'
RP_PROFS                           = '<Profs>'
RP_DOCTOR_SALARY_PUBLIC            = '<Doctor Salary Public>'
RP_NURSE_SALARY_PUBLIC             = '<Nurse Salary Public>'
RP_SKILLED_BIRTH_COSTS             = '<Skilled Birth Costs>'
RP_ANC_COSTS                       = '<ANC Costs>'
RP_PERC_DOCTORS                    = '<Percent Doctors>'
RP_PERC_NURSES                     = '<Percent Nurses>'
RP_PERC_IMPROVED_WATER_SOURCE      = '<Percent Improved Water Source>'
RP_PERC_IMPROVED_SANI              = '<Percent Improved Sanitation>'
RP_UNIT_COST_1000_L_WATER          = '<Unit Cost per 1,000 Liters of Water>'
RP_CAP_COST_PP_IMPROVED_WATER      = '<Capital Cost PP Improved Water>'
RP_CAP_COST_PP_IMPROVED_SANI       = '<Capital Cost PP Improved Sanitation>'
RP_PERC_PEOPLE_PHASE_4_PLUS        = '<Percent People in Phase 4 Plus>'
RP_SEVERE_INSECURITY               = '<Severe Insecurity>'
RP_AREA_HARVESTED                  = '<Area Harvested>'
RP_STAPLE_PRODUCTION               = '<Staple Production (In Tons)>'
RP_DOMINANT_CROP                   = '<Dominant Crop (Maize, Wheat or Rice)>'
RP_AGRICULTURAL_LAND               = '<Agricultural Land (Hectares)>'
RP_CROPLAND_HECTARES               = '<Cropland Hectares>'
RP_STAPLE_ANNUAL_CONSUMP_PER_CAP   = '<Staple Annual Consumption per Capita (kg)>'
RP_PROD_COST_PER_TON_DOMINANT_CROP = '<Production Cost per Ton for Dominant Crop>'
RP_DAILY_COST_FOOD_AID_PER_PERSON  = '<Daily Cost of Food Aid per Person>'
RP_PERC_POP_ELECTRICITY            = '<Percent Pop Electricity>'
RP_ELECTRICITY_PROD_PER_CAP        = '<Electricity Produced per Capita>'
RP_COST_PER_KWH                    = '<Cost per KWh>'
RP_LCOE_0_PER_PERSON_PER_DAY       = '<LCOE 0 per Person per Day>'
RP_CLEAN_COOKING                   = '<Clean Cooking>'
RP_CLEAN_COOKING_CAP_COST          = '<Clean Cooking Capital Cost>'
RP_UNEMPLOYMENT                    = '<Unemployment>'
RP_GDP_PER_CAP                     = '<GDP per Capita>'
RP_AVG_GROWTH_RATE                 = '<Avg Growth Rate>'
RP_LABOR_MALES                     = '<Labor Males>'
RP_LABOR_FEMALES                   = '<Labor Females>'
RP_LABOR_BOTH                      = '<Labor Both>'
RP_YOUTH_NEED_ALL                  = '<Youth NEET All>'
RP_YOUTH_NEED_MALE                 = '<Youth NEET Male>'
RP_YOUTH_NEED_FEMALE               = '<Youth NEET Female>'
RP_1_DEGREE_GDP                    = '<1 Degree GDP>'
RP_1_DEGREE_STAPLE                 = '<1 Degree Staple>'
RP_2_DEGREE_STAPLE                 = '<2 Degree Staple>'
RP_3_DEGREE_STAPLE                 = '<3 Degree Staple>'
RP_1_DEGREE_ON_ENERGY              = '<1 Degree on Energy>'

def create_country_defaults_DB_RP(version = str):

    log('Creating RP country defaults DB')

    country_list = []
    wb = load_workbook(ddu.get_source_data_path(gbc.GB_RP) + '\RPModData.xlsx')
    sheet = wb[rpc.RP_COUNTRY_DEFAULTS_DB_NAME]
    
    tag_row = 1
    first_data_row = 2
    first_data_col = 4
    num_rows = sheet.max_row
    num_cols = sheet.max_column

    # Establish tag columns.  Not many, so don't bother searching for them.
    iso_alpha_3_country_code_col = 2

    classification_col = gbc.GB_NOT_FOUND                 
    region_col = gbc.GB_NOT_FOUND               
    exch_rate_col = gbc.GB_NOT_FOUND              
    HH_size_col = gbc.GB_NOT_FOUND           
    perc_urban_informal_col = gbc.GB_NOT_FOUND          
    cost_sterilization_col = gbc.GB_NOT_FOUND              
    cost_IUD_col = gbc.GB_NOT_FOUND                
    cost_implant_col = gbc.GB_NOT_FOUND                  
    cost_injections_col = gbc.GB_NOT_FOUND                 
    cost_pill_col = gbc.GB_NOT_FOUND                      
    cost_condoms_col = gbc.GB_NOT_FOUND                   
    cost_indirects_col = gbc.GB_NOT_FOUND                  
    age_start_prim_col = gbc.GB_NOT_FOUND                 
    age_end_prim_col = gbc.GB_NOT_FOUND                   
    age_start_sec_col = gbc.GB_NOT_FOUND                  
    age_end_sec_col = gbc.GB_NOT_FOUND                    
    perc_enroll_prim_col = gbc.GB_NOT_FOUND                
    prim_enroll_females_col = gbc.GB_NOT_FOUND             
    prim_enroll_males_col = gbc.GB_NOT_FOUND              
    perc_enroll_sec_col  = gbc.GB_NOT_FOUND                
    sec_enroll_females_col = gbc.GB_NOT_FOUND              
    sec_enroll_males_col = gbc.GB_NOT_FOUND                
    TEACHER_RATIO_PRIM = gbc.GB_NOT_FOUND              
    TEACHER_RATIO_SEC  = gbc.GB_NOT_FOUND              
    PRIM_COSTS = gbc.GB_NOT_FOUND                     
    SEC_COSTS  = gbc.GB_NOT_FOUND                      
    PRIM_TEACHER_SALARY = gbc.GB_NOT_FOUND             
    SEC_TEACHER_SALARY = gbc.GB_NOT_FOUND              
    SKILLED_BIRTHS = gbc.GB_NOT_FOUND                  
    ANC_4_PLUS = gbc.GB_NOT_FOUND                      
    PROFS = gbc.GB_NOT_FOUND                           
    DOCTOR_SALARY_PUBLIC = gbc.GB_NOT_FOUND            
    NURSE_SALARY_PUBLIC = gbc.GB_NOT_FOUND             
    SKILLED_BIRTH_COSTS = gbc.GB_NOT_FOUND             
    ANC_COSTS  = gbc.GB_NOT_FOUND                      
    PERC_DOCTORS = gbc.GB_NOT_FOUND                    
    PERC_NURSES = gbc.GB_NOT_FOUND                    
    PERC_IMPROVED_WATER_SOURCE = gbc.GB_NOT_FOUND    
    PERC_IMPROVED_SANI = gbc.GB_NOT_FOUND           
    UNIT_COST_1000_L_WATER  = gbc.GB_NOT_FOUND         
    CAP_COST_PP_IMPROVED_WATER = gbc.GB_NOT_FOUND     
    CAP_COST_PP_IMPROVED_SANI = gbc.GB_NOT_FOUND     
    PERC_PEOPLE_PHASE_4_PLUS = gbc.GB_NOT_FOUND      
    SEVERE_INSECURITY = gbc.GB_NOT_FOUND            
    AREA_HARVESTED = gbc.GB_NOT_FOUND              
    STAPLE_PRODUCTION  = gbc.GB_NOT_FOUND              
    DOMINANT_CROP = gbc.GB_NOT_FOUND              
    AGRICULTURAL_LAND = gbc.GB_NOT_FOUND             
    CROPLAND_HECTARES = gbc.GB_NOT_FOUND              
    STAPLE_ANNUAL_CONSUMP_PER_CAP = gbc.GB_NOT_FOUND   
    PROD_COST_PER_TON_DOMINANT_CROP = gbc.GB_NOT_FOUND 
    DAILY_COST_FOOD_AID_PER_PERSON = gbc.GB_NOT_FOUND 
    PERC_POP_ELECTRICITY  = gbc.GB_NOT_FOUND          
    ELECTRICITY_PROD_PER_CAP = gbc.GB_NOT_FOUND        
    COST_PER_KWH = gbc.GB_NOT_FOUND       
    LCOE_0_PER_PERSON_PER_DAY = gbc.GB_NOT_FOUND      
    CLEAN_COOKING = gbc.GB_NOT_FOUND       
    CLEAN_COOKING_CAP_COST = gbc.GB_NOT_FOUND       
    UNEMPLOYMENT = gbc.GB_NOT_FOUND                 
    GDP_PER_CAP = gbc.GB_NOT_FOUND                   
    AVG_GROWTH_RATE = gbc.GB_NOT_FOUND                
    LABOR_MALES = gbc.GB_NOT_FOUND                 
    LABOR_FEMALES = gbc.GB_NOT_FOUND                 
    LABOR_BOTH = gbc.GB_NOT_FOUND                 
    YOUTH_NEED_ALL = gbc.GB_NOT_FOUND                 
    YOUTH_NEED_MALE = gbc.GB_NOT_FOUND                
    YOUTH_NEED_FEMALE = gbc.GB_NOT_FOUND              
    1_DEGREE_GDP = gbc.GB_NOT_FOUND              
    1_DEGREE_STAPLE = gbc.GB_NOT_FOUND            
    2_DEGREE_STAPLE = gbc.GB_NOT_FOUND            
    3_DEGREE_STAPLE = gbc.GB_NOT_FOUND             
    1_DEGREE_ON_ENERGY = gbc.GB_NOT_FOUND            




    # Get each row from the sheet and create a dictionary for each each country
    for row in islice(sheet.values, first_data_row - 1, num_rows):
        country_dict = {}
        intervention_list = []

        iso3 = row[iso_alpha_3_country_code_col - 1]

        if iso3 != None:
            country_dict[icdbc.IC_ISO_ALPHA_3_COUNTRY_CODE_KEY_PINDB] = iso3

            for col, col_val in enumerate(row):
                if col >= (first_data_col - 1):

                    # Single values
                    if span_row_list[col] == IC_SPAN_SINGLE:
                        intervention_dict = {}
                        intervention_dict[icdbc.IC_INTERV_MST_ID_KEY_PINDB] = interv_mstID_row_list[col]
                        intervention_dict[icdbc.IC_PIN_KEY_PINDB] = col_val
                        intervention_list.append(intervention_dict)
                        #log(intervention_dict)

                    # Values by age group
                    elif span_row_list[col] != IC_SPAN_SKIP:
                        # First column
                        if span_row_list[col] == IC_SPAN_START:
                            intervention_dict = {}
                            intervention_dict[icdbc.IC_INTERV_MST_ID_KEY_PINDB] = interv_mstID_row_list[col]
                            intervention_dict[icdbc.IC_PIN_KEY_PINDB] = []
                            intervention_dict[icdbc.IC_PIN_KEY_PINDB].append(col_val)
                        
                        # Last column
                        elif span_row_list[col] == IC_SPAN_END:
                            intervention_dict[icdbc.IC_PIN_KEY_PINDB].append(col_val)
                            intervention_list.append(intervention_dict)
                            #log(intervention_dict)

                        else:
                            intervention_dict[icdbc.IC_PIN_KEY_PINDB].append(col_val)

            country_dict[icdbc.IC_INTERVENTION_LIST_KEY_PINDB] = intervention_list
            country_list.append(country_dict)

    RP_JSON_data_path = ddu.get_JSON_data_path(gbc.GB_RP) + '\\' + rpc.RP_COUNTRY_DEFAULTS_DB_DIR
    os.makedirs(RP_JSON_data_path + '\\', exist_ok = True)
    
    for country_obj in country_list:    
        iso3 = country_obj[rpdbc.RP_ISO_ALPHA_3_COUNTRY_CODE_KEY_CDDB]
        with open(RP_JSON_data_path + '\\' + iso3 + '_' + version + '.' + gbc.GB_JSON, 'w') as f:
            ujson.dump(country_obj, f)

    log('Finished RP country defaults DB')

def upload_country_defaults_DB_RP(version):
    walk_path = ddu.get_JSON_data_path(gbc.GB_RP) + '\\' + rpc.RP_COUNTRY_DEFAULTS_DB_DIR + '\\'
    ddu.uploadFilesInDir(gbc.GB_RP_CONTAINER, walk_path, version, rpc.RP_COUNTRY_DEFAULTS_DB_DIR + '\\')
    log('Uploaded RP country defaults DB')
            
