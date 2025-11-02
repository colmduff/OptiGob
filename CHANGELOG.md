# Changelog

<!--next-version-placeholder-->

## v0.1.3 (02/11/2025)

- **Documentation Migration**: Migrated documentation hosting from GitHub Pages to Read the Docs.
- Added `.readthedocs.yml` configuration file for automated documentation builds on Read the Docs.
- Updated documentation dependencies in `docs/requirements.txt` (changed `autoapi` to `sphinx-autoapi`).
- Updated README with Read the Docs documentation badges and links.
- Documentation now available at: <https://optigob.readthedocs.io/en/latest/>
- Improved documentation build process with automated Sphinx builds on commit.

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

