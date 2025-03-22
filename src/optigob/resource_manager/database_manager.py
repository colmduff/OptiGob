"""
Database Manager Module
=======================

This module provides the DatabaseManager class, which is responsible for managing 
the connection to an SQLite database and retrieving various scaler tables as pandas DataFrames.

Classes:
    DatabaseManager: Manages database connections and retrieves scaler tables.

Methods:
    create_engine: Creates a SQLAlchemy engine connected to the SQLite database.
    get_livestock_emission_scaler_table: Retrieves the 'animal_emission_scalers' table.
    get_static_livestock_emission_scaler_table: Retrieves the 'static_animal_emission_scalers' table.
    get_static_livestock_area_scaler_table: Retrieves the 'static_animal_area_scalers' table.
    get_livestock_area_scaler_table: Retrieves the 'animal_area_scalers' table.
    get_forest_scaler_table: Retrieves the 'forest_scalers' table.
    get_static_forest_scaler_table: Retrieves the 'static_forest_scalers' table.
    get_ccs_scaler_table: Retrieves the 'ccs_scalers' table.
    get_hwp_scaler_table: Retrieves the 'hwp_scalers' table.
    get_substitution_scaler_table: Retrieves the 'substitution_scalers' table.
    get_ad_emission_scaler_table: Retrieves the 'ad_emission_scalers' table.
    get_ad_area_scaler_table: Retrieves the 'ad_area_scalers' table.
    get_organic_soil_emission_scaler_table: Retrieves the 'organic_soils_emission_scalers' table.
    get_organic_soil_area_scaler_table: Retrieves the 'organic_soils_area_scalers' table.
    get_crop_scaler_table: Retrieves the 'crop_scalers' table.
"""

import sqlalchemy as sqa
import pandas as pd
from optigob.database import get_local_dir
import os


class DatabaseManager:
    def __init__(self, database_path=None):
        """
        Initializes the DataManager class.
        
        Parameters:
            database_path (str, optional): Path to the SQLite database file. 
                                           If None, uses the default database located in the local directory.
        """
        if database_path is None:
            self.database_dir = get_local_dir()
            self.database_path = os.path.abspath(
                os.path.join(self.database_dir, "optigob_default.db")
            )
        else:
            self.database_path = os.path.abspath(database_path)
            
        self.engine = self.create_engine()

    def create_engine(self):
        """
        Creates a SQLAlchemy engine connected to the SQLite database specified by self.database_path.
        
        Returns:
            sqlalchemy.engine.Engine: A SQLAlchemy engine instance connected to the specified SQLite database.
        """
        engine_url = f"sqlite:///{self.database_path}"
        return sqa.create_engine(engine_url)

    def get_livestock_emission_scaler_table(self):
        """
        Retrieves the 'animal_emission_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'animal_emission_scalers' table data.
        """
        table = "animal_emission_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_static_livestock_emission_scaler_table(self):
        """
        Retrieves the 'static_animal_emission_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'static_animal_emission_scalers' table data.
        """
        table = "static_animal_emission_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_static_livestock_area_scaler_table(self):
        """
        Retrieves the 'static_animal_area_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'static_animal_area_scalers' table data.
        """
        table = "static_animal_area_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_livestock_area_scaler_table(self):
        """
        Retrieves the 'animal_area_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'animal_area_scalers' table data.
        """
        table = "animal_area_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_forest_scaler_table(self):
        """
        Retrieves the 'forest_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'forest_scalers' table data.
        """
        table = "forest_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe

    def get_static_forest_scaler_table(self):
        """
        Retrieves the 'static_forest_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'static_forest_scalers' table data.
        """
        table = "static_forest_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_ccs_scaler_table(self):
        """
        Retrieves the 'ccs_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'ccs_scalers' table data.
        """
        table = "ccs_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_hwp_scaler_table(self):
        """
        Retrieves the 'hwp_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'hwp_scalers' table data.
        """
        table = "hwp_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_substitution_scaler_table(self):
        """
        Retrieves the 'substitution_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'substitution_scalers' table data.
        """
        table = "substitution_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_ad_emission_scaler_table(self):
        """
        Retrieves the 'ad_emission_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'ad_emission_scalers' table data.
        """
        table = "ad_emission_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_ad_area_scaler_table(self):
        """
        Retrieves the 'ad_area_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'ad_area_scalers' table data.
        """
        table = "ad_area_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_organic_soil_emission_scaler_table(self):
        """
        Retrieves the 'organic_soils_emission_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'organic_soils_emission_scalers' table data.
        """
        table = "organic_soils_emission_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_organic_soil_area_scaler_table(self):
        """
        Retrieves the 'organic_soils_area_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'organic_soils_area_scalers' table data.
        """
        table = "organic_soils_area_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
    
    def get_crop_scaler_table(self):
        """
        Retrieves the 'crop_scalers' table from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing the 'crop_scalers' table data.
        """
        table = "crop_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe