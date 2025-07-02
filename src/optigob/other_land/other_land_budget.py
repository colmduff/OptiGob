"""
other_land_budget
=================

This module contains the OtherLandBudget class, which is responsible for calculating various emissions and areas related to wetland restoration and organic soil management.

Class:
    OtherLandBudget: Calculates emissions and areas for wetland restoration and organic soils.

Methods in OtherLandBudget:
    __init__(self, optigob_data_manager): Initializes the OtherLandBudget class with the provided data manager.
    get_wetland_restoration_emission_co2e(self): Calculates and returns the CO2e emissions from wetland restoration.
    get_wetland_restoration_emission_ch4(self): Calculates and returns the CH4 emissions from wetland restoration.
    get_wetland_restoration_emission_n2o(self): Calculates and returns the N2O emissions from wetland restoration.
    get_wetland_restoration_emission_co2(self): Calculates and returns the CO2 emissions from wetland restoration.
    get_drained_organic_soil_area(self): Calculates and returns the area of drained organic soil.
    get_rewetted_organic_area(self): Calculates and returns the area of rewetted organic soil.
    get_drained_wetland_area(self): Calculates and returns the area of drained wetland.
    get_rewetted_wetland_area(self): Calculates and returns the area of rewetted wetland.
    get_total_other_land_area(self): Calculates and returns the total area of other land, including drained and rewetted organic soil and wetland.
"""

class OtherLandBudget:
    def __init__(self, optigob_data_manager):
        """
        Initializes the OtherLandBudget class with the provided data manager.

        Parameters:
            optigob_data_manager: The data manager instance to be used for data retrieval.
        """
        self.data_manager_class = optigob_data_manager

        self.target_year = self.data_manager_class.get_target_year()
        self.wetland_restored_fraction = self.data_manager_class.get_wetland_restored_fraction()
        self.organic_soil_under_grass_fraction = self.data_manager_class.get_organic_soil_under_grass_fraction()

    def get_wetland_restoration_emission_co2e(self):
        """
        Calculates and returns the CO2e emissions from wetland restoration.

        Returns:
            float: The CO2e emissions value.
        """
        wetland_df = self.data_manager_class.get_organic_soil_emission_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = wetland_df[wetland_df["ghg"] == "CO2e"]

        return filtered["emission_value"].item()
    
    def get_wetland_restoration_emission_ch4(self):
        """
        Calculates and returns the CH4 emissions from wetland restoration.

        Returns:
            float: The CH4 emissions value.
        """
        wetland_df = self.data_manager_class.get_organic_soil_emission_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = wetland_df[wetland_df["ghg"] == "CH4"]

        return filtered["emission_value"].item()
    
    def get_wetland_restoration_emission_n2o(self):
        """
        Calculates and returns the N2O emissions from wetland restoration.

        Returns:
            float: The N2O emissions value.
        """
        wetland_df = self.data_manager_class.get_organic_soil_emission_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = wetland_df[wetland_df["ghg"] == "N2O"]

       
        return filtered["emission_value"].item()
    
    def get_wetland_restoration_emission_co2(self):
        """
        Calculates and returns the CO2 emissions from wetland restoration.

        Returns:
            float: The CO2 emissions value.
        """
        wetland_df = self.data_manager_class.get_organic_soil_emission_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = wetland_df[wetland_df["ghg"] == "CO2"]

        return filtered["emission_value"].item()

    def get_drained_organic_soil_area(self):
        """
        Calculates and returns the area of drained organic soil.

        Returns:
            float: The area of drained organic soil in hectares.
        """
        drained_organic_soil_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )
        
        filtered = drained_organic_soil_area_df[drained_organic_soil_area_df["type"] == "drained_organic"]

        return filtered["areas_ha"].item()
    
    def get_rewetted_organic_area(self):
        """
        Calculates and returns the area of rewetted organic soil.

        Returns:
            float: The area of rewetted organic soil in hectares.
        """
        rewtted_organic_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = rewtted_organic_area_df[rewtted_organic_area_df["type"] == "rewetted_organic"]

        return filtered["areas_ha"].item()
    
    def get_drained_wetland_area(self):
        """
        Calculates and returns the area of drained wetland.

        Returns:
            float: The area of drained wetland in hectares.
        """
        drained_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = drained_wetland_area_df[drained_wetland_area_df["type"] == "drained_wetland"]

        return filtered["areas_ha"].item()
    
    def get_rewetted_wetland_area(self):
        """
        Calculates and returns the area of rewetted wetland.

        Returns:
            float: The area of rewetted wetland in hectares.
        """
        rewetted_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = rewetted_wetland_area_df[rewetted_wetland_area_df["type"] == "rewetted_wetland"]

        return filtered["areas_ha"].item()
    
    def get_near_natural_wetland_area(self):
        """
        Calculates and returns the area of near-natural wetland.

        Returns:
            float: The area of near-natural wetland in hectares.
        """
        near_natural_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )
        filtered = near_natural_wetland_area_df[near_natural_wetland_area_df["type"] == "near_natural_wetland"]

        return filtered["areas_ha"].item()
    
    def get_total_other_land_area(self):
        """
        Calculates and returns the total area of other land, including drained and rewetted organic soil and wetland.

        Returns:
            float: The total area of other land in hectares.
        """
        drained_organic_soil_area = self.get_drained_organic_soil_area()
        rewetted_organic_area = self.get_rewetted_organic_area()
        drained_wetland_area = self.get_drained_wetland_area()
        rewetted_wetland_area = self.get_rewetted_wetland_area()
        near_natural_wetland_area = self.get_near_natural_wetland_area()

        return drained_organic_soil_area + rewetted_organic_area + drained_wetland_area + rewetted_wetland_area + near_natural_wetland_area

    def get_rewetted_organic_hnv_area(self):
        """
        Returns the area of rewetted high nature value (HNV) organic soil.

        Returns:
            float: The area of rewetted HNV organic soil in hectares.
        """
        rewetted_organic_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = rewetted_organic_area_df[rewetted_organic_area_df["type"] == "rewetted_organic"]
        
        return filtered["hnv_area"].item()
    
    def get_rewetted_wetland_hnv_area(self):
        """
        Returns the area of rewetted high nature value (HNV) wetland.

        Returns:
            float: The area of rewetted HNV wetland in hectares.
        """
        rewetted_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = rewetted_wetland_area_df[rewetted_wetland_area_df["type"] == "rewetted_wetland"]

        return filtered["hnv_area"].item()
    
    def get_near_natural_wetland_hnv_area(self):
        """
        Returns the area of near-natural high nature value (HNV) wetland.

        Returns:
            float: The area of near-natural HNV wetland in hectares.
        """
        near_natural_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = near_natural_wetland_area_df[near_natural_wetland_area_df["type"] == "near_natural_wetland"]

        return filtered["hnv_area"].item()
