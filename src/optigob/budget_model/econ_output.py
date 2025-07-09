"""
EconOutput Module
=================

This module contains the EconOutput class which represents the economic output of the model.
It initializes various budgets and provides methods to calculate total protein and bioenergy by sector for both scenario and baseline, as well as HWP and forest outputs.

Classes:
    EconOutput: Represents the economic output of the model.

Methods in EconOutput:
    __init__(self, optigob_data_manager): Initializes the EconOutput class.
    get_total_scenario_protein_by_sector(self): Returns the protein sectors for the scenario in kg.
    get_total_baseline_protein_by_sector(self): Returns the protein sectors for the baseline in kg.
    get_total_scenario_bioenergy_by_sector(self): Returns scenario bioenergy by sector.
    get_total_baseline_bioenergy_by_sector(self): Returns baseline bioenergy by sector.
    get_hwp_volume(self): Returns harvested wood product volume.
    get_forest_offset(self): Returns forest emission offset.
    get_forest_hnv_area(self): Returns HNV area for forests.
    ... (add any additional methods as implemented)
"""

from optigob.static_ag.baseline_static_ag import BaselineStaticAg
from optigob.livestock.baseline_livestock import BaselineLivestock
from optigob.static_ag.static_ag_budget import StaticAgBudget
from optigob.livestock.livestock_budget import LivestockBudget
from optigob.budget_model.emissions_budget import EmissionsBudget
from optigob.protein_crops.protein_crops_budget import ProteinCropsBudget
from optigob.bioenergy.bioenergy_budget import BioEnergyBudget
from optigob.forest.baseline_forest import BaselineForest
from optigob.forest.forest_budget import ForestBudget


class EconOutput:
    """
    Class that represents the economic output of the model.
    """
    def __init__(self, optigob_data_manager):
        """
        Initializes the EconOutput class.
        """
        self.data_manager_class = optigob_data_manager

        self.emission_budget = EmissionsBudget(self.data_manager_class)

        self.baseline_static_ag = BaselineStaticAg(self.data_manager_class)
        self.baseline_livestock = BaselineLivestock(self.data_manager_class)
        self.static_ag_budget = StaticAgBudget(self.data_manager_class)
        self.livestock_budget = LivestockBudget(self.data_manager_class
                                                ,self.emission_budget.get_net_zero_budget()
                                                ,self.emission_budget.get_split_gas_budget())
        
        self.protein = ProteinCropsBudget(self.data_manager_class)
        self.bio_energy_budget = BioEnergyBudget(self.data_manager_class)
        self.baseline_forest = BaselineForest(self.data_manager_class)
        self.forest_budget = ForestBudget(self.data_manager_class)

        self.scenario_protein_methods = {
            "pig_and_poultry": self.static_ag_budget.get_pig_and_poultry_protein,
            "sheep": self.static_ag_budget.get_sheep_protein,
            "beef": self.livestock_budget.get_total_beef_protein,
            "milk": self.livestock_budget.get_total_milk_protein,
            "protein_crops": self.protein.get_crop_protein_yield,
        }

        self.baseline_protein_methods = {
            "pig_and_poultry": self.baseline_static_ag.get_pig_and_poultry_protein,
            "sheep": self.baseline_static_ag.get_sheep_protein,
            "beef": self.baseline_livestock.get_total_beef_protein,
            "milk": self.baseline_livestock.get_total_milk_protein,
            "protein_crops": lambda:0,  # Protein crops are not included in the baseline
        }

        self.scenario_energy_methods = {
            "ad": self.bio_energy_budget.get_ad_bioenergy_output,
            "willow_biomass": self.bio_energy_budget.get_willow_bioenergy_output,
            "forest_biomass": self.bio_energy_budget.get_forest_bioenergy_output,
        }

        self.baseline_energy_methods = {
            "ad": lambda: 0,  # Anaerobic digestion is not included in the baseline
            "willow_biomass": lambda: 0,  # Willow biomass is not included in the baseline
            "forest_biomass": lambda: 0,  # Forest biomass is not included in the baseline
        }

        self.scenario_population_methods = {
            "dairy": self.livestock_budget.get_dairy_population,
            "beef": self.livestock_budget.get_beef_population,
        }

        self.baseline_population_methods = {
            "dairy": self.data_manager_class.get_baseline_dairy_population,
            "beef": self.data_manager_class.get_baseline_beef_population,
        }


    def get_total_scenario_protein_by_sector(self):
        """
        Returns the protein sectors for the scenario in kg.
        """
        
        return {sector: self.scenario_protein_methods[sector]() for sector in self.scenario_protein_methods}
    
    def get_total_baseline_protein_by_sector(self):
        """
        Returns the protein sectors for the baseline in kg.
        """
        return {sector: self.baseline_protein_methods[sector]() for sector in self.baseline_protein_methods}


    def get_total_scenario_bioenergy_by_sector(self):
        """
        Returns the energy sectors for the scenario in kWh.
        """
        return {sector: self.scenario_energy_methods[sector]() for sector in self.scenario_energy_methods}
    
    def get_total_baseline_bioenergy_by_sector(self):
        """
        Returns the energy sectors for the baseline in kWh.
        """
        return {sector: self.baseline_energy_methods[sector]() for sector in self.baseline_energy_methods}

    
    def get_hwp_volume(self):
        """
        Returns the harvested wood products (HWP) volume in m3.
        """
        baseline = self.baseline_forest.get_hwp_volume()
        scenario = self.forest_budget.get_hwp_volume()


        return {            
            "baseline": {"hwp": baseline,},
            "scenario": {"hwp": scenario,}
        }
    
    def get_scenario_livestock_population(self, scale=10000):
        """
        Returns the Dairy and Beef population in number of animals.
        """

        return {sector: self.scenario_population_methods[sector]() for sector in self.scenario_population_methods}
       
    def get_baseline_livestock_population(self, scale=10000):
        """
        Returns the Dairy and Beef population in number of animals.
        """
        return {sector: self.baseline_population_methods[sector]() * scale for sector in self.baseline_population_methods}