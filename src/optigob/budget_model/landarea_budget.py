"""
landarea_budget
===============

This module defines the LandAreaBudget class, which is responsible for calculating 
the baseline and scenario land areas by sector. The calculations include areas for 
agriculture, afforested land, existing forests, other land use, protein crops, and anaerobic digestion (AD).

Classes:
    LandAreaBudget: Manages the land area budgets for different sectors.

Methods in LandAreaBudget:
    __init__(self, optigob_data_manager): Initializes the LandAreaBudget with the provided data manager.
    get_baseline_agriculture_area(self): Returns the total baseline agriculture area in hectares.
    get_total_baseline_land_area_by_sector(self): Returns the total baseline land area by sector in hectares.
    get_scenario_agriculture_area(self): Returns the total scenario agriculture area in hectares.
    get_total_scenario_land_area_by_sector(self): Returns the total scenario land area by sector in hectares.
    get_baseline_hnv_area_by_sector(self): Returns the baseline HNV area by sector.
    get_scenario_hnv_area_by_sector(self): Returns the scenario HNV area by sector.
    get_baseline_land_area_agg(self): Returns aggregated baseline land area.
    get_scenario_land_area_agg(self): Returns aggregated scenario land area.
    get_baseline_land_area_disagg(self): Returns disaggregated baseline land area.
    get_scenario_land_area_disagg(self): Returns disaggregated scenario land area.
"""

from optigob.forest.forest_budget import ForestBudget
from optigob.bioenergy.bioenergy_budget import BioEnergyBudget
from optigob.other_land.other_land_budget import OtherLandBudget
from optigob.static_ag.static_ag_budget import StaticAgBudget
from optigob.livestock.livestock_budget import LivestockBudget
from optigob.livestock.baseline_livestock import BaselineLivestock
from optigob.forest.baseline_forest import BaselineForest
from optigob.static_ag.baseline_static_ag import BaselineStaticAg
from optigob.other_land.baseline_other_land import BaselineOtherLand
from optigob.budget_model.emissions_budget import EmissionsBudget
from optigob.protein_crops.protein_crops_budget import ProteinCropsBudget


