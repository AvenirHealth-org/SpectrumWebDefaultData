
import Scripts.tuberculosis as tuberculosis

def TBRunScripts():

    user_input = input("Would you like to run TB scripts?  ")
    if user_input.lower() in ['y', 'yes']:
        try:
            # Note if you run WHO country data then you should also run fort inputs and outputs afterwards
            # tuberculosis.create_TB_WHOCountryData('V6')
            # tuberculosis.upload_TB_WHOCountryData('V6')

            # tuberculosis.create_TB_fort_input('V7')
            # tuberculosis.upload_tb_fort_inputs_db('V7')

            # tuberculosis.create_TB_fort_outputs('V8')
            # tuberculosis.upload_tb_fort_outputs_db('V8')

            # tuberculosis.create_TB_subnational_list('V3')
            # tuberculosis.upload_TB_subnational_list('V3')

            # tuberculosis.create_TB_subnationals('V2')
            # tuberculosis.upload_TB_subnationals('V2')

            # tuberculosis.create_TB_DyanmicalModelData('V1')
            # tuberculosis.upload_TB_DyanmicalModelData('V1')

            # tuberculosis.create_TB_DiagEditorDefaults('V7')
            tuberculosis.upload_TB_DiagEditorDefaults('V7')

            # tuberculosis.create_TBScreeningDefaults('')
            # tuberculosis.upload_TBScreeningDefaults('')
            print("TB scripts completed successfully.")
        except Exception as e:
            print(f"An error occurred while running TB scripts: {e}")   
    else:
        print("Operation cancelled by user.")

        