"""
BaselineOtherLand
=================

This module provides the BaselineOtherLand class, which calculates various emissions and areas related to wetland restoration and organic soil management.

Class:
    BaselineOtherLand: Calculates baseline emissions and areas for wetland restoration and organic soils.

Methods in BaselineOtherLand:
    __init__(self, optigob_data_manager): Initializes the BaselineOtherLand instance with the provided data manager.
    get_wetland_restoration_emission_co2e(self): Returns the CO2e emissions from wetland restoration (kiloton).
    get_wetland_restoration_emission_ch4(self): Returns the CH4 emissions from wetland restoration (kiloton).
    get_wetland_restoration_emission_n2o(self): Returns the N2O emissions from wetland restoration (kiloton).
    get_wetland_restoration_emission_co2(self): Returns the CO2 emissions from wetland restoration (kiloton).
    get_drained_organic_soil_area(self): Returns the area of drained organic soil in hectares.
    get_rewetted_organic_area(self): Returns the area of rewetted organic soil in hectares.
    get_drained_wetland_area(self): Returns the area of drained wetland in hectares.
    get_rewetted_wetland_area(self): Returns the area of rewetted wetland in hectares.
    get_total_other_land_area(self): Returns the total area of other land, including drained and rewetted organic soil and wetland (hectares).
    get_rewetted_organic_hnv_area(self): Returns the area of rewetted high nature value (HNV) wetland.
    get_rewetted_wetland_hnv_area(self): Returns the area of rewetted high nature value (HNV) wetland.
    get_near_natural_wetland_hnv_area(self): Returns the area of near-natural high nature value (HNV) wetland.
    get_total_other_land_hnv_area(self): Returns the total area of other land, including rewetted organic soil, rewetted wetland, and near-natural wetland, that is high nature value (HNV).
"""

class BaselineOtherLand:
    def __init__(self, optigob_data_manager):
        """
        Initializes the BaselineOtherLand instance with the provided data manager.

        Args:
            optigob_data_manager: An instance of the data manager class.
        """
        self.data_manager_class = optigob_data_manager

        self.baseline_year = self.data_manager_class.get_baseline_year() 
        self.wetland_restored_fraction = self.data_manager_class.get_wetland_restored_fraction()
        self.organic_soil_under_grass_fraction = self.data_manager_class.get_organic_soil_under_grass_fraction()

    def get_wetland_restoration_emission_co2e(self):
        """
        Returns the CO2e emissions from wetland restoration.

        Returns:
            float: The CO2e emissions value in kiloton.
        """
        wetland_df = self.data_manager_class.get_organic_soil_emission_scaler(
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = wetland_df[wetland_df["ghg"] == "CO2e"]

        return filtered["emission_value"].item()
    
    def get_wetland_restoration_emission_ch4(self):
        """
        Returns the CH4 emissions from wetland restoration.

        Returns:
            float: The CH4 emissions value in kiloton.
        """
        #CHANGE BACK TO BASELINE YEAR
        wetland_df = self.data_manager_class.get_organic_soil_emission_scaler(
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = wetland_df[wetland_df["ghg"] == "CH4"]

        return filtered["emission_value"].item()
    
    def get_wetland_restoration_emission_n2o(self):
        """
        Returns the N2O emissions from wetland restoration.

        Returns:
            float: The N2O emissions value in kiloton.
        """
        wetland_df = self.data_manager_class.get_organic_soil_emission_scaler(
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = wetland_df[wetland_df["ghg"] == "N2O"]

       
        return filtered["emission_value"].item()
    
    def get_wetland_restoration_emission_co2(self):
        """
        Returns the CO2 emissions from wetland restoration.

        Returns:
            float: The CO2 emissions value in kiloton.
        """
        wetland_df = self.data_manager_class.get_organic_soil_emission_scaler(
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = wetland_df[wetland_df["ghg"] == "CO2"]

        return filtered["emission_value"].item()

    def get_drained_organic_soil_area(self):
        """
        Returns the area of drained organic soil in hectares.

        Returns:
            float: The area of drained organic soil in hectares.
        """
        drained_organic_soil_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )
        
        filtered = drained_organic_soil_area_df[drained_organic_soil_area_df["type"] == "drained_organic"]

        return filtered["areas_ha"].item()
    
    def get_rewetted_organic_area(self):
        """
        Returns the area of rewetted organic soil in hectares.

        Returns:
            float: The area of rewetted organic soil in hectares.
        """
        rewtted_organic_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = rewtted_organic_area_df[rewtted_organic_area_df["type"] == "rewetted_organic"]

        return filtered["areas_ha"].item()
    
    def get_drained_wetland_area(self):
        """
        Returns the area of drained wetland in hectares.

        Returns:
            float: The area of drained wetland in hectares.
        """
        drained_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = drained_wetland_area_df[drained_wetland_area_df["type"] == "drained_wetland"]

        return filtered["areas_ha"].item()
    
    def get_rewetted_wetland_area(self):
        """
        Returns the area of rewetted wetland in hectares.

        Returns:
            float: The area of rewetted wetland in hectares.
        """
        rewetted_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = rewetted_wetland_area_df[rewetted_wetland_area_df["type"] == "rewetted_wetland"]

        return filtered["areas_ha"].item()
    
    def get_near_natural_wetland_area(self):
        """
        Returns the area of near-natural wetland in hectares.

        Returns:
            float: The area of near-natural wetland in hectares.
        """
        near_natural_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )
        filtered = near_natural_wetland_area_df[near_natural_wetland_area_df["type"] == "near_natural_wetland"]

        return filtered["areas_ha"].item()
    
    def get_total_other_land_area(self):
        """
        Returns the total area of other land, including drained and rewetted organic soil and wetland.

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
        Returns the area of rewetted high nature value (HNV) wetland.

        Returns:
            float: The area of rewetted HNV wetland in hectares.
        """
        rewetted_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )   

        filtered = rewetted_wetland_area_df[rewetted_wetland_area_df["type"] == "rewetted_organic"]

        return filtered["hnv_area"].item()

    def get_rewetted_wetland_hnv_area(self):
        """
        Returns the area of rewetted high nature value (HNV) wetland.

        Returns:
            float: The area of rewetted HNV wetland in hectares.
        """
        rewetted_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.baseline_year,
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
            target_year=self.baseline_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )
        filtered = near_natural_wetland_area_df[near_natural_wetland_area_df["type"] == "near_natural_wetland"]

        return filtered["hnv_area"].item()
    
    def get_total_other_land_hnv_area(self):
        """
        Returns the total area of other land, including rewetted organic soil, rewetted wetland, and near-natural wetland, that is high nature value (HNV).

        Returns:
            float: The total HNV area of other land in hectares.
        """
        rewetted_organic_hnv_area = self.get_rewetted_organic_hnv_area()
        rewetted_wetland_hnv_area = self.get_rewetted_wetland_hnv_area()
        near_natural_wetland_hnv_area = self.get_near_natural_wetland_hnv_area()

        return rewetted_organic_hnv_area + rewetted_wetland_hnv_area + near_natural_wetland_hnv_area
