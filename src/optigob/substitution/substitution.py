"""
Substitution Module
==================

This module contains the Substitution class, which centralizes all substitution impact logic (AD, wood, willow, etc.)
from across the codebase. All substitution-related calculations should be implemented or wrapped here for modularity and maintainability.

Class:
    Substitution: Centralizes substitution impact calculations for AD, wood, willow, and other relevant sectors.

Methods in Substitution:
    __init__(self, optigob_data_manager): Initializes the Substitution class with the data manager.
    get_ad_substitution_co2_emission(self): Returns the AD-Substitution CO2 emissions in kilotons.
    get_ad_substitution_ch4_emission(self): Returns the AD-Substitution CH4 emissions in kilotons.
    get_ad_substitution_n2o_emission(self): Returns the AD-Substitution N2O emissions in kilotons.
    get_ad_substitution_co2e_emission(self): Returns the AD-Substitution CO2e emissions in kilotons.
    get_forest_substitution_offset_co2e(self): Calculates the emission offset from forest substitution effects (in kt).
    get_willow_substitution_offset_co2e(self): Calculates the willow substitution emission offset in kilotons.
"""

class Substitution:
    def __init__(self, optigob_data_manager):
        """
        Initializes the Substitution class.
        """
        self.data_manager_class = optigob_data_manager
        self.beccs_included = self.data_manager_class.get_beccs_included()
        self.biomethane_included = self.data_manager_class.get_biomethane_included()

        self.target_year = self.data_manager_class.get_target_year()
        self.afforestation_rate = self.data_manager_class.get_afforestation_rate_kha_per_year()
        self.harvest_rate = self.data_manager_class.get_forest_harvest_intensity()
        self.organic_soil_fraction = self.data_manager_class.get_organic_soil_fraction_forest()
        self.broadleaf_fraction = self.data_manager_class.get_broadleaf_fraction()

    
    def zero_if_beccs_not_included(method):
        def wrapper(self, *args, **kwargs):
            if not self.beccs_included:
                return 0
            return method(self, *args, **kwargs)
        return wrapper
    
    def zero_if_biomethane_not_included(method):
        def wrapper(self, *args, **kwargs):
            if not self.biomethane_included:
                return 0
            return method(self, *args, **kwargs)
        return wrapper

    @zero_if_biomethane_not_included
    def get_ad_substitution_co2_emission(self):
        """
        Returns the AD-Substitution CO2 emissions in kilotons.
        """
        ad_substitution_co2_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_co2_emission[(ad_substitution_co2_emission["type"] == "AD-Substitution") & (ad_substitution_co2_emission["ghg"] == "CO2")]

        return filtered["emission_value"].item()
    
    @zero_if_biomethane_not_included
    def get_ad_substitution_ch4_emission(self):
        """
        Returns the AD-Substitution CH4 emissions in kilotons.
        """
        ad_substitution_ch4_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_ch4_emission[(ad_substitution_ch4_emission["type"] == "AD-Substitution") & (ad_substitution_ch4_emission["ghg"] == "CH4")]

        return filtered["emission_value"].item()
    
    @zero_if_biomethane_not_included
    def get_ad_substitution_n2o_emission(self):
        """
        Returns the AD-Substitution N2O emissions in kilotons.
        """
        ad_substitution_n2o_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_n2o_emission[(ad_substitution_n2o_emission["type"] == "AD-Substitution") & (ad_substitution_n2o_emission["ghg"] == "N2O")]

        return filtered["emission_value"].item()
    
    
    @zero_if_biomethane_not_included
    def get_ad_substitution_co2e_emission(self):
        """
        Returns the AD-Substitution CO2e emissions in kilotons.
        """
        ad_substitution_co2e_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_co2e_emission[(ad_substitution_co2e_emission["type"] == "AD-Substitution") & (ad_substitution_co2e_emission["ghg"] == "CO2e")]

        return filtered["emission_value"].item()
    
    
    def get_forest_substitution_offset_co2e(self):
        """
        Calculates the emission offset from substitution effects.
        """
        substitution_df = self.data_manager_class.get_substitution_scaler(
            target_year=self.target_year,
            affor_rate=self.afforestation_rate,
            broadleaf_frac=self.broadleaf_fraction,
            organic_soil_frac=self.organic_soil_fraction,
            harvest=self.harvest_rate
        )
        return substitution_df["emission_value"].item()
    
    @zero_if_beccs_not_included
    def get_willow_substitution_offset_co2e(self):
        """
        Calculates the willow substitution emission offset in kilotons.
        """
        willow_substitution = self.data_manager_class.get_willow_bioenergy_scaler(
            year= self.target_year,
            type="bioenergy_substitution",
            ghg="CO2e"
        )

        return willow_substitution["emission_value"].item()