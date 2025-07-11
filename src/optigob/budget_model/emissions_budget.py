"""
Emissions Budget Module
=======================

This module defines the EmissionsBudget class, which calculates and aggregates emissions budgets and categories
across all sectors using the optigob_data_manager. Emissions are returned in kilotons (kt).

Class:
    EmissionsBudget: Calculates total and sectoral emissions (CO2e, CO2, CH4, N2O), net zero and split gas budgets, and substitution emissions.

Methods:
    __init__(self, optigob_data_manager):
        Initializes the EmissionsBudget with the provided data manager and sets up all sectoral budget classes and emission methods.
    _get_total_beccs_co2e(self):
        Calculates total BECCS CO2e emissions (kt).
    _get_total_beccs_co2(self):
        Calculates total BECCS CO2 emissions (kt).
    _get_total_beccs_ch4(self):
        Calculates total BECCS CH4 emissions (kt).
    _get_total_beccs_n2o(self):
        Calculates total BECCS N2O emissions (kt).
    _get_total_emission_co2e_budget(self):
        Calculates the total CO2e emissions budget (kt) for net zero.
    _get_total_emission_co2e(self):
        Calculates the current total CO2e emissions (kt).
    _split_gas_emissions_total_budget_co2e(self):
        Calculates the total split gas emissions budget (kt).
    _get_total_emission_ch4(self):
        Calculates the current total CH4 emissions (kt).
    _get_total_emission_n2o(self):
        Calculates the current total N2O emissions (kt).
    _get_total_emission_co2(self):
        Calculates the current total CO2 emissions (kt).
    _check_net_zero_status(self):
        Checks if the net zero budget is met (returns True/False).
    check_status(self):
        Returns a dict with the status of net zero and split gas budgets.
    _check_split_gas_net_zero_status(self):
        Checks if the split gas budget is met (returns True/False).
    get_split_gas_budget(self):
        Returns the split gas budget (kt).
    get_net_zero_budget(self):
        Returns the net zero budget (kt).
    total_agriculture_co2e_emission(self):
        Calculates total agriculture CO2e emissions (kt).
    total_agriculture_co2_emission(self):
        Calculates total agriculture CO2 emissions (kt).
    get_total_agriculture_ch4_emission(self):
        Calculates total agriculture CH4 emissions (kt).
    get_total_agriculture_n2o_emission(self):
        Calculates total agriculture N2O emissions (kt).
    get_co2e_emission_categories(self):
        Returns CO2e emissions by sector/category (kt).
    get_co2_emission_categories(self):
        Returns CO2 emissions by sector/category (kt).
    get_ch4_emission_categories(self):
        Returns CH4 emissions by sector/category (kt).
    get_n2o_emission_categories(self):
        Returns N2O emissions by sector/category (kt).
    get_total_co2e_emission(self):
        Returns total CO2e emissions (kt) summed across all sectors.
    get_total_co2_emission(self):
        Returns total CO2 emissions (kt) summed across all sectors.
    get_total_ch4_emission(self):
        Returns total CH4 emissions (kt) summed across all sectors.
    get_total_n2o_emission(self):
        Returns total N2O emissions (kt) summed across all sectors.
    get_substitution_emission_co2e(self):
        Returns substitution emissions for CO2e by category (kt).
    get_substitution_emission_co2(self):
        Returns substitution emissions for CO2 by category (kt).
    get_substitution_emission_ch4(self):
        Returns substitution emissions for CH4 by category (kt).
    get_substitution_emission_n2o(self):
        Returns substitution emissions for N2O by category (kt).
"""

from optigob.forest.forest_budget import ForestBudget
from optigob.bioenergy.bioenergy_budget import BioEnergyBudget
from optigob.other_land.other_land_budget import OtherLandBudget
from optigob.static_ag.static_ag_budget import StaticAgBudget
from optigob.livestock.livestock_budget import LivestockBudget
from optigob.protein_crops.protein_crops_budget import ProteinCropsBudget
from optigob.substitution.substitution import Substitution

