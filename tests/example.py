from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager


def main():
    data = './data/sip.yaml'
    # Initialize the data manager
    data_manager = OptiGobDataManager(data)

    # Create an instance of Optigob
    optigob = Optigob(data_manager)

    # Get baseline and target populations
    print(optigob.get_total_emissions_co2e_by_sector())

    print(optigob.get_total_emissions_co2e_by_sector_df())

    print(optigob.get_total_land_area_by_sector())

    print(optigob.get_total_land_area_by_sector_df())

    print(optigob.get_total_protein_by_sector())

    print(optigob.get_total_protein_by_sector_df())

if __name__ == '__main__':
    main()