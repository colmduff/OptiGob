"""
Optigob module
==============

This module provides the Optigob class, which serves as the central interface for retrieving, aggregating, and analyzing all model outputs related to land use, emissions, protein, bioenergy, harvested wood products, and substitution impacts in the FORESIGHT system. The Optigob class enables unified access to both baseline and scenario results, supporting sectoral and total values for CO2e, CO2, CH4, N2O, land area (aggregated/disaggregated/HNV), protein, bioenergy, harvested wood products, and substitution impacts. All results can be returned as dictionaries or tidy Pandas DataFrames for further analysis and reporting.

Class:
    Optigob: Central interface for retrieving and aggregating all model outputs by sector and scenario.

Methods:
    __init__(self, optigob_data_manager): Initialize the Optigob class with the provided data manager.
    check_net_zero_status(self): Check if the model is set to net zero (returns bool).
    get_livestock_split_gas_ch4_emission_budget(self): Retrieve total livestock split gas CH4 emissions (kt) budget available.
    total_emission_co2e(self): Return the total scenario CO2e emissions (kt) for all sectors combined.
    get_baseline_co2e_emissions_by_sector(self): Retrieve baseline CO2e emissions by sector.
    get_baseline_ch4_emissions_by_sector(self): Retrieve baseline CH4 emissions by sector.
    get_baseline_n2o_emissions_by_sector(self): Retrieve baseline N2O emissions by sector.
    get_baseline_co2_emissions_by_sector(self): Retrieve baseline CO2 emissions by sector.
    get_baseline_co2e_emissions_total(self): Retrieve total baseline CO2e emissions.
    get_baseline_co2_emissions_total(self): Retrieve total baseline CO2 emissions.
    get_baseline_ch4_emissions_total(self): Retrieve total baseline CH4 emissions.
    get_baseline_n2o_emissions_total(self): Retrieve total baseline N2O emissions.
    get_scenario_co2e_emissions_by_sector(self): Retrieve scenario CO2e emissions by sector.
    get_scenario_ch4_emissions_by_sector(self): Retrieve scenario CH4 emissions by sector.
    get_scenario_n2o_emissions_by_sector(self): Retrieve scenario N2O emissions by sector.
    get_scenario_co2_emissions_by_sector(self): Retrieve scenario CO2 emissions by sector.
    get_total_emissions_co2e_by_sector(self): Retrieve total CO2e emissions by sector for both baseline and scenario.
    get_total_emissions_ch4_by_sector(self): Retrieve total CH4 emissions by sector for both baseline and scenario.
    get_total_emissions_n2o_by_sector(self): Retrieve total N2O emissions by sector for both baseline and scenario.
    get_total_emissions_co2_by_sector(self): Retrieve total CO2 emissions by sector for both baseline and scenario.
    get_total_emissions_co2e_by_sector_df(self): Return total CO2e emissions as a tidy DataFrame.
    get_aggregated_total_land_area_by_sector(self): Retrieve aggregated land area by sector for both baseline and scenario.
    get_aggregated_total_land_area_by_sector_df(self): Return aggregated land area as a tidy DataFrame.
    get_disaggregated_total_land_area_by_sector(self): Retrieve disaggregated land area by sector for both baseline and scenario.
    get_disaggregated_total_land_area_by_sector_df(self): Return disaggregated land area as a tidy DataFrame.
    get_total_protein_by_sector(self): Retrieve total protein by sector for both baseline and scenario.
    get_total_protein_by_sector_df(self): Return total protein as a tidy DataFrame.
    get_total_hnv_land_area_by_sector(self): Retrieve HNV land area by sector for both baseline and scenario.
    get_total_hnv_land_area_by_sector_df(self): Return HNV land area as a tidy DataFrame.
    get_bioenergy_by_sector(self): Retrieve bioenergy area by sector for both baseline and scenario.
    get_bioenergy_by_sector_df(self): Return bioenergy area as a tidy DataFrame.
    get_hwp_volume(self): Retrieve harvested wood product volume for both baseline and scenario.
    get_hwp_volume_df(self): Return harvested wood product volume as a tidy DataFrame.
    get_substitution_emission_by_sector_co2e(self): Retrieve substitution emissions by sector for CO2e.
    get_substitution_emission_by_sector_co2e_df(self): Return substitution emissions for CO2e as a tidy DataFrame.
    get_substitution_emission_by_sector_co2(self): Retrieve substitution emissions by sector for CO2.
    get_substitution_emission_by_sector_co2_df(self): Return substitution emissions for CO2 as a tidy DataFrame.
    get_substitution_emission_by_sector_ch4(self): Retrieve substitution emissions by sector for CH4.
    get_substitution_emission_by_sector_ch4_df(self): Return substitution emissions for CH4 as a tidy DataFrame.
    get_substitution_emission_by_sector_n2o(self): Retrieve substitution emissions by sector for N2O.
    get_substitution_emission_by_sector_n2o_df(self): Return substitution emissions for N2O as a tidy DataFrame.
    get_livestock_population(self): Retrieve livestock population for both baseline and scenario.
    get_livestock_population_df(self): Return livestock population as a tidy DataFrame.
"""

