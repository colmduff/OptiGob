import pandas as pd
from pyomo.environ import ConcreteModel, Var, Constraint, Objective, NonNegativeReals, maximize, SolverFactory


class LivestockOptimisation:

    def __init__(self, solver="cplex_direct"):
        self.solver = solver

    def solve_optimiser(self, emissions_budget, dairy_beef_ratio, year, scenario, scalers_file):
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
        dairy_scaler, beef_scaler = load_scalers(scalers_file, year, scenario)
        
        # Create the Pyomo model
        model = ConcreteModel()
        
        # Decision variables: x for beef, y for dairy (both in units of 10,000 animals)
        model.x = Var(domain=NonNegativeReals)  # beef units
        model.y = Var(domain=NonNegativeReals)  # dairy units
        
        # Constraint: dairy-to-beef ratio (y = ratio * x)
        model.ratio_constraint = Constraint(expr=model.y == dairy_beef_ratio * model.x)
        
        # Constraint: total emissions from both dairy and beef should not exceed the emissions budget.
        # Here, the emissions for each type are calculated by multiplying the respective scaler.
        model.emissions_constraint = Constraint(expr=beef_scaler * model.x + dairy_scaler * model.y <= emissions_budget)
        
        # Objective: maximize total animal units. Since each unit is 10,000 animals,
        # maximizing (x + y) will maximize the total number of animals.
        model.obj = Objective(expr=model.x + model.y, sense=maximize)
        
        # Solve the model with a suitable solver, e.g. GLPK
        solver = SolverFactory('glpk')
        result = solver.solve(model, tee=True)
        
        # Retrieve the optimal values
        beef_units = model.x.value
        dairy_units = model.y.value
        total_animals = (beef_units + dairy_units) * 10000  # converting units to actual animal numbers
        
        return beef_units, dairy_units, total_animals
