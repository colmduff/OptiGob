"""
optigob_data_manager
====================

This module provides the OptiGobDataManager class, which is responsible for managing and retrieving
various data scalers related to livestock emissions, forest management, and other land use sectors.
The class interacts with a database to load and cache scaler values, and provides methods to retrieve
these values based on specific parameters.

Classes:
    OptiGobDataManager: Manages and retrieves data scalers for various sectors.

Methods:
    get_ha_to_kha: Retrieves the conversion factor from hectares to kilohectares.
    get_kha_to_ha: Retrieves the conversion factor from square kilohectares to hectares.
    get_AR_gwp100_values: Retrieves the GWP values for each gas based on the AR value.
    get_emission_sectors: Retrieves the emission sectors.
    get_livestock_emission_scaler: Retrieves the scaler value for a given year, system, gas, scenario, and abatement.
    get_livestock_area_scaler: Retrieves the scaler value for a given year, system, scenario, and abatement.
    get_livestock_protein_scaler: Retrieves the scaler value for a given year, system, item, scenario, and abatement.
    get_static_livestock_emission_scaler: Retrieves the static scaler value for a given year, system, gas, and abatement.
    get_static_livestock_area_scaler: Retrieves the static scaler value for a given year, system, and abatement.
    get_static_livestock_protein_scaler: Retrieves the static scaler value for a given year, system, and abatement.
    get_forest_scaler: Retrieves the scaler value for a given year and forest management parameters.
    get_static_forest_scaler: Retrieves the static scaler value for a given year and harvest intensity.
    get_ccs_scaler: Retrieves the CCS scaler value for a given year and forest management parameters.
    get_hwp_scaler: Retrieves the HWP scaler value for a given year and forest management parameters.
    get_substitution_scaler: Retrieves the substitution scaler value for a given year and forest management parameters.
    get_organic_soil_emission_scaler: Retrieves the organic soil emission scaler value for a given year and land management parameters.
    get_organic_soil_area_scaler: Retrieves the organic soil area scaler value for a given year and land management parameters.
    get_ad_area_scaler: Retrieves the AD area scaler value for a given year and land management parameters.
    get_ad_emission_scaler: Retrieves the AD emission scaler value for a given year.
    get_crop_scaler: Retrieves the crop scaler value for a given year, gas, and abatement.
    get_baseline_year: Retrieves the baseline year from the SIP input file.
    get_target_year: Retrieves the target year from the SIP input file.
    get_abatement_scenario: Retrieves the abatement scenario from the SIP input file.
    get_dairy_beef_ratio: Retrieves the dairy to beef ratio from the SIP input file.
    get_forest_harvest_intensity: Retrieves the forest harvest intensity from the SIP input file.
    get_afforestation_rate_kha_per_year: Retrieves the afforestation rate in kha per year from the SIP input file.
    get_broadleaf_fraction: Retrieves the broadleaf fraction from the SIP input file.
    get_organic_soil_fraction_forest: Retrieves the organic soil fraction for forest from the SIP input file.
    get_beccs_included: Retrieves whether BECCS is included from the SIP input file.
    get_wetland_restored_fraction: Retrieves the wetland restored fraction from the SIP input file.
    get_organic_soil_under_grass_fraction: Retrieves the organic soil under grass fraction from the SIP input file.
    get_biomethane_included: Retrieves whether biomethane is included from the SIP input file.
    get_abatement_type: Retrieves the abatement type from the SIP input file.
    get_AR: Retrieves the AR value from the SIP input file.
    get_split_gas: Retrieves whether split gas is used from the SIP input file.
    get_split_gas_fraction: Retrieves the split gas fraction from the SIP input file.
    get_baseline_dairy_population: Retrieves the baseline dairy population from the SIP input file.
    get_baseline_beef_population: Retrieves the baseline beef population from the SIP input file.
"""

from optigob.resource_manager.database_manager import DatabaseManager
from optigob.resource_manager.import_factory import ImportFactory  # Import the ImportFactory
from optigob.resource_manager.input_query import InputQuery
from optigob.logger import get_logger

