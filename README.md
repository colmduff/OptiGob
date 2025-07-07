# optigob

[![PyPI version](https://img.shields.io/pypi/v/optigob.svg)](https://pypi.org/project/optigob/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/optigob.svg)](https://pypi.org/project/optigob/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/colmduff/OptiGob/ci.yml?branch=main)](https://github.com/colmduff/OptiGob/actions)

A land use change and environmental assessment tool based on preconfigured data animal population numbers based on negative emissions allowance.

---

## High-Level Architecture & Module Interaction

The `optigob` package is a modular land use and environmental assessment framework. It is designed to calculate, aggregate, and analyze greenhouse gas emissions, land use, protein, bioenergy, harvested wood products, and substitution impacts for both baseline and scenario cases. The system is built around a central API (`Optigob`), which coordinates specialized modules for each sector and data type.

### Module Structure

```
optigob/
├── budget_model/
│   ├── baseline_emissions.py
│   ├── emissions_budget.py
│   ├── landarea_budget.py
│   ├── econ_output.py
│   └── substitution.py
├── bioenergy/
│   └── bioenergy_budget.py
├── database/
│   └── ...
├── forest/
│   └── forest_budget.py
├── livestock/
│   └── livestock_budget.py
├── other_land/
│   ├── baseline_other_land.py
│   └── other_land_budget.py
├── protein_crops/
│   ├── __init__.py
│   └── protein_crops_budget.py
├── resource_manager/
│   └── optigob_data_manager.py
├── optigob.py
└── ...
```

### Core Modules and Their Roles

- **optigob/optigob.py**: Central interface (`Optigob` class) for retrieving all model outputs. Orchestrates calls to all other modules and provides unified access to results as dictionaries or tidy DataFrames.
- **resource_manager/optigob_data_manager.py**: Loads, validates, and provides access to all input data and configuration. Supplies data to all budget and output modules.
- **budget_model/emissions_budget.py**: Calculates scenario emissions (CO2e, CO2, CH4, N2O) by sector, including substitution impacts. Handles net zero logic and split gas configuration.
- **budget_model/baseline_emissions.py**: Provides baseline emissions by sector for all gases.
- **budget_model/landarea_budget.py**: Calculates land area (aggregated, disaggregated, HNV) by sector for baseline and scenario.
- **budget_model/econ_output.py**: Calculates protein, bioenergy, harvested wood products, and livestock population by sector.
- **budget_model/substitution.py**: Centralizes logic for substitution impacts (e.g., wood for fossil, protein crop substitution).
- **protein_crops/protein_crops_budget.py**: Handles protein crop area, yield, and protein output calculations.
- **livestock/livestock_budget.py**: Calculates livestock sector budgets, including emissions, land use, and protein.
- **forest/forest_budget.py**: Handles forest sector land area, emissions, and harvested wood product calculations.
- **bioenergy/bioenergy_budget.py**: Calculates bioenergy area and output by sector.
- **other_land/other_land_budget.py**: Handles other land types and their contributions to area and emissions.
- **database/**: Contains data loaders and helpers for accessing and managing input datasets.

### Module Interaction Diagram (Textual)

```text
[Optigob]
   |
   |-- [resource_manager/optigob_data_manager.py] <--- loads all input data
   |
   |-- [budget_model/emissions_budget.py] <--- uses data_manager, calls substitution.py
   |-- [budget_model/baseline_emissions.py]
   |-- [budget_model/landarea_budget.py]
   |-- [budget_model/econ_output.py]
   |-- [budget_model/substitution.py]
   |
   |-- [protein_crops/protein_crops_budget.py]
   |-- [livestock/livestock_budget.py]
   |-- [forest/forest_budget.py]
   |-- [bioenergy/bioenergy_budget.py]
   |-- [other_land/other_land_budget.py]
   |
   |-- [database/] (data loaders)
```

- The `Optigob` class is the main entry point. It receives a data manager instance, which loads all configuration and input data.
- Each budget/output module (emissions, land area, protein, etc.) is initialized with the data manager and provides sectoral and total results.
- Substitution logic is centralized in `substitution.py` and called by emissions and output modules as needed.
- Specialized sector modules (livestock, forest, protein crops, etc.) encapsulate sector-specific calculations and are used by the budget modules.

---

## Features

- Calculate total and sectoral CO2e, CO2, CH4, N2O emissions for baseline and scenario
- Calculate total and sectoral land area (aggregated, disaggregated, HNV)
- Calculate protein, bioenergy, and harvested wood product outputs by sector
- Centralized logic for substitution impacts (e.g., wood for fossil, protein crop substitution)
- Generate detailed tidy DataFrames for all outputs
- Easy integration with preconfigured data sources
- Modular, extensible architecture for new sectors or outputs

## Installation

To install the package, use pip:

```bash
pip install optigob
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

if __name__ == '__main__':
    main()
```

---

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`optigob` was created by Colm Duffy. It is licensed under the terms of the MIT license.

## Credits

`optigob` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).