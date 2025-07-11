"""
input_query.py
=============

This module defines the InputQuery class, which provides utilities for querying and generating valid input parameter combinations for scenario analysis in the OptiGob framework. It is designed to help users and developers enumerate all valid combinations of key coupled input parameters (such as organic soil and forest management options) for use in scenario generation, sensitivity analysis, or batch modeling.

Classes:
    InputQuery: Provides methods to retrieve all valid input parameter combinations for major coupled parameters (e.g., organic soil, forest) as lists or DataFrames.

Methods in InputQuery:
    __init__(self): Initializes the InputQuery class and underlying data manager.
    get_organic_soil_input_combos(self): Returns all valid organic soil input combinations as a list of dicts.
    get_forest_input_combos(self): Returns all valid forest input combinations as a list of dicts.
    get_abatement_and_productivity_input_combos(self): Returns all valid abatement and productivity input combinations as a list of dicts.
    get_all_input_combos(self): Returns a dict of all valid input combinations for major coupled parameters.
    get_all_input_combos_df(self): Returns a pandas DataFrame of all valid input combinations for major coupled parameters.

Typical usage example:
    iq = InputQuery()
    combos = iq.get_all_input_combos()
    combos_df = iq.get_all_input_combos_df()
"""

from optigob.resource_manager.database_manager import DatabaseManager

class InputQuery():
    """
    InputQuery class for managing input queries in OptiGob.
    Provides methods to enumerate all valid combinations of key input parameters for scenario generation and analysis.
    """

    def __init__(self):
        """
        Initializes the InputQuery class.
        """
        self.data_manager= DatabaseManager()

        self.organic_soil_template =""



    def get_organic_soil_input_combos(self):
        """
        Retrieves all valid organic soil input combinations.
        Returns:
            list: A list of organic soil input combinations.
        """
        organic_soil_df = self.data_manager.get_organic_soil_emission_scaler_table().copy()

        combo_cols = ["wetland_restored_frac", 
                      "organic_soil_under_grass_frac"]
        
        combos = (
            organic_soil_df[combo_cols]
            .drop_duplicates()
            .to_dict(orient="records")
        )
        return combos
    
    def get_forest_input_combos(self):
        """
        Retrieves all valid forest input combinations.
        Returns:
            list: A list of forest input combinations.
        """
        forest_df = self.data_manager.get_forest_scaler_table().copy()

        combo_cols = ["affor_rate_kha-yr", 
                      "broadleaf_frac",
                      "organic_soil_frac",
                      "harvest"]
        
        names = {"afforestation_rate_kha_per_year": "affor_rate_kha-yr",
                 "broadleaf_fraction": "broadleaf_frac",
                 "organic_soil_fraction": "organic_soil_frac",
                 "harvest": "forest_harvest_intensity"}
        
        combos = (
            forest_df[combo_cols]
            .drop_duplicates()
            .rename(columns=names)
            .to_dict(orient="records")
        )
        return combos
    
    def get_abatement_and_productivity_input_combos(self):
        """
        Retrieves all valid input combinations for abatement and productivity scenarios.
        Returns:
            list: A list of abatement and productivity input combinations.
        """

        livestock_protein_df = self.data_manager.get_livestock_protein_scaler_table().copy()

        combo_cols = ["abatement", 
                      "scenario"]
        
        names = {"abatement_type": "abatement",
                 "abatement_scenario": "scenario"}
        
        combos = (
            livestock_protein_df[combo_cols]
            .drop_duplicates()
            .rename(columns=names)
            .to_dict(orient="records")
        )
        return combos
    
    def get_all_input_combos(self):
        """
        Returns a dict of all valid input combinations for major coupled parameters.
        Returns:
            dict: {"forest": [...], "organic_soil": [...]}
        """
        return {
            "forest": self.get_forest_input_combos(),
            "organic_soil": self.get_organic_soil_input_combos(),
            "abatement_and_productivity": self.get_abatement_and_productivity_input_combos(),
            # Add others as needed
        }
    

    def get_all_input_combos_df(self):
        """
        Returns a DataFrame of all valid input combinations for major coupled parameters.
        Returns:
            pd.DataFrame: DataFrame with all input combinations.
        """
        import pandas as pd
        all_combos = self.get_all_input_combos()
        df_list = []
        for key, combos in all_combos.items():
            df = pd.DataFrame(combos)
            df['input_type'] = key  
            df_list.append(df)
        return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()