"""
Emissions Budget Module
=======================

This module defines the EmissionsBudget class, which calculates various emissions budgets and categories 
based on data from the optigob_data_manager. Emissions are returned in kilotons (kt).

Methods:
    __init__(self, optigob_data_manager): Initializes the EmissionsBudget with data manager.
    _get_total_emission_co2e(self): Calculates total CO2e emissions (kt).
    _split_gas_emissions_total(self): Calculates total split gas emissions (kt).
    _get_total_emission_ch4(self): Calculates total CH4 emissions (kt).
    _get_total_emission_n2o(self): Calculates total N2O emissions (kt).
    _get_total_emission_co2(self): Calculates total CO2 emissions (kt).
    get_split_gas_budget(self): Returns the split gas budget (kt).
    get_net_zero_budget(self): Returns the net zero budget (kt).
    total_agriculture_co2e_emission(self): Calculates total agriculture CO2e emissions (kt).
    total_agriculture_co2_emission(self): Calculates total agriculture CO2 emissions (kt).
    get_total_agriculture_ch4_emission(self): Calculates total agriculture CH4 emissions (kt).
    get_total_agriculture_n2o_emission(self): Calculates total agriculture N2O emissions (kt).
    get_co2e_emission_categories(self): Returns CO2e emissions by category (kt).
    get_co2_emission_categories(self): Returns CO2 emissions by category (kt).
    get_ch4_emission_categories(self): Returns CH4 emissions by category (kt).
    get_n2o_emission_categories(self): Returns N2O emissions by category (kt).
    get_total_co2e_emission(self): Returns total CO2e emissions (kt).
    get_total_co2_emission(self): Returns total CO2 emissions (kt).
    get_total_ch4_emission(self): Returns total CH4 emissions (kt).
    get_total_n2o_emission(self): Returns total N2O emissions (kt).
"""

from optigob.forest.forest_budget import ForestBudget
from optigob.biomethane.biomethane_budget import BioMethaneBudget
from optigob.other_land.other_land_budget import OtherLandBudget
from optigob.static_ag.static_ag_budget import StaticAgBudget
from optigob.livestock.livestock_budget import LivestockBudget

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
        self.biomethane_budget = BioMethaneBudget(self.data_manager_class)
        self.other_land_budget = OtherLandBudget(self.data_manager_class)
        self.static_ag_budget = StaticAgBudget(self.data_manager_class)

        self.net_zero_budget = abs(self._get_total_emission_co2e())
        self.split_gas_budget = abs(self._split_gas_emissions_total())
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
            "wood_substitution": self.forest_budget.get_subsitution_offset,
            "wood_ccs": self.forest_budget.get_ccs_offset if self.beccs_included else lambda: 0,
            "ad": self.biomethane_budget.get_biomethane_co2e_total if self.biomethane_included else lambda: 0,
            },
            "CO2": {
            "agriculture": self.total_agriculture_co2_emission,
            "afforestation": self.forest_budget.get_afforestation_offset,
            "existing_forest": self.forest_budget.get_managed_forest_offset,
            "other_land_use": self.other_land_budget.get_wetland_restoration_emission_co2,
            "hwp": self.forest_budget.get_hwp_offset,
            "wood_substitution": self.forest_budget.get_subsitution_offset,
            "wood_ccs": self.forest_budget.get_ccs_offset if self.beccs_included else lambda: 0,
            "ad": self.biomethane_budget.get_biomethane_co2_total if self.biomethane_included else lambda: 0,
            },
            "CH4": {
            "agriculture": self.get_total_agriculture_ch4_emission,
            "other_land_use": self.other_land_budget.get_wetland_restoration_emission_ch4,
            "ad": self.biomethane_budget.get_biomethane_ch4_total if self.biomethane_included else lambda: 0,
            },
            "N2O": {
            "agriculture": self.get_total_agriculture_n2o_emission,
            "other_land_use": self.other_land_budget.get_wetland_restoration_emission_n2o,
            "ad": self.biomethane_budget.get_biomethane_n2o_total if self.biomethane_included else lambda: 0,
            }

        }


    def _get_total_emission_co2e(self):
        """
        Calculates total CO2e emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_co2e()
        forest_emission = self.forest_budget.total_emission_offset()
        other_land_emission = self.other_land_budget.get_wetland_restoration_emission_co2e()
        if self.biomethane_included:
            biomethane_emission = self.biomethane_budget.get_biomethane_co2e_total()
        else:
            biomethane_emission = 0

        return static_ag_emission + forest_emission + other_land_emission + biomethane_emission
    

    def _split_gas_emissions_total(self):
        """
        Calculates total split gas emissions (kt).
        """
        forest_emission = self.forest_budget.total_emission_offset()

        total_emission_n2o = self._get_total_emission_n2o() 
        total_emission_co2 = self._get_total_emission_co2()

        total_emission = (total_emission_n2o * self.data_manager_class.get_AR_gwp100_values("N2O")) + total_emission_co2

        return forest_emission + total_emission


    def _get_total_emission_ch4(self):
        """
        Calculates total CH4 emissions (kt).
        """

        static_ag_emission = self.static_ag_budget.get_total_static_ag_ch4()
        other_land_emission = self.other_land_budget.get_wetland_restoration_emission_ch4()

        if self.biomethane_included:
            biomethane_emission = self.biomethane_budget.get_biomethane_ch4_total()
        else:
            biomethane_emission = 0

        return static_ag_emission + other_land_emission + biomethane_emission
    

    def _get_total_emission_n2o(self):
        """
        Calculates total N2O emissions (kt).
        """

        static_ag_emission = self.static_ag_budget.get_total_static_ag_n2o()
        other_land_emission = self.other_land_budget.get_wetland_restoration_emission_n2o()

        if self.biomethane_included:
            biomethane_emission = self.biomethane_budget.get_biomethane_n2o_total()
        else:
            biomethane_emission = 0

        return static_ag_emission + other_land_emission + biomethane_emission
    

    def _get_total_emission_co2(self):
        """
        Calculates total CO2 emissions (kt).
        """

        static_ag_emission = self.static_ag_budget.get_total_static_ag_co2()
        other_land_emission = self.other_land_budget.get_wetland_restoration_emission_co2()

        if self.biomethane_included:
            biomethane_emission = self.biomethane_budget.get_biomethane_co2_total()
        else:
            biomethane_emission = 0

        return static_ag_emission + other_land_emission + biomethane_emission
    
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

        return static_ag_emission + livestock_emission
    
    def total_agriculture_co2_emission(self):
        """
        Calculates total agriculture CO2 emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_co2()
        livestock_emission = self.livestock_budget.get_total_co2_emission()

        return static_ag_emission + livestock_emission
    
    def get_total_agriculture_ch4_emission(self):
        """
        Calculates total agriculture CH4 emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_ch4()
        livestock_emission = self.livestock_budget.get_total_ch4_emission()

        return static_ag_emission + livestock_emission
    
    def get_total_agriculture_n2o_emission(self):
        """
        Calculates total agriculture N2O emissions (kt).
        """
        static_ag_emission = self.static_ag_budget.get_total_static_ag_n2o()
        livestock_emission = self.livestock_budget.get_total_n2o_emission()

        return static_ag_emission + livestock_emission
    
        
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