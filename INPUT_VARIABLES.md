# OptiGob Input Variables Reference

This document provides detailed explanations for each input variable used in the OptiGob framework. These variables are used to configure scenarios for land use, emissions, and environmental assessment.

## Important: Valid Parameter Combinations

**Not all parameter combinations are valid!** The system validates parameter combinations against the underlying database. For certain parameter groups (forest, organic soil, and abatement/productivity), only specific combinations that have been modeled are allowed.

To explore valid combinations before running your scenario:

```python
from optigob.input_helper import InputHelper
helper = InputHelper()

# View all valid combinations
helper.print_all_combos()

# Filter by type
helper.filter_combos(input_type='forest')
helper.filter_combos(input_type='organic_soil')
helper.filter_combos(input_type='abatement_and_productivity')
```

**Parameter Groups That Are Validated:**

1. **Forest Parameters** (all 4 must form a valid combination):
   - `afforestation_rate_kha_per_year`
   - `broadleaf_fraction`
   - `organic_soil_fraction`
   - `forest_harvest_intensity`

2. **Organic Soil Parameters** (both must form a valid combination):
   - `wetland_restored_frac`
   - `organic_soil_under_grass_frac`

3. **Abatement/Productivity Parameters** (both must form a valid combination):
   - `abatement_type`
   - `abatement_scenario`

If you provide an invalid combination, `OptiGobDataManager` will raise a `ValueError` with details about the invalid parameters and guidance on finding valid combinations.

---

## Input Variables

### AR
- **Description:** Area of afforestation/reforestation (in thousands of hectares, kha), as defined by the IPCC Assessment Report.
- **Type:** Numeric (int)
- **Usage:** Specifies AR conversion values. Currently AR5 or AR6

### split_gas
- **Description:** Whether to use split gas accounting for greenhouse gases (GHGs).
- **Type:** Boolean (`true` or `false`)
- **Usage:** If `true`, emissions target is set as a proportional reduction of baseline for CH~4~, with Net-Zero for N~2~O and CO~2~e ; if `false`, all are aggregated as CO~2~e.

### split_gas_frac
- **Description:** Fraction of emissions to be split under split gas accounting.
- **Type:** Numeric (float, 0–1)
- **Usage:** if `split_gas` is `true`, proportion of total baseline CH~4~ emissions to be reduced.

### target_year
- **Description:** The scenario's target year for projections or policy goals.
- **Type:** Integer (2030, 2050)
- **Range:** 2020 - 2050 (2100 in future iterations)
- **Usage:** Sets the year for which scenario results are calculated.

