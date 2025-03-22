
class OtherLandBudget:
    def __init__(self, optigob_data_manager):
        self.data_manager_class = optigob_data_manager

        self.target_year = self.data_manager_class.get_target_year()
        self.wetland_restored_fraction = self.data_manager_class.get_wetland_restored_fraction()
        self.organic_soil_under_grass_fraction = self.data_manager_class.get_organic_soil_under_grass_fraction()


    def get_wetland_restoration_emission_co2e(self):
        """
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
        """
        drained_organic_soil_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )
        
        filtered = drained_organic_soil_area_df[drained_organic_soil_area_df["type"] == "drained_organic"]

        return filtered["areas_ha"].item() * self.data_manager_class.get_kha_to_ha()
    
    def get_rewetted_organic_area(self):
        """
        """
        rewtted_organic_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = rewtted_organic_area_df[rewtted_organic_area_df["type"] == "rewetted_organic"]

        return filtered["areas_ha"].item() * self.data_manager_class.get_kha_to_ha()
    
    def get_drained_wetland_area(self):
        """
        """
        drained_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = drained_wetland_area_df[drained_wetland_area_df["type"] == "drained_wetland"]

        return filtered["areas_ha"].item() * self.data_manager_class.get_kha_to_ha()
    
    def get_rewetted_wetland_area(self):
        """
        """
        rewetted_wetland_area_df = self.data_manager_class.get_organic_soil_area_scaler(
            target_year=self.target_year,
            wetland_restored_frac=self.wetland_restored_fraction,
            organic_soil_under_grass_frac=self.organic_soil_under_grass_fraction
        )

        filtered = rewetted_wetland_area_df[rewetted_wetland_area_df["type"] == "rewetted_wetland"]

        return filtered["areas_ha"].item() * self.data_manager_class.get_kha_to_ha()
    
    def get_total_other_land_area(self):
        """
        """
        drained_organic_soil_area = self.get_drained_organic_soil_area()
        rewetted_organic_area = self.get_rewetted_organic_area()
        drained_wetland_area = self.get_drained_wetland_area()
        rewetted_wetland_area = self.get_rewetted_wetland_area()

        return drained_organic_soil_area + rewetted_organic_area + drained_wetland_area + rewetted_wetland_area
    