"""
Optigob module.
================
This module provides the Optigob class, which is used to manage and retrieve 
various emissions and land area budgets. The class interfaces with baseline 
emissions, emissions budgets, and land area budgets to provide detailed 
information on CO2e, CO2, CH4, and N2O emissions by sector, as well as land area usage.
area usage.

Classes:
    Optigob: Manages and retrieves emissions and land area budgets.

Methods:
    get_baseline_co2e_emissions_by_sector: Retrieves baseline CO2e emissions by sector.
    get_baseline_ch4_emissions_by_sector: Retrieves baseline CH4 emissions by sector.
    get_baseline_n2o_emissions_by_sector: Retrieves baseline N2O emissions by sector.
    get_baseline_co2_emissions_by_sector: Retrieves baseline CO2 emissions by sector.
    get_baseline_co2e_emissions_total: Retrieves total baseline CO2e emissions.
    get_baseline_co2_emissions_total: Retrieves total baseline CO2 emissions.
    get_baseline_ch4_emissions_total: Retrieves total baseline CH4 emissions.
    get_baseline_n2o_emissions_total: Retrieves total baseline N2O emissions.
    get_scenario_co2e_emissions_by_sector: Retrieves scenario CO2e emissions by sector.
    get_scenario_ch4_emissions_by_sector: Retrieves scenario CH4 emissions by sector.
    get_scenario_n2o_emissions_by_sector: Retrieves scenario N2O emissions by sector.
    get_scenario_co2_emissions_by_sector: Retrieves scenario CO2 emissions by sector.
    get_total_emissions_co2e_by_sector: Retrieves total CO2e emissions by sector for both baseline and scenario.
    get_total_emissions_ch4_by_sector: Retrieves total CH4 emissions by sector for both baseline and scenario.
    get_total_emissions_n2o_by_sector: Retrieves total N2O emissions by sector for both baseline and scenario.
    get_total_emissions_co2_by_sector: Retrieves total CO2 emissions by sector for both baseline and scenario.
    get_total_emissions_co2e_by_sector_df: Returns total CO2e emissions in a tidy Pandas DataFrame.
    get_total_land_area_by_sector: Retrieves total land area by sector for both baseline and scenario.
    get_total_land_area_by_sector_df: Returns total land area in a tidy Pandas DataFrame.
"""

from optigob.budget_model.baseline_emssions import BaselineEmission
from optigob.budget_model.emissions_budget import EmissionsBudget
from optigob.budget_model.landarea_budget import LandAreaBudget
import pandas as pd


