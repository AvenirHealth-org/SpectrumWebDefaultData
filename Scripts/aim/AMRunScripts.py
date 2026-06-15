
import Scripts.aim as aim

def AMRunScripts():
    user_input = input("Would you like to run AIM scripts?  ")
    if user_input.lower() in ['y', 'yes']:
        try:
            ####### AIM #######
            # aim.write_aim_db('V8')
            # aim.upload_aim_db('V8')

            # aim.write_easyAIM_db('V5')
            # aim.upload_easyAIM_db('V5')

            # aim.write_CSAVR_db(AMCSAVRDatabaseVersion)
            # aim.upload_CSAVR_db(AMCSAVRDatabaseVersion)

            # aim.upload_aim_UNAIDSSummaryTemplate_db('V2')

            # aim uncertainty analysis
            # aim.upload_UA_db(DPUADatabaseVersion)

            # Prevention needs tool
            aim.CreatePreventionNeedsDB('V5')
            aim.UploadPreventionNeedsDB('V5')
            print("AIM scripts completed successfully.")
        except Exception as e:
            print(f"An error occurred while running AIM scripts: {e}")
    else:
        print("Operation cancelled by user.")