"""
baseline_emissions
==================

This module calculates baseline emissions for various sectors including agriculture, existing forests, and other land uses.
All emissions are returned in kilotons (kt).

Classes:
    BaselineEmission: Manages and calculates baseline emissions for different sectors.

Methods in BaselineEmission:
    __init__(self, optigob_data_manager): Initializes the BaselineEmission class with data manager.
    total_agriculture_co2e_emission(self): Calculates total CO2e emissions for agriculture.
    total_agriculture_co2_emission(self): Calculates total CO2 emissions for agriculture.
    get_total_agriculture_ch4_emission(self): Calculates total CH4 emissions for agriculture.
    get_total_agriculture_n2o_emission(self): Calculates total N2O emissions for agriculture.
    get_co2e_emission_categories(self): Returns CO2e emissions for all categories.
    get_co2_emission_categories(self): Returns CO2 emissions for all categories.
    get_ch4_emission_categories(self): Returns CH4 emissions for all categories.
    get_n2o_emission_categories(self): Returns N2O emissions for all categories.
    get_total_ch4_emission(self): Calculates total CH4 emissions for all sectors.
    get_total_n2o_emission(self): Calculates total N2O emissions for all sectors.
    get_total_co2_emission(self): Calculates total CO2 emissions for all sectors.
    get_total_co2e_emission(self): Calculates total CO2e emissions for all sectors.
"""

from optigob.other_land.baseline_other_land import BaselineOtherLand
from optigob.static_ag.baseline_static_ag import BaselineStaticAg
from optigob.livestock.baseline_livestock import BaselineLivestock
from optigob.forest.baseline_forest import BaselineForest

class BaselineEmission:
    def __init__(self, optigob_data_manager):
        """
        Initializes the BaselineEmission class with the provided data manager.
        """
        self.data_manager_class = optigob_data_manager

        self.forest_baseline = BaselineForest(self.data_manager_class)
        self.other_land_baseline = BaselineOtherLand(self.data_manager_class)
        self.static_ag_baseline = BaselineStaticAg(self.data_manager_class)
        self.livestock_baseline = BaselineLivestock(self.data_manager_class)

        self.emission_sectors = self.data_manager_class.get_emission_sectors()

        self.emission_methods = {
            "CO2e":{
            "agriculture": self.total_agriculture_co2e_emission,
            "existing_forest": self.forest_baseline.get_total_forest_offset,
            "other_land_use": self.other_land_baseline.get_wetland_restoration_emission_co2e
            },
            "CO2": {
            "agriculture": self.total_agriculture_co2_emission,
            "existing_forest": self.forest_baseline.get_total_forest_offset,
            "other_land_use": self.other_land_baseline.get_wetland_restoration_emission_co2
            },
            "CH4": {
            "agriculture": self.get_total_agriculture_ch4_emission,
            "other_land_use": self.other_land_baseline.get_wetland_restoration_emission_ch4
            },
            "N2O": {
            "agriculture": self.get_total_agriculture_n2o_emission,
            "other_land_use": self.other_land_baseline.get_wetland_restoration_emission_n2o
            }

        }

    def total_agriculture_co2e_emission(self):
        """
        Calculates total CO2e emissions for agriculture.
        Returns:
            float: Total CO2e emissions in kilotons (kt).
        """
        static_ag_emission = self.static_ag_baseline.get_total_static_ag_co2e()
        livestock_emission = self.livestock_baseline.get_total_co2e_emission()

        return static_ag_emission + livestock_emission
    
    def total_agriculture_co2_emission(self):
        """
        Calculates total CO2 emissions for agriculture.
        Returns:
            float: Total CO2 emissions in kilotons (kt).
        """
        static_ag_emission = self.static_ag_baseline.get_total_static_ag_co2()
        livestock_emission = self.livestock_baseline.get_total_co2_emission()

        return static_ag_emission + livestock_emission
    
    def get_total_agriculture_ch4_emission(self):
        """
        Calculates total CH4 emissions for agriculture.
        Returns:
            float: Total CH4 emissions in kilotons (kt).
        """
        static_ag_emission = self.static_ag_baseline.get_total_static_ag_ch4()

        livestock_emission = self.livestock_baseline.get_total_ch4_emission()

        return static_ag_emission + livestock_emission
    
    def get_total_agriculture_n2o_emission(self):
        """
        Calculates total N2O emissions for agriculture.
        Returns:
            float: Total N2O emissions in kilotons (kt).
        """
        static_ag_emission = self.static_ag_baseline.get_total_static_ag_n2o()
        livestock_emission = self.livestock_baseline.get_total_n2o_emission()

        return static_ag_emission + livestock_emission


    def get_co2e_emission_categories(self):
        """
        Returns CO2e emissions for all categories.
        Returns:
            dict: CO2e emissions in kilotons (kt) for each category.
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
        Returns CO2 emissions for all categories.
        Returns:
            dict: CO2 emissions in kilotons (kt) for each category.
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
        Returns CH4 emissions for all categories.
        Returns:
            dict: CH4 emissions in kilotons (kt) for each category.
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
        Returns N2O emissions for all categories.
        Returns:
            dict: N2O emissions in kilotons (kt) for each category.
        """
        result_dict = {}

        for key in self.emission_sectors:
            func = self.emission_methods["N2O"].get(key)
            if func:
                result_dict[key] = func()
            else:
                result_dict[key] = 0

        return result_dict
    

    def get_total_ch4_emission(self):
        """
        Calculates total CH4 emissions for all sectors.
        Returns:
            float: Total CH4 emissions in kilotons (kt).
        """
        total = 0 
        for key in self.emission_sectors:
            func = self.emission_methods["CH4"].get(key)
            if func:
                total += func()
        return total
    

    def get_total_n2o_emission(self):
        """
        Calculates total N2O emissions for all sectors.
        Returns:
            float: Total N2O emissions in kilotons (kt).
        """
        total = 0 
        for key in self.emission_sectors:
            func = self.emission_methods["N2O"].get(key)
            if func:
                total += func()
        return total
    

    def get_total_co2_emission(self):
        """
        Calculates total CO2 emissions for all sectors.
        Returns:
            float: Total CO2 emissions in kilotons (kt).
        """
        total = 0 
        for key in self.emission_sectors:
            func = self.emission_methods["CO2"].get(key)
            if func:
                total += func()
        return total
    
    
    def get_total_co2e_emission(self):
        """
        Calculates total CO2e emissions for all sectors.
        Returns:
            float: Total CO2e emissions in kilotons (kt).
        """
        total = 0 
        for key in self.emission_sectors:
            func = self.emission_methods["CO2e"].get(key)
            if func:
                total += func()
        return total
