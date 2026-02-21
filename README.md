# optigob

[![PyPI version](https://img.shields.io/pypi/v/optigob.svg)](https://pypi.org/project/optigob/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/optigob.svg)](https://pypi.org/project/optigob/)
[![Documentation Status](https://readthedocs.org/projects/optigob/badge/?version=latest)](https://optigob.readthedocs.io/en/latest/?badge=latest)

[GitHub](https://github.com/colmduff/OptiGob) |
[Documentation](https://optigob.readthedocs.io/en/latest/) |

`OptiGob` is a Python-based decision support tool for exploring Ireland's agriculture, forestry, and other land use (AFOLU) sector under different climate and land use transition pathways. It combines pre-computed scenario data from [GOBLIN Lite](https://github.com/colmduff/goblin_lite) (agriculture and land use), FERS-CBM (forestry carbon balance), and LCAD2.0 (anaerobic digestion) into a single interface that optimises livestock populations subject to land and emissions constraints — without requiring users to run the upstream modelling chains. It is designed for researchers, policymakers, and educators investigating environmental and economic trade-offs associated with net-zero and split-gas emissions targets.

---

## High-Level Architecture & Module Interaction

The `optigob` package is a modular land use and environmental assessment framework. It calculates greenhouse gas emissions, land use, protein output, bioenergy, harvested wood products, and substitution impacts for both baseline and scenario cases. The system is built around a central API (`Optigob`), which coordinates specialised modules for each sector and data type.

### Module Structure

```
optigob/
├── budget_model/
│   ├── baseline_emissions.py
│   ├── emissions_budget.py
│   ├── landarea_budget.py
│   └── econ_output.py
├── substitution/
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
- **substitution/substitution.py**: Centralizes logic for substitution impacts (e.g., wood for fossil, protein crop substitution).
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
   |-- [substitution/substitution.py]
   |
   |-- [protein_crops/protein_crops_budget.py]
   |-- [livestock/livestock_budget.py]
   |-- [forest/forest_budget.py]
   |-- [bioenergy/bioenergy_budget.py]
   |-- [other_land/other_land_budget.py]
   |-- [static_ag/static_ag_budget.py]
   |
   |-- [database/] (data loaders)
```

- The `Optigob` class is the main entry point. It receives a data manager instance, which loads all configuration and input data.
- Each budget/output module (emissions, land area, protein, etc.) is initialized with the data manager and provides sectoral and total results.
- Substitution logic is centralized in `substitution.py` and called by emissions and output modules as needed.
- Specialized sector modules (livestock, forest, protein crops, etc.) encapsulate sector-specific calculations and are used by the budget modules.

### Input Data and Default Database

`optigob` ships with a pre-built SQLite database (`src/optigob/database/optigob_default_0.1.1.db`) that is installed automatically with the package. **No additional data download is required.**

#### Data provenance

The bundled database does not contain raw observational data. It contains **derived scenario scaler tables** generated by three upstream, sector-specific models:

| Upstream model | Domain | Reference |
|---|---|---|
| [GOBLIN Lite](https://github.com/colmduff/goblin_lite) | Agriculture and land use emissions, areas, livestock productivity | Duffy et al. (2022, 2024) |
| [FERS-CBM](https://www.ucd.ie/forestecosystemresearch/) | Forest carbon balance (afforestation, existing forest, harvested wood) | Black et al. (2025); Kurz et al. (2008) |
| [LCAD2.0](https://github.com/GOBLIN-Proj/lcad_gob) | Anaerobic digestion area, emissions, and bioenergy output | Martinez-Acre et al. (2025) |

These models were run across a defined set of valid parameter combinations for **Ireland**, and reflect three levels of abatement (Baseline, MACC, Frontier). The resulting scaler tables were stored in the SQLite database. At runtime, `optigob` queries these scalers to parameterise its optimisation model — effectively acting as a surrogate that stitches together pre-computed sectoral outputs without re-running the upstream models.

#### Database contents

The database contains scaler tables for:

- Livestock emissions, area, and protein (by species, abatement type, productivity tier)
- Forest emissions, area, harvested wood products, and wood CCS
- Organic soil emissions and area
- Anaerobic digestion emissions and area
- Protein crop emissions, area, and protein output
- Willow bioenergy area and output
- Substitution impacts (wood-for-fossil, crop-for-animal protein)

#### Predefined combinations

Not all parameter combinations are valid — only those that were modelled by the upstream tools exist in the database. Use the `InputHelper` class to explore valid combinations:

```python
from optigob.input_helper import InputHelper
helper = InputHelper()
helper.print_all_combos()  # View all valid parameter sets
```

See `INPUT_VARIABLES.md` for full parameter definitions and validation requirements.

#### Using a custom database

While the default database is supplied, users can update it or supply a custom database using `DatabaseManager`:

```python
from optigob.resource_manager.database_manager import DatabaseManager
db = DatabaseManager(database_path="/path/to/custom_database.db")
```

The custom database must follow the same table schema as the default.

---

## Features

- Calculate total and sectoral CO2e, CO2, CH4, N2O emissions for baseline and scenario
- Calculate total and sectoral land area (aggregated, disaggregated, HNV)
- Calculate protein, bioenergy, and harvested wood product outputs
- Centralized logic for substitution impacts (e.g., wood for fossil, protein crop substitution)
- Generate detailed DataFrames for all outputs
- Default database supports modelling up to 2050. Users can extend scenarios beyond 2050 by supplying a custom database.

## Installation

To install the package, use pip:

```bash
pip install "optigob[solvers]"
```

if you would prefer to use an alternative solver to HiGHS, the install command is: 

```bash
pip install optigob
```

Be sure to specify the solver in "solver_name" in the SIP.yaml.

For example: 

```yaml
solver_name: "highs"
```

## Usage

Here is some example input data:

```yaml
    solver_name: "highs"
    AR: 5
    split_gas: true
    split_gas_frac: 0.3
    target_year: 2050
    abatement_type: "frontier"
    abatement_scenario: 9
    livestock_ratio_type: "dairy_per_beef"
    livestock_ratio_value: 10
    forest_harvest_intensity: low
    afforestation_rate_kha_per_year: 16
    broadleaf_fraction: 0.3
    organic_soil_fraction: 0
    beccs_included: true
    beccs_willow_area_multiplier: 1.5
    wetland_restored_frac: 0.9
    organic_soil_under_grass_frac: 0.5
    biomethane_included: true
    protein_crop_included: false
    protein_crop_multiplier: 0
    pig_and_poultry_multiplier: 1.2
    baseline_year: 2020
    baseline_dairy_pop: 156.8
    baseline_beef_pop: 98.4
```

Here is a short example of how to use the `Optigob` class:

```python
from pathlib import Path
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
from optigob.input_helper import InputHelper
from optigob.logger import configure_logging
import logging


def main():

    # add a path to for a log file, if none is provided, messages are returned to the terminal 
    LOGPATH = str(Path('.') / 'data' / 'logs' / 'example_log.log')

    # Logger will capture critical information on scenarios. 
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
```

---

## Future Releases

`OptiGob` is designed to operate using a pre-generated SQLite scenario database. The current release ships with a default database derived from upstream sector models (GOBLIN Lite, FERS-CBM, LCAD2.0).

The underlying architecture already separates data generation from optimisation logic, and the `DatabaseManager` class accepts a custom database path (see [Using a custom database](#using-a-custom-database)). However, constructing a compatible database currently requires familiarity with the expected schema and upstream modelling workflows.

Future releases will focus on making this capability more accessible, including:

- Documentation and worked examples for modifying the existing database or replacing it with alternative datasets (e.g., for different national or regional contexts),
- Tooling to help users regenerate compatible scenario databases from updated upstream models,
- Validation utilities for verifying custom databases against the expected schema.

This is an area of active development. Users interested in building custom databases for their own contexts are welcome to get in touch.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`optigob` was created by Colm Duffy. It is licensed under the terms of the MIT license.

## Credits

`optigob` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
