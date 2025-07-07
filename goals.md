# Package Goals

`optigob` is a land use change and environmental assessment tool built to model the impacts of livestock population scenarios under a negative emissions framework. It operates on precomputed environmental outputs and organizes them into actionable insights using a modular, extensible Python package.

The core logic hinges on the idea of using a GHG emissions budget as a currency: the user can only "buy" as many livestock as the emissions allowance permits. Freed-up land from livestock reductions is automatically reallocated to other land types, constrained by minimum area commitments. The system supports analysis of land use, protein production, harvested wood products, substitution impacts, and more.

## 🔧 High-Level Architecture

The system is built around a central API (`Optigob`) that manages interactions across specialized modules:

```text
optigob/
├── budget_model/                # Sector-agnostic aggregations
├── livestock/                  # Livestock emissions, and population optimisation
├── forest/                     # Forest land, HWP, emissions
├── bioenergy/                  # Bioenergy land & output
├── protein_crops/              # Protein crops area & yield
├── other_land/                # Remaining land types
├── resource_manager/          # Input loader & validator
├── database/                  # Data access helpers
├── optigob.py                 # Central orchestrator (Optigob class)
```

### 🧠 Key Modules

| Module                                                                                 | Role                                                            |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [`optigob.py`](optigob.py)                                                             | Main interface: orchestrates optimization and outputs           |
| [`resource_manager/optigob_data_manager.py`](resource_manager/optigob_data_manager.py) | Loads and validates input data                                  |
| [`budget_model/emissions_budget.py`](budget_model/emissions_budget.py)                 | Calculates emissions under different scenarios                  |
| [`budget_model/landarea_budget.py`](budget_model/landarea_budget.py)                   | Calculates total, disaggregated, and HNV land areas             |
| [`budget_model/econ_output.py`](budget_model/econ_output.py)                           | Computes protein, HWP, and livestock population                 |
| [`livestock/livestock_budget.py`](livestock/livestock_budget.py)                       | Livestock-specific calculations (emissions, land, protein)      |
| [`forest/forest_budget.py`](forest/forest_budget.py)                                   | Forest land use and harvested wood outputs                      |
| [`protein_crops/protein_crops_budget.py`](protein_crops/protein_crops_budget.py)       | Protein crop area/yield                                         |
| [`bioenergy/bioenergy_budget.py`](bioenergy/bioenergy_budget.py)                       | Bioenergy land use and outputs                                  |
| [`budget_model/substitution.py`](budget_model/substitution.py)                         | Calculates substitution impacts (e.g. fossil fuel replacements) |

## 🌟 What the Package Does

* Optimizes livestock numbers under an emissions constraint
* Allocates remaining land to other uses under area commitments
* Aggregates land use, emissions, and production data by sector
* Centralizes emissions substitution logic
* Returns tidy, analysis-ready outputs (DataFrames or dicts)

## 📈 Example Use Case

See the full example in the [`README.md`](README.md), which includes a script to:

* Load configuration from YAML
* Initialize the `Optigob` class
* Print emissions, land area, protein, and substitution outputs

## 📌 Use This File For

* Understanding **why** the package exists
* Seeing how the **modules interact**
* Providing **context** to agents like GitHub Copilot or human reviewers

---

For further details, see the complete [`README.md`](README.md) or explore the modules listed above.
