"""
biomethane_budget
=================

This module contains the BioMethaneBudget class, which is used to calculate various biomethane-related metrics
such as area and emissions for different types of anaerobic digestion (AD) processes.

Class:
    BioMethaneBudget:
        __init__(self, optigob_data_manager): Initializes the BioMethaneBudget with the given data manager.
        get_ad_ag_area(self): Returns the AD-Ag area in hectares.
        get_ad_substitution_area(self): Returns the AD-Substitution area in hectares.
        get_ad_ccs_area(self): Returns the AD-CCS area in hectares.
        get_total_biomethane_area(self): Returns the total biomethane area in hectares.
        get_ad_ag_co2_emission(self): Returns the AD-Ag CO2 emissions in kilotons.
        get_ad_substitution_co2_emission(self): Returns the AD-Substitution CO2 emissions in kilotons.
        get_ad_ccs_co2_emission(self): Returns the AD-CCS CO2 emissions in kilotons.
        get_ad_ag_ch4_emission(self): Returns the AD-Ag CH4 emissions in kilotons.
        get_ad_substitution_ch4_emission(self): Returns the AD-Substitution CH4 emissions in kilotons.
        get_ad_ccs_ch4_emission(self): Returns the AD-CCS CH4 emissions in kilotons.
        get_ad_ag_n2o_emission(self): Returns the AD-Ag N2O emissions in kilotons.
        get_ad_substitution_n2o_emission(self): Returns the AD-Substitution N2O emissions in kilotons.
        get_ad_ccs_n2o_emission(self): Returns the AD-CCS N2O emissions in kilotons.
        get_ad_ag_co2e_emission(self): Returns the AD-Ag CO2e emissions in kilotons.
        get_ad_substitution_co2e_emission(self): Returns the AD-Substitution CO2e emissions in kilotons.
        get_ad_ccs_co2e_emission(self): Returns the AD-CCS CO2e emissions in kilotons.
        get_biomethane_co2e_total(self): Returns the total CO2e emissions from biomethane in kilotons.
        get_biomethane_co2_total(self): Returns the total CO2 emissions from biomethane in kilotons.
        get_biomethane_ch4_total(self): Returns the total CH4 emissions from biomethane in kilotons.
        get_biomethane_n2o_total(self): Returns the total N2O emissions from biomethane in kilotons.
"""

