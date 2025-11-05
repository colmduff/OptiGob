from pathlib import Path
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
from optigob.input_helper import InputHelper
from optigob.logger import configure_logging
import logging


def main():

    LOGPATH = str(Path('.') / 'data' / 'logs' / 'example_log.log')

    # Log to both console and file
    configure_logging(
        level=logging.INFO,
        log_to_file=str(LOGPATH)
    )

    print("#" * 50)
    print("OptiGob Budget Model Input Combinations")

    # Initialize the input helper
    helper = InputHelper()

    helper.print_readable_combos(12)

    data = './data/sip.yaml'
    # Initialize the data manager
    data_manager = OptiGobDataManager(data)

    # Create an instance of Optigob
    optigob = Optigob(data_manager)

    print("#" * 50)
    print("OptiGob Budget Model Input Combinations")
    
    # Get baseline and target populations
    print("#" * 50)
    print("GHG Emissions by Sector")
    print(optigob.get_total_emissions_co2e_by_sector())

    print(optigob.get_total_emissions_co2e_by_sector_df())

    print("#" * 50)
    print("Aggregated Total Land Area by Sector")

    print(optigob.get_aggregated_total_land_area_by_sector())
    print(optigob.get_aggregated_total_land_area_by_sector_df())

    print("#" * 50)
    print("Protein by Sector")

    print(optigob.get_total_protein_by_sector())
    print(optigob.get_total_protein_by_sector_df())

    print("#" * 50)
    print("Area by Sector")
    
    print(optigob.get_disaggregated_total_land_area_by_sector())
    print(optigob.get_disaggregated_total_land_area_by_sector_df())

    print("#" * 50)
    print("High Nature Value (HNV) Land Area by Sector")

    print(optigob.get_total_hnv_land_area_by_sector())
    print(optigob.get_total_hnv_land_area_by_sector_df())

    print("#" * 50)
    print("Bioenergy by Sector")
    print(optigob.get_bioenergy_by_sector())
    print(optigob.get_bioenergy_by_sector_df())

    print("#" * 50)
    print("HWP")
    print(optigob.get_hwp_volume())
    print(optigob.get_hwp_volume_df())

    print("#" * 50)
    print("Substitution")

    print(optigob.get_substitution_emission_by_sector_co2e())
    print(optigob.get_substitution_emission_by_sector_co2e_df())
    
    print("#" * 50)
    print("NZ Status")

    print(optigob.check_net_zero_status())

    print(f"total emissions co2e: {optigob.total_emission_co2e()} kt")

    print("#" * 50)
    print("Livestock Population")

    print(optigob.get_livestock_population())
    print(optigob.get_livestock_population_df())

    print("#" * 50)
    print("Livestock CH4 Emissions budget")
    print(optigob.get_livestock_split_gas_ch4_emission_budget())

    print("#" * 50)
    print("Livestock CO2e Emissions budget")
    print(optigob.get_livestock_co2e_emission_budget())

    print("#" * 50)
    print("AREA comparison")

    df = optigob.get_disaggregated_total_land_area_by_sector_df()
    print(df)
    print("\nSum of each column:")
    print(df.sum())


if __name__ == '__main__':
    main()