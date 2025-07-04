import pandas as pd
from pyomo.environ import ConcreteModel, Var, Constraint, Objective, NonNegativeReals, maximize, SolverFactory
from optigob.livestock.baseline_livestock import BaselineLivestock

class OptimisationResult(dict):
    """
    A convenience wrapper for optimisation outputs that always includes status and message,
    and supports a .feasible property for quick checks.
    """
    @property
    def feasible(self):
        return self.get("status", "ok") == "ok"

class LivestockOptimisation:
    """
    Class for optimising livestock populations under emissions constraints.
    """
    def __init__(self, optigob_data_manager):
        self.solver = "cplex_direct"
        self.data_manager_class = optigob_data_manager
        self.baseline_livestock = BaselineLivestock(self.data_manager_class)

    def scalar(self,x):
        # Utility to ensure value is a float
        if hasattr(x, "item"):
            return float(x.item())
        return float(x)
    
    def optimise_livestock_pop(self,
                               ratio_type,
                               ratio_value,
                               year,
                               scenario,
                               abatement,
                               emissions_budget,
                               area_commitment,
                               ch4_budget=None):
        """
        Set up and solve the optimisation model.
        Returns an OptimisationResult object (like a dict).
        """
       
        # ==== 1. Load and normalise all data up front ====

        co2e_dairy_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Dairy', gas='CO2e', scenario=scenario, abatement=abatement
        )
        co2e_beef_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Beef', gas='CO2e', scenario=scenario, abatement=abatement
        )
        ch4_dairy_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Dairy', gas='CH4', scenario=scenario, abatement=abatement
        )
        ch4_beef_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Beef', gas='CH4', scenario=scenario, abatement=abatement
        )

        co2_dairy_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Dairy', gas='CO2', scenario=scenario
            , abatement=abatement
        )
        co2_beef_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Beef', gas='CO2', scenario=scenario, abatement=abatement
        )

        n2o_dairy_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Dairy', gas='N2O', scenario=scenario, abatement=abatement
        )
        n2o_beef_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Beef', gas='N2O', scenario=scenario, abatement=abatement
        )

        
        dairy_area_scaler = self.data_manager_class.get_livestock_area_scaler(
            year=year, system='Dairy', scenario=scenario, abatement=abatement
        )
        beef_area_scaler = self.data_manager_class.get_livestock_area_scaler(
            year=year, system='Beef', scenario=scenario, abatement=abatement
        )
        dairy_beef_area_scaler = self.data_manager_class.get_livestock_area_scaler(
            year=year, system='Dairy+Beef', scenario=scenario, abatement=abatement
        )

        total_beef_area = dairy_beef_area_scaler["area"] + beef_area_scaler["area"]

        baseline_area = self.scalar(self.baseline_livestock.get_total_area())

        n20_conversion_factor = self.data_manager_class.get_AR_gwp100_values("N2O")

        split_gas_co2e_dairy = (n2o_dairy_scaler["value"]* n20_conversion_factor) + co2_dairy_scaler["value"]
        split_gas_co2e_beef = (n2o_beef_scaler["value"] * n20_conversion_factor) + co2_beef_scaler["value"]

        # ==== 2. Build the Pyomo model ====
        model = ConcreteModel()
        model.x = Var(domain=NonNegativeReals)  # beef
        model.y = Var(domain=NonNegativeReals)  # dairy

        model.area_constraint = Constraint(
            expr=(model.x * self.scalar(total_beef_area) +
                  model.y * self.scalar(dairy_area_scaler["area"]))
                 <= (baseline_area - area_commitment)
        )

        if ratio_type == "dairy_per_beef":
            model.ratio_constraint = Constraint(expr=model.y == ratio_value * model.x)
        elif ratio_type == "beef_per_dairy":
            model.ratio_constraint = Constraint(expr=model.x == ratio_value * model.y)
        else:
            raise ValueError(f"Invalid ratio_type: {ratio_type}. Must be 'dairy_per_beef' or 'beef_per_dairy'.")
        
        if ch4_budget is not None:
            model.emissions_constraint = Constraint(
                expr=(self.scalar(split_gas_co2e_beef) * model.x +
                    self.scalar(split_gas_co2e_dairy) * model.y)
                    <= emissions_budget
            )
        else:
            model.emissions_constraint = Constraint(
                expr=(self.scalar(co2e_beef_scaler["value"]) * model.x +
                    self.scalar(co2e_dairy_scaler["value"]) * model.y)
                    <= emissions_budget
            )
        if ch4_budget is not None:
            model.ch4_constraint = Constraint(
                expr=(self.scalar(ch4_beef_scaler["value"]) * model.x +
                      self.scalar(ch4_dairy_scaler["value"]) * model.y)
                    <= ch4_budget
            )

        model.obj = Objective(expr=model.x + model.y, sense=maximize)
        solver = SolverFactory(self.solver)
        result = solver.solve(model)

        # ==== 3. Wrap up result: always return OptimisationResult ====
        termination = str(result.solver.termination_condition).lower()
        beef_units = model.x.value
        dairy_units = model.y.value

        if 'infeasible' in termination or beef_units is None or dairy_units is None:
            # Give a clear, helpful, custom message
            print("Optimization infeasible: No feasible solution for the provided constraints.")

        # --- Otherwise, return the solution as usual, with status "ok" ---
        total_dairy_animals = dairy_units * self.scalar(co2e_dairy_scaler["pop"])
        total_beef_animals = beef_units * self.scalar(co2e_beef_scaler["pop"])

        out = {
            "status": "ok",
            "Dairy_animals": total_dairy_animals, 
            "Beef_animals": total_beef_animals,
            "Scenario": scenario,
            "Year": year,
            "Emissions_budget_CO2e": emissions_budget,
            "Dairy_emissions_CO2e": self.scalar(co2e_dairy_scaler["value"]) * dairy_units,
            "Beef_emissions_CO2e": self.scalar(co2e_beef_scaler["value"]) * beef_units
        }
        if ch4_budget is not None:
            out.update({
                "CH4_budget": ch4_budget,
                "Dairy_emissions_CH4": self.scalar(ch4_dairy_scaler["value"]) * dairy_units,
                "Beef_emissions_CH4": self.scalar(ch4_beef_scaler["value"]) * beef_units
            })
        return OptimisationResult(out)