class Optigob:
    def __init__(self, optigob_data_manager):
        """
        Initializes the Optigob class with the provided data manager.

        Args:
            optigob_data_manager: An instance of the data manager class.
        """
        self.data_manager_class = optigob_data_manager

        self.baseline_emission = BaselineEmission(self.data_manager_class)
        self.emission_budget = EmissionsBudget(self.data_manager_class)
        self.land_area_budget = LandAreaBudget(self.data_manager_class)

    def get_baseline_co2e_emissions_by_sector(self):
        """
        Retrieves baseline CO2e emissions by sector.

        Returns:
            dict: A dictionary with sectors as keys and CO2e emissions as values.
        """
        return self.baseline_emission.get_co2e_emission_categories()
    
    def get_baseline_ch4_emissions_by_sector(self):
        """
        Retrieves baseline CH4 emissions by sector.

        Returns:
            dict: A dictionary with sectors as keys and CH4 emissions as values.
        """
        return self.baseline_emission.get_ch4_emission_categories()
    
    def get_baseline_n2o_emissions_by_sector(self):
        """
        Retrieves baseline N2O emissions by sector.

        Returns:
            dict: A dictionary with sectors as keys and N2O emissions as values.
        """
        return self.baseline_emission.get_n2o_emission_categories()
    
    def get_baseline_co2_emissions_by_sector(self):
        """
        Retrieves baseline CO2 emissions by sector.

        Returns:
            dict: A dictionary with sectors as keys and CO2 emissions as values.
        """
        return self.baseline_emission.get_co2_emission_categories()
    
    def get_baseline_co2e_emissions_total(self):
        """
        Retrieves total baseline CO2e emissions.

        Returns:
            float: Total CO2e emissions.
        """
        return self.baseline_emission.get_total_co2e_emission()
    
    def get_baseline_co2_emissions_total(self):
        """
        Retrieves total baseline CO2 emissions.

        Returns:
            float: Total CO2 emissions.
        """
        return self.baseline_emission.get_total_co2_emission()
    
    def get_baseline_ch4_emissions_total(self):
        """
        Retrieves total baseline CH4 emissions.

        Returns:
            float: Total CH4 emissions.
        """
        return self.baseline_emission.get_total_ch4_emission()
    
    def get_baseline_n2o_emissions_total(self):
        """
        Retrieves total baseline N2O emissions.

        Returns:
            float: Total N2O emissions.
        """
        return self.baseline_emission.get_total_n2o_emission()
    
    def get_scenario_co2e_emissions_by_sector(self):
        """
        Retrieves scenario CO2e emissions by sector.

        Returns:
            dict: A dictionary with sectors as keys and CO2e emissions as values.
        """
        return self.emission_budget.get_co2e_emission_categories()
    
    def get_scenario_ch4_emissions_by_sector(self):
        """
        Retrieves scenario CH4 emissions by sector.

        Returns:
            dict: A dictionary with sectors as keys and CH4 emissions as values.
        """
        return self.emission_budget.get_ch4_emission_categories()
    
    def get_scenario_n2o_emissions_by_sector(self):
        """
        Retrieves scenario N2O emissions by sector.

        Returns:
            dict: A dictionary with sectors as keys and N2O emissions as values.
        """
        return self.emission_budget.get_n2o_emission_categories()
    
    def get_scenario_co2_emissions_by_sector(self):
        """
        Retrieves scenario CO2 emissions by sector.

        Returns:
            dict: A dictionary with sectors as keys and CO2 emissions as values.
        """
        return self.emission_budget.get_co2_emission_categories()
    
    def get_total_emissions_co2e_by_sector(self):
        """
        Retrieves total CO2e emissions by sector for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of sector emissions as values.
        """
        return {"baseline": self.get_baseline_co2e_emissions_by_sector(), 
                "scenario": self.get_scenario_co2e_emissions_by_sector()}
    
    def get_total_emissions_ch4_by_sector(self):
        """
        Retrieves total CH4 emissions by sector for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of sector emissions as values.
        """
        return {"baseline": self.get_baseline_ch4_emissions_by_sector(), 
                "scenario": self.get_scenario_ch4_emissions_by_sector()}        
    
    def get_total_emissions_n2o_by_sector(self):
        """
        Retrieves total N2O emissions by sector for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of sector emissions as values.
        """
        return {"baseline": self.get_baseline_n2o_emissions_by_sector(), 
                "scenario": self.get_scenario_n2o_emissions_by_sector()}
    
    def get_total_emissions_co2_by_sector(self):
        """
        Retrieves total CO2 emissions by sector for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of sector emissions as values.
        """
        return {"baseline": self.get_baseline_co2_emissions_by_sector(), 
                "scenario": self.get_scenario_co2_emissions_by_sector()}
    
    def get_total_emissions_co2e_by_sector_df(self):
        """
        Returns total CO2e emissions in a tidy Pandas DataFrame with sectors as rows 
        and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with sectors as rows and 'baseline' and 
                          'scenario' as columns.
        """
        data = {
            "baseline": self.get_baseline_co2e_emissions_by_sector(),
            "scenario": self.get_scenario_co2e_emissions_by_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df
    
    def get_total_land_area_by_sector(self):
        """
        Retrieves total land area by sector for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of sector land areas as values.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_land_area_by_sector(),
            "scenario": self.land_area_budget.get_total_scenario_land_area_by_sector()
        }
        return data
    
    def get_total_land_area_by_sector_df(self):
        """
        Returns total land area in a tidy Pandas DataFrame with sectors as rows 
        and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with sectors as rows and 'baseline' and 
                          'scenario' as columns.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_land_area_by_sector(),
            "scenario": self.land_area_budget.get_total_scenario_land_area_by_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df
