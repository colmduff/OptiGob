from optigob.livestock.livestock_optimisation import LivestockOptimisation
from optigob.budget_model.baseline_emssions import BaselineEmission

class LivestockBudget:
    def __init__(self, optigob_data_manager,
                 net_zero_budget=None,
                 split_gas_budget=None):
        
        self.net_zero_budget = net_zero_budget
        self.split_gas_budget = split_gas_budget
        self.data_manager_class = optigob_data_manager
        self.optimisation = LivestockOptimisation(self.data_manager_class)
        self.baseline_emission = BaselineEmission(self.data_manager_class)

        self.target_year = self.data_manager_class.get_target_year()
        self.scenario = self.data_manager_class.get_abatement_scenario()
        self.abatement = self.data_manager_class.get_abatement_type()
        self.dairy_beef_ratio = self.data_manager_class.get_dairy_beef_ratio()
        
        self.split_gas_approach = self.data_manager_class.get_split_gas()
        self.split_gas_frac = self.data_manager_class.get_split_gas_fraction()

        self.ch4_baseline = self.baseline_emission.get_total_ch4_emission()

        if self.split_gas_approach:
            self.ch4_budget = self.get_ch4_budget()

        self._optomisation_outputs = None


    def _load_optomisation_outputs(self):
        """
        """
        if self._optomisation_outputs is None:
            self._optomisation_outputs = self.get_optomisation_outputs()
        return self._optomisation_outputs
    
    def get_ch4_budget(self):
        """
        """
        return self.ch4_baseline * (1-self.split_gas_frac)


    def get_optomisation_outputs(self):
        """
        """

        if self.split_gas_approach:
            return self.optimisation.optimise_livestock_pop(
                self.dairy_beef_ratio,
                self.target_year,
                self.scenario,
                self.abatement,
                self.split_gas_budget,
                self.ch4_budget
            )
        else:
            return self.optimisation.optimise_livestock_pop(
                self.dairy_beef_ratio,
                self.target_year,
                self.scenario,
                self.abatement,
                self.net_zero_budget
            )
        

    def get_dairy_population(self):
        """
        """
        return self._load_optomisation_outputs()["Dairy_animals"]


    def get_beef_population(self):
        """
        """
        return self._load_optomisation_outputs()["Beef_animals"]
    

    def get_dairy_cows_co2_emission(self):
        """
        """
        dairy_cows = self.get_dairy_population()

        dairy_co2 = self.data_manager_class.get_livestock_emission_scaler(
            year=self.target_year,
            system='Dairy',
            gas="CO2",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return dairy_co2["value"] * (dairy_cows/dairy_co2["pop"])
    
    def get_dairy_cows_ch4_emission(self):
        """
        """
        dairy_cows = self.get_dairy_population()

        dairy_ch4 = self.data_manager_class.get_livestock_emission_scaler(
            year=self.target_year,
            system='Dairy',
            gas="CH4",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return dairy_ch4["value"] * (dairy_cows/dairy_ch4["pop"])
    
    def get_dairy_cows_n2o_emission(self):
        """
        """
        dairy_cows = self.get_dairy_population()

        dairy_n2o = self.data_manager_class.get_livestock_emission_scaler(
            year=self.target_year,
            system='Dairy',
            gas="N2O",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return dairy_n2o["value"] * (dairy_cows/dairy_n2o["pop"])
    
    def get_dairy_cows_co2e_emission(self):
        """
        """
        dairy_cows = self.get_dairy_population()

        dairy_co2e = self.data_manager_class.get_livestock_emission_scaler(
            year=self.target_year,
            system='Dairy',
            gas="CO2e",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return dairy_co2e["value"] * (dairy_cows/dairy_co2e["pop"])
    
    def get_beef_cows_co2_emission(self):
        """
        """
        beef_cows = self.get_beef_population()

        beef_co2 = self.data_manager_class.get_livestock_emission_scaler(
            year=self.target_year,
            system='Beef',
            gas="CO2",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return beef_co2["value"] * (beef_cows/beef_co2["pop"])
    
    def get_beef_cows_ch4_emission(self):
        """
        """
        beef_cows = self.get_beef_population()

        beef_ch4 = self.data_manager_class.get_livestock_emission_scaler(
            year=self.target_year,
            system='Beef',
            gas="CH4",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return beef_ch4["value"] * (beef_cows/beef_ch4["pop"])
    
    def get_beef_cows_n2o_emission(self):
        """
        """
        beef_cows = self.get_beef_population()

        beef_n2o = self.data_manager_class.get_livestock_emission_scaler(
            year=self.target_year,
            system='Beef',
            gas="N2O",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return beef_n2o["value"] * (beef_cows/beef_n2o["pop"])
    
    def get_beef_cows_co2e_emission(self):
        """
        """
        beef_cows = self.get_beef_population()

        beef_co2e = self.data_manager_class.get_livestock_emission_scaler(
            year=self.target_year,
            system='Beef',
            gas="CO2e",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return beef_co2e["value"] * (beef_cows/beef_co2e["pop"])
    
    def get_total_co2_emission(self):
        """
        """
        return self.get_dairy_cows_co2_emission() + self.get_beef_cows_co2_emission()
    
    def get_total_ch4_emission(self):
        """
        """
        return self.get_dairy_cows_ch4_emission() + self.get_beef_cows_ch4_emission()
    
    def get_total_n2o_emission(self):
        """
        """
        return self.get_dairy_cows_n2o_emission() + self.get_beef_cows_n2o_emission()
    
    def get_total_co2e_emission(self):
        """
        """
        return self.get_dairy_cows_co2e_emission() + self.get_beef_cows_co2e_emission()
    
