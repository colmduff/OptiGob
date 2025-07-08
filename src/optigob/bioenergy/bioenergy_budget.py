"""
biomethane_budget
=================

This module contains the BioEnergyBudget class, which is used to calculate various biomethane-related metrics
such as area, emissions, and energy output for different types of anaerobic digestion (AD) processes, willow bioenergy, and BECCS.

Class:
    BioEnergyBudget: Calculates area, emissions, and energy output for AD, willow, and BECCS.

Methods in BioEnergyBudget:
    __init__(self, optigob_data_manager): Initializes the BioEnergyBudget with the given data manager.
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
    get_total_willow_area(self): Returns the total willow area in hectares.
    get_willow_bioenergy_hnv_area(self): Returns the willow bioenergy HNV area in hectares.
    get_ad_bioenergy_output(self): Returns the AD energy output in MWh.
    get_willow_bioenergy_output(self): Returns the Willow bioenergy output in MWh.
    get_willow_beccs_co2_emission(self): Returns the CO2 emissions from Willow BECCS in kilotons.
    get_total_ccs_co2_emission(self): Returns the total CO2 emissions from CCS in kilotons.
    get_total_ccs_co2e_emission(self): Returns the total CO2e emissions from CCS in kilotons.
    get_total_ccs_ch4_emission(self): Returns the total CH4 emissions from CCS in kilotons.
    get_total_ccs_n2o_emission(self): Returns the total N2O emissions from CCS in kilotons.
"""

