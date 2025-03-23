"""
EconOutput Module
=================

This module contains the EconOutput class which represents the economic output of the model.
It initializes various budgets and provides methods to calculate total protein by sector for both scenario and baseline.

Classes:
    EconOutput: Represents the economic output of the model.

Methods:
    __init__(self, optigob_data_manager): Initializes the EconOutput class.
    get_total_scenario_protein_by_sector(self): Returns the protein sectors for the scenario in kg.
    get_total_baseline_protein_by_sector(self): Returns the protein sectors for the baseline in kg.
"""

from optigob.static_ag.baseline_static_ag import BaselineStaticAg
from optigob.livestock.baseline_livestock import BaselineLivestock
from optigob.static_ag.static_ag_budget import StaticAgBudget
from optigob.livestock.livestock_budget import LivestockBudget
from optigob.budget_model.emissions_budget import EmissionsBudget


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

        self.scenario_protein_methods = {
            "pig_and_poultry": self.static_ag_budget.get_pig_and_poultry_protein,
            "sheep": self.static_ag_budget.get_sheep_protein,
            "beef": self.livestock_budget.get_total_beef_protein,
            "milk": self.livestock_budget.get_total_milk_protein,
        }

        self.baseline_protein_methods = {
            "pig_and_poultry": self.baseline_static_ag.get_pig_and_poultry_protein,
            "sheep": self.baseline_static_ag.get_sheep_protein,
            "beef": self.baseline_livestock.get_total_beef_protein,
            "milk": self.baseline_livestock.get_total_milk_protein,
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


