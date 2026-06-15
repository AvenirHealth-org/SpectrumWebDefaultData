
import Scripts.demproj as demproj

def DPRunScripts():
    user_input = input("Would you like to run DP scripts?  ")
    if user_input.lower() in ['y', 'yes']:
        try:
            ####### DemProj #######
            # demproj.write_UPD_db(DPUPDVersion)
            # demproj.upload_UPD_db(DPUPDVersion)

            # demproj.write_demproj_db(DPDatabaseVersion)
            # demproj.upload_demproj_db(DPDatabaseVersion)# test this before using
            # demproj.write_DP_population_db(DPInitialConditionsDBVersion)
            # demproj.upload_DP_population_db(DPInitialConditionsDBVersion)



            demproj.create_DP_subnationals('V2')
            demproj.upload_DP_subnationals('V2')
            print("DP scripts completed successfully.")
        except Exception as e:
            print(f"An error occurred while running DP scripts: {e}")
    else:
        print("Operation cancelled by user.")