class BioEnergyBudget:
    def __init__(self, optigob_data_manager):
        self.data_manager_class = optigob_data_manager
        self.target_year = self.data_manager_class.get_target_year()

        self.biomethane_included = self.data_manager_class.get_biomethane_included()
        self.beccs_included = self.data_manager_class.get_beccs_included()

        self.afforestation_rate = self.data_manager_class.get_afforestation_rate_kha_per_year()
        self.harvest_rate = self.data_manager_class.get_forest_harvest_intensity()
        self.organic_soil_fraction = self.data_manager_class.get_organic_soil_fraction_forest()
        self.broadleaf_fraction = self.data_manager_class.get_broadleaf_fraction()
        self.beccs_included = self.data_manager_class.get_beccs_included()
        self.beccs_willow_area_multiplier = self.data_manager_class.get_beccs_willow_area_multiplier()

    def zero_if_biomethane_not_included(method):
        def wrapper(self, *args, **kwargs):
            if not self.biomethane_included:
                return 0
            return method(self, *args, **kwargs)
        return wrapper

    def zero_if_beccs_not_included(method):
        def wrapper(self, *args, **kwargs):
            if not self.beccs_included:
                return 0
            return method(self, *args, **kwargs)
        return wrapper
    
    @zero_if_beccs_not_included
    def get_total_willow_area(self):
        """
        Returns the total willow area in hectares.
        """
        willow_area = self.data_manager_class.get_willow_bioenergy_scaler(
            year= self.target_year,
            type="bioenergy_substitution",
            ghg="CO2e"
        )

        return willow_area["area"].item() * self.beccs_willow_area_multiplier
    
    @zero_if_beccs_not_included
    def get_willow_bioenergy_hnv_area(self):
        """
        Returns the willow bioenergy area in hectares.
        """
        willow_area = self.data_manager_class.get_willow_bioenergy_scaler(
            year= self.target_year,
            type="bioenergy_substitution",
            ghg="CO2e"
        )

        return willow_area["hnv_area"].item() * self.beccs_willow_area_multiplier

    #AD methods
    @zero_if_biomethane_not_included
    def get_ad_ag_area(self):
        """
        Returns the AD-Ag area in hectares.
        """
        ad_ag_area = self.data_manager_class.get_ad_area_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_area[(ad_ag_area["type"] == "AD-Ag") & (ad_ag_area["unit"] == "area_ha")]

        return filtered["value"].item()
    
    @zero_if_biomethane_not_included
    def get_total_biomethane_area(self):
        """
        Returns the total biomethane area in hectares.
        """
        ad_ag_area = self.get_ad_ag_area()

        return ad_ag_area
    
    @zero_if_biomethane_not_included
    def get_ad_ag_co2_emission(self):
        """
        Returns the AD-Ag CO2 emissions in kilotons.
        """
        ad_ag_co2_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_co2_emission[(ad_ag_co2_emission["type"] == "AD-Ag") & (ad_ag_co2_emission["ghg"] == "CO2")]

        return filtered["emission_value"].item()
    

    @zero_if_biomethane_not_included
    def get_ad_ag_ch4_emission(self):
        """
        Returns the AD-Ag CH4 emissions in kilotons.
        """
        ad_ag_ch4_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_ch4_emission[(ad_ag_ch4_emission["type"] == "AD-Ag") & (ad_ag_ch4_emission["ghg"] == "CH4")]

        return filtered["emission_value"].item()
    
    @zero_if_biomethane_not_included
    def get_ad_ag_n2o_emission(self):
        """
        Returns the AD-Ag N2O emissions in kilotons.
        """
        ad_ag_n2o_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_n2o_emission[(ad_ag_n2o_emission["type"] == "AD-Ag") & (ad_ag_n2o_emission["ghg"] == "N2O")]

        return filtered["emission_value"].item()

    @zero_if_biomethane_not_included
    def get_ad_ag_co2e_emission(self):
        """
        Returns the AD-Ag CO2e emissions in kilotons.
        """
        ad_ag_co2e_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ag_co2e_emission[(ad_ag_co2e_emission["type"] == "AD-Ag") & (ad_ag_co2e_emission["ghg"] == "CO2e")]

        return filtered["emission_value"].item()
    
    #Energy methods
    @zero_if_biomethane_not_included
    def get_ad_bioenergy_output(self):
        """
        Returns the AD energy output in MWh.
        """
        ad_energy_output = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_energy_output[(ad_energy_output["type"] == "AD-Ag") & (ad_energy_output["energy_unit"] == "MWh") & (ad_energy_output["ghg"] == "CO2e")]

        return filtered["energy"].item()
    
    @zero_if_beccs_not_included
    def get_willow_bioenergy_output(self):
        """
        Returns the Willow bioenergy output in MWh.
        """
        willow_bioenergy_output = self.data_manager_class.get_willow_bioenergy_scaler(
            year= self.target_year,
            type="bioenergy_substitution",
            ghg="CO2e"
        )

        return willow_bioenergy_output["energy"].item() * self.beccs_willow_area_multiplier
    

    def get_forest_bioenergy_output(self):
        """
        Returns the forest bioenergy output in MWh.
        """
        forest_bioenergy_output = self.data_manager_class.get_substitution_scaler(
            target_year=self.target_year,
            affor_rate=self.afforestation_rate,
            broadleaf_frac=self.broadleaf_fraction,
            organic_soil_frac=self.organic_soil_fraction,
            harvest=self.harvest_rate
        )


        return forest_bioenergy_output["energy"].item()

    #CCS methods
    @zero_if_beccs_not_included
    def get_ad_ccs_co2_emission(self):
        """
        Returns the AD-CCS CO2 emissions in kilotons.
        """
        ad_ccs_co2_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_co2_emission[(ad_ccs_co2_emission["type"] == "AD-CCS") & (ad_ccs_co2_emission["ghg"] == "CO2")]

        return filtered["emission_value"].item()
    
    @zero_if_beccs_not_included
    def get_ad_ccs_ch4_emission(self):
        """
        Returns the AD-CCS CH4 emissions in kilotons.
        """
        ad_ccs_ch4_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_ch4_emission[(ad_ccs_ch4_emission["type"] == "AD-CCS") & (ad_ccs_ch4_emission["ghg"] == "CH4")]

        return filtered["emission_value"].item()
    
    @zero_if_beccs_not_included
    def get_ad_ccs_n2o_emission(self):
        """
        Returns the AD-CCS N2O emissions in kilotons.
        """
        ad_ccs_n2o_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_n2o_emission[(ad_ccs_n2o_emission["type"] == "AD-CCS") & (ad_ccs_n2o_emission["ghg"] == "N2O")]

        return filtered["emission_value"].item()
    
    @zero_if_beccs_not_included
    def get_ad_ccs_co2e_emission(self):
        """
        Returns the AD-CCS CO2e emissions in kilotons.
        """
        ad_ccs_co2e_emission = self.data_manager_class.get_ad_emission_scaler(
            target_year= self.target_year
        )

        filtered = ad_ccs_co2e_emission[(ad_ccs_co2e_emission["type"] == "AD-CCS") & (ad_ccs_co2e_emission["ghg"] == "CO2e")]

        return filtered["emission_value"].item()
    
    @zero_if_beccs_not_included
    def get_willow_beccs_co2_emission(self):
        """
        Returns the CO2 emissions from Willow BECCS in kilotons.
        """
        willow_beccs_co2_emission = self.data_manager_class.get_willow_bioenergy_scaler(
            year= self.target_year,
            type="beccs",
            ghg="CO2"
        )

        return willow_beccs_co2_emission["emission_value"].item() * self.beccs_willow_area_multiplier
    

    def get_total_ccs_co2_emission(self):
        """
        Returns the total CO2 emissions from CCS in kilotons.
        """
        ad_ccs_co2_emission = self.get_ad_ccs_co2_emission()
        willow_beccs_co2_emission = self.get_willow_beccs_co2_emission()

        return ad_ccs_co2_emission + willow_beccs_co2_emission
    

    def get_total_ccs_co2e_emission(self):
        """
        Returns the total CO2e emissions from CCS in kilotons.
        """
        ad_ccs_co2e_emission = self.get_ad_ccs_co2e_emission()
        willow_beccs_co2_emission = self.get_willow_beccs_co2_emission()

        return ad_ccs_co2e_emission + willow_beccs_co2_emission
    
    def get_total_ccs_ch4_emission(self):
        """
        Returns the total CH4 emissions from CCS in kilotons.
        """
        ad_ccs_ch4_emission = self.get_ad_ccs_ch4_emission()

        return ad_ccs_ch4_emission 
    
    def get_total_ccs_n2o_emission(self):
        """
        Returns the total N2O emissions from CCS in kilotons.
        """
        ad_ccs_n2o_emission = self.get_ad_ccs_n2o_emission()

        return ad_ccs_n2o_emission