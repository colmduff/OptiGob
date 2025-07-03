# optigob

A land use change and environmental assessment tool based on preconfigured data animal population numbers based on negative emissions allowance.

## Features

- Calculate total CO2e emissions by sector
- Calculate total land area by sector
- Generate detailed dataframes for emissions and land area
- Easy integration with preconfigured data sources

## Installation

To install the package, use pip:

```bash
$ pip install optigob
```

## Usage

Here is a short example of how to use the `Optigob` class:

```python
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

def main():
    data = './data/sip.yaml'
    # Initialize the data manager
    data_manager = OptiGobDataManager(data)

    # Create an instance of Optigob
    optigob = Optigob(data_manager)

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

    print(optigob.get_substiution_emission_by_sector_co2e())
    print(optigob.get_substiution_emission_by_sector_co2e_df())
    
    print("#" * 50)
    print("NZ Status")

    print(optigob.check_net_zero_status())

    print(f"total emissions co2e: {optigob.total_emission_co2e()} kt")

    print("#" * 50)
    print("Livestock Population")

    print(optigob.get_livestock_population())
    print(optigob.get_livestock_population_df())

if __name__ == '__main__':
    main()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`optigob` was created by Colm Duffy. It is licensed under the terms of the MIT license.

## Credits

`optigob` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