class BioMethaneBudget:
    def __init__(self, optigob_data_manager):
        self.data_manager_class = optigob_data_manager
        self.target_year = self.data_manager_class.get_target_year()

    def get_ad_ag_area(self):
        """
        Returns the AD-Ag area in hectares.
        """
        ad_ag_area = self.data_manager_class.get_ad_area_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_area[(ad_ag_area["type"] == "AD-Ag") & (ad_ag_area["unit"] == "area_ha")]

        return filtered["value"].item()
    
    def get_ad_substitution_area(self):
        """
        Returns the AD-Substitution area in hectares.
        """
        ad_substitution_area = self.data_manager_class.get_ad_area_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_area[(ad_substitution_area["type"] == "AD-Substitution") & (ad_substitution_area["unit"] == "area_ha")]

        return filtered["value"].item()
    
    def get_ad_ccs_area(self):
        """
        Returns the AD-CCS area in hectares.
        """
        ad_ccs_area = self.data_manager_class.get_ad_area_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_area[(ad_ccs_area["type"] == "AD-CCS") & (ad_ccs_area["unit"] == "area_ha")]

        return filtered["value"].item()
    
    def get_total_biomethane_area(self):
        """
        Returns the total biomethane area in hectares.
        """
        ad_ag_area = self.get_ad_ag_area()
        ad_substitution_area = self.get_ad_substitution_area()
        ad_ccs_area = self.get_ad_ccs_area()

        return ad_ag_area + ad_substitution_area + ad_ccs_area
    
    
    def get_ad_ag_co2_emission(self):
        """
        Returns the AD-Ag CO2 emissions in kilotons.
        """
        ad_ag_co2_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_co2_emission[(ad_ag_co2_emission["type"] == "AD-Ag") & (ad_ag_co2_emission["ghg"] == "CO2")]

        return filtered["emission_value"].item()
    
    def get_ad_substitution_co2_emission(self):
        """
        Returns the AD-Substitution CO2 emissions in kilotons.
        """
        ad_substitution_co2_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_co2_emission[(ad_substitution_co2_emission["type"] == "AD-Substitution") & (ad_substitution_co2_emission["ghg"] == "CO2")]

        return filtered["emission_value"].item()
    
    def get_ad_ccs_co2_emission(self):
        """
        Returns the AD-CCS CO2 emissions in kilotons.
        """
        ad_ccs_co2_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_co2_emission[(ad_ccs_co2_emission["type"] == "AD-CCS") & (ad_ccs_co2_emission["ghg"] == "CO2")]

        return filtered["emission_value"].item()
    
    def get_ad_ag_ch4_emission(self):
        """
        Returns the AD-Ag CH4 emissions in kilotons.
        """
        ad_ag_ch4_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_ch4_emission[(ad_ag_ch4_emission["type"] == "AD-Ag") & (ad_ag_ch4_emission["ghg"] == "CH4")]

        return filtered["emission_value"].item()
    
    def get_ad_substitution_ch4_emission(self):
        """
        Returns the AD-Substitution CH4 emissions in kilotons.
        """
        ad_substitution_ch4_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_ch4_emission[(ad_substitution_ch4_emission["type"] == "AD-Substitution") & (ad_substitution_ch4_emission["ghg"] == "CH4")]

        return filtered["emission_value"].item()
    
    def get_ad_ccs_ch4_emission(self):
        """
        Returns the AD-CCS CH4 emissions in kilotons.
        """
        ad_ccs_ch4_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_ch4_emission[(ad_ccs_ch4_emission["type"] == "AD-CCS") & (ad_ccs_ch4_emission["ghg"] == "CH4")]

        return filtered["emission_value"].item()
    
    def get_ad_ag_n2o_emission(self):
        """
        Returns the AD-Ag N2O emissions in kilotons.
        """
        ad_ag_n2o_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_n2o_emission[(ad_ag_n2o_emission["type"] == "AD-Ag") & (ad_ag_n2o_emission["ghg"] == "N2O")]

        return filtered["emission_value"].item()
    
    def get_ad_substitution_n2o_emission(self):
        """
        Returns the AD-Substitution N2O emissions in kilotons.
        """
        ad_substitution_n2o_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_n2o_emission[(ad_substitution_n2o_emission["type"] == "AD-Substitution") & (ad_substitution_n2o_emission["ghg"] == "N2O")]

        return filtered["emission_value"].item()
    
    def get_ad_ccs_n2o_emission(self):
        """
        Returns the AD-CCS N2O emissions in kilotons.
        """
        ad_ccs_n2o_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_n2o_emission[(ad_ccs_n2o_emission["type"] == "AD-CCS") & (ad_ccs_n2o_emission["ghg"] == "N2O")]

        return filtered["emission_value"].item()
    
    def get_ad_ag_co2e_emission(self):
        """
        Returns the AD-Ag CO2e emissions in kilotons.
        """
        ad_ag_co2e_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_co2e_emission[(ad_ag_co2e_emission["type"] == "AD-Ag") & (ad_ag_co2e_emission["ghg"] == "CO2e")]

        return filtered["emission_value"].item()
    
    def get_ad_substitution_co2e_emission(self):
        """
        Returns the AD-Substitution CO2e emissions in kilotons.
        """
        ad_substitution_co2e_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_substitution_co2e_emission[(ad_substitution_co2e_emission["type"] == "AD-Substitution") & (ad_substitution_co2e_emission["ghg"] == "CO2e")]

        return filtered["emission_value"].item()
    
    def get_ad_ccs_co2e_emission(self):
        """
        Returns the AD-CCS CO2e emissions in kilotons.
        """
        ad_ccs_co2e_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_co2e_emission[(ad_ccs_co2e_emission["type"] == "AD-CCS") & (ad_ccs_co2e_emission["ghg"] == "CO2e")]

        return filtered["emission_value"].item()


    def get_biomethane_co2e_total(self):
        """
        Returns the total CO2e emissions from biomethane in kilotons.
        """
        ad_ag_co2e_emission = self.get_ad_ag_co2e_emission()
        ad_substitution_co2e_emission = self.get_ad_substitution_co2e_emission()
        ad_ccs_co2e_emission = self.get_ad_ccs_co2e_emission()

        return ad_ag_co2e_emission + ad_substitution_co2e_emission + ad_ccs_co2e_emission
    
    def get_biomethane_co2_total(self):
        """
        Returns the total CO2 emissions from biomethane in kilotons.
        """
        ad_ag_co2_emission = self.get_ad_ag_co2_emission()
        ad_substitution_co2_emission = self.get_ad_substitution_co2_emission()
        ad_ccs_co2_emission = self.get_ad_ccs_co2_emission()

        return ad_ag_co2_emission + ad_substitution_co2_emission + ad_ccs_co2_emission
    
    def get_biomethane_ch4_total(self):
        """
        Returns the total CH4 emissions from biomethane in kilotons.
        """
        ad_ag_ch4_emission = self.get_ad_ag_ch4_emission()
        ad_substitution_ch4_emission = self.get_ad_substitution_ch4_emission()
        ad_ccs_ch4_emission = self.get_ad_ccs_ch4_emission()

        return ad_ag_ch4_emission + ad_substitution_ch4_emission + ad_ccs_ch4_emission  
    
    def get_biomethane_n2o_total(self):
        """
        Returns the total N2O emissions from biomethane in kilotons.
        """
        ad_ag_n2o_emission = self.get_ad_ag_n2o_emission()
        ad_substitution_n2o_emission = self.get_ad_substitution_n2o_emission()
        ad_ccs_n2o_emission = self.get_ad_ccs_n2o_emission()

        return ad_ag_n2o_emission + ad_substitution_n2o_emission + ad_ccs_n2o_emission

