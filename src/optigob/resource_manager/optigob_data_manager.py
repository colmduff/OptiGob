from optigob.resource_manager.database_manager import DatabaseManager
from optigob.resource_manager.import_factory import ImportFactory  # Import the ImportFactory
import json

class OptiGobDataManager:
    def __init__(self, sip):
        """
        Initializes the OptiGobDataManager.

        Parameters:
            sip (str or dict): A file path to a JSON, YAML, CSV file or a dictionary containing
                               the standard input parameters. Expected keys are:
                               - "baseline_year"
                               - "target_year"
                               - "abatement_scenario"
                               - "gas"
                               - "emissions_budget"
                               - "dairy_beef_ratio"
        """
        # If sip is a string, assume it's a file path and load the configuration using ImportFactory.
        if isinstance(sip, str):
            self.standard_input_parameters = ImportFactory.load_config(sip)
        else:
            self.standard_input_parameters = sip
        
        self.db_manager = DatabaseManager()

        self._livestock_emission_scalers = None  
        self._livestock_area_scalers = None
        self._forest_scalers = None
        self._static_forest_scalers = None
        self._ccs_scalers = None
        self._hwp_scalers = None
        self._substitution_scalers = None
        self._organic_soil_emission_scalers = None
        self._organic_soil_area_scalers = None
        self._ad_area_scalers = None
        self._ad_emission_scalers = None
        self._crop_scalers = None
        self._static_livestock_emission_scalers = None
        self._static_livestock_area_scalers = None

        self._ha_to_kha = 1e-3
        self._kha_to_ha = 1e3

        self._AR_VALUES = {
            "AR5": {
                "CO2": 1,
                "CH4": 28,
                "N2O": 265,
            },
            "AR6": {
                "CO2": 1,
                "CH4": 27,
                "N2O": 273,
            },
        }

        self.emission_sectors = [
            "agriculture",
            "existing_forest",
            "afforestation",
            "hwp",
            "wood_substitution",
            "wood_ccs",
            "other_land_use",
            "ad"]

    def get_ha_to_kha(self):
        """
        Retrieves the conversion factor from hectares to square kilometers.

        Returns:
            float: The conversion factor.
        """
        return self._ha_to_kha
    
    def get_kha_to_ha(self):
        """
        Retrieves the conversion factor from square kilometers to hectares.

        Returns:
            float: The conversion factor.
        """
        return self._kha_to_ha
    

    def get_AR_gwp100_values(self, gas):
        """
        Retrieves the GWP values for each gas based on the AR value.

        Returns:
            dict: The GWP values for each gas.
        """
        return self._AR_VALUES["AR"+str(self.get_AR())][gas]
    
    def get_emission_sectors(self):
        """
        Retrieves the emission sectors.

        Returns:
            list: The emission sectors.
        """
        return self.emission_sectors

    def _load_livestock_emission_scalers(self):
        """Loads and caches the livestock scalers from the database."""
        if self._livestock_emission_scalers is None:
            self._livestock_emission_scalers = self.db_manager.get_livestock_emission_scaler_table()
        return self._livestock_emission_scalers.copy()
    
    def _load_static_livestock_emission_scalers(self):
        """Loads and caches the livestock scalers from the database."""
        if self._static_livestock_emission_scalers is None:
            self._static_livestock_emission_scalers = self.db_manager.get_static_livestock_emission_scaler_table()
        return self._static_livestock_emission_scalers.copy()
    
    def _load_livestock_area_scalers(self):
        """Loads and caches the livestock area scalers from the database."""
        if self._livestock_area_scalers is None:
            self._livestock_area_scalers = self.db_manager.get_livestock_area_scaler_table()
        return self._livestock_area_scalers.copy()
    
    def _load_static_livestock_area_scalers(self):
        """Loads and caches the livestock area scalers from the database."""
        if self._static_livestock_area_scalers is None:
            self._static_livestock_area_scalers = self.db_manager.get_static_livestock_area_scaler_table()
        return self._static_livestock_area_scalers.copy()
    
    def _load_forest_scalers(self):
        """Loads and caches the forest scalers from the database."""
        if self._forest_scalers is None:
            self._forest_scalers = self.db_manager.get_forest_scaler_table()
        return self._forest_scalers.copy()
    
    def _load_static_forest_scalers(self):
        """Loads and caches the forest scalers from the database."""
        if self._static_forest_scalers is None:
            self._static_forest_scalers = self.db_manager.get_static_forest_scaler_table()
        return self._static_forest_scalers.copy()

    
    def _load_ccs_scalers(self):
        """Loads and caches the CCS scalers from the database."""
        if self._ccs_scalers is None:
            self._ccs_scalers = self.db_manager.get_ccs_scaler_table()
        return self._ccs_scalers.copy()
    
    def _load_hwp_scalers(self):
        """Loads and caches the HWP scalers from the database."""
        if self._hwp_scalers is None:
            self._hwp_scalers = self.db_manager.get_hwp_scaler_table()
        return self._hwp_scalers.copy()
    
    def _load_substitution_scalers(self):
        """Loads and caches the substitution scalers from the database."""
        if self._substitution_scalers is None:
            self._substitution_scalers = self.db_manager.get_substitution_scaler_table()
        return self._substitution_scalers.copy()

    def _load_organic_soil_emission_scalers(self):
        """Loads and caches the organic soil emission scalers from the database."""
        if self._organic_soil_emission_scalers is None:
            self._organic_soil_emission_scalers = self.db_manager.get_organic_soil_emission_scaler_table()
        return self._organic_soil_emission_scalers.copy()
    
    def _load_organic_soil_area_scalers(self):
        """Loads and caches the organic soil area scalers from the database."""
        if self._organic_soil_area_scalers is None:
            self._organic_soil_area_scalers = self.db_manager.get_organic_soil_area_scaler_table()
        return self._organic_soil_area_scalers.copy()
    
    def _load_ad_area_scalers(self):
        """Loads and caches the AD scalers from the database."""
        if self._ad_area_scalers is None:
            self._ad_area_scalers = self.db_manager.get_ad_area_scaler_table()
        return self._ad_area_scalers.copy()
    
    def _load_ad_emission_scalers(self):
        """Loads and caches the AD emission scalers from the database."""
        if self._ad_emission_scalers is None:
            self._ad_emission_scalers = self.db_manager.get_ad_emission_scaler_table()
        return self._ad_emission_scalers.copy()
    
    def _load_crop_scalers(self):
        """Loads and caches the crop scalers from the database."""
        if self._crop_scalers is None:
            self._crop_scalers = self.db_manager.get_crop_scaler_table()
        return self._crop_scalers.copy()
    
    def get_livestock_emission_scaler(self, year, system, gas, scenario, abatement):
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
        df = self._load_livestock_emission_scalers()
        # Filter the DataFrame based on the provided parameters.

        filtered = df[
            (df["year"] == year) &
            (df["system"] == system) &
            (df["ghg"] == gas) &
            (df["scenario"] == scenario) & 
            (df["abatement"] == abatement)
        ]

        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.

        output = {"system": system, 
                  "gas": gas, 
                  "scenario": scenario, 
                  "year": year, 
                  "value": filtered["value"].item(),
                  "pop": filtered["pop"].item()}
        return output            
    
    def get_livestock_area_scaler(self, year, system, scenario, abatement):
        """
        Retrieves the scaler value for a given year, system, and scenario.
        
        Parameters:
            year (int): The year of interest.
            system (str): The system identifier.
            scenario (int): The scenario identifier.
        
        Returns:
           dataframe: containing the scaler value from the "value" column.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_livestock_area_scalers()

        # Ensure `system` is treated as a list
        if not isinstance(system, list):
            system = [system]

        filtered = df[
            (df["year"] == year) &
            (df["system"].isin(system)) &
            (df["scenario"] == scenario) &
            (df["abatement"] == abatement)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered
    
    def get_static_livestock_emission_scaler(self,
                                            year,
                                            system, 
                                            gas, 
                                            abatement):
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
        df = self._load_static_livestock_emission_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == year) &
            (df["system"] == system) &
            (df["ghg"] == gas) &
            (df["scenario"] == 0) & 
            (df["abatement"] == abatement)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_static_livestock_area_scaler(self,
                                        year,
                                        system,
                                        abatement):
        """
        Retrieves the scaler value for a given year, system, and scenario.

        Parameters:
            year (int): The year of interest.
            system (str): The system identifier.
            scenario (int): The scenario identifier.

        Returns:
            float: The scaler value from the "Value" column.

        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_static_livestock_area_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == year) &
            (df["system"] == system) &
            (df["scenario"] == 0) & 
            (df["abatement"] == abatement)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered


    def get_forest_scaler(self, target_year, affor_rate, broadleaf_frac, organic_soil_frac, harvest):
        """
        Retrieves the scaler value for a given year and forest management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            affor_rate (float): The afforestation rate in kha per year.
            broad_frac (float): The fraction of broadleaf trees.
            org_soil_frac (float): The fraction of organic soil.
            harvest_intensity (float): The forest harvest intensity.
        
        Returns:
            float: The scaler value from the "Value" column.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_forest_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year) &
            (df["affor_rate_kha-yr"] == affor_rate) &
            (df["broadleaf_frac"] == broadleaf_frac) &
            (df["organic_soil_frac"] == organic_soil_frac) &
            (df["harvest"] == harvest)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered
    
    def get_static_forest_scaler(self, target_year,harvest):

        df = self._load_static_forest_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year) &
            (df["harvest"] == harvest)
        ]

        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered
    
    def get_ccs_scaler(self,target_year, affor_rate, broadleaf_frac, organic_soil_frac, harvest):
        """
        Retrieves the scaler value for a given year and forest management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            affor_rate (float): The afforestation rate in kha per year.
            broad_frac (float): The fraction of broadleaf trees.
            org_soil_frac (float): The fraction of organic soil.
            harvest_intensity (float): The forest harvest intensity.
        
        Returns:
            float: The scaler value from the "Value" column.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_ccs_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year) &
            (df["affor_rate_kha-yr"] == affor_rate) &
            (df["broadleaf_frac"] == broadleaf_frac) &
            (df["organic_soil_frac"] == organic_soil_frac) &
            (df["harvest"] == harvest)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered
    
    def get_hwp_scaler(self,target_year, affor_rate, broadleaf_frac, organic_soil_frac, harvest):
        """
        Retrieves the scaler value for a given year and forest management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            affor_rate (float): The afforestation rate in kha per year.
            broad_frac (float): The fraction of broadleaf trees.
            org_soil_frac (float): The fraction of organic soil.
            harvest_intensity (float): The forest harvest intensity.
        
        Returns:
            float: The scaler value from the "Value" column.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_hwp_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year) &
            (df["affor_rate_kha-yr"] == affor_rate) &
            (df["broadleaf_frac"] == broadleaf_frac) &
            (df["organic_soil_frac"] == organic_soil_frac) &
            (df["harvest"] == harvest)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered
    
    def get_substitution_scaler(self,target_year, affor_rate, broadleaf_frac, organic_soil_frac, harvest):
        """
        Retrieves the scaler value for a given year and forest management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            affor_rate (float): The afforestation rate in kha per year.
            broad_frac (float): The fraction of broadleaf trees.
            org_soil_frac (float): The fraction of organic soil.
            harvest_intensity (float): The forest harvest intensity.
        
        Returns:
            float: The scaler value from the "Value" column.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_substitution_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year) &
            (df["affor_rate_kha-yr"] == affor_rate) &
            (df["broadleaf_frac"] == broadleaf_frac) &
            (df["organic_soil_frac"] == organic_soil_frac) &
            (df["harvest"] == harvest)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered


    def get_organic_soil_emission_scaler(self, 
                                         target_year,
                                        wetland_restored_frac, 
                                        organic_soil_under_grass_frac):
        """
        Retrieves the scaler value for a given year and forest management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            wetland_restored_frac (float): The fraction of wetland restored.
            organic_soil_under_grass_frac (float): The fraction of organic soil under grass.
        
        Returns:
            float: The scaler value from the "Value" column.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_organic_soil_emission_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year) &
            (df["wetland_restored_frac"] == wetland_restored_frac) &
            (df["organic_soil_under_grass_frac"] == organic_soil_under_grass_frac)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered
    
    def get_organic_soil_area_scaler(self,
                                    target_year,
                                    wetland_restored_frac,
                                    organic_soil_under_grass_frac):
        """
        Retrieves the scaler value for a given year and forest management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            wetland_restored_frac (float): The fraction of wetland restored.
            organic_soil_under_grass_frac (float): The fraction of organic soil under grass.
        
        Returns:
            float: The scaler value from the "Value" column.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_organic_soil_area_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year) &
            (df["wetland_restored_frac"] == wetland_restored_frac) &
            (df["organic_soil_under_grass_frac"] == organic_soil_under_grass_frac)
        ]


        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered
    
    def get_ad_area_scaler(self, target_year):
        """
        Retrieves the area scaler value for a given year.
        
        Parameters:
            target_year (int): The year of interest.
        
        Returns:
            float: The area scaler value from the "Value" column.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_ad_area_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered
    
    def get_ad_emission_scaler(self, target_year):
        """
        Retrieves the emission scaler value for a given year.
        
        Parameters:
            target_year (int): The year of interest.
        
        Returns:
            float: The emission scaler value from the "Value" column.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_ad_emission_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year)
        ]
        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered
    
    def get_crop_scaler(self, year, gas, abatement):
        """
        Retrieves the scaler value for a given year, gas, and scenario.
        
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
        df = self._load_crop_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == year) &
            (df["ghg"] == gas) &
            (df["scenario"] == 0) & 
            (df["abatement"] == abatement)
        ]

        if filtered.empty:
            raise ValueError("No matching scaler found for the provided parameters.")
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered


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

    def get_forest_harvest_intensity(self):
        return self.standard_input_parameters.get("forest_harvest_intensity")

    def get_afforestation_rate_kha_per_year(self):
        return self.standard_input_parameters.get("afforestation_rate_kha_per_year")

    def get_broadleaf_fraction(self):
        return self.standard_input_parameters.get("broadleaf_fraction")

    def get_organic_soil_fraction_forest(self):
        return self.standard_input_parameters.get("organic_soil_fraction")
    
    def get_beccs_included(self):
        return self.standard_input_parameters.get("beccs_included")

    def get_wetland_restored_fraction(self):
        return self.standard_input_parameters.get("wetland_restored_frac")
    
    def get_organic_soil_under_grass_fraction(self):
        return self.standard_input_parameters.get("organic_soil_under_grass_frac")
    
    def get_biomethane_included(self):
        return self.standard_input_parameters.get("biomethane_included")

    def get_abatement_type(self):
        return self.standard_input_parameters.get("abatement_type")
    
    def get_AR(self):
        return self.standard_input_parameters.get("AR")
    
    def get_split_gas(self):
        return self.standard_input_parameters.get("split_gas")
    
    def get_split_gas_fraction(self):
        return self.standard_input_parameters.get("split_gas_frac")
    
    def get_baseline_dairy_population(self):
        return self.standard_input_parameters.get("baseline_dairy_pop")
    
    def get_baseline_beef_population(self):
        return self.standard_input_parameters.get("baseline_beef_pop")