logger = get_logger("data_manager")

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
        self._livestock_protein_scalers = None
        self._forest_scalers = None
        self._static_forest_scalers = None
        self._wood_ccs_scalers = None
        self._hwp_scalers = None
        self._substitution_scalers = None
        self._organic_soil_emission_scalers = None
        self._organic_soil_area_scalers = None
        self._ad_area_scalers = None
        self._ad_emission_scalers = None
        self._crop_scalers = None
        self._static_livestock_emission_scalers = None
        self._static_livestock_area_scalers = None
        self._static_livestock_protein_scalers = None
        self._protein_crop_emission_scalers = None
        self._protein_crop_protein_scalers = None
        self._protein_content_scalers = None
        self._willow_bioenergy_scalers = None

        # Validate input parameters after loading
        self._validate_input_parameters()


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
            "other_land_use",
            "ad",
            "beccs"]

    def _validate_input_parameters(self):
        """
        Validate that input parameters are consistent and within valid ranges.

        This method performs two types of validation:
        1. Parameter consistency checks (e.g., split_gas and split_gas_frac)
        2. Database combination validation (e.g., forest, organic soil, abatement parameters)

        For database combination validation, the method checks if the provided parameter
        combinations exist in the underlying database. Not all parameter combinations are
        valid - the database contains only specific combinations that have been modeled.

        Use the InputHelper class to explore valid combinations:
            from optigob.input_helper import InputHelper
            helper = InputHelper()
            helper.print_all_combos()  # View all valid combinations

        Raises:
            ValueError: If parameters are invalid, inconsistent, or form an invalid combination
                       not present in the database.

        Warns:
            UserWarning: If parameters are confusing but don't affect calculations.
        """
        split_gas = self.standard_input_parameters.get('split_gas', False)
        split_gas_frac = self.standard_input_parameters.get('split_gas_frac')

        # Warn if split_gas_frac is set when split_gas is False
        if not split_gas and split_gas_frac is not None and split_gas_frac != 0:
            logger.warning(
                f"Parameter Validation Warning:\n"
                f"  split_gas=False but split_gas_frac={split_gas_frac}\n"
                f"  The split_gas_frac parameter is IGNORED when split_gas=False.\n"
                f"  Set split_gas_frac=0 or remove it to avoid confusion."
            )

        # Validate split_gas_frac range when split_gas is True
        if split_gas:
            if split_gas_frac is None or split_gas_frac <= 0 or split_gas_frac >= 1:
                error_msg = (
                    f"Parameter Error:\n"
                    f"  split_gas=True requires split_gas_frac in range (0, 1).\n"
                    f"  Got: split_gas_frac={split_gas_frac}"
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

        # Validate parameter combinations against database
        # Only validate if parameters are provided (allows partial specification)
        self._validate_forest_parameters()
        self._validate_organic_soil_parameters()
        self._validate_abatement_productivity_parameters()

    def _validate_forest_parameters(self):
        """
        Validate forest parameter combinations against database.

        Checks if the provided forest parameters form a valid combination that exists
        in the database. Only validates if all four forest parameters are provided.

        Raises:
            ValueError: If the forest parameter combination is invalid.
        """
        # Extract forest parameters
        affor_rate = self.standard_input_parameters.get('afforestation_rate_kha_per_year')
        broadleaf = self.standard_input_parameters.get('broadleaf_fraction')
        organic = self.standard_input_parameters.get('organic_soil_fraction')
        harvest = self.standard_input_parameters.get('forest_harvest_intensity')

        # Only validate if all parameters are provided
        if not all([affor_rate is not None, broadleaf is not None,
                    organic is not None, harvest is not None]):
            return

        # Get valid combinations from database
        input_query = InputQuery()
        valid_combos = input_query.get_forest_input_combos()

        # Check if the provided combination exists
        user_combo = {
            'affor_rate_kha-yr': affor_rate,
            'broadleaf_frac': broadleaf,
            'organic_soil_frac': organic,
            'forest_harvest_intensity': harvest
        }

        if not any(
            combo['affor_rate_kha-yr'] == user_combo['affor_rate_kha-yr'] and
            combo['broadleaf_frac'] == user_combo['broadleaf_frac'] and
            combo['organic_soil_frac'] == user_combo['organic_soil_frac'] and
            combo['forest_harvest_intensity'] == user_combo['forest_harvest_intensity']
            for combo in valid_combos
        ):
            error_msg = (
                f"Invalid Forest Parameter Combination:\n"
                f"  afforestation_rate_kha_per_year: {affor_rate}\n"
                f"  broadleaf_fraction: {broadleaf}\n"
                f"  organic_soil_fraction: {organic}\n"
                f"  forest_harvest_intensity: {harvest}\n\n"
                f"This combination does not exist in the database.\n"
                f"To see all valid forest parameter combinations, use:\n"
                f"  from optigob.input_helper import InputHelper\n"
                f"  helper = InputHelper()\n"
                f"  helper.filter_combos(input_type='forest')"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

    def _validate_organic_soil_parameters(self):
        """
        Validate organic soil parameter combinations against database.

        Checks if the provided organic soil parameters form a valid combination that
        exists in the database. Only validates if both organic soil parameters are provided.

        Raises:
            ValueError: If the organic soil parameter combination is invalid.
        """
        # Extract organic soil parameters
        wetland = self.standard_input_parameters.get('wetland_restored_frac')
        grass = self.standard_input_parameters.get('organic_soil_under_grass_frac')

        # Only validate if both parameters are provided
        if wetland is None or grass is None:
            return

        # Get valid combinations from database
        input_query = InputQuery()
        valid_combos = input_query.get_organic_soil_input_combos()

        # Check if the provided combination exists
        if not any(
            combo['wetland_restored_frac'] == wetland and
            combo['organic_soil_under_grass_frac'] == grass
            for combo in valid_combos
        ):
            error_msg = (
                f"Invalid Organic Soil Parameter Combination:\n"
                f"  wetland_restored_frac: {wetland}\n"
                f"  organic_soil_under_grass_frac: {grass}\n\n"
                f"This combination does not exist in the database.\n"
                f"To see all valid organic soil parameter combinations, use:\n"
                f"  from optigob.input_helper import InputHelper\n"
                f"  helper = InputHelper()\n"
                f"  helper.filter_combos(input_type='organic_soil')"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

    def _validate_abatement_productivity_parameters(self):
        """
        Validate abatement and productivity parameter combinations against database.

        Checks if the provided abatement_type and abatement_scenario form a valid
        combination that exists in the database. Only validates if both parameters are provided.

        Raises:
            ValueError: If the abatement/productivity parameter combination is invalid.
        """
        # Extract abatement parameters
        abatement_type = self.standard_input_parameters.get('abatement_type')
        abatement_scenario = self.standard_input_parameters.get('abatement_scenario')

        # Only validate if both parameters are provided
        if abatement_type is None or abatement_scenario is None:
            return

        # Get valid combinations from database
        input_query = InputQuery()
        valid_combos = input_query.get_abatement_and_productivity_input_combos()

        # Check if the provided combination exists
        if not any(
            combo['abatement'] == abatement_type and
            combo['scenario'] == abatement_scenario
            for combo in valid_combos
        ):
            error_msg = (
                f"Invalid Abatement/Productivity Parameter Combination:\n"
                f"  abatement_type: {abatement_type}\n"
                f"  abatement_scenario: {abatement_scenario}\n\n"
                f"This combination does not exist in the database.\n"
                f"Valid combinations:\n"
                f"  baseline: scenarios 1, 2, 3\n"
                f"  macc: scenarios 4, 5, 6\n"
                f"  frontier: scenarios 7, 8, 9\n\n"
                f"To see all valid combinations, use:\n"
                f"  from optigob.input_helper import InputHelper\n"
                f"  helper = InputHelper()\n"
                f"  helper.filter_combos(input_type='abatement_and_productivity')"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

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

        Parameters:
            gas (str): The gas identifier (e.g., "CO2", "CH4", "N2O").

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
        """Loads and caches the static livestock scalers from the database."""
        if self._static_livestock_emission_scalers is None:
            self._static_livestock_emission_scalers = self.db_manager.get_static_livestock_emission_scaler_table()
        return self._static_livestock_emission_scalers.copy()
    
    def _load_livestock_area_scalers(self):
        """Loads and caches the livestock area scalers from the database."""
        if self._livestock_area_scalers is None:
            self._livestock_area_scalers = self.db_manager.get_livestock_area_scaler_table()
        return self._livestock_area_scalers.copy()
    
    def _load_static_livestock_area_scalers(self):
        """Loads and caches the static livestock area scalers from the database."""
        if self._static_livestock_area_scalers is None:
            self._static_livestock_area_scalers = self.db_manager.get_static_livestock_area_scaler_table()
        return self._static_livestock_area_scalers.copy()
    
    def _load_livestock_protein_scalers(self):
        """Loads and caches the livestock protein scalers from the database."""
        if self._livestock_protein_scalers is None:
            self._livestock_protein_scalers = self.db_manager.get_livestock_protein_scaler_table()
        return self._livestock_protein_scalers.copy()
    
    def _load_static_livestock_protein_scalers(self):
        """Loads and caches the static livestock protein scalers from the database."""
        if self._static_livestock_protein_scalers is None:
            self._static_livestock_protein_scalers = self.db_manager.get_static_livestock_protein_scaler_table()
        return self._static_livestock_protein_scalers.copy()
    
    def _load_forest_scalers(self):
        """Loads and caches the forest scalers from the database."""
        if self._forest_scalers is None:
            self._forest_scalers = self.db_manager.get_forest_scaler_table()
        return self._forest_scalers.copy()
    
    def _load_static_forest_scalers(self):
        """Loads and caches the static forest scalers from the database."""
        if self._static_forest_scalers is None:
            self._static_forest_scalers = self.db_manager.get_static_forest_scaler_table()
        return self._static_forest_scalers.copy()

    
    def _load_wood_ccs_scalers(self):
        """Loads and caches the CCS scalers from the database."""
        if self._wood_ccs_scalers is None:
            self._wood_ccs_scalers = self.db_manager.get_wood_ccs_scaler_table()
        return self._wood_ccs_scalers.copy()
    
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
        """Loads and caches the AD area scalers from the database."""
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
    
    def _load_protein_crop_emission_scalers(self):
        """Loads and caches the protein crop emission scalers from the database."""
        if self._protein_crop_emission_scalers is None:
            self._protein_crop_emission_scalers = self.db_manager.get_protein_crop_emission_scaler_table()
        return self._protein_crop_emission_scalers.copy()

    def _load_protein_crop_protein_scalers(self):
        """Loads and caches the protein crop protein scalers from the database."""
        if self._protein_crop_protein_scalers is None:
            self._protein_crop_protein_scalers = self.db_manager.get_protein_crop_protein_scaler_table()
        return self._protein_crop_protein_scalers.copy()
    
    def _load_protein_content_scalers(self):
        """Loads and caches the protein content scalers from the database."""
        if self._protein_content_scalers is None:
            self._protein_content_scalers = self.db_manager.get_protein_content_scaler_table()
        return self._protein_content_scalers.copy()

    def _load_willow_bioenergy_scalers(self):
        """Loads and caches the willow bioenergy scalers from the database."""
        if self._willow_bioenergy_scalers is None:
            self._willow_bioenergy_scalers = self.db_manager.get_willow_bioengery_scaler_table()
        return self._willow_bioenergy_scalers.copy()
    

    def get_livestock_emission_scaler(self, year, system, gas, scenario, abatement):
        """
        Retrieves the scaler value for a given year, system, gas, and scenario.
        
        Parameters:
            year (int): The year of interest.
            system (str): The system identifier.
            gas (str): The gas identifier.
            scenario (int): The scenario identifier.
            abatement (int): The abatement identifier.
        
        Returns:
            dict: The scaler value and additional information.
        
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
            error_msg = (
                f"No matching livestock emission scaler found for:\n"
                f"  year={year}, system={system}, gas={gas}, "
                f"scenario={scenario}, abatement={abatement}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
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
            system (str or list): The system identifier(s).
            scenario (int): The scenario identifier.
            abatement (int): The abatement identifier.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_livestock_area_scalers()

        filtered = df[
            (df["year"] == year) &
            (df["system"]== system) &
            (df["scenario"] == scenario) &
            (df["abatement"] == abatement)
        ]
        if filtered.empty:
            error_msg = (
                f"No matching livestock area scaler found for:\n"
                f"  year={year}, system={system}, "
                f"scenario={scenario}, abatement={abatement}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.

        output = {"system": system,
                  "scenario": scenario,
                  "year": year,
                  "area": filtered["value"].item(),
                  "hnv_area": filtered["hnv_area"].item()}
        return output
    
    def get_livestock_protein_scaler(self, year, system, item, scenario, abatement):
        """
        Retrieves the scaler value for a given year, system, and scenario.
        
        Parameters:
            year (int): The year of interest.
            system (str): The system identifier.
            item (str): The item identifier.
            scenario (int): The scenario identifier.
            abatement (int): The abatement identifier.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_livestock_protein_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == year) &
            (df["system"] == system) &
            (df["item"] == item) &
            (df["scenario"] == scenario) &
            (df["abatement"] == abatement)
        ]
        if filtered.empty:
            error_msg = (
                f"No matching livestock protein scaler found for:\n"
                f"  year={year}, system={system}, item={item}, "
                f"scenario={scenario}, abatement={abatement}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_static_livestock_emission_scaler(self,
                                            year,
                                            system, 
                                            gas, 
                                            abatement):
        """
        Retrieves the static scaler value for a given year, system, gas, and abatement.
        
        Parameters:
            year (int): The year of interest.
            system (str): The system identifier.
            gas (str): The gas identifier.
            abatement (int): The abatement identifier.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
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
            error_msg = (
                f"No matching static livestock emission scaler found for:\n"
                f"  year={year}, system={system}, gas={gas}, abatement={abatement}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_static_livestock_area_scaler(self,
                                        year,
                                        system,
                                        abatement):
        """
        Retrieves the static scaler value for a given year, system, and abatement.
        
        Parameters:
            year (int): The year of interest.
            system (str): The system identifier.
            abatement (int): The abatement identifier.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
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
            error_msg = (
                f"No matching static livestock area scaler found for:\n"
                f"  year={year}, system={system}, abatement={abatement}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_static_livestock_protein_scaler(self, year, system, item, abatement):
        """
        Retrieves the static scaler value for a given year, system, and abatement.
        
        Parameters:
            year (int): The year of interest.
            system (str): The system identifier.
            item (str): The item identifier.
            abatement (int): The abatement identifier.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_static_livestock_protein_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == year) &
            (df["system"] == system) &
            (df["item"] == item) &
            (df["scenario"] == 0) &
            (df["abatement"] == abatement)
        ]
        if filtered.empty:
            error_msg = (
                f"No matching static livestock protein scaler found for:\n"
                f"  year={year}, system={system}, item={item}, abatement={abatement}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_forest_scaler(self, target_year, affor_rate, broadleaf_frac, organic_soil_frac, harvest):
        """
        Retrieves the scaler value for a given year and forest management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            affor_rate (float): The afforestation rate in kha per year.
            broadleaf_frac (float): The fraction of broadleaf trees.
            organic_soil_frac (float): The fraction of organic soil.
            harvest (float): The forest harvest intensity.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
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
            error_msg = (
                f"No matching forest scaler found for:\n"
                f"  year={target_year}, affor_rate={affor_rate}, broadleaf_frac={broadleaf_frac}, "
                f"organic_soil_frac={organic_soil_frac}, harvest={harvest}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_static_forest_scaler(self, target_year,harvest):
        """
        Retrieves the static scaler value for a given year and harvest intensity.
        
        Parameters:
            target_year (int): The year of interest.
            harvest (float): The forest harvest intensity.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_static_forest_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year) &
            (df["harvest"] == harvest)
        ]

        if filtered.empty:
            error_msg = (
                f"No matching static forest scaler found for:\n"
                f"  year={target_year}, harvest={harvest}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_wood_ccs_scaler(self,target_year, affor_rate, broadleaf_frac, organic_soil_frac, harvest):
        """
        Retrieves the CCS scaler value for a given year and forest management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            affor_rate (float): The afforestation rate in kha per year.
            broadleaf_frac (float): The fraction of broadleaf trees.
            organic_soil_frac (float): The fraction of organic soil.
            harvest (float): The forest harvest intensity.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_wood_ccs_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year) &
            (df["affor_rate_kha-yr"] == affor_rate) &
            (df["broadleaf_frac"] == broadleaf_frac) &
            (df["organic_soil_frac"] == organic_soil_frac) &
            (df["harvest"] == harvest)
        ]
        if filtered.empty:
            error_msg = (
                f"No matching wood CCS scaler found for:\n"
                f"  year={target_year}, affor_rate={affor_rate}, broadleaf_frac={broadleaf_frac}, "
                f"organic_soil_frac={organic_soil_frac}, harvest={harvest}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_hwp_scaler(self,target_year, affor_rate, broadleaf_frac, organic_soil_frac, harvest):
        """
        Retrieves the HWP scaler value for a given year and forest management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            affor_rate (float): The afforestation rate in kha per year.
            broadleaf_frac (float): The fraction of broadleaf trees.
            organic_soil_frac (float): The fraction of organic soil.
            harvest (float): The forest harvest intensity.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
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
            error_msg = (
                f"No matching HWP scaler found for:\n"
                f"  year={target_year}, affor_rate={affor_rate}, broadleaf_frac={broadleaf_frac}, "
                f"organic_soil_frac={organic_soil_frac}, harvest={harvest}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_substitution_scaler(self,target_year, affor_rate, broadleaf_frac, organic_soil_frac, harvest):
        """
        Retrieves the substitution scaler value for a given year and forest management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            affor_rate (float): The afforestation rate in kha per year.
            broadleaf_frac (float): The fraction of broadleaf trees.
            organic_soil_frac (float): The fraction of organic soil.
            harvest (float): The forest harvest intensity.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
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
            error_msg = (
                f"No matching substitution scaler found for:\n"
                f"  year={target_year}, affor_rate={affor_rate}, broadleaf_frac={broadleaf_frac}, "
                f"organic_soil_frac={organic_soil_frac}, harvest={harvest}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered


    def get_organic_soil_emission_scaler(self, 
                                         target_year,
                                        wetland_restored_frac, 
                                        organic_soil_under_grass_frac):
        """
        Retrieves the organic soil emission scaler value for a given year and land management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            wetland_restored_frac (float): The fraction of wetland restored.
            organic_soil_under_grass_frac (float): The fraction of organic soil under grass.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
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
            error_msg = (
                f"No matching organic soil emission scaler found for:\n"
                f"  year={target_year}, wetland_restored_frac={wetland_restored_frac}, "
                f"organic_soil_under_grass_frac={organic_soil_under_grass_frac}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_organic_soil_area_scaler(self,
                                    target_year,
                                    wetland_restored_frac,
                                    organic_soil_under_grass_frac):
        """
        Retrieves the organic soil area scaler value for a given year and land management parameters.
        
        Parameters:
            target_year (int): The year of interest.
            wetland_restored_frac (float): The fraction of wetland restored.
            organic_soil_under_grass_frac (float): The fraction of organic soil under grass.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
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
            error_msg = (
                f"No matching organic soil area scaler found for:\n"
                f"  year={target_year}, wetland_restored_frac={wetland_restored_frac}, "
                f"organic_soil_under_grass_frac={organic_soil_under_grass_frac}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_ad_area_scaler(self, target_year):
        """
        Retrieves the AD area scaler value for a given year.
        
        Parameters:
            target_year (int): The year of interest.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_ad_area_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year)
        ]
        if filtered.empty:
            error_msg = f"No matching AD area scaler found for: year={target_year}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_ad_emission_scaler(self, target_year):
        """
        Retrieves the AD emission scaler value for a given year.
        
        Parameters:
            target_year (int): The year of interest.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_ad_emission_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == target_year)
        ]
        if filtered.empty:
            error_msg = f"No matching AD emission scaler found for: year={target_year}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    def get_crop_scaler(self, year, gas, abatement):
        """
        Retrieves the crop scaler value for a given year, gas, and abatement.
        
        Parameters:
            year (int): The year of interest.
            gas (str): The gas identifier.
            abatement (int): The abatement identifier.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
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
            error_msg = (
                f"No matching crop scaler found for:\n"
                f"  year={year}, gas={gas}, abatement={abatement}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered


    def get_protein_crop_emission_scaler(self, year, ghg,abatement):
        """
        Retrieves the protein crop emission scaler value for a given year, crop, gas, and abatement.
        """


        df = self._load_protein_crop_emission_scalers()

        filtered = df[
            (df["year"] == year) &
            (df["ghg"] == ghg) &
            (df["abatement"] == abatement)
        ]
        if filtered.empty:
            error_msg = (
                f"No matching protein crop emission scaler found for:\n"
                f"  year={year}, ghg={ghg}, abatement={abatement}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        return filtered

    def get_protein_crop_protein_scaler(self, year, abatement):
        """
        Retrieves the protein crop protein scaler value for a given year, crop, and abatement.
        """
        df = self._load_protein_crop_protein_scalers()
        filtered = df[
            (df["year"] == year) &
            (df["abatement"] == abatement)
        ]
        if filtered.empty:
            error_msg = (
                f"No matching protein crop protein scaler found for:\n"
                f"  year={year}, abatement={abatement}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        return filtered

    def get_protein_content_scaler(self, type):
        """
        Retrieves the protein content scaler value.
        
        Returns:
            DataFrame: The DataFrame containing the protein content scaler values.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_protein_content_scalers()
        # Filter the DataFrame based on the provided type.
        filtered = df[df["type"] == type]

        if filtered.empty:
            error_msg = f"No matching protein content scaler found for: type={type}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        item = filtered["conversion"].item()
        return item

    def get_willow_bioenergy_scaler(self, year, type, ghg):
        """
        Retrieves the willow bioenergy scaler value for a given year, type, and gas.
        
        Parameters:
            year (int): The year of interest.
            type (str): The type of willow bioenergy.
            ghg (str): The greenhouse gas identifier.
        
        Returns:
            DataFrame: The filtered DataFrame containing the scaler values.
        
        Raises:
            ValueError: If no matching row is found.
        """
        df = self._load_willow_bioenergy_scalers()

        # Filter the DataFrame based on the provided parameters.
        filtered = df[
            (df["year"] == year) &
            (df["type"] == type) &
            (df["ghg"] == ghg)
        ]
        if filtered.empty:
            error_msg = (
                f"No matching willow bioenergy scaler found for:\n"
                f"  year={year}, type={type}, ghg={ghg}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Return the scaler value; if more than one row matches, we take the first.
        return filtered

    # Getter methods for the input parameters.
    def get_baseline_year(self):
        """
        Retrieves the baseline year from the SIP input file.

        Returns:
            int: The baseline year.
        """
        return self.standard_input_parameters.get("baseline_year")

    def get_target_year(self):
        """
        Retrieves the target year from the SIP input file.

        Returns:
            int: The target year.
        """
        return self.standard_input_parameters.get("target_year")

    def get_abatement_scenario(self):
        """
        Retrieves the abatement scenario from the SIP input file.

        Returns:
            str: The abatement scenario.
        """
        return self.standard_input_parameters.get("abatement_scenario")
    
    def get_livestock_ratio_type(self):
        """
        Retrieves the livestock ratio type from the SIP input file.

        Returns:
            str: The livestock ratio type.
        """
        return self.standard_input_parameters.get("livestock_ratio_type")

    def get_livestock_ratio_value(self):
        """
        Retrieves the livestock ratio from the SIP input file.

        Returns:
            float: The livestock ratio.
        """
        return self.standard_input_parameters.get("livestock_ratio_value")

    def get_forest_harvest_intensity(self):
        """
        Retrieves the forest harvest intensity from the SIP input file.

        Returns:
            float: The forest harvest intensity.
        """
        return self.standard_input_parameters.get("forest_harvest_intensity")

    def get_afforestation_rate_kha_per_year(self):
        """
        Retrieves the afforestation rate in kha per year from the SIP input file.

        Returns:
            float: The afforestation rate in kha per year.
        """
        return self.standard_input_parameters.get("afforestation_rate_kha_per_year")

    def get_broadleaf_fraction(self):
        """
        Retrieves the broadleaf fraction from the SIP input file.

        Returns:
            float: The broadleaf fraction.
        """
        return self.standard_input_parameters.get("broadleaf_fraction")

    def get_organic_soil_fraction_forest(self):
        """
        Retrieves the organic soil fraction for forest from the SIP input file.

        Returns:
            float: The organic soil fraction for forest.
        """
        return self.standard_input_parameters.get("organic_soil_fraction")
    
    def get_beccs_included(self):
        """
        Retrieves whether BECCS is included from the SIP input file.

        Returns:
            bool: True if BECCS is included, False otherwise.
        """
        return self.standard_input_parameters.get("beccs_included")

    def get_wetland_restored_fraction(self):
        """
        Retrieves the wetland restored fraction from the SIP input file.

        Returns:
            float: The wetland restored fraction.
        """
        return self.standard_input_parameters.get("wetland_restored_frac")
    
    def get_organic_soil_under_grass_fraction(self):
        """
        Retrieves the organic soil under grass fraction from the SIP input file.

        Returns:
            float: The organic soil under grass fraction.
        """
        return self.standard_input_parameters.get("organic_soil_under_grass_frac")
    
    def get_biomethane_included(self):
        """
        Retrieves whether biomethane is included from the SIP input file.

        Returns:
            bool: True if biomethane is included, False otherwise.
        """
        return self.standard_input_parameters.get("biomethane_included")

    def get_abatement_type(self):
        """
        Retrieves the abatement type from the SIP input file.

        Returns:
            str: The abatement type.
        """
        return self.standard_input_parameters.get("abatement_type")
    
    def get_AR(self):
        """
        Retrieves the AR value from the SIP input file.

        Returns:
            str: The AR value.
        """
        return self.standard_input_parameters.get("AR")
    
    def get_split_gas(self):
        """
        Retrieves whether split gas is used from the SIP input file.

        Returns:
            bool: True if split gas is used, False otherwise.
        """
        return self.standard_input_parameters.get("split_gas")
    
    def get_split_gas_fraction(self):
        """
        Retrieves the split gas fraction from the SIP input file.

        Returns:
            float: The split gas fraction.
        """
        return self.standard_input_parameters.get("split_gas_frac")
    
    def get_protein_crop_included(self):
        """
        Retrieves whether protein crop is included from the SIP input file.

        Returns:
            bool: True if protein crop is included, False otherwise.
        """
        return self.standard_input_parameters.get("protein_crop_included")
    
    def get_protein_crop_multiplier(self):
        """
        Retrieves the protein crop multiplier from the SIP input file.

        Returns:
            float: The protein crop multiplier.
        """
        return self.standard_input_parameters.get("protein_crop_multiplier")
    
    def get_beccs_willow_area_multiplier(self):
        """
        Retrieves the BECCS willow area multiplier from the SIP input file.

        Returns:
            float: The BECCS willow area multiplier.
        """
        return self.standard_input_parameters.get("beccs_willow_area_multiplier")
    
    def get_pig_and_poultry_multiplier(self):
        """
        Retrieves the pig and poultry multiplier from the SIP input file.

        Returns:
            float: The pig and poultry multiplier.
        """
        return self.standard_input_parameters.get("pig_and_poultry_multiplier")
    
    def get_baseline_dairy_population(self):
        """
        Retrieves the baseline dairy population from the SIP input file.

        Returns:
            int: The baseline dairy population.
        """
        return self.standard_input_parameters.get("baseline_dairy_pop")
    
    def get_baseline_beef_population(self):
        """
        Retrieves the baseline beef population from the SIP input file.

        Returns:
            int: The baseline beef population.
        """
        return self.standard_input_parameters.get("baseline_beef_pop")