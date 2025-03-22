class StaticAgBudget:
    def __init__(self, optigob_data_manager):
        self.data_manager_class = optigob_data_manager

        self.target_year = self.data_manager_class.get_target_year()
        self.abatement_type = self.data_manager_class.get_abatement_type()


    def get_pig_and_poultry_co2_emission(self):
        """
        """
        pig_and_poultry_co2_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Pig_Poultry', gas='CO2', abatement=self.abatement_type
        )
        return pig_and_poultry_co2_emission["emission_value"].item()
    
    def get_pig_and_poultry_ch4_emission(self):
        """
        """
        pig_and_poultry_ch4_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Pig_Poultry', gas='CH4', abatement=self.abatement_type
        )

        return pig_and_poultry_ch4_emission["emission_value"].item()
    
    def get_pig_and_poultry_n2o_emission(self):
        """
        """
        pig_and_poultry_n2o_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Pig_Poultry', gas='N2O', abatement=self.abatement_type
        )

        return pig_and_poultry_n2o_emission["emission_value"].item()
    
    def get_pig_and_poultry_co2e_emission(self):
        """
        """
        pig_and_poultry_co2e_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Pig_Poultry', gas='CO2e', abatement=self.abatement_type
        )

        return pig_and_poultry_co2e_emission["emission_value"].item()
    
    def get_sheep_co2_emission(self):
        """
        """
        sheep_co2_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Sheep', gas='CO2', abatement=self.abatement_type
        )


        return sheep_co2_emission["emission_value"].item()
    
    def get_sheep_ch4_emission(self):
        """
        """
        sheep_ch4_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Sheep', gas='CH4', abatement=self.abatement_type
        )

        return sheep_ch4_emission["emission_value"].item()
    
    def get_sheep_n2o_emission(self):
        """
        """
        sheep_n2o_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Sheep', gas='N2O', abatement=self.abatement_type
        )

        return sheep_n2o_emission["emission_value"].item()
    
    def get_sheep_co2e_emission(self):
        """
        """
        sheep_co2e_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Sheep', gas='CO2e', abatement=self.abatement_type
        )

        return sheep_co2e_emission["emission_value"].item()
    

    def get_crop_co2_emission(self):
        """
        """
        crop_co2_emission = self.data_manager_class.get_crop_scaler(
            year=self.target_year,gas='CO2', abatement=self.abatement_type

        )
        return crop_co2_emission["value"].item()

    def get_crop_ch4_emission(self):
        """
        """
        crop_ch4_emission = self.data_manager_class.get_crop_scaler(
            year=self.target_year,gas='CH4', abatement=self.abatement_type

        )
        return crop_ch4_emission["value"].item()
    
    def get_crop_n2o_emission(self):
        """
        """
        crop_n2o_emission = self.data_manager_class.get_crop_scaler(
            year=self.target_year,gas='N2O', abatement=self.abatement_type

        )
        return crop_n2o_emission["value"].item()
    
    def get_crop_co2e_emission(self):
        """
        """
        crop_co2e_emission = self.data_manager_class.get_crop_scaler(
            year=self.target_year,gas='CO2e', abatement=self.abatement_type

        )
        return crop_co2e_emission["value"].item()
    
    def get_total_static_ag_co2e(self):
        """
        """
        pig_and_poultry_co2e_emission = self.get_pig_and_poultry_co2e_emission()
        sheep_co2e_emission = self.get_sheep_co2e_emission()
        crop_co2e_emission = self.get_crop_co2e_emission()

        return pig_and_poultry_co2e_emission + sheep_co2e_emission + crop_co2e_emission

    def get_total_static_ag_co2(self):
        """
        """
        pig_and_poultry_co2_emission = self.get_pig_and_poultry_co2_emission()
        sheep_co2_emission = self.get_sheep_co2_emission()
        crop_co2_emission = self.get_crop_co2_emission()

        return pig_and_poultry_co2_emission + sheep_co2_emission + crop_co2_emission
    
    def get_total_static_ag_ch4(self):
        """
        """
        pig_and_poultry_ch4_emission = self.get_pig_and_poultry_ch4_emission()
        sheep_ch4_emission = self.get_sheep_ch4_emission()
        crop_ch4_emission = self.get_crop_ch4_emission()

        return pig_and_poultry_ch4_emission + sheep_ch4_emission + crop_ch4_emission
    
    def get_total_static_ag_n2o(self):
        """
        """
        pig_and_poultry_n2o_emission = self.get_pig_and_poultry_n2o_emission()
        sheep_n2o_emission = self.get_sheep_n2o_emission()
        crop_n2o_emission = self.get_crop_n2o_emission()

        return pig_and_poultry_n2o_emission + sheep_n2o_emission + crop_n2o_emission
    
    def get_sheep_area(self):
        """
        """
        sheep_area = self.data_manager_class.get_static_livestock_area_scaler(
            year=self.target_year, system='Sheep', abatement=self.abatement_type
        )

        return sheep_area["value"].item()
    
    def get_pig_and_poultry_area(self):
        """
        """
        pig_and_poultry_area = self.data_manager_class.get_static_livestock_area_scaler(
            year=self.target_year, system='Pig_Poultry', abatement=self.abatement_type
        )

        return pig_and_poultry_area["value"].item()
    
    def get_crop_area(self):
        """
        """
        crop_area = self.data_manager_class.get_crop_scaler(
            year=self.target_year,gas="CO2e", abatement=self.abatement_type
        )

        return crop_area["area_ha"].item()


    def get_total_static_ag_area(self):
        """
        """
        sheep_area = self.get_sheep_area()
        pig_and_poultry_area = self.get_pig_and_poultry_area()
        crop_area = self.get_crop_area()

        return sheep_area + pig_and_poultry_area + crop_area