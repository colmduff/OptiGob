class BaselineLivestock:
    def __init__(self, optigob_data_manager):
        self.data_manager_class = optigob_data_manager

        self.baseline_year = self.data_manager_class.get_baseline_year()
        self.dairy_cows = self.data_manager_class.get_baseline_dairy_population()
        self.beef_cows = self.data_manager_class.get_baseline_beef_population()
        self.scenario = 1
        self.abatement = "baseline"

    def get_dairy_cows_co2_emission(self):
        """
        """
        dairy_co2 = self.data_manager_class.get_livestock_emission_scaler(
            year=self.baseline_year,
            system='Dairy',
            gas="CO2",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return dairy_co2["value"] * self.dairy_cows
    
    def get_dairy_cows_ch4_emission(self):
        """
        """
        dairy_ch4 = self.data_manager_class.get_livestock_emission_scaler(
            year=self.baseline_year,
            system='Dairy',
            gas="CH4",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return dairy_ch4["value"] * self.dairy_cows
    
    def get_dairy_cows_n2o_emission(self):
        """
        """
        dairy_n2o = self.data_manager_class.get_livestock_emission_scaler(
            year=self.baseline_year,
            system='Dairy',
            gas="N2O",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return dairy_n2o["value"] * self.dairy_cows
    
    def get_dairy_cows_co2e_emission(self):
        """
        """
        dairy_co2e = self.data_manager_class.get_livestock_emission_scaler(
            year=self.baseline_year,
            system='Dairy',
            gas="CO2e",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return dairy_co2e["value"] * self.dairy_cows
    
    def get_beef_cows_co2_emission(self):
        """
        """
        beef_co2 = self.data_manager_class.get_livestock_emission_scaler(
            year=self.baseline_year,
            system='Beef',
            gas="CO2",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return beef_co2["value"] * self.beef_cows
    
    def get_beef_cows_ch4_emission(self):
        """
        """
        beef_ch4 = self.data_manager_class.get_livestock_emission_scaler(
            year=self.baseline_year,
            system='Beef',
            gas="CH4",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return beef_ch4["value"] * self.beef_cows
    
    def get_beef_cows_n2o_emission(self):
        """
        """
        beef_n2o = self.data_manager_class.get_livestock_emission_scaler(
            year=self.baseline_year,
            system='Beef',
            gas="N2O",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return beef_n2o["value"] * self.beef_cows
    
    def get_beef_cows_co2e_emission(self):
        """
        """
        beef_co2e = self.data_manager_class.get_livestock_emission_scaler(
            year=self.baseline_year,
            system='Beef',
            gas="CO2e",
            scenario=self.scenario,
            abatement=self.abatement
        )
        return beef_co2e["value"] * self.beef_cows
    

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
    


    def get_dairy_cows_area(self):
        """
        """
        dairy_data = self.data_manager_class.get_livestock_area_scaler(
            year=self.baseline_year,
            system=['Dairy','Dairy+Beef'],
            scenario=self.scenario,
            abatement=self.abatement
        )

        dairy_area = dairy_data[dairy_data["system"] == "Dairy"]["value"].item()
        dairy_beef_area = dairy_data[dairy_data["system"] == "Dairy+Beef"]["value"].item()

        total_area = dairy_area + dairy_beef_area

        return total_area * self.dairy_cows
    
    def get_beef_cows_area(self):
        """
        """
        beef_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.baseline_year,
            system='Beef',
            scenario=self.scenario,
            abatement=self.abatement
        )


        return beef_area['value'].item() * self.beef_cows


    def get_total_area(self):
        """
        """
        return self.get_dairy_cows_area() + self.get_beef_cows_area()