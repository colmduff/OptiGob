"""
Optigob module
==============

This module provides the Optigob class, which manages and retrieves emissions, land area, protein, and bioenergy budgets for both baseline and scenario cases. It provides a unified interface to access sectoral and total values for CO2e, CO2, CH4, N2O, land area (aggregated/disaggregated/HNV), protein, bioenergy, harvested wood products, and substitution impacts. All results can be returned as dictionaries or tidy Pandas DataFrames for further analysis.

Class:
    Optigob: Central interface for retrieving all model outputs by sector and scenario.

Methods:
    __init__(self, optigob_data_manager): Initializes the Optigob class with the provided data manager.
    check_net_zero_status(self): Checks if the model is set to net zero (returns bool).
    get_baseline_co2e_emissions_by_sector(self): Retrieves baseline CO2e emissions by sector.
    get_baseline_ch4_emissions_by_sector(self): Retrieves baseline CH4 emissions by sector.
    get_baseline_n2o_emissions_by_sector(self): Retrieves baseline N2O emissions by sector.
    get_baseline_co2_emissions_by_sector(self): Retrieves baseline CO2 emissions by sector.
    get_baseline_co2e_emissions_total(self): Retrieves total baseline CO2e emissions.
    get_baseline_co2_emissions_total(self): Retrieves total baseline CO2 emissions.
    get_baseline_ch4_emissions_total(self): Retrieves total baseline CH4 emissions.
    get_baseline_n2o_emissions_total(self): Retrieves total baseline N2O emissions.
    get_scenario_co2e_emissions_by_sector(self): Retrieves scenario CO2e emissions by sector.
    get_scenario_ch4_emissions_by_sector(self): Retrieves scenario CH4 emissions by sector.
    get_scenario_n2o_emissions_by_sector(self): Retrieves scenario N2O emissions by sector.
    get_scenario_co2_emissions_by_sector(self): Retrieves scenario CO2 emissions by sector.
    get_total_emissions_co2e_by_sector(self): Retrieves total CO2e emissions by sector for both baseline and scenario.
    get_total_emissions_ch4_by_sector(self): Retrieves total CH4 emissions by sector for both baseline and scenario.
    get_total_emissions_n2o_by_sector(self): Retrieves total N2O emissions by sector for both baseline and scenario.
    get_total_emissions_co2_by_sector(self): Retrieves total CO2 emissions by sector for both baseline and scenario.
    get_total_emissions_co2e_by_sector_df(self): Returns total CO2e emissions as a tidy DataFrame.
    get_aggregated_total_land_area_by_sector(self): Retrieves aggregated land area by sector for both baseline and scenario.
    get_aggregated_total_land_area_by_sector_df(self): Returns aggregated land area as a tidy DataFrame.
    get_disaggregated_total_land_area_by_sector(self): Retrieves disaggregated land area by sector for both baseline and scenario.
    get_disaggregated_total_land_area_by_sector_df(self): Returns disaggregated land area as a tidy DataFrame.
    get_total_protein_by_sector(self): Retrieves total protein by sector for both baseline and scenario.
    get_total_protein_by_sector_df(self): Returns total protein as a tidy DataFrame.
    get_total_hnv_land_area_by_sector(self): Retrieves HNV land area by sector for both baseline and scenario.
    get_total_hnv_land_area_by_sector_df(self): Returns HNV land area as a tidy DataFrame.
    get_bioenergy_by_sector(self): Retrieves bioenergy area by sector for both baseline and scenario.
    get_bioenergy_by_sector_df(self): Returns bioenergy area as a tidy DataFrame.
    get_hwp_volume(self): Retrieves harvested wood product volume for both baseline and scenario.
    get_hwp_volume_df(self): Returns harvested wood product volume as a tidy DataFrame.
    get_substiution_emission_by_sector_co2e(self): Retrieves substitution emissions by sector for CO2e.
    get_substiution_emission_by_sector_co2e_df(self): Returns substitution emissions for CO2e as a tidy DataFrame.
    get_substiution_emission_by_sector_co2(self): Retrieves substitution emissions by sector for CO2.
    get_substiution_emission_by_sector_co2_df(self): Returns substitution emissions for CO2 as a tidy DataFrame.
    get_substiution_emission_by_sector_ch4(self): Retrieves substitution emissions by sector for CH4.
    get_substiution_emission_by_sector_ch4_df(self): Returns substitution emissions for CH4 as a tidy DataFrame.
    get_substiution_emission_by_sector_n2o(self): Retrieves substitution emissions by sector for N2O.
    get_substiution_emission_by_sector_n2o_df(self): Returns substitution emissions for N2O as a tidy DataFrame.
"""

