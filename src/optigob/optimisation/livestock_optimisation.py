import pandas as pd
from pyomo.environ import ConcreteModel, Var, Constraint, Objective, NonNegativeReals, maximize, SolverFactory


class LivestockOptimisation():
    """
    """
    
    def __init__(self, optigob_data_manager):
        """
        Initializes the optimisation class with a specified solver.

        :param solver: Solver to use for optimisation (default: 'cplex').
        """
        self.solver = "cplex_direct"
        self.data_manager_class = optigob_data_manager



    def optimise_livestock_pop(self, gas, emissions_budget, dairy_beef_ratio, year, scenario):
        """
        Set up and solve the optimisation model.
        
        Parameters:
        emissions_budget: Total allowable emissions.
        dairy_beef_ratio: Ratio of dairy animals to beef animals (e.g., 10 for a 10:1 ratio).
        year: Year to select the correct row from the CSV.
        scenario: Abatement scenario to determine the scalers block.
        scalers_file: CSV file containing the scaler table.
        
        Returns:
        Optimal units (in 10,000 animals) for beef and dairy, and total number of animals.
        """
        # Load scaler values from CSV
        dairy_scaler = self.data_manager_class.get_livestock_scaler(
            year=year, system='Dairy', gas=gas, scenario=scenario
        )

        beef_scaler = self.data_manager_class.get_livestock_scaler(
            year=year, system='Beef', gas=gas, scenario=scenario
        )
        
        # Create the Pyomo model
        model = ConcreteModel()
        
        # Decision variables: x for beef, y for dairy (both in units of 10,000 animals)
        model.x = Var(domain=NonNegativeReals)  # beef units
        model.y = Var(domain=NonNegativeReals)  # dairy units
        
        # Constraint: dairy-to-beef ratio (y = ratio * x)
        model.ratio_constraint = Constraint(expr=model.y == dairy_beef_ratio * model.x)
        
        # Constraint: total emissions from both dairy and beef should not exceed the emissions budget.
        # Here, the emissions for each type are calculated by multiplying the respective scaler.
        model.emissions_constraint = Constraint(expr=beef_scaler["Value"] * model.x + dairy_scaler["Value"] * model.y <= emissions_budget)
        
        # Objective: maximize total animal units. Since each unit is 10,000 animals,
        # maximizing (x + y) will maximize the total number of animals.
        model.obj = Objective(expr=model.x + model.y, sense=maximize)
        
        # Solve the model 
        solver = SolverFactory(self.solver)
        result = solver.solve(model)
        
        # Retrieve the optimal values
        beef_units = model.x.value
        dairy_units = model.y.value

        total_dairy_animals = (dairy_units*dairy_scaler["Pop"]) # converting units to actual animal numbers
        total_beef_animals = (beef_units*beef_scaler["Pop"])

        output = {"Dairy_animals": total_dairy_animals, 
                  "Beef_animals": total_beef_animals,
                  "Gas": gas,
                  "Scenario": scenario,
                  "Year": year,
                  "Emissions": emissions_budget,
                  "Dairy_emissions": dairy_scaler["Value"] * dairy_units,
                  "Beef_emissions": beef_scaler["Value"] * beef_units}
        
        return output