class LandAreaBudget:
    def __init__(self, optigob_data_manager):
        """
        Initializes the LandAreaBudget with the provided data manager.
        
        Args:
            optigob_data_manager: The data manager class instance.
        """
        self.data_manager_class = optigob_data_manager
        self.biomethane_included = self.data_manager_class.get_biomethane_included()
        self.protein_crops_included = self.data_manager_class.get_protein_crop_included()
        self.beccs_included = self.data_manager_class.get_beccs_included()
        self.split_gas_frac = self.data_manager_class.get_split_gas_fraction()

        self.forest_budget = ForestBudget(self.data_manager_class)
        self.bio_energy_budget = BioEnergyBudget(self.data_manager_class)
        self.other_land_budget = OtherLandBudget(self.data_manager_class)
        self.static_ag_budget = StaticAgBudget(self.data_manager_class)
        self.protein_crops_budget = ProteinCropsBudget(self.data_manager_class)

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
            "ad": lambda: 0,
            "protein_crops": lambda: 0,  # Baseline does not include protein crops
            "beccs_willow": lambda: 0,  # Baseline does not include BECCS
        }

        self.scenario_area_methods = {
            "agriculture": self.get_scenario_agriculture_area,
            "afforested": self.forest_budget.get_afforestation_area,
            "existing_forest": self.forest_budget.get_managed_forest_area,
            "other_land_use": self.other_land_budget.get_total_other_land_area,
            "ad": self.bio_energy_budget.get_total_biomethane_area if self.biomethane_included else lambda: 0,
            "protein_crops": self.protein_crops_budget.get_crop_area if self.protein_crops_included else lambda: 0,
            "beccs_willow": self.bio_energy_budget.get_total_willow_area if self.beccs_included else lambda: 0,

        }

        self.disaggregated_scenario_area_methods = {
            "dairy": self.livestock_budget.get_dairy_cows_area,
            "beef": self.livestock_budget.get_beef_cows_area,
            "sheep": self.static_ag_budget.get_sheep_area,
            "pig_and_poultry": self.static_ag_budget.get_pig_and_poultry_area,
            "static_crops": self.static_ag_budget.get_crop_area,
            "protein_crops": self.protein_crops_budget.get_crop_area if self.protein_crops_included else lambda: 0,
            "beccs_willow": self.bio_energy_budget.get_total_willow_area if self.beccs_included else lambda: 0,
            "anaerobic_digestion": self.bio_energy_budget.get_ad_ag_area if self.biomethane_included else lambda: 0,
            "managed forest": self.forest_budget.get_managed_forest_area,
            "afforestation": self.forest_budget.get_afforestation_area,
            "other_land_use": self.other_land_budget.get_total_other_land_area,
        }

        self.disaggregated_baseline_area_methods = {
            "dairy": self.baseline_livestock.get_dairy_cows_area,
            "beef": self.baseline_livestock.get_beef_cows_area,
            "sheep": self.baseline_static_ag.get_sheep_area,
            "pig_and_poultry": self.baseline_static_ag.get_pig_and_poultry_area,
            "static_crops": self.baseline_static_ag.get_crop_area,
            "protein_crops": lambda: 0,  # Baseline does not include protein crops
            "beccs_willow": lambda: 0,  # Baseline does not include BECCS
            "anaerobic_digestion": lambda: 0,  # Baseline does not include anaerobic digestion
            "managed forest": self.baseline_forest.get_managed_forest_area,
            "afforestation": lambda: 0,  # Baseline does not include afforestation
            "other_land_use": self.baseline_other_land.get_total_other_land_area,
            "available_area": lambda: 0,  # Placeholder for remaining area
        }

        self.scenario_hnv_area_methods = {
            "agriculture": self.livestock_budget.get_hnv_area,
            "afforested": self.forest_budget.get_afforestation_hnv_area,
            "existing_forest": self.forest_budget.get_managed_forest_hnv_area,
            "wetland": self.other_land_budget.get_near_natural_wetland_hnv_area,
            "rewetted_wetland": self.other_land_budget.get_rewetted_wetland_hnv_area,
            "organic_soil": self.other_land_budget.get_rewetted_wetland_hnv_area,
            "beccs": self.bio_energy_budget.get_willow_bioenergy_hnv_area if self.beccs_included else lambda: 0,
        }

        self.baseline_hnv_area_methods = {
            "agriculture": self.baseline_livestock.get_hnv_area,
            "afforested": lambda: 0,  # Baseline does not include afforestation
            "existing_forest": self.baseline_forest.get_managed_forest_hnv_area,
            "wetland": self.baseline_other_land.get_near_natural_wetland_hnv_area,
            "rewetted_wetland": self.baseline_other_land.get_rewetted_wetland_hnv_area,
            "organic_soil": self.baseline_other_land.get_rewetted_wetland_hnv_area,
            "beccs": lambda: 0,  # Baseline does not include BECCS
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
    

    def get_total_baseline_land_area_by_aggregated_sector(self):
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
        protein_crop_area = self.protein_crops_budget.get_crop_area()

        return static_ag + livestock + protein_crop_area
    
    def get_total_scenario_land_area_by_aggregated_sector(self):
        """
        Returns the total scenario land area by sector in hectares.
        
        Returns:
            dict: Total scenario land area by sector in hectares.
        """

        return {sector: self.scenario_area_methods[sector]() for sector in self.scenario_area_methods.keys()}
    
    
    def get_total_scenario_land_area_by_disaggregated_sector(self):
        """
        Returns the total scenario land area by disaggregated sector in hectares.
        
        Returns:
            dict: Total scenario land area by disaggregated sector in hectares.
        """

        baseline_area = self.get_total_baseline_land_area_by_disaggregated_sector()
        scenario_area = {sector: self.disaggregated_scenario_area_methods[sector]() for sector in self.disaggregated_scenario_area_methods.keys()} 

        # Calculate the remaining area
        remaining_area = sum(baseline_area.values()) - sum(scenario_area.values())

        scenario_area["available_area"] = remaining_area
        
        return scenario_area
    

    def get_total_baseline_land_area_by_disaggregated_sector(self):
        """
        Returns the total baseline land area by disaggregated sector in hectares.
        
        Returns:
            dict: Total baseline land area by disaggregated sector in hectares.
        """
        return {sector: self.disaggregated_baseline_area_methods[sector]() for sector in self.disaggregated_baseline_area_methods.keys()}
    
    def get_total_baseline_hnv_land_area_disaggregated_by_sector(self):
        """
        Returns the total baseline HNV land area by disaggregated sector in hectares.
        Returns:
            dict: Total baseline HNV land area by disaggregated sector in hectares.
        """
        return {sector: self.baseline_hnv_area_methods[sector]() for sector in self.baseline_hnv_area_methods.keys()}
    
    def get_total_scenario_hnv_land_area_disaggregated_by_sector(self):
        """
        Returns the total scenario HNV land area by disaggregated sector in hectares.
        
        Returns:
            dict: Total scenario HNV land area by disaggregated sector in hectares.
        """
        return {sector: self.scenario_hnv_area_methods[sector]() for sector in self.scenario_hnv_area_methods.keys()}
