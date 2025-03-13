from optigob.resource_manager.database_manager import DatabaseManager
import pandas as pd
import json


class OptiGobDataManager:
    def __init__(self, sip):
        """
        Initializes the OptiGobDataManager.

        Parameters:
            sip (str or dict): A file path to a JSON file or a dictionary containing
                               the standard input parameters. Expected keys are:
                               - "baseline_year"
                               - "target_year"
                               - "abatement_scenario"
                               - "gas"
                               - "emissions_budget"
                               - "dairy_beef_ratio"
        """
        # If sip is a string, assume it's a file path and load the JSON.
        if isinstance(sip, str):
            with open(sip, 'r') as f:
                self.standard_input_parameters = json.load(f)
        else:
            self.standard_input_parameters = sip
        
        self.db_manager = DatabaseManager()
        self._livestock_scalers = None  # 


    def _load_livestock_scalers(self):
        """Loads and caches the livestock scalers from the database."""
        if self._livestock_scalers is None:
            self._livestock_scalers = self.db_manager.get_livestock_scalers()
        return self._livestock_scalers


    def get_livestock_scaler(self, year, system, gas, scenario):
        """
        Retrieves the scaler value for a given year, system, gas, and scenario.
        
        Parameters:
            year (int): The year of interest.
            system (str): The system identifier.
            gas (str): The gas identifier.
            scenario (int): The scenario identifier.
        
        Returns:
            float: The scaler value from the "Value" column.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_livestock_scalers()
        # Filter the DataFrame based on the provided parameters.

        filtered = df[
            (df["Year"] == year) &
            (df["System"] == system) &
            (df["Gas"] == gas) &
            (df["Scenario"] == scenario)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.

        output = {"System": system, 
                  "Gas": gas, 
                  "Scenario": scenario, 
                  "Year": year, 
                  "Value": filtered["Value"].values[0],
                  "Pop": filtered["Pop"].values[0]}
        return output            
    

    # Getter methods for the input parameters.
    def get_baseline_year(self):
        return self.standard_input_parameters.get("baseline_year")

    def get_target_year(self):
        return self.standard_input_parameters.get("target_year")

    def get_abatement_scenario(self):
        return self.standard_input_parameters.get("abatement_scenario")

    def get_gas(self):
        return self.standard_input_parameters.get("gas")

    def get_emissions_budget(self):
        return self.standard_input_parameters.get("emissions_budget")

    def get_dairy_beef_ratio(self):
        return self.standard_input_parameters.get("dairy_beef_ratio")