class BioMethaneBudget:
    def __init__(self, optigob_data_manager):
        self.data_manager_class = optigob_data_manager

        self.target_year = self.data_manager_class.get_target_year()


    
    def get_ad_ag_area(self):
        """
        """
        ad_ag_area = self.data_manager_class.get_ad_area_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_area[(ad_ag_area["type"] == "AD-Ag") & (ad_ag_area["unit"] == "area_ha")]

        return filtered["value"].item()
    
    def get_ad_substitution_area(self):
        """
        """
        ad_substitution_area = self.data_manager_class.get_ad_area_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_area[(ad_substitution_area["type"] == "AD-Substitution") & (ad_substitution_area["unit"] == "area_ha")]

        return filtered["value"].item()
    
    def get_ad_ccs_area(self):
        """
        """
        ad_ccs_area = self.data_manager_class.get_ad_area_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_area[(ad_ccs_area["type"] == "AD-CCS") & (ad_ccs_area["unit"] == "area_ha")]

        return filtered["value"].item()
    
    def get_total_biomethane_area(self):
        """
        """
        ad_ag_area = self.get_ad_ag_area()
        ad_substitution_area = self.get_ad_substitution_area()
        ad_ccs_area = self.get_ad_ccs_area()

        return ad_ag_area + ad_substitution_area + ad_ccs_area
    
    
    def get_ad_ag_co2_emission(self):
        """
        """
        ad_ag_co2_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_co2_emission[(ad_ag_co2_emission["type"] == "AD-Ag") & (ad_ag_co2_emission["ghg"] == "CO2")]

        return filtered["emission_value"].item()
    
    def get_ad_substitution_co2_emission(self):
        """
        """
        ad_substitution_co2_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_co2_emission[(ad_substitution_co2_emission["type"] == "AD-Substitution") & (ad_substitution_co2_emission["ghg"] == "CO2")]

        return filtered["emission_value"].item()
    
    def get_ad_ccs_co2_emission(self):
        """
        """
        ad_ccs_co2_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_co2_emission[(ad_ccs_co2_emission["type"] == "AD-CCS") & (ad_ccs_co2_emission["ghg"] == "CO2")]

        return filtered["emission_value"].item()
    
    def get_ad_ag_ch4_emission(self):
        """
        """
        ad_ag_ch4_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_ch4_emission[(ad_ag_ch4_emission["type"] == "AD-Ag") & (ad_ag_ch4_emission["ghg"] == "CH4")]

        return filtered["emission_value"].item()
    
    def get_ad_substitution_ch4_emission(self):
        """
        """
        ad_substitution_ch4_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_ch4_emission[(ad_substitution_ch4_emission["type"] == "AD-Substitution") & (ad_substitution_ch4_emission["ghg"] == "CH4")]

        return filtered["emission_value"].item()
    
    def get_ad_ccs_ch4_emission(self):
        """
        """
        ad_ccs_ch4_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_ch4_emission[(ad_ccs_ch4_emission["type"] == "AD-CCS") & (ad_ccs_ch4_emission["ghg"] == "CH4")]

        return filtered["emission_value"].item()
    
    def get_ad_ag_n2o_emission(self):
        """
        """
        ad_ag_n2o_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_n2o_emission[(ad_ag_n2o_emission["type"] == "AD-Ag") & (ad_ag_n2o_emission["ghg"] == "N2O")]

        return filtered["emission_value"].item()
    
    def get_ad_substitution_n2o_emission(self):
        """
        """
        ad_substitution_n2o_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_n2o_emission[(ad_substitution_n2o_emission["type"] == "AD-Substitution") & (ad_substitution_n2o_emission["ghg"] == "N2O")]

        return filtered["emission_value"].item()
    
    def get_ad_ccs_n2o_emission(self):
        """
        """
        ad_ccs_n2o_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_n2o_emission[(ad_ccs_n2o_emission["type"] == "AD-CCS") & (ad_ccs_n2o_emission["ghg"] == "N2O")]

        return filtered["emission_value"].item()
    
    def get_ad_ag_co2e_emission(self):
        """
        """
        ad_ag_co2e_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_co2e_emission[(ad_ag_co2e_emission["type"] == "AD-Ag") & (ad_ag_co2e_emission["ghg"] == "CO2e")]

        return filtered["emission_value"].item()
    
    def get_ad_substitution_co2e_emission(self):
        """
        """
        ad_substitution_co2e_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_co2e_emission[(ad_substitution_co2e_emission["type"] == "AD-Substitution") & (ad_substitution_co2e_emission["ghg"] == "CO2e")]

        return filtered["emission_value"].item()
    
    def get_ad_ccs_co2e_emission(self):
        """
        """
        ad_ccs_co2e_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_co2e_emission[(ad_ccs_co2e_emission["type"] == "AD-CCS") & (ad_ccs_co2e_emission["ghg"] == "CO2e")]

        return filtered["emission_value"].item()


    def get_biomethane_co2e_total(self):
        """
        """
        ad_ag_co2e_emission = self.get_ad_ag_co2e_emission()
        ad_substitution_co2e_emission = self.get_ad_substitution_co2e_emission()
        ad_ccs_co2e_emission = self.get_ad_ccs_co2e_emission()

        return ad_ag_co2e_emission + ad_substitution_co2e_emission + ad_ccs_co2e_emission
    
    def get_biomethane_co2_total(self):
        """
        """
        ad_ag_co2_emission = self.get_ad_ag_co2_emission()
        ad_substitution_co2_emission = self.get_ad_substitution_co2_emission()
        ad_ccs_co2_emission = self.get_ad_ccs_co2_emission()

        return ad_ag_co2_emission + ad_substitution_co2_emission + ad_ccs_co2_emission
    
    def get_biomethane_ch4_total(self):
        """
        """
        ad_ag_ch4_emission = self.get_ad_ag_ch4_emission()
        ad_substitution_ch4_emission = self.get_ad_substitution_ch4_emission()
        ad_ccs_ch4_emission = self.get_ad_ccs_ch4_emission()

        return ad_ag_ch4_emission + ad_substitution_ch4_emission + ad_ccs_ch4_emission  
    
    def get_biomethane_n2o_total(self):
        """
        """
        ad_ag_n2o_emission = self.get_ad_ag_n2o_emission()
        ad_substitution_n2o_emission = self.get_ad_substitution_n2o_emission()
        ad_ccs_n2o_emission = self.get_ad_ccs_n2o_emission()

        return ad_ag_n2o_emission + ad_substitution_n2o_emission + ad_ccs_n2o_emission
    