from optigob.budget_model.baseline_emissions import BaselineEmission
from optigob.budget_model.emissions_budget import EmissionsBudget
from optigob.budget_model.landarea_budget import LandAreaBudget
from optigob.budget_model.econ_output import EconOutput
import pandas as pd


class Optigob:
    """
    Central interface for retrieving, aggregating, and analyzing all model outputs in the FORESIGHT system.

    The Optigob class provides a unified API for accessing emissions, land area, protein, bioenergy, harvested wood products, and substitution impacts for both baseline and scenario cases. It wraps all major model outputs, including sectoral and total values for CO2e, CO2, CH4, N2O, land area (aggregated/disaggregated/HNV), protein, bioenergy, harvested wood products, and substitution impacts. All results can be returned as dictionaries or tidy Pandas DataFrames for further analysis and reporting.

    Args:
        optigob_data_manager: An instance of the data manager class, typically OptiGobDataManager, providing access to all model data and configuration.
    """
    def __init__(self, optigob_data_manager):
        """
        Initialize the Optigob class with the provided data manager.

        Args:
            optigob_data_manager: Data manager instance providing access to all model data and configuration.
        """
        self.data_manager_class = optigob_data_manager

        self.baseline_emission = BaselineEmission(self.data_manager_class)
        self.emission_budget = EmissionsBudget(self.data_manager_class)
        self.land_area_budget = LandAreaBudget(self.data_manager_class)
        self.econ_output = EconOutput(self.data_manager_class)

        self.split_gas = self.data_manager_class.get_split_gas()

    def get_livestock_co2e_emission_budget(self):
        """
        Retrieve the total livestock CO2e emissions (kt) budget available for the scenario.

        Returns:
            float: Total livestock CO2e emissions budget in kilotons.
        """
        if self.split_gas:
            emission_budget = self.emission_budget._split_gas_emissions_total_budget_co2e()
        else:
            emission_budget = self.emission_budget._get_total_emission_co2e_budget()

        return emission_budget
            
    

    def get_livestock_split_gas_ch4_emission_budget(self):
        """
        Retrieve the total livestock split gas CH4 emissions (kt) budget available for the scenario.

        Returns:
            float: Total livestock split gas CH4 emissions budget in kilotons.

        Raises:
            ValueError: If split gas is not included in the model configuration.
        """
        if self.split_gas:
            return self.emission_budget.get_total_livestock_ch4_emission_budget()
        else:
            raise ValueError("Split gas is not included in the model configuration.")
        
        
    def total_emission_co2e(self):
        """
        Return the total scenario CO2e emissions (kt) for all sectors combined.

        Returns:
            float: Total scenario CO2e emissions in kilotons.
        """
        return self.emission_budget.get_total_emission_co2e()

    def check_net_zero_status(self):
        """
        Check if the model is set to net zero, using either the split gas or net zero budget as appropriate.

        Returns:
            bool or None: True if the model is set to net zero (or split gas net zero), False otherwise. None if not applicable.
        """
        status = self.emission_budget.check_net_zero_status()
        if self.split_gas:
            return status.get("split_gas", None)
        else:
            return status.get("net_zero", None)

    def get_baseline_co2e_emissions_by_sector(self):
        """
        Retrieve baseline CO2e emissions by sector.

        Returns:
            dict: Sectors as keys and baseline CO2e emissions (kt) as values.
        """
        return self.baseline_emission.get_co2e_emission_categories()

    def get_baseline_ch4_emissions_by_sector(self):
        """
        Retrieve baseline CH4 emissions by sector.

        Returns:
            dict: Sectors as keys and baseline CH4 emissions (kt) as values.
        """
        return self.baseline_emission.get_ch4_emission_categories()

    def get_baseline_n2o_emissions_by_sector(self):
        """
        Retrieve baseline N2O emissions by sector.

        Returns:
            dict: Sectors as keys and baseline N2O emissions (kt) as values.
        """
        return self.baseline_emission.get_n2o_emission_categories()

    def get_baseline_co2_emissions_by_sector(self):
        """
        Retrieve baseline CO2 emissions by sector.

        Returns:
            dict: Sectors as keys and baseline CO2 emissions (kt) as values.
        """
        return self.baseline_emission.get_co2_emission_categories()

    def get_baseline_co2e_emissions_total(self):
        """
        Retrieve total baseline CO2e emissions.

        Returns:
            float: Total baseline CO2e emissions in kilotons.
        """
        return self.baseline_emission.get_total_co2e_emission()

    def get_baseline_co2_emissions_total(self):
        """
        Retrieve total baseline CO2 emissions.

        Returns:
            float: Total baseline CO2 emissions in kilotons.
        """
        return self.baseline_emission.get_total_co2_emission()

    def get_baseline_ch4_emissions_total(self):
        """
        Retrieve total baseline CH4 emissions.

        Returns:
            float: Total baseline CH4 emissions in kilotons.
        """
        return self.baseline_emission.get_total_ch4_emission()

    def get_baseline_n2o_emissions_total(self):
        """
        Retrieve total baseline N2O emissions.

        Returns:
            float: Total baseline N2O emissions in kilotons.
        """
        return self.baseline_emission.get_total_n2o_emission()

    def get_scenario_co2e_emissions_by_sector(self):
        """
        Retrieve scenario CO2e emissions by sector.

        Returns:
            dict: Sectors as keys and scenario CO2e emissions (kt) as values.
        """
        return self.emission_budget.get_co2e_emission_categories()

    def get_scenario_ch4_emissions_by_sector(self):
        """
        Retrieve scenario CH4 emissions by sector.

        Returns:
            dict: Sectors as keys and scenario CH4 emissions (kt) as values.
        """
        return self.emission_budget.get_ch4_emission_categories()

    def get_scenario_n2o_emissions_by_sector(self):
        """
        Retrieve scenario N2O emissions by sector.

        Returns:
            dict: Sectors as keys and scenario N2O emissions (kt) as values.
        """
        return self.emission_budget.get_n2o_emission_categories()

    def get_scenario_co2_emissions_by_sector(self):
        """
        Retrieve scenario CO2 emissions by sector.

        Returns:
            dict: Sectors as keys and scenario CO2 emissions (kt) as values.
        """
        return self.emission_budget.get_co2_emission_categories()

    def get_total_emissions_co2e_by_sector(self):
        """
        Retrieve total CO2e emissions by sector for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of sector emissions as values.
        """
        return {"baseline": self.get_baseline_co2e_emissions_by_sector(), 
                "scenario": self.get_scenario_co2e_emissions_by_sector()}

    def get_total_emissions_ch4_by_sector(self):
        """
        Retrieve total CH4 emissions by sector for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of sector emissions as values.
        """
        return {"baseline": self.get_baseline_ch4_emissions_by_sector(), 
                "scenario": self.get_scenario_ch4_emissions_by_sector()}        

    def get_total_emissions_n2o_by_sector(self):
        """
        Retrieve total N2O emissions by sector for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of sector emissions as values.
        """
        return {"baseline": self.get_baseline_n2o_emissions_by_sector(), 
                "scenario": self.get_scenario_n2o_emissions_by_sector()}

    def get_total_emissions_co2_by_sector(self):
        """
        Retrieve total CO2 emissions by sector for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of sector emissions as values.
        """
        return {"baseline": self.get_baseline_co2_emissions_by_sector(), 
                "scenario": self.get_scenario_co2_emissions_by_sector()}

    def get_total_emissions_co2e_by_sector_df(self):
        """
        Return total CO2e emissions as a tidy DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "baseline": self.get_baseline_co2e_emissions_by_sector(),
            "scenario": self.get_scenario_co2e_emissions_by_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df

    def get_aggregated_total_land_area_by_sector(self):
        """
        Retrieve aggregated land area by sector for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of sector land areas as values.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_land_area_by_aggregated_sector(),
            "scenario": self.land_area_budget.get_total_scenario_land_area_by_aggregated_sector()
        }
        return data

    def get_aggregated_total_land_area_by_sector_df(self):
        """
        Return aggregated land area as a tidy DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_land_area_by_aggregated_sector(),
            "scenario": self.land_area_budget.get_total_scenario_land_area_by_aggregated_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df

    def get_disaggregated_total_land_area_by_sector(self):
        """
        Retrieve disaggregated land area by sector for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of disaggregated sector land areas as values.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_land_area_by_disaggregated_sector(),
            "scenario": self.land_area_budget.get_total_scenario_land_area_by_disaggregated_sector()
        }
        return data

    def get_disaggregated_total_land_area_by_sector_df(self):
        """
        Return disaggregated land area as a tidy DataFrame with disaggregated sectors as rows and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with disaggregated sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_land_area_by_disaggregated_sector(),
            "scenario": self.land_area_budget.get_total_scenario_land_area_by_disaggregated_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df
    

    def get_total_protein_by_sector(self):
        """
        Retrieve total protein by sector for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of sector protein as values.
        """
        data = {
            "baseline": self.econ_output.get_total_baseline_protein_by_sector(),
            "scenario": self.econ_output.get_total_scenario_protein_by_sector()
        }
        return data

    def get_total_protein_by_sector_df(self):
        """
        Return total protein as a tidy DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "baseline": self.econ_output.get_total_baseline_protein_by_sector(),
            "scenario": self.econ_output.get_total_scenario_protein_by_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df

    def get_total_hnv_land_area_by_sector(self):
        """
        Retrieve total HNV (High Nature Value) land area by sector for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of HNV land areas as values.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_hnv_land_area_disaggregated_by_sector(),
            "scenario": self.land_area_budget.get_total_scenario_hnv_land_area_disaggregated_by_sector()
        }
        return data

    def get_total_hnv_land_area_by_sector_df(self):
        """
        Return total HNV land area as a tidy DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "baseline": self.land_area_budget.get_total_baseline_hnv_land_area_disaggregated_by_sector(),
            "scenario": self.land_area_budget.get_total_scenario_hnv_land_area_disaggregated_by_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df

    def get_bioenergy_by_sector(self):
        """
        Retrieve bioenergy area by sector for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of bioenergy areas as values.
        """
        data = {
            "baseline": self.econ_output.get_total_baseline_bioenergy_by_sector(),
            "scenario": self.econ_output.get_total_scenario_bioenergy_by_sector()
        }
        return data

    def get_bioenergy_by_sector_df(self):
        """
        Return bioenergy area as a tidy DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "baseline": self.econ_output.get_total_baseline_bioenergy_by_sector(),
            "scenario": self.econ_output.get_total_scenario_bioenergy_by_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df

    def get_hwp_volume(self):
        """
        Retrieve the volume of harvested wood products (in cubic meters) for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and HWP volumes as values.
        """
        return self.econ_output.get_hwp_volume()

    def get_hwp_volume_df(self):
        """
        Return the harvested wood products (HWP) volume as a tidy DataFrame with 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with 'baseline' and 'scenario' as columns.
        """
        return pd.DataFrame.from_dict(self.get_hwp_volume(), orient='columns')

    def get_substitution_emission_by_sector_co2e(self):
        """
        Retrieve substitution emissions by sector for CO2e.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of substitution emissions as values.
        """
        return self.emission_budget.get_substitution_emission_co2e()

    def get_substitution_emission_by_sector_co2e_df(self):
        """
        Return substitution emissions for CO2e as a tidy DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "scenario": self.get_substitution_emission_by_sector_co2e()
        }

        return pd.DataFrame.from_dict(data, orient='columns')


    def get_substitution_emission_by_sector_co2(self):
        """
        Retrieve substitution emissions by sector for CO2.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of substitution emissions as values.
        """
        return self.emission_budget.get_substitution_emission_co2()

    def get_substitution_emission_by_sector_co2_df(self):
        """
        Return substitution emissions for CO2 as a tidy DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "scenario":self.get_substitution_emission_by_sector_co2()
        }
        return pd.DataFrame.from_dict(data, orient='columns')

    def get_substitution_emission_by_sector_ch4(self):
        """
        Retrieve substitution emissions by sector for CH4.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of substitution emissions as values.
        """
        return self.emission_budget.get_substitution_emission_ch4()

    def get_substitution_emission_by_sector_ch4_df(self):
        """
        Return substitution emissions for CH4 as a tidy DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "scenario":self.get_substitution_emission_by_sector_ch4()
        }
        return pd.DataFrame.from_dict(data, orient='columns')


    def get_substitution_emission_by_sector_n2o(self):
        """
        Retrieve substitution emissions by sector for N2O.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of substitution emissions as values.
        """
        return self.emission_budget.get_substitution_emission_n2o()

    def get_substitution_emission_by_sector_n2o_df(self):
        """
        Return substitution emissions for N2O as a tidy DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "scenario":self.get_substitution_emission_by_sector_n2o()
        }
        return pd.DataFrame.from_dict(data, orient='columns')


    def get_livestock_population(self):
        """
        Retrieve the livestock population in number of animals for both baseline and scenario.

        Returns:
            dict: Dictionary with 'baseline' and 'scenario' as keys and dictionaries of livestock populations as values.
        """
        return {
            "baseline": self.econ_output.get_baseline_livestock_population(),
            "scenario": self.econ_output.get_scenario_livestock_population()
        }

    def get_livestock_population_df(self):
        """
        Return the livestock population as a tidy DataFrame with 'baseline' and 'scenario' as columns.

        Returns:
            pd.DataFrame: DataFrame with 'baseline' and 'scenario' as columns.
        """
        data = self.get_livestock_population()
        return pd.DataFrame.from_dict(data, orient='columns')

