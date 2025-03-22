"""
landarea_budget
================

This module defines the LandAreaBudget class, which is responsible for calculating 
the baseline and scenario land areas by sector. The calculations include areas for 
agriculture, afforested land, existing forests, other land use, and anaerobic digestion (AD).

Classes:
    - LandAreaBudget: Manages the land area budgets for different sectors.

Methods:
    - __init__(self, optigob_data_manager): Initializes the LandAreaBudget with the provided data manager.
    - get_baseline_agriculture_area(self): Returns the total baseline agriculture area in hectares.
    - get_total_baseline_land_area_by_sector(self): Returns the total baseline land area by sector in hectares.
    - get_scenario_agriculture_area(self): Returns the total scenario agriculture area in hectares.
    - get_total_scenario_land_area_by_sector(self): Returns the total scenario land area by sector in hectares.
"""

from optigob.forest.forest_budget import ForestBudget
from optigob.biomethane.biomethane_budget import BioMethaneBudget
from optigob.other_land.other_land_budget import OtherLandBudget
from optigob.static_ag.static_ag_budget import StaticAgBudget
from optigob.livestock.livestock_budget import LivestockBudget
from optigob.livestock.baseline_livestock import BaselineLivestock
from optigob.forest.baseline_forest import BaselineForest
from optigob.static_ag.baseline_static_ag import BaselineStaticAg
from optigob.other_land.baseline_other_land import BaselineOtherLand
from optigob.budget_model.emissions_budget import EmissionsBudget


class LandAreaBudget:
    def __init__(self, optigob_data_manager):
        """
        Initializes the LandAreaBudget with the provided data manager.
        
        Args:
            optigob_data_manager: The data manager class instance.
        """
        self.data_manager_class = optigob_data_manager
        self.biomethane_included = self.data_manager_class.get_biomethane_included()
        self.beccs_included = self.data_manager_class.get_beccs_included()
        self.split_gas_frac = self.data_manager_class.get_split_gas_fraction()

        self.forest_budget = ForestBudget(self.data_manager_class)
        self.biomethane_budget = BioMethaneBudget(self.data_manager_class)
        self.other_land_budget = OtherLandBudget(self.data_manager_class)
        self.static_ag_budget = StaticAgBudget(self.data_manager_class)

        self.emission_budget = EmissionsBudget(self.data_manager_class)

        self.livestock_budget = LivestockBudget(self.data_manager_class, 
                                                self.emission_budget.get_net_zero_budget(),
                                                self.emission_budget.get_split_gas_budget())
        
        self.baseline_livestock = BaselineLivestock(self.data_manager_class)
        self.baseline_forest = BaselineForest(self.data_manager_class)
        self.baseline_static_ag = BaselineStaticAg(self.data_manager_class)
        self.baseline_other_land = BaselineOtherLand(self.data_manager_class)


        self.baseline_area_methods = {
            "agriculture": self.get_baseline_agriculture_area,
            "afforested": lambda: 0,
            "existing_forest": self.baseline_forest.get_managed_forest_area,
            "other_land_use": self.baseline_other_land.get_total_other_land_area,
            "ad": lambda: 0
        }

        self.scenario_area_methods = {
            "agriculture": self.get_scenario_agriculture_area,
            "afforested": self.forest_budget.get_afforestation_area,
            "existing_forest": self.forest_budget.get_managed_forest_area,
            "other_land_use": self.other_land_budget.get_total_other_land_area,
            "ad": self.biomethane_budget.get_total_biomethane_area if self.biomethane_included else lambda: 0
        }


    def get_baseline_agriculture_area(self):
        """
        Returns the total baseline agriculture area in hectares.
        
        Returns:
            float: Total baseline agriculture area in hectares.
        """
        static = self.baseline_static_ag.get_total_static_ag_area()
        livestock = self.baseline_livestock.get_total_area()

        return static + livestock
    

    def get_total_baseline_land_area_by_sector(self):
        """
        Returns the total baseline land area by sector in hectares.
        
        Returns:
            dict: Total baseline land area by sector in hectares.
        """
        return {sector: self.baseline_area_methods[sector]() for sector in self.baseline_area_methods.keys()}


    def get_scenario_agriculture_area(self):
        """
        Returns the total scenario agriculture area in hectares.
        
        Returns:
            float: Total scenario agriculture area in hectares.
        """
        static_ag = self.static_ag_budget.get_total_static_ag_area()
        livestock = self.livestock_budget.get_total_area()
        return static_ag + livestock
    
    def get_total_scenario_land_area_by_sector(self):
        """
        Returns the total scenario land area by sector in hectares.
        
        Returns:
            dict: Total scenario land area by sector in hectares.
        """
        return {sector: self.scenario_area_methods[sector]() for sector in self.scenario_area_methods.keys()}