from optigob.budget_model.baseline_emssions import BaselineEmission
from optigob.budget_model.emissions_budget import EmissionsBudget
import pandas as pd


class Optigob:
    def __init__(self, optigob_data_manager):
        self.data_manager_class = optigob_data_manager

        self.baseline_emission = BaselineEmission(self.data_manager_class)
        self.emission_budget = EmissionsBudget(self.data_manager_class)


    def get_baseline_co2e_emissions_by_sector(self):
        """
        """
        return self.baseline_emission.get_co2e_emission_categories()
    
    def get_baseline_ch4_emissions_by_sector(self):
        """
        """
        return self.baseline_emission.get_ch4_emission_categories()
    
    def get_baseline_n2o_emissions_by_sector(self):
        """
        """
        return self.baseline_emission.get_n2o_emission_categories()
    
    def get_baseline_co2_emissions_by_sector(self):
        """
        """
        return self.baseline_emission.get_co2_emission_categories()
    
    def get_baseline_co2e_emissions_total(self):
        """
        """
        return self.baseline_emission.get_total_co2e_emission()
    
    def get_baseline_co2_emissions_total(self):
        """
        """
        return self.baseline_emission.get_total_co2_emission()
    
    def get_baseline_ch4_emissions_total(self):
        """
        """
        return self.baseline_emission.get_total_ch4_emission()
    
    def get_baseline_n2o_emissions_total(self):
        """
        """
        return self.baseline_emission.get_total_n2o_emission()
    
    def get_scenario_co2e_emissions_by_sector(self):
        """
        """
        return self.emission_budget.get_co2e_emission_categories()
    
    def get_scenario_ch4_emissions_by_sector(self):
        """
        """
        return self.emission_budget.get_ch4_emission_categories()
    
    def get_scenario_n2o_emissions_by_sector(self):
        """
        """
        return self.emission_budget.get_n2o_emission_categories()
    
    def get_scenario_co2_emissions_by_sector(self):
        """
        """
        return self.emission_budget.get_co2_emission_categories()
    

    def get_total_emissions_co2e_by_sector(self):
        """
        """
        return {"baseline": self.get_baseline_co2e_emissions_by_sector(), 
                "scenario": self.get_scenario_co2e_emissions_by_sector()}
    
    def get_total_emissions_ch4_by_sector(self):
        """
        """
        return {"baseline": self.get_baseline_ch4_emissions_by_sector(), 
                "scenario": self.get_scenario_ch4_emissions_by_sector()}        
    
    def get_total_emissions_n2o_by_sector(self):
        """
        """
        return {"baseline": self.get_baseline_n2o_emissions_by_sector(), 
                "scenario": self.get_scenario_n2o_emissions_by_sector()}
    
    def get_total_emissions_co2_by_sector(self):
        """
        """
        return {"baseline": self.get_baseline_co2_emissions_by_sector(), 
                "scenario": self.get_scenario_co2_emissions_by_sector()}
    
    
    def get_total_emissions_co2e_by_sector_df(self):
        """
        Returns total emissions in a tidy Pandas DataFrame with sectors as rows and 'baseline' and 'scenario' as columns.
        """
        data = {
            "baseline": self.get_baseline_co2e_emissions_by_sector(),
            "scenario": self.get_scenario_co2e_emissions_by_sector()
        }

        df = pd.DataFrame.from_dict(data, orient='columns')
        return df
