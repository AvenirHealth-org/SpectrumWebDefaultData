import Scripts.supplychain as supplychain


def LGRunScripts():

    user_input = input("Would you like to run LG scripts?  ")
    if user_input.lower() in ["y", "yes"]:
        try:
            # supplychain.create_default_cold_chain_DB_LG(LG_COLD_CHAIN_DB_CURR_VERSION)
            # supplychain.upload_default_cold_chain_DB_LG(LG_COLD_CHAIN_DB_CURR_VERSION)
            # supplychain.create_default_waste_management_DB_LG(LG_WASTE_MANAGEMENT_DB_CURR_VERSION)
            # supplychain.upload_default_waste_management_DB_LG(LG_WASTE_MANAGEMENT_DB_CURR_VERSION)
            print("LG scripts completed successfully.")
        except Exception as e:
            print(f"An error occurred while running LG scripts: {e}")
    else:
        print("Operation cancelled by user.")
