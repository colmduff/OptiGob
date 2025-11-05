
from pathlib import Path
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
from optigob.logger import configure_logging
import logging

def main():


    BUG1_PATH = str(Path('.') / 'data' / 'sip_bug1.yaml')
    BUG2_PATH = str(Path('.') / 'data' / 'sip_bug2.yaml')

    LOGPATH = str(Path('.') / 'data' / 'logs' / 'retest_log.log')

    # Log to both console and file
    configure_logging(
        level=logging.INFO,
        log_to_file=str(LOGPATH)
    )
    
    # Initialize the data manager
    bug1_data_manager = OptiGobDataManager(BUG1_PATH)

    # Create an instance of Optigob
    bug1_optigob = Optigob(bug1_data_manager)

    # Initialize the data manager
    bug2_data_manager = OptiGobDataManager(BUG2_PATH)

    # Create an instance of Optigob
    bug2_optigob = Optigob(bug2_data_manager)

        # Get baseline and target populations
    print("#" * 50)
    print("GHG Emissions by Sector")

    
    print("Bug1:")
    try:
        print(bug1_optigob.get_total_emissions_co2e_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    
    print("Bug2:")
    try:
        print(bug2_optigob.get_total_emissions_co2e_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    print("#" * 50)
    print("Aggregated Total Land Area by Sector")


    print("Bug1")
    try:
        print(bug1_optigob.get_aggregated_total_land_area_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")
    try:
        print(bug2_optigob.get_aggregated_total_land_area_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    print("#" * 50)
    print("Protein by Sector")

    print("Bug1")
    try:
        print(bug1_optigob.get_total_protein_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")
    try:
        print(bug2_optigob.get_total_protein_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    print("#" * 50)
    print("Area by Sector")
    
    print("Bug1")
    try:
        print(bug1_optigob.get_disaggregated_total_land_area_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")
    try:
        print(bug2_optigob.get_disaggregated_total_land_area_by_sector())
    except Exception as e:
        print(f"Error: {e}")


    print("#" * 50)
    print("High Nature Value (HNV) Land Area by Sector")

    print("Bug1")
    try:
        print(bug1_optigob.get_total_hnv_land_area_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")
    try:
        print(bug2_optigob.get_total_hnv_land_area_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    print("#" * 50)
    print("Bioenergy by Sector")

    print("Bug1")
    try:
        print(bug1_optigob.get_bioenergy_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")
    try:
        print(bug2_optigob.get_bioenergy_by_sector())
    except Exception as e:
        print(f"Error: {e}")

    print("#" * 50)
    print("HWP")

    print("Bug1")
    try:
        print(bug1_optigob.get_hwp_volume())
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")
    try:
        print(bug2_optigob.get_hwp_volume())
    except Exception as e:
        print(f"Error: {e}")

    print("#" * 50)
    print("Substitution")

    print("Bug1")
    try:
        print(bug1_optigob.get_substitution_emission_by_sector_co2e())
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")
    try:
        print(bug2_optigob.get_substitution_emission_by_sector_co2e())
    except Exception as e:
        print(f"Error: {e}")
    
    print("#" * 50)
    print("NZ Status")

    print("Bug1")
    try:
        print(bug1_optigob.check_net_zero_status())

        print(f"total emissions co2e: {bug1_optigob.total_emission_co2e()} kt")
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")

    try:
        print(bug2_optigob.check_net_zero_status())

        print(f"total emissions co2e: {bug2_optigob.total_emission_co2e()} kt")
    except Exception as e:
        print(f"Error: {e}")

    print("#" * 50)
    print("Livestock Population")

    print("Bug1")
    try:
        print(bug1_optigob.get_livestock_population())
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")
    try:
        print(bug2_optigob.get_livestock_population())
    except Exception as e:
        print(f"Error: {e}")

    print("#" * 50)
    print("Livestock CH4 Emissions budget")

    print("Bug1")
    
    try:
        print(bug1_optigob.get_livestock_split_gas_ch4_emission_budget())
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")
    try:
        print(bug2_optigob.get_livestock_split_gas_ch4_emission_budget())
    except Exception as e:
        print(f"Error: {e}")

    print("#" * 50)
    print("Livestock CO2e Emissions budget")

    print("Bug1")

    try:
        print(bug1_optigob.get_livestock_co2e_emission_budget())
    except Exception as e:
        print(f"Error: {e}")

    print("Bug2")
    try:
        print(bug2_optigob.get_livestock_co2e_emission_budget())
    except Exception as e:
        print(f"Error: {e}")

    print("#" * 50)
    print("AREA comparison")

    df = bug1_optigob.get_disaggregated_total_land_area_by_sector_df()
    print(df)
    print("\nSum of each column:")
    print(df.sum())

if __name__ == "__main__":
    main()