
import Scripts.famplan  as famplan

# from SpectrumCommon.Const.GB import *
from SpectrumCommon.Const.FP import *

def FPRunScripts():
    user_input = input("Would you like to run FP scripts?  ")
    if user_input.lower() in ['y', 'yes']:
        try:
            ####### FP #######
            for mode in [FP_All, FP_MAR, FP_MARUMSA, FP_AllUninterpolated, FP_MARUninterpolated, FP_MARUMSAUninterpolated]:
                # famplan.create_famplan_db('V3', mode) 
                famplan.upload_famplan_db('V3', mode)
            # famplan.upload_famplan_db('V8')


            # effectiveness
            # famplan.create_famplan_effectiveness('V5')
            # famplan.upload_famplan_effectiveness('V5')
            print("FP scripts completed successfully.")
        except Exception as e:
            print(f"An error occurred while running FP scripts: {e}")
    else:
        print("Operation cancelled by user.")