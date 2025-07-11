"""
static_ag_budget
================

This module contains the StaticAgBudget class, which is responsible for calculating various emissions and areas 
related to static agriculture, including livestock (pig, poultry, sheep) and crops. The class interacts with 
an OptigobDataManager instance to retrieve necessary data and perform calculations for CO2, CH4, N2O, and CO2e 
emissions, as well as the total area used for agriculture.

Classes:
    StaticAgBudget: A class to calculate emissions and areas for static agriculture.

Methods:
    __init__(optigob_data_manager): Initializes the StaticAgBudget with a data manager.
    get_pig_and_poultry_co2_emission(): Returns CO2 emissions for pig and poultry.
    get_pig_and_poultry_ch4_emission(): Returns CH4 emissions for pig and poultry.
    get_pig_and_poultry_n2o_emission(): Returns N2O emissions for pig and poultry.
    get_pig_and_poultry_co2e_emission(): Returns CO2e emissions for pig and poultry.
    get_sheep_co2_emission(): Returns CO2 emissions for sheep.
    get_sheep_ch4_emission(): Returns CH4 emissions for sheep.
    get_sheep_n2o_emission(): Returns N2O emissions for sheep.
    get_sheep_co2e_emission(): Returns CO2e emissions for sheep.
    get_crop_co2_emission(): Returns CO2 emissions for crops.
    get_crop_ch4_emission(): Returns CH4 emissions for crops.
    get_crop_n2o_emission(): Returns N2O emissions for crops.
    get_crop_co2e_emission(): Returns CO2e emissions for crops.
    get_total_static_ag_co2e(): Returns total CO2e emissions for all static agriculture.
    get_total_static_ag_co2(): Returns total CO2 emissions for all static agriculture.
    get_total_static_ag_ch4(): Returns total CH4 emissions for all static agriculture.
    get_total_static_ag_n2o(): Returns total N2O emissions for all static agriculture.
    get_sheep_area(): Returns the area used for sheep farming.
    get_pig_and_poultry_area(): Returns the area used for pig and poultry farming.
    get_crop_area(): Returns the area used for crop farming.
    get_total_static_ag_area(): Returns the total area used for all static agriculture.
    get_sheep_protein(): Get the protein value for Sheep systems.
    get_pig_and_poultry_protein(): Get the protein value for Pig and Poultry systems.
    get_total_static_ag_protein(): Get the total protein value for all static agricultural systems.
"""