from optigob.budget_model.baseline_emssions import BaselineEmission
from optigob.budget_model.emissions_budget import EmissionsBudget
from optigob.budget_model.landarea_budget import LandAreaBudget
from optigob.budget_model.econ_output import EconOutput
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
        self.econ_output = EconOutput(self.data_manager_class)

        self.split_gas = self.data_manager_class.get_split_gas()

    def total_emission_co2e(self):
        """
        Returns the total CO2e emissions (kt).

        Returns:
            float: Total CO2e emissions.
        """
        return self.emission_budget.get_total_emission_co2e()
    
    def check_net_zero_status(self):
        """
        Checks if the model is set to net zero.

        Returns:
            bool: True if the model is set to net zero, False otherwise.
        """
        status = self.emission_budget.check_net_zero_status()
        if self.split_gas:
            return status.get("split_gas", None)
        else:
            return status.get("net_zero", None)
        
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
        Returns total CO2e emissions as a tidy DataFrame with sectors as rows 
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
    
    def get_aggregated_total_land_area_by_sector(self):
        """
        Retrieves aggregated land area by sector for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of sector land areas as values.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_land_area_by_aggregated_sector(),
            "scenario": self.land_area_budget.get_total_scenario_land_area_by_aggregated_sector()
        }
        return data
    
    def get_aggregated_total_land_area_by_sector_df(self):
        """
        Returns aggregated land area as a tidy DataFrame with sectors as rows 
        and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with sectors as rows and 'baseline' and 
                          'scenario' as columns.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_land_area_by_aggregated_sector(),
            "scenario": self.land_area_budget.get_total_scenario_land_area_by_aggregated_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df
    
    def get_disaggregated_total_land_area_by_sector(self):
        """
        Retrieves disaggregated land area by sector for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of disaggregated sector land areas as values.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_land_area_by_disaggregated_sector(),
            "scenario": self.land_area_budget.get_total_scenario_land_area_by_disaggregated_sector()
        }
        return data
    
    def get_disaggregated_total_land_area_by_sector_df(self):
        """
        Returns disaggregated land area as a tidy DataFrame with disaggregated sectors as rows 
        and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with disaggregated sectors as rows and 'baseline' and 
                          'scenario' as columns.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_land_area_by_disaggregated_sector(),
            "scenario": self.land_area_budget.get_total_scenario_land_area_by_disaggregated_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df
    

    def get_total_protein_by_sector(self):
        """
        Retrieves total protein by sector for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of sector protein as values.
        """
        data = {
            "baseline": self.econ_output.get_total_baseline_protein_by_sector(),
            "scenario": self.econ_output.get_total_scenario_protein_by_sector()
        }
        return data
    
    def get_total_protein_by_sector_df(self):
        """
        Returns total protein as a tidy DataFrame with sectors as rows
        and 'baseline' and 'scenario' as columns.   "
        """
        data = {
            "baseline": self.econ_output.get_total_baseline_protein_by_sector(),
            "scenario": self.econ_output.get_total_scenario_protein_by_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df
    
    def get_total_hnv_land_area_by_sector(self):
        """
        Retrieves total HNV land area by sector for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of HNV land areas as values.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_hnv_land_area_disaggregated_by_sector(),
            "scenario": self.land_area_budget.get_total_scenario_hnv_land_area_disaggregated_by_sector()
        }
        return data
    
    def get_total_hnv_land_area_by_sector_df(self):
        """
        Returns total HNV land area as a tidy DataFrame with sectors as rows 
        and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with sectors as rows and 'baseline' and 
                          'scenario' as columns.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_hnv_land_area_disaggregated_by_sector(),
            "scenario": self.land_area_budget.get_total_scenario_hnv_land_area_disaggregated_by_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df
    
    def get_bioenergy_by_sector(self):
        """
        Retrieves bioenergy area by sector for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of bioenergy areas as values.
        """
        data = {
            "baseline": self.econ_output.get_total_baseline_bioenergy_by_sector(),
            "scenario": self.econ_output.get_total_scenario_bioenergy_by_sector()
        }
        return data
    
    def get_bioenergy_by_sector_df(self):
        """
        Returns bioenergy area as a tidy DataFrame with sectors as rows 
        and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with sectors as rows and 'baseline' and 
                          'scenario' as columns.
        """
        data = {
            "baseline": self.econ_output.get_total_baseline_bioenergy_by_sector(),
            "scenario": self.econ_output.get_total_scenario_bioenergy_by_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df
    
    def get_hwp_volume(self):
        """
        Retrieves the volume of harvested wood products (in cubic meters) for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and HWP volumes as values.
        """
        return self.econ_output.get_hwp_volume()
    
    def get_hwp_volume_df(self):
        """
        Returns the harvested wood products (HWP) volume as a tidy DataFrame with 'baseline' and 
        'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with 'baseline' and 'scenario' as columns.
        """
        return pd.DataFrame.from_dict(self.get_hwp_volume(), orient='columns')
    
    def get_substiution_emission_by_sector_co2e(self):
        """
        Retrieves substitution emissions by sector for CO2e.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of substitution emissions as values.
        """
        return self.emission_budget.get_substitution_emission_co2e()
    
    def get_substiution_emission_by_sector_co2e_df(self):
        """
        Returns substitution emissions for CO2e as a tidy DataFrame with sectors as rows 
        and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with sectors as rows and 'baseline' and 
                          'scenario' as columns.
        """
        data = {
            "scenario": self.get_substiution_emission_by_sector_co2e()
        }

        return pd.DataFrame.from_dict(data, orient='columns')

    
    def get_substiution_emission_by_sector_co2(self):
        """
        Retrieves substitution emissions by sector for CO2.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of substitution emissions as values.
        """
        return self.emission_budget.get_substitution_emission_co2()
    
    def get_substiution_emission_by_sector_co2_df(self):
        """
        Returns substitution emissions for CO2 as a tidy DataFrame with sectors as rows 
        and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with sectors as rows and 'baseline' and 
                          'scenario' as columns.
        """
        data = {
            "scenario":self.get_substiution_emission_by_sector_co2()
        }
        return pd.DataFrame.from_dict(data, orient='columns')
    
    def get_substiution_emission_by_sector_ch4(self):
        """
        Retrieves substitution emissions by sector for CH4.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of substitution emissions as values.
        """
        return self.emission_budget.get_substitution_emission_ch4()
    
    def get_substiution_emission_by_sector_ch4_df(self):
        """
        Returns substitution emissions for CH4 as a tidy DataFrame with sectors as rows 
        and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with sectors as rows and 'baseline' and 
                          'scenario' as columns.
        """
        data = {
            "scenario":self.get_substiution_emission_by_sector_ch4()
        }
        return pd.DataFrame.from_dict(data, orient='columns')

    
    def get_substiution_emission_by_sector_n2o(self):
        """
        Retrieves substitution emissions by sector for N2O.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of substitution emissions as values.
        """
        return self.emission_budget.get_substitution_emission_n2o()
    
    def get_substiution_emission_by_sector_n2o_df(self):
        """
        Returns substitution emissions for N2O as a tidy DataFrame with sectors as rows 
        and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with sectors as rows and 'baseline' and 
                          'scenario' as columns.
        """
        data = {
            "scenario":self.get_substiution_emission_by_sector_n2o()
        }
        return pd.DataFrame.from_dict(data, orient='columns')
    

    def get_livestock_population(self):
        """
        Returns the livestock population in number of animals for both baseline and scenario.

        Returns:
            dict: A dictionary with 'baseline' and 'scenario' as keys and 
                  dictionaries of livestock populations as values.
        """
        return {
            "baseline": self.econ_output.get_baseline_livestock_population(),
            "scenario": self.econ_output.get_scenario_livestock_population()
        }
    
    def get_livestock_population_df(self):
        """
        Returns the livestock population as a tidy DataFrame with 'baseline' and 
        'scenario' as columns.

        Returns:
            pd.DataFrame: A DataFrame with 'baseline' and 'scenario' as columns.
        """
        data = self.get_livestock_population()
        return pd.DataFrame.from_dict(data, orient='columns')

