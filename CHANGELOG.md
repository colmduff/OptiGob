# Changelog

<!--next-version-placeholder-->

## v0.1.4 (05/11/2025)

### Features

- **Logging System**: Implemented comprehensive logging system with `logger.py` module
  - Added `get_logger()` and `configure_logging()` functions for user control
  - All warnings, errors, and info messages now use Python's standard logging module
  - Users can control logging level (DEBUG, INFO, WARNING, ERROR) and output destination
  - Support for logging to files

- **Enhanced Error Messages**: Improved all ValueError exceptions with specific context
  - Parameter validation errors include specific parameter names and values
  - Database query failures show exactly which parameters were searched
  - Example: "No matching livestock emission scaler found for: year=2050, system=Dairy, gas=CH4, scenario=1, abatement=1"

### Bug Fixes

- **Parameter Combination Validation**: Added comprehensive validation for parameter combinations
  - **Forest parameters**: Validates combinations of afforestation_rate, broadleaf_fraction, organic_soil_fraction, and forest_harvest_intensity (12 valid combinations)
  - **Organic soil parameters**: Validates combinations of wetland_restored_frac and organic_soil_under_grass_frac (3 valid combinations)
  - **Abatement/productivity parameters**: Validates combinations of abatement_type and abatement_scenario (9 valid combinations)
  - Validation only triggers when all parameters in a group are provided together
  - Provides early fail with clear error messages referencing `InputHelper` for discovering valid combinations
  - Prevents running expensive optimizations with invalid parameter combinations that don't exist in database

- **split_gas_frac Validation**: Added validation for `split_gas_frac` parameter
  - Logs warning when `split_gas=False` but `split_gas_frac` is set (parameter ignored)
  - Raises `ValueError` when `split_gas=True` but `split_gas_frac` is invalid (must be in range 0 < x < 1)

- **CH4 Budget Check**: Added pre-flight validation before optimization
  - Logs detailed warning when CH4 budget is exhausted by non-livestock emissions
  - Returns zero livestock and continues (allows batch processing)
  - Warning includes breakdown of all CH4 sources and actionable suggestions

- **Zero CO2e Budget**: Added informational messaging for zero livestock scenarios
  - Logs detailed explanation when CO2e budget doesn't allow livestock
  - Clarifies that zero livestock is correct, not an error

- **Infeasible Optimization**: Fixed crash in optimization when no feasible solution exists
  - Returns `OptimisationResult` with `status="infeasible"` instead of crashing
  - Prevents `TypeError` from NoneType multiplication

### Testing

- Added comprehensive input validation test suite (`tests/test_input_validation.py`)
  - Tests all three parameter groups: forest, organic soil, and abatement/productivity
  - Tests valid and invalid combinations for each group
  - Tests combined parameter validation across multiple groups
  - Tests error message quality and helpfulness
- Added bug fix test suite (`tests/test_bugs_enhanced.py`)
- Added test scenarios (`tests/data/sip_bug1.yaml`, `tests/data/sip_bug2.yaml`)
- Added zero budget tests (`tests/test_zero_budget_message.py`, `tests/test_co2e_budget_confirmation.py`)

### Documentation

- **Read the Docs Migration**: Documentation now hosted at <https://optigob.readthedocs.io/en/latest/>
- **Logging Guide**: Added comprehensive logging documentation
  - `tests/data/logs/LOGGING_GUIDE.md` - beginner-friendly guide to logging
  - `tests/logging_example.py` - 6 interactive examples
  - `tests/data/logs/IMPLEMENTATION_SUMMARY.md` - technical reference
- **CLAUDE.md**: Added "Logging" section and updated "Error Handling" section with current behavior
- Documented all bug fixes, input validation, and zero budget scenarios

## v0.1.3 (11/07/2025)

- Added `InputHelper` class for user-friendly querying and filtering of valid input parameter combinations for scenarios.
- Added `input_helper.py` module and comprehensive documentation for input query utilities.
- Added new test files for `InputQuery` and `InputHelper` (prints all combos and filtering to screen).
- Improved and standardized module-level and class-level docstrings for `input_query.py` and related modules.
- Added draw.io-compatible architecture diagram (flow.xml) for model documentation.
- Expanded and clarified README with module structure, architecture, and usage examples.
- Improved scenario and baseline area accounting and documentation in `landarea_budget.py`.
- Updated and expanded test coverage for input query and helper utilities.
- Minor bug fixes and documentation improvements across multiple modules.

## v0.1.2 (23/03/2025)

- added additional testing, all tests passing
- added data tables for protein (sheep, pig and poultry, dairy and beef)
- added econ_output.py in budget model to link baseline and scenario with protein outputs
- updated the example to include the protein dictionary and dataframe output 
- update the main optigob module 
- updated documentation to reflect changes. 
- 124 unittests passing

## v0.1.1 (22/03/2025)

- Bug fixes and performance improvements.
- added updated database to include biomethane, livestock, static ag, 
forest, and otherland
- calculates emissions and land area 
- optimised beef and dairy animal numbers for each scenario based on calculated
emissions budget 
- optimised constraints include CO2e and methane, for a split gas approach

## v0.1.0 (13/03/2025)

- First release of `optigob`!