class StaticAgBudget:
    def __init__(self, optigob_data_manager):
        """
        Initializes the StaticAgBudget with a data manager.

        Parameters:
            optigob_data_manager: An instance of OptigobDataManager to retrieve data.
        """
        self.data_manager_class = optigob_data_manager

        self.target_year = self.data_manager_class.get_target_year()
        self.abatement_type = self.data_manager_class.get_abatement_type()

        self.pig_and_poultry_protein = self.data_manager_class.get_protein_content_scaler('pig')
        self.sheep_protein = self.data_manager_class.get_protein_content_scaler('sheep')
        self.crop_protein = self.data_manager_class.get_protein_content_scaler('crops')

        self._pig_poultry_multiplier = self.data_manager_class.get_pig_and_poultry_multiplier()



    def get_pig_and_poultry_co2_emission(self):
        """
        Returns CO2 emissions for pig and poultry.

        Returns:
            float: CO2 emissions for pig and poultry.
        """
        pig_and_poultry_co2_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Pig_Poultry', gas='CO2', abatement=self.abatement_type
        )
        return pig_and_poultry_co2_emission["emission_value"].item()
    
    def get_pig_and_poultry_ch4_emission(self):
        """
        Returns CH4 emissions for pig and poultry.

        Returns:
            float: CH4 emissions for pig and poultry.
        """
        pig_and_poultry_ch4_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Pig_Poultry', gas='CH4', abatement=self.abatement_type
        )
        return pig_and_poultry_ch4_emission["emission_value"].item()
    
    def get_pig_and_poultry_n2o_emission(self):
        """
        Returns N2O emissions for pig and poultry.

        Returns:
            float: N2O emissions for pig and poultry.
        """
        pig_and_poultry_n2o_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Pig_Poultry', gas='N2O', abatement=self.abatement_type
        )
        return pig_and_poultry_n2o_emission["emission_value"].item()
    
    def get_pig_and_poultry_co2e_emission(self):
        """
        Returns CO2e emissions for pig and poultry.

        Returns:
            float: CO2e emissions for pig and poultry.
        """
        pig_and_poultry_co2e_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Pig_Poultry', gas='CO2e', abatement=self.abatement_type
        )
        return pig_and_poultry_co2e_emission["emission_value"].item()
    
    def get_sheep_co2_emission(self):
        """
        Returns CO2 emissions for sheep.

        Returns:
            float: CO2 emissions for sheep.
        """
        sheep_co2_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Sheep', gas='CO2', abatement=self.abatement_type
        )
        return sheep_co2_emission["emission_value"].item()
    
    def get_sheep_ch4_emission(self):
        """
        Returns CH4 emissions for sheep.

        Returns:
            float: CH4 emissions for sheep.
        """
        sheep_ch4_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Sheep', gas='CH4', abatement=self.abatement_type
        )
        return sheep_ch4_emission["emission_value"].item()
    
    def get_sheep_n2o_emission(self):
        """
        Returns N2O emissions for sheep.

        Returns:
            float: N2O emissions for sheep.
        """
        sheep_n2o_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Sheep', gas='N2O', abatement=self.abatement_type
        )
        return sheep_n2o_emission["emission_value"].item()
    
    def get_sheep_co2e_emission(self):
        """
        Returns CO2e emissions for sheep.

        Returns:
            float: CO2e emissions for sheep.
        """
        sheep_co2e_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.target_year, system='Sheep', gas='CO2e', abatement=self.abatement_type
        )
        return sheep_co2e_emission["emission_value"].item()
    
    def get_crop_co2_emission(self):
        """
        Returns CO2 emissions for crops.

        Returns:
            float: CO2 emissions for crops.
        """
        crop_co2_emission = self.data_manager_class.get_crop_scaler(
            year=self.target_year, gas='CO2', abatement=self.abatement_type
        )
        return crop_co2_emission["value"].item()

    def get_crop_ch4_emission(self):
        """
        Returns CH4 emissions for crops.

        Returns:
            float: CH4 emissions for crops.
        """
        crop_ch4_emission = self.data_manager_class.get_crop_scaler(
            year=self.target_year, gas='CH4', abatement=self.abatement_type
        )
        return crop_ch4_emission["value"].item()
    
    def get_crop_n2o_emission(self):
        """
        Returns N2O emissions for crops.

        Returns:
            float: N2O emissions for crops.
        """
        crop_n2o_emission = self.data_manager_class.get_crop_scaler(
            year=self.target_year, gas='N2O', abatement=self.abatement_type
        )
        return crop_n2o_emission["value"].item()
    
    def get_crop_co2e_emission(self):
        """
        Returns CO2e emissions for crops.

        Returns:
            float: CO2e emissions for crops.
        """
        crop_co2e_emission = self.data_manager_class.get_crop_scaler(
            year=self.target_year, gas='CO2e', abatement=self.abatement_type
        )
        return crop_co2e_emission["value"].item()
    
    def get_total_static_ag_co2e(self):
        """
        Returns total CO2e emissions for all static agriculture.

        Returns:
            float: Total CO2e emissions for all static agriculture.
        """
        pig_and_poultry_co2e_emission = self.get_pig_and_poultry_co2e_emission()
        sheep_co2e_emission = self.get_sheep_co2e_emission()
        crop_co2e_emission = self.get_crop_co2e_emission()

        return pig_and_poultry_co2e_emission + sheep_co2e_emission + crop_co2e_emission

    def get_total_static_ag_co2(self):
        """
        Returns total CO2 emissions for all static agriculture.

        Returns:
            float: Total CO2 emissions for all static agriculture.
        """
        pig_and_poultry_co2_emission = self.get_pig_and_poultry_co2_emission()
        sheep_co2_emission = self.get_sheep_co2_emission()
        crop_co2_emission = self.get_crop_co2_emission()

        return pig_and_poultry_co2_emission + sheep_co2_emission + crop_co2_emission
    
    def get_total_static_ag_ch4(self):
        """
        Returns total CH4 emissions for all static agriculture.

        Returns:
            float: Total CH4 emissions for all static agriculture.
        """
        pig_and_poultry_ch4_emission = self.get_pig_and_poultry_ch4_emission()
        sheep_ch4_emission = self.get_sheep_ch4_emission()
        crop_ch4_emission = self.get_crop_ch4_emission()

        return pig_and_poultry_ch4_emission + sheep_ch4_emission + crop_ch4_emission
    
    def get_total_static_ag_n2o(self):
        """
        Returns total N2O emissions for all static agriculture.

        Returns:
            float: Total N2O emissions for all static agriculture.
        """
        pig_and_poultry_n2o_emission = self.get_pig_and_poultry_n2o_emission()
        sheep_n2o_emission = self.get_sheep_n2o_emission()
        crop_n2o_emission = self.get_crop_n2o_emission()

        return pig_and_poultry_n2o_emission + sheep_n2o_emission + crop_n2o_emission
    
    def get_sheep_area(self):
        """
        Returns the area used for sheep farming.

        Returns:
            float: Area used for sheep farming.
        """
        sheep_area = self.data_manager_class.get_static_livestock_area_scaler(
            year=self.target_year, system='Sheep', abatement=self.abatement_type
        )
        return sheep_area["area"].item()
    
    def get_pig_and_poultry_area(self):
        """
        Returns the area used for pig and poultry farming.

        Returns:
            float: Area used for pig and poultry farming.
        """
        pig_and_poultry_area = self.data_manager_class.get_static_livestock_area_scaler(
            year=self.target_year, system='Pig_Poultry', abatement=self.abatement_type
        )
        return pig_and_poultry_area["area"].item()
    
    def get_crop_area(self):
        """
        Returns the area used for crop farming.

        Returns:
            float: Area used for crop farming.
        """
        crop_area = self.data_manager_class.get_crop_scaler(
            year=self.target_year, gas="CO2e", abatement=self.abatement_type
        )
        return float(crop_area["area"].item())

    def get_total_static_ag_area(self):
        """
        Returns the total area used for all static agriculture.

        Returns:
            float: Total area used for all static agriculture.
        """
        sheep_area = self.get_sheep_area()
        pig_and_poultry_area = self.get_pig_and_poultry_area()
        crop_area = self.get_crop_area()

        return sheep_area + pig_and_poultry_area + crop_area
    
    def get_sheep_protein(self):
        """
        Get the protein value for Sheep systems.

        Returns:
            float: The protein value in kg.
        """
        sheep_protein = self.data_manager_class.get_static_livestock_protein_scaler(
            year=self.target_year, system='Sheep', item='meat',abatement=self.abatement_type
        )

        return sheep_protein["value"].item() * self.sheep_protein
    

    def get_pig_and_poultry_protein(self):
        """
        Get the protein value for Pig and Poultry systems.

        Returns:
            float: The protein value in kg.
        """
        pig_and_poultry_protein = self.data_manager_class.get_static_livestock_protein_scaler(
            year=self.target_year, system='Pig_Poultry', item='meat', abatement=self.abatement_type
        )

        return pig_and_poultry_protein["value"].item() * self.pig_and_poultry_protein * self._pig_poultry_multiplier
    
    def get_crop_protein(self):
        """
        Get the protein value for crop systems.

        Returns:
            float: The protein value in kg.
        """
        crop_area = self.get_crop_area()

        return crop_area * self.crop_protein


    def get_total_static_ag_protein(self):
        """
        Get the total protein value for all static agricultural systems.

        Returns:
            float: The total protein value in kg.
        """
        sheep_protein = self.get_sheep_protein()
        pig_and_poultry_protein = self.get_pig_and_poultry_protein()
        crop_protein = self.get_crop_protein()


        return sheep_protein + pig_and_poultry_protein + crop_protein
    
    def get_pig_and_poultry_population(self):
        """
        Returns the population of pig and poultry in number of animals.

        Returns:
            float: Population of pig and poultry.
        """
        pig_and_poultry_population = self.data_manager_class.get_static_livestock_population_scaler(
            year=self.target_year, system='Pig_Poultry', abatement=self.abatement_type
        )
        return pig_and_poultry_population["population"].item()
    
    