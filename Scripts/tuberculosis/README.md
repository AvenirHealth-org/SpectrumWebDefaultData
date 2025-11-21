# TB Database Update Guide

This guide outlines the process for updating TB (Tuberculosis) databases in the Spectrum system.

**IMPORTANT:** If WHO data has changed then fort inputs and outputs needs to be redone

**IMPORTANT:** Don't upload data without approval of TB team. 

## Prerequisites

- Access to the Spectrum codebase
- Local development environment set up for Spectrum React client and Spectrum engine servers
- Appropriate permissions for beta deployment

## Step-by-Step Process

### 1. Update Version Numbers

Update version numbers in the following locations for all three database types:

**Database types to version:**
- **WHO data** - World Health Organization tuberculosis data
- **Fort inputs** - Fort model input parameters  
- **Fort outputs** - Fort model output data


```python
# Example version updates in GBVersions.py
TB_WHO_DB_VERSION = 'V6'
TB_FORT_INPUT_VERSION = 'V7'
TB_FORT_OUTPUT_VERSION = 'V7'
```

### 2. Test Run with Limited Countries

Run the database update scripts for a subset of countries using `TB_RUN_DEFAULT_COUNTRIES`:

```python
# Update scripts to use the test country list
TB_RUN_DEFAULT_COUNTRIES = ["ZMB", "IDN", "VNM"]

tuberculosis.create_TB_WHOCountryData('V6')
tuberculosis.upload_TB_WHOCountryData('V6')

tuberculosis.create_TB_fort_input('V7')
tuberculosis.upload_tb_fort_inputs_db('V7')

tuberculosis.create_TB_fort_outputs('V7')
tuberculosis.upload_tb_fort_outputs_db('V7')

```

**Scripts that may need modification:**
- WHO data extraction scripts
- Fort input generation scripts
- Fort output processing scripts

**Verify:**
- Scripts execute without errors
- Output data is generated correctly
- File formats and structures are maintained

### 3. Local Testing and Validation

Start the spectrum engine serves, TB client. 
Create a projection and calculate. 


**Testing checklist:**
- [ ] Input modvars are being created correctly
- [ ] TB notification data appears reasonable
- [ ] TB incidence calculations are within expected ranges
- [ ] No console errors or warnings
- [ ] Data loads properly in the UI
- [ ] Charts and visualizations render correctly

**Key files to verify:**
- `GBVersions.py` - Ensure version numbers are correct
- `TBConst.py` - Verify year ranges and constants are updated

### 4. Full Production Run

Once testing is successful, run the database update scripts for all countries:

```python
# Remove or comment out the country filter
TB_RUN_DEFAULT_COUNTRIES = None  # Run for all countries
```

**Execute in order:**
1. WHO data scripts
2. Fort inputs scripts  
3. Fort outputs scripts


## File Locations

```
Spectrum/
├── SpectrumCommon/Const/GB/
│   ├── GBConst.py
│   ├── GBVersions.py  
├── SpectrumCommon/Const/TB/
│   └── TBConst.py
└── DefaultData/Scripts/tuberculosis/
    ├── TBUploadWHOCountryData.py
    ├── TBUploadFortModelInputs.py
    └── TBUploadFortModelOutputs.py
```

## Notes

- Always backup existing databases before updating
- Document any script modifications made during the process
- Keep detailed logs of processing times and any errors encountered
- Coordinate with TB team for optimal testing windows