class EmissionsBudget:
    def __init__(self, optigob_data_manager):
        """
        Initializes the EmissionsBudget with data manager.
        """
        self.data_manager_class = optigob_data_manager
        self.biomethane_included = self.data_manager_class.get_biomethane_included()
        self.beccs_included = self.data_manager_class.get_beccs_included()
        self.split_gas_frac = self.data_manager_class.get_split_gas_fraction()

        self.emission_sectors = self.data_manager_class.get_emission_sectors()

        self.forest_budget = ForestBudget(self.data_manager_class)
        self.bio_energy_budget = BioEnergyBudget(self.data_manager_class)
        self.other_land_budget = OtherLandBudget(self.data_manager_class)
        self.static_ag_budget = StaticAgBudget(self.data_manager_class)
        self.protein_crops_budget = ProteinCropsBudget(self.data_manager_class)
        self.substitution_budget = Substitution(self.data_manager_class)

        self.net_zero_budget = abs(self._get_total_emission_co2e_budget())
        self.split_gas_budget = abs(self._split_gas_emissions_total_budget_co2e())
        self.livestock_budget = LivestockBudget(self.data_manager_class, 
                                                self.net_zero_budget,
                                                self.split_gas_budget)

        
        self.emission_methods = {
            "CO2e":{
            "agriculture": self.total_agriculture_co2e_emission,
            "afforestation": self.forest_budget.get_afforestation_offset,
            "existing_forest": self.forest_budget.get_managed_forest_offset,
            "other_land_use": self.other_land_budget.get_wetland_restoration_emission_co2e,
            "hwp": self.forest_budget.get_hwp_offset,
            "ad": self.bio_energy_budget.get_ad_ag_co2e_emission if self.biomethane_included else lambda: 0,
            "beccs": self._get_total_beccs_co2e if self.beccs_included else lambda: 0
            },
            "CO2": {
            "agriculture": self.total_agriculture_co2_emission,
            "afforestation": self.forest_budget.get_afforestation_offset,
            "existing_forest": self.forest_budget.get_managed_forest_offset,
            "other_land_use": self.other_land_budget.get_wetland_restoration_emission_co2,
            "hwp": self.forest_budget.get_hwp_offset,
            "ad": self.bio_energy_budget.get_ad_ag_co2_emission if self.biomethane_included else lambda: 0,
            "beccs": self._get_total_beccs_co2 if self.beccs_included else lambda: 0
            },
            "CH4": {
            "agriculture": self.get_total_agriculture_ch4_emission,
            "other_land_use": self.other_land_budget.get_wetland_restoration_emission_ch4,
            "ad": self.bio_energy_budget.get_ad_ag_ch4_emission if self.biomethane_included else lambda: 0,
            "beccs": self._get_total_beccs_ch4 if self.beccs_included else lambda: 0
            },
            "N2O": {
            "agriculture": self.get_total_agriculture_n2o_emission,
            "other_land_use": self.other_land_budget.get_wetland_restoration_emission_n2o,
            "ad": self.bio_energy_budget.get_ad_ag_n2o_emission if self.biomethane_included else lambda: 0,
            "beccs": self._get_total_beccs_n2o if self.beccs_included else lambda: 0
            }

        }


        self.substitution_methods = {
            "CO2e": {
            "ad_substitution": self.substitution_budget.get_ad_substitution_co2e_emission,
            "forest_substitution": self.substitution_budget.get_forest_substitution_offset_co2e,
            "willow_substitution": self.substitution_budget.get_willow_substitution_offset_co2e
            },
            "CO2": {
            "ad_substitution": self.substitution_budget.get_ad_substitution_co2_emission,
            "forest_substitution": self.substitution_budget.get_forest_substitution_offset_co2e,
            "willow_substitution": self.substitution_budget.get_willow_substitution_offset_co2e
            },
            "CH4": {
            "ad_substitution": self.substitution_budget.get_ad_substitution_ch4_emission,
            "forest_substitution": lambda: 0,  # No forest substitution for CH4
            "willow_substitution": lambda: 0  # No willow substitution for CH4
            },
            "N2O": {
            "ad_substitution": self.substitution_budget.get_ad_substitution_n2o_emission,
            "forest_substitution": lambda: 0,  # No forest substitution for N2O
            "willow_substitution": lambda: 0  # No willow substitution for N2O
            }
        }


    def _get_total_beccs_co2e(self):
        """
        Calculates total BECCS CO2e emissions (kt).
        """
        bio_energy_beccs_co2e = self.bio_energy_budget.get_total_ccs_co2e_emission()
        forest_beccs_co2e = self.forest_budget.get_wood_ccs_offset()
        return bio_energy_beccs_co2e + forest_beccs_co2e
    
    def _get_total_beccs_co2(self):
        """
        Calculates total BECCS CO2 emissions (kt).
        """
        bio_energy_beccs_co2 = self.bio_energy_budget.get_total_ccs_co2_emission()
        forest_beccs_co2 = self.forest_budget.get_wood_ccs_offset()
        
        return bio_energy_beccs_co2 + forest_beccs_co2
    
    def _get_total_beccs_ch4(self):
        """
        Calculates total BECCS CH4 emissions (kt).
        """
        bio_energy_beccs_ch4 = self.bio_energy_budget.get_total_ccs_ch4_emission()

        return bio_energy_beccs_ch4
    
    def _get_total_beccs_n2o(self):
        """
        Calculates total BECCS N2O emissions (kt).
        """
        bio_energy_beccs_n2o = self.bio_energy_budget.get_total_ccs_n2o_emission()

        return bio_energy_beccs_n2o 
    
    def _get_total_emission_co2e_budget(self):
        """
        Calculates total CO2e emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_co2e()
        forest_emission = self.forest_budget.total_emission_offset()
        beccs_emission = self._get_total_beccs_co2e()
        other_land_emission = self.other_land_budget.get_wetland_restoration_emission_co2e()
        protein_crop_emission = self.protein_crops_budget.get_crop_emission_co2e()
        ad_ag_emission = self.bio_energy_budget.get_ad_ag_co2e_emission()

        total_emission = (static_ag_emission + forest_emission + other_land_emission +
                          beccs_emission + protein_crop_emission + ad_ag_emission)
        
        if total_emission > 0:
            total_emission = 0
        return total_emission
    
    def _get_total_emission_co2e(self):
        """
        Calculates total CO2e emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_co2e()
        livestock_emission = self.livestock_budget.get_total_co2e_emission()
        forest_emission = self.forest_budget.total_emission_offset()
        beccs_emission = self._get_total_beccs_co2e()
        other_land_emission = self.other_land_budget.get_wetland_restoration_emission_co2e()
        protein_crop_emission = self.protein_crops_budget.get_crop_emission_co2e()
        ad_ag_emission = self.bio_energy_budget.get_ad_ag_co2e_emission()

        total_emission = (static_ag_emission + livestock_emission + forest_emission + other_land_emission +
                          beccs_emission + protein_crop_emission + ad_ag_emission)

        return total_emission

    def _split_gas_emissions_total_budget_co2e(self):
        """
        Calculates total split gas emissions CO2e budget (kt).
        """
        forest_emission = self._get_total_forest_co2e()
        total_emission_n2o = self._get_total_emission_n2o() * self.data_manager_class.get_AR_gwp100_values("N2O")
        total_emission_co2 = self._get_total_emission_co2()
        total_emission = forest_emission + total_emission_n2o + total_emission_co2

        if total_emission > 0:
            total_emission = 0
       
        return total_emission


    def _get_total_emission_n2o(self):
        """
        Calculates total N2O emissions (kt).
        """

        static_ag_emission = self.static_ag_budget.get_total_static_ag_n2o()
        other_land_emission = self.other_land_budget.get_wetland_restoration_emission_n2o()
        ad_ag_emission = self.bio_energy_budget.get_ad_ag_n2o_emission()
        protein_crop_emission = self.protein_crops_budget.get_crop_emission_n2o()
        beccs_emission = self._get_total_beccs_n2o()

        total_emission = (static_ag_emission + other_land_emission +
                          beccs_emission + protein_crop_emission + ad_ag_emission)
        
        return total_emission

    def _get_total_emission_ch4(self):
        """
        Calculates total CH4 emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_ch4()
        other_land_emission = self.other_land_budget.get_wetland_restoration_emission_ch4()
        beccs_emission = self._get_total_beccs_ch4()
        protein_crop_emission = self.protein_crops_budget.get_crop_emission_ch4()
        ad_ag_emission = self.bio_energy_budget.get_ad_ag_ch4_emission()

        total_emission = (static_ag_emission + other_land_emission +
                          beccs_emission + protein_crop_emission + ad_ag_emission)
        
        return total_emission

    def _get_total_emission_co2(self):
        """
        Calculates total CO2 emissions (kt).
        """

        static_ag_emission = self.static_ag_budget.get_total_static_ag_co2()
        other_land_emission = self.other_land_budget.get_wetland_restoration_emission_co2()
        ad_ag_emission = self.bio_energy_budget.get_ad_ag_co2_emission()
        protein_crop_emission = self.protein_crops_budget.get_crop_emission_co2()
        beccs_emission = self._get_total_beccs_co2()
        
        total_emission = (static_ag_emission + other_land_emission +
                          beccs_emission + protein_crop_emission + ad_ag_emission )  
        
        return total_emission
    
    def _get_total_forest_co2e(self):
        """
        Calculates total forest and hwp CO2e emissions (kt).
        """
        forest_biomass = self.forest_budget.get_total_forest_offset()
        hwp_biomass = self.forest_budget.get_hwp_offset()

        return forest_biomass + hwp_biomass
        
    
    def _check_split_gas_net_zero_status(self, tolerance=1):
        """
        Checks if the split gas budget is met.
        Returns:
            bool: True if split gas budget is met, False otherwise.
        """
        forest_emission = self.forest_budget.total_emission_offset()
        emissions_total_co2= self._get_total_emission_co2()
        emissions_total_n2o = self._get_total_emission_n2o()

        total_emission = ((emissions_total_n2o * self.data_manager_class.get_AR_gwp100_values("N2O")) + emissions_total_co2) + forest_emission
        return total_emission <= tolerance
    
    def check_net_zero_status(self):
        """
        Checks the status of the emissions budget.
        Returns:
            dict: A dictionary with keys 'net_zero' and 'split_gas' indicating the status.
        """
        return {
            "net_zero": self._check_net_zero_status(),
            "split_gas": self._check_split_gas_net_zero_status()
        }

    def _check_net_zero_status(self, tolerance=1):
        """
        Checks if the net zero budget is met.
        Returns:
            bool: True if net zero budget is met, False otherwise.
        """
        emissions_total = self._get_total_emission_co2e()
        return emissions_total <= tolerance
    
    def get_total_emission_co2e(self):
        """
        Returns the total CO2e emissions (kt).
        """
        return self._get_total_emission_co2e()
    

    def get_split_gas_budget(self):
        """
        Returns the split gas budget (kt).
        """
        return self.split_gas_budget
    
    def get_net_zero_budget(self):
        """
        Returns the net zero budget (kt).
        """
        return self.net_zero_budget

    def total_agriculture_co2e_emission(self):
        """
        Calculates total agriculture CO2e emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_co2e()
        livestock_emission = self.livestock_budget.get_total_co2e_emission()
        protein_crop_emission = self.protein_crops_budget.get_crop_emission_co2e()

        return static_ag_emission + livestock_emission + protein_crop_emission
    
    def total_agriculture_co2_emission(self):
        """
        Calculates total agriculture CO2 emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_co2()
        livestock_emission = self.livestock_budget.get_total_co2_emission()
        protein_crop_emission = self.protein_crops_budget.get_crop_emission_co2()

        return static_ag_emission + livestock_emission + protein_crop_emission
    
    def get_total_agriculture_ch4_emission(self):
        """
        Calculates total agriculture CH4 emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_ch4()
        livestock_emission = self.livestock_budget.get_total_ch4_emission()
        protein_crop_emission = self.protein_crops_budget.get_crop_emission_ch4()

        return static_ag_emission + livestock_emission + protein_crop_emission
    
    def get_total_agriculture_n2o_emission(self):
        """
        Calculates total agriculture N2O emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_n2o()
        livestock_emission = self.livestock_budget.get_total_n2o_emission()
        protein_crop_emission = self.protein_crops_budget.get_crop_emission_n2o()

        return static_ag_emission + livestock_emission + protein_crop_emission
    
        
    def get_co2e_emission_categories(self):
        """
        Returns CO2e emissions by category (kt).
        """
        result_dict = {}

        for key in self.emission_sectors:
            func = self.emission_methods["CO2e"].get(key)
            if func:
                result_dict[key] = func()
            else:
                result_dict[key] = 0  # default value if key not found

        return result_dict
    
    def get_co2_emission_categories(self):
        """
        Returns CO2 emissions by category (kt).
        """
        result_dict = {}    

        for key in self.emission_sectors:
            func = self.emission_methods["CO2"].get(key)
            if func:
                result_dict[key] = func()
            else:
                result_dict[key] = 0

        return result_dict
    
    def get_ch4_emission_categories(self):
        """
        Returns CH4 emissions by category (kt).
        """
        result_dict = {}    

        for key in self.emission_sectors:
            func = self.emission_methods["CH4"].get(key)
            if func:
                result_dict[key] = func()
            else:
                result_dict[key] = 0

        return result_dict
    
    def get_n2o_emission_categories(self):
        """
        Returns N2O emissions by category (kt).
        """
        result_dict = {}    

        for key in self.emission_sectors:
            func = self.emission_methods["N2O"].get(key)
            if func:
                result_dict[key] = func()
            else:
                result_dict[key] = 0

        return result_dict
    
    
    def get_total_co2e_emission(self):
        """
        Returns total CO2e emissions (kt).
        """
        total = 0 
        for key in self.emission_sectors:
            func = self.emission_methods["CO2e"].get(key)
            if func:
                total += func()
        return total
    
    def get_total_co2_emission(self):
        """
        Returns total CO2 emissions (kt).
        """
        total = 0 
        for key in self.emission_sectors:
            func = self.emission_methods["CO2"].get(key)
            if func:
                total += func()
        return total
    
    def get_total_ch4_emission(self):
        """
        Returns total CH4 emissions (kt).
        """
        total = 0 
        for key in self.emission_sectors:
            func = self.emission_methods["CH4"].get(key)
            if func:
                total += func()
        return total
    
    def get_total_n2o_emission(self):
        """
        Returns total N2O emissions (kt).
        """
        total = 0 
        for key in self.emission_sectors:
            func = self.emission_methods["N2O"].get(key)
            if func:
                total += func()
        return total
    
    def get_substitution_emission_co2e(self):
        """
        Returns substitution emissions for CO2e by category (kt).
        """
        result_dict = {}

        for key in self.substitution_methods["CO2e"]:
            func = self.substitution_methods["CO2e"].get(key)
            if func:
                result_dict[key] = func()
            else:
                result_dict[key] = 0

        return result_dict
    
    def get_substitution_emission_co2(self):
        """
        Returns substitution emissions for CO2 by category (kt).
        """
        result_dict = {}

        for key in self.substitution_methods["CO2"]:
            func = self.substitution_methods["CO2"].get(key)
            if func:
                result_dict[key] = func()
            else:
                result_dict[key] = 0

        return result_dict
    
    def get_substitution_emission_ch4(self):
        """
        Returns substitution emissions for CH4 by category (kt).
        """
        result_dict = {}

        for key in self.substitution_methods["CH4"]:
            func = self.substitution_methods["CH4"].get(key)
            if func:
                result_dict[key] = func()
            else:
                result_dict[key] = 0

        return result_dict
    
    def get_substitution_emission_n2o(self):
        """
        Returns substitution emissions for N2O by category (kt).
        """
        result_dict = {}

        for key in self.substitution_methods["N2O"]:
            func = self.substitution_methods["N2O"].get(key)
            if func:
                result_dict[key] = func()
            else:
                result_dict[key] = 0

        return result_dict
    
    def get_total_livestock_ch4_emission_budget(self):
        """
        Returns total livestock split gas CH4 emissions (kt) budget.
        """
        return self.livestock_budget.get_split_gas_ch4_emission()