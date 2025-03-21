import pandas as pd
from pyomo.environ import ConcreteModel, Var, Constraint, Objective, NonNegativeReals, maximize, SolverFactory


class LivestockOptimisation():
    """
    Class for optimising livestock populations under emissions constraints.
    """
    
    def __init__(self, optigob_data_manager):
        """
        Initializes the optimisation class with a specified solver.
        """
        self.solver = "cplex_direct"
        self.data_manager_class = optigob_data_manager

    def optimise_livestock_pop(self,
                               dairy_beef_ratio,
                               year,
                               scenario,
                               abatement,
                               emissions_budget,
                               ch4_budget=None):
        """
        Set up and solve the optimisation model.
        
        Parameters:
        emissions_budget: Total allowable emissions in CO2e.
        ch4_budget: Optional methane (CH4) emissions constraint.
        dairy_beef_ratio: Ratio of dairy animals to beef animals (e.g., 10 for a 10:1 ratio).
        year: Year to select the correct row from the scaler data.
        scenario: Abatement scenario.
        
        Returns:
        Dictionary with optimal population sizes and emissions data.
        """
        # Get CO2e scalers
        dairy_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Dairy', gas='CO2e', scenario=scenario, abatement=abatement
        )

        beef_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Beef', gas='CO2e', scenario=scenario, abatement=abatement
        )
        
        # Get CH4 scalers
        ch4_dairy_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Dairy', gas='CH4', scenario=scenario, abatement=abatement
        )

        ch4_beef_scaler = self.data_manager_class.get_livestock_emission_scaler(
            year=year, system='Beef', gas='CH4', scenario=scenario, abatement=abatement
        )
        
        # Create the Pyomo model
        model = ConcreteModel()
        
        # Decision variables: x for beef, y for dairy (both in units of 10,000 animals)
        model.x = Var(domain=NonNegativeReals)  # beef units
        model.y = Var(domain=NonNegativeReals)  # dairy units
        
        # Constraint: dairy-to-beef ratio (y = ratio * x)
        model.ratio_constraint = Constraint(expr=model.y == dairy_beef_ratio * model.x)
        
        # Constraint: total emissions (CO2e) must not exceed emissions budget
        model.emissions_constraint = Constraint(expr=beef_scaler["value"] * model.x + dairy_scaler["value"] * model.y <= emissions_budget)
        
        # Optional CH4 constraint
        if ch4_budget is not None:
            model.ch4_constraint = Constraint(expr=ch4_beef_scaler["value"] * model.x + ch4_dairy_scaler["value"] * model.y <= ch4_budget)
        
        # Objective: maximize total animal units
        model.obj = Objective(expr=model.x + model.y, sense=maximize)
        
        # Solve the model 
        solver = SolverFactory(self.solver)
        result = solver.solve(model)
        
        # Retrieve optimal values
        beef_units = model.x.value
        dairy_units = model.y.value

        total_dairy_animals = dairy_units * dairy_scaler["pop"]  # converting units to actual animal numbers
        total_beef_animals = beef_units * beef_scaler["pop"]

        output = {
            "Dairy_animals": total_dairy_animals, 
            "Beef_animals": total_beef_animals,
            "Scenario": scenario,
            "Year": year,
            "Emissions_budget_CO2e": emissions_budget,
            "Dairy_emissions_CO2e": dairy_scaler["value"] * dairy_units,
            "Beef_emissions_CO2e": beef_scaler["value"] * beef_units
        }

        if ch4_budget is not None:
            output.update({
                "CH4_budget": ch4_budget,
                "Dairy_emissions_CH4": ch4_dairy_scaler["value"] * dairy_units,
                "Beef_emissions_CH4": ch4_beef_scaler["value"] * beef_units
            })
        
        return output
