"""
Module: forest_budget

This module contains the ForestBudget class, which is responsible for calculating various forest-related offsets and metrics.
The class interacts with an optigob data manager to retrieve necessary data for these calculations.

Methods:
    - __init__(self, optigob_data_manager): Initializes the ForestBudget instance with data from the optigob data manager.
    - get_managed_forest_offset(self): Calculates the emission offset from managed forests (in kt).
    - get_afforestation_offset(self): Calculates the emission offset from afforestation activities (in kt).
    - get_total_forest_offset(self): Calculates the total emission offset from both managed forests and afforestation (in kt).
    - get_hwp_offset(self): Calculates the emission offset from harvested wood products (HWP) (in kt).
    - get_ccs_offset(self): Calculates the emission offset from carbon capture and storage (CCS) (in kt).
    - get_subsitution_offset(self): Calculates the emission offset from substitution effects (in kt).
    - total_emission_offset(self): Calculates the total emission offset from all sources (in kt).
    - get_managed_forest_area(self): Retrieves the area of managed forests (in hectares).
    - get_afforestation_area(self): Retrieves the area of afforestation activities (in hectares).
    - get_hwp_volume(self): Retrieves the volume of harvested wood products (in cubic meters).
    - get_ccs_volume(self): Retrieves the volume of carbon captured and stored (in cubic meters).
"""

class ForestBudget:
    def __init__(self, optigob_data_manager):
        self.data_manager_class = optigob_data_manager

        self.target_year = self.data_manager_class.get_target_year()
        self.afforestation_rate = self.data_manager_class.get_afforestation_rate_kha_per_year()
        self.harvest_rate = self.data_manager_class.get_forest_harvest_intensity()
        self.organic_soil_fraction = self.data_manager_class.get_organic_soil_fraction_forest()
        self.broadleaf_fraction = self.data_manager_class.get_broadleaf_fraction()
        self.beccs_included = self.data_manager_class.get_beccs_included()

    def get_managed_forest_offset(self):
        """
        Calculates the emission offset from managed forests.
        """
        managed_forest_df = self.data_manager_class.get_static_forest_scaler(
            target_year=self.target_year,
            harvest=self.harvest_rate
        )
        return managed_forest_df["emission_value"].item()

    def get_afforestation_offset(self):
        """
        Calculates the emission offset from afforestation activities.
        """
        afforestation_df = self.data_manager_class.get_forest_scaler(
            target_year=self.target_year,
            affor_rate=self.afforestation_rate,
            broadleaf_frac=self.broadleaf_fraction,
            organic_soil_frac=self.organic_soil_fraction,
            harvest=self.harvest_rate
        )
        return afforestation_df["emission_value"].item()
    
    def get_total_forest_offset(self):
        """
        Calculates the total emission offset from both managed forests and afforestation.
        """
        afforestation_offset = self.get_afforestation_offset()
        managed_forest_offset = self.get_managed_forest_offset()

        return afforestation_offset + managed_forest_offset
    
    def get_hwp_offset(self):
        """
        Calculates the emission offset from harvested wood products (HWP).
        """
        hwp_df = self.data_manager_class.get_hwp_scaler(
            target_year=self.target_year,
            affor_rate=self.afforestation_rate,
            broadleaf_frac=self.broadleaf_fraction,
            organic_soil_frac=self.organic_soil_fraction,
            harvest=self.harvest_rate
        )
        return hwp_df["emission_value"].item()
    
    def get_ccs_offset(self):
        """
        Calculates the emission offset from carbon capture and storage (CCS).
        """
        ccs_df = self.data_manager_class.get_ccs_scaler(
            target_year=self.target_year,
            affor_rate=self.afforestation_rate,
            broadleaf_frac=self.broadleaf_fraction,
            organic_soil_frac=self.organic_soil_fraction,
            harvest=self.harvest_rate
        )
        return ccs_df["emission_value"].item()
    
    def get_subsitution_offset(self):
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
    
    def total_emission_offset(self):
        """
        Calculates the total emission offset from all sources.
        """
        total_offset_biomass = self.get_total_forest_offset()
        hwp_offset = self.get_hwp_offset()
        substitution_offset = self.get_subsitution_offset()
        if not self.beccs_included:
            ccs_offset = 0
        else:   
            ccs_offset = self.get_ccs_offset()

        return total_offset_biomass + hwp_offset + substitution_offset + ccs_offset

    def get_managed_forest_area(self):
        """
        Retrieves the area of managed forests.
        """
        managed_forest_df = self.data_manager_class.get_static_forest_scaler(
            target_year=self.target_year,
            harvest=self.harvest_rate
        )
        return managed_forest_df["area_ha"].item()
    
    def get_afforestation_area(self):
        """
        Retrieves the area of afforestation activities.
        """
        afforestation_df = self.data_manager_class.get_forest_scaler(
            target_year=self.target_year,
            affor_rate=self.afforestation_rate,
            broadleaf_frac=self.broadleaf_fraction,
            organic_soil_frac=self.organic_soil_fraction,
            harvest=self.harvest_rate
        )
        return afforestation_df["area_ha"].item()
    
    def get_hwp_volume(self):
        """
        Retrieves the volume of harvested wood products (in cubic meters).
        """
        hwp_df = self.data_manager_class.get_hwp_scaler(
            target_year=self.target_year,
            affor_rate=self.afforestation_rate,
            broadleaf_frac=self.broadleaf_fraction,
            organic_soil_frac=self.organic_soil_fraction,
            harvest=self.harvest_rate
        )
        return hwp_df["volume"].item()
    
    def get_ccs_volume(self):
        """
        Retrieves the volume of carbon captured and stored (in cubic meters).
        """
        ccs_df = self.data_manager_class.get_ccs_scaler(
            target_year=self.target_year,
            affor_rate=self.afforestation_rate,
            broadleaf_frac=self.broadleaf_fraction,
            organic_soil_frac=self.organic_soil_fraction,
            harvest=self.harvest_rate
        )
        return ccs_df["volume"].item()