### abatement_type
- **Description:** The type of abatement strategy applied.
- **Type:** String (e.g., `frontier`, `macc`, `baseline`)
- **Usage:** Determines which mitigation approach is used in the scenario. See [table 1](#table-1-abatement-scenario-productivity-scenario). 

### abatement_scenario
- **Description:** Numeric code for the productivity level in the abatement scenario. Numbers are related to specific scenarios (`baseline`: 1,2,3; `macc`: 4,5,6; `frontier`: 7,8,9). Each sequence corresponds to `baseline productivity`, `moderate productivity` and `strong productivity` within the specified abatement scenario. See [table 1](#table-1-abatement-scenario-productivity-scenario).
- **Type:** Integer
- **Range:** 1-9
- **Usage:** Selects a specific abatement scenario configuration.

### livestock_ratio_type
- **Description:** The method for specifying livestock population ratios.
- **Type:** String (e.g., `dairy_per_beef`, `beef_per_dairy`)
- **Usage:** Determines the ration of dairy units to beef units, or the other way around.

### livestock_ratio_value
- **Description:** The value for the livestock ratio.
- **Type:** Numeric (float or int)
- **Usage:** Sets the ratio between livestock types (e.g., dairy to beef).

### forest_harvest_intensity
- **Description:** Intensity of forest harvesting.
- **Type:** String (e.g., `low`, `high`)
- **Usage:** Controls the level of harvesting in forest management scenarios.

### afforestation_rate_kha_per_year
- **Description:** Annual afforestation rate in thousands of hectares per year.
- **Type:** Numeric (float or int)
- **Usage:** Specifies the yearly rate of new forest establishment.

### broadleaf_fraction
- **Description:** Fraction of afforestation area planted with broadleaf species.
- **Type:** Numeric (float, 0–1)
- **Usage:** Sets the proportion of broadleaf trees in new forests.

### organic_soil_fraction
- **Description:** Fraction of land afforested area with organic soils.
- **Type:** Numeric (float, 0–1)
- **Usage:** Used to model emissions and sequestration on organic soils.

### beccs_included
- **Description:** Whether BECCS (Bioenergy with Carbon Capture and Storage) is included.
- **Type:** Boolean (`true` or `false`)
- **Usage:** If `true`, BECCS is part of the scenario.

### beccs_willow_area_multiplier
- **Description:** Multiplier for willow area used in BECCS scenarios.
- **Type:** Numeric (float)
- **Usage:** Scales the area of willow for BECCS calculations.

### wetland_restored_frac
- **Description:** Fraction of wetland area restored.
- **Type:** Numeric (float, 0–1)
- **Usage:** Sets the proportion of wetlands restored in the scenario.

### organic_soil_under_grass_frac
- **Description:** Fraction of organic soils under grassland rewetted.
- **Type:** Numeric (float, 0–1)
- **Usage:** Used for emissions calculations on grassland organic soils.

### biomethane_included
- **Description:** Whether biomethane production is included.
- **Type:** Boolean (`true` or `false`)
- **Usage:** If `true`, biomethane is considered in the scenario outputs.

### protein_crop_included
- **Description:** Whether protein crop production (peas and beans) is included.
- **Type:** Boolean (`true` or `false`)
- **Usage:** If `true`, protein crops are included in the scenario.

### protein_crop_multiplier
- **Description:** Multiplier for protein crop area or output.
- **Type:** Numeric (float)
- **Usage:** Scales the area or yield of protein crops.

### pig_and_poultry_multiplier
- **Description:** Multiplier for pig and poultry outputs, scales the output directly.
- **Type:** Numeric (float)
- **Usage:** Scales the output of pigs and poultry in the scenario.

### baseline_year
- **Description:** The baseline year for scenario comparison.
- **Type:** Integer (e.g., 2020)
- **Usage:** Sets the reference year for baseline calculations. Cannot be lower than 2020.

### baseline_dairy_pop
- **Description:** Baseline dairy cattle population (tens of thousands).
- **Type:** Numeric (float or int)
- **Usage:** Used as the starting value for dairy population in scenarios.

### baseline_beef_pop
- **Description:** Baseline beef cattle population (tens of thousands).
- **Type:** Numeric (float or int)
- **Usage:** Used as the starting value for beef population in scenarios.

---

## Valid Combinations

Not all combinations of these variables are valid. To explore valid input parameter combinations for your scenario, use the `InputHelper` class provided in [`src/optigob/input_helper.py`](src/optigob/input_helper.py). 

## Example usage:

```python
from optigob.input_helper import InputHelper
helper = InputHelper()
helper.print_all_combos()  # Print all valid combinations
df = helper.get_combos_df()  # Get as a DataFrame
filtered = helper.filter_combos(input_type="forest", broadleaf_frac=0.5)  # Filtered combos
```

This will help you construct valid input dictionaries for use with the OptiGob API.


#### Table 1. Abatement scenario, productivity scenario

| Scenario                           | Description                                                                                                                                                                                                                                            |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Baseline**                       | Zero additional abatement beyond 2020 baseline.                                                                                                                                                                                                        |
| **MACC**                           | Full implementation of agriculture abatement measures in the Teagasc 2023 MACC (equivalent to a 19% reduction in emissions across all gases, at a given level of production, i.e. excluding animal production efficiency measures).                    |
| **Frontier**                       | Implementation of the main measures identified as technically feasible in recent studies, with a focus on livestock system abatement from use of grass-clover swards, enteric methane inhibitors, anaerobic digestion, and manure emission inhibitors. |
| **Baseline productivity**          | Productivity maintained at 2020 levels.                                                                                                                                                                                                                |
| **Moderate productivity increase** | Milk output per cow increases by 15%, and beef slaughter age is reduced gradually by 50 days until 2050.                                                                                                                                               |
| **Strong productivity increase**   | Milk yield per cow increases by 30%, and beef slaughter age reduces gradually by 100 days until 2050.                                                                                                                                                  |
