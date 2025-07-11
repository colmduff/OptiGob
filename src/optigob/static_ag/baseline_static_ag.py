"""
BaselineStaticAg
================
This module defines the BaselineStaticAg class, which is responsible for calculating 
various types of emissions (CO2, CH4, N2O, and CO2e) and areas for different agricultural 
systems (Pig_Poultry, Sheep, and Crops) based on baseline data. The class interacts with 
an OptigobDataManager instance to retrieve necessary data for these calculations.

Classes:
    BaselineStaticAg: A class to calculate emissions and areas for static agricultural systems.

Methods:
    get_pig_and_poultry_co2_emission: Get the CO2 emission for Pig and Poultry systems.
    get_pig_and_poultry_ch4_emission: Get the CH4 emission for Pig and Poultry systems.
    get_pig_and_poultry_n2o_emission: Get the N2O emission for Pig and Poultry systems.
    get_pig_and_poultry_co2e_emission: Get the CO2e emission for Pig and Poultry systems.
    get_sheep_co2_emission: Get the CO2 emission for Sheep systems.
    get_sheep_ch4_emission: Get the CH4 emission for Sheep systems.
    get_sheep_n2o_emission: Get the N2O emission for Sheep systems.
    get_sheep_co2e_emission: Get the CO2e emission for Sheep systems.
    get_crop_co2_emission: Get the CO2 emission for Crop systems.
    get_crop_ch4_emission: Get the CH4 emission for Crop systems.
    get_crop_n2o_emission: Get the N2O emission for Crop systems.
    get_crop_co2e_emission: Get the CO2e emission for Crop systems.
    get_total_static_ag_co2e: Get the total CO2e emission for all static agricultural systems.
    get_total_static_ag_co2: Get the total CO2 emission for all static agricultural systems.
    get_total_static_ag_ch4: Get the total CH4 emission for all static agricultural systems.
    get_total_static_ag_n2o: Get the total N2O emission for all static agricultural systems.
    get_sheep_area: Get the area for Sheep systems.
    get_pig_and_poultry_area: Get the area for Pig and Poultry systems.
    get_crop_area: Get the area for Crop systems.
    get_total_static_ag_area: Get the total area for all static agricultural systems.
    get_sheep_protein: Get the protein value for Sheep systems.
    get_pig_and_poultry_protein: Get the protein value for Pig and Poultry systems.
    get_total_static_ag_protein: Get the total protein value for all static agricultural systems.
"""

class BaselineStaticAg:
    def __init__(self, optigob_data_manager):
        """
        Initialize the BaselineStaticAg instance.

        Args:
            optigob_data_manager: An instance of OptigobDataManager to manage data retrieval.
        """
        self.data_manager_class = optigob_data_manager

        self.baseline_year = self.data_manager_class.get_baseline_year()
        self.abatement_type = "baseline"

        self.pig_and_poultry_protein = self.data_manager_class.get_protein_content_scaler('pig')
        self.sheep_protein = self.data_manager_class.get_protein_content_scaler('sheep')
        self.crop_protein = self.data_manager_class.get_protein_content_scaler('crops')


    def get_pig_and_poultry_co2_emission(self):
        """
        Get the CO2 emission for Pig and Poultry systems.

        Returns:
            float: The CO2 emission value.
        """
        
        pig_and_poultry_co2_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.baseline_year, system='Pig_Poultry', gas='CO2', abatement=self.abatement_type
        )
        
        return pig_and_poultry_co2_emission["emission_value"].item()
    
    def get_pig_and_poultry_ch4_emission(self):
        """
        Get the CH4 emission for Pig and Poultry systems.

        Returns:
            float: The CH4 emission value.
        """
        pig_and_poultry_ch4_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.baseline_year, system='Pig_Poultry', gas='CH4', abatement=self.abatement_type
        )

        return pig_and_poultry_ch4_emission["emission_value"].item()
    
    def get_pig_and_poultry_n2o_emission(self):
        """
        Get the N2O emission for Pig and Poultry systems.

        Returns:
            float: The N2O emission value.
        """
        pig_and_poultry_n2o_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.baseline_year, system='Pig_Poultry', gas='N2O', abatement=self.abatement_type
        )

        return pig_and_poultry_n2o_emission["emission_value"].item()
    
    def get_pig_and_poultry_co2e_emission(self):
        """
        Get the CO2e emission for Pig and Poultry systems.

        Returns:
            float: The CO2e emission value.
        """
        pig_and_poultry_co2e_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.baseline_year, system='Pig_Poultry', gas='CO2e', abatement=self.abatement_type
        )

        return pig_and_poultry_co2e_emission["emission_value"].item()
    
    def get_sheep_co2_emission(self):
        """
        Get the CO2 emission for Sheep systems.

        Returns:
            float: The CO2 emission value.
        """
        sheep_co2_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.baseline_year, system='Sheep', gas='CO2', abatement=self.abatement_type
        )


        return sheep_co2_emission["emission_value"].item()
    
    def get_sheep_ch4_emission(self):
        """
        Get the CH4 emission for Sheep systems.

        Returns:
            float: The CH4 emission value.
        """
        sheep_ch4_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.baseline_year, system='Sheep', gas='CH4', abatement=self.abatement_type
        )

        return sheep_ch4_emission["emission_value"].item()
    
    def get_sheep_n2o_emission(self):
        """
        Get the N2O emission for Sheep systems.

        Returns:
            float: The N2O emission value.
        """
        sheep_n2o_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.baseline_year, system='Sheep', gas='N2O', abatement=self.abatement_type
        )

        return sheep_n2o_emission["emission_value"].item()
    
    def get_sheep_co2e_emission(self):
        """
        Get the CO2e emission for Sheep systems.

        Returns:
            float: The CO2e emission value.
        """
        sheep_co2e_emission = self.data_manager_class.get_static_livestock_emission_scaler(
            year=self.baseline_year, system='Sheep', gas='CO2e', abatement=self.abatement_type
        )

        return sheep_co2e_emission["emission_value"].item()
    

    def get_crop_co2_emission(self):
        """
        Get the CO2 emission for Crop systems.

        Returns:
            float: The CO2 emission value.
        """
        crop_co2_emission = self.data_manager_class.get_crop_scaler(
            year=self.baseline_year,gas='CO2', abatement=self.abatement_type

        )
        return crop_co2_emission["value"].item()

    def get_crop_ch4_emission(self):
        """
        Get the CH4 emission for Crop systems.

        Returns:
            float: The CH4 emission value.
        """
        crop_ch4_emission = self.data_manager_class.get_crop_scaler(
            year=self.baseline_year,gas='CH4', abatement=self.abatement_type

        )
        return crop_ch4_emission["value"].item()
    
    def get_crop_n2o_emission(self):
        """
        Get the N2O emission for Crop systems.

        Returns:
            float: The N2O emission value.
        """
        crop_n2o_emission = self.data_manager_class.get_crop_scaler(
            year=self.baseline_year,gas='N2O', abatement=self.abatement_type

        )
        return crop_n2o_emission["value"].item()
    
    def get_crop_co2e_emission(self):
        """
        Get the CO2e emission for Crop systems.

        Returns:
            float: The CO2e emission value.
        """
        crop_co2e_emission = self.data_manager_class.get_crop_scaler(
            year=self.baseline_year,gas='CO2e', abatement=self.abatement_type

        )
        return crop_co2e_emission["value"].item()
    
    def get_total_static_ag_co2e(self):
        """
        Get the total CO2e emission for all static agricultural systems.

        Returns:
            float: The total CO2e emission value.
        """
        pig_and_poultry_co2e_emission = self.get_pig_and_poultry_co2e_emission()
        sheep_co2e_emission = self.get_sheep_co2e_emission()
        crop_co2e_emission = self.get_crop_co2e_emission()

        return pig_and_poultry_co2e_emission + sheep_co2e_emission + crop_co2e_emission

    def get_total_static_ag_co2(self):
        """
        Get the total CO2 emission for all static agricultural systems.

        Returns:
            float: The total CO2 emission value.
        """
        pig_and_poultry_co2_emission = self.get_pig_and_poultry_co2_emission()
        sheep_co2_emission = self.get_sheep_co2_emission()
        crop_co2_emission = self.get_crop_co2_emission()

        return pig_and_poultry_co2_emission + sheep_co2_emission + crop_co2_emission
    
    def get_total_static_ag_ch4(self):
        """
        Get the total CH4 emission for all static agricultural systems.

        Returns:
            float: The total CH4 emission value.
        """
        pig_and_poultry_ch4_emission = self.get_pig_and_poultry_ch4_emission()
        sheep_ch4_emission = self.get_sheep_ch4_emission()
        crop_ch4_emission = self.get_crop_ch4_emission()

        return pig_and_poultry_ch4_emission + sheep_ch4_emission + crop_ch4_emission
    
    def get_total_static_ag_n2o(self):
        """
        Get the total N2O emission for all static agricultural systems.

        Returns:
            float: The total N2O emission value.
        """
        pig_and_poultry_n2o_emission = self.get_pig_and_poultry_n2o_emission()
        sheep_n2o_emission = self.get_sheep_n2o_emission()
        crop_n2o_emission = self.get_crop_n2o_emission()

        return pig_and_poultry_n2o_emission + sheep_n2o_emission + crop_n2o_emission
    
    def get_sheep_area(self):
        """
        Get the area for Sheep systems.

        Returns:
            float: The area value in hectares.
        """
        sheep_area = self.data_manager_class.get_static_livestock_area_scaler(
            year=self.baseline_year, system='Sheep', abatement=self.abatement_type
        )

        return sheep_area["area"].item()
    
    def get_pig_and_poultry_area(self):
        """
        Get the area for Pig and Poultry systems.

        Returns:
            float: The area value in hectares.
        """
        pig_and_poultry_area = self.data_manager_class.get_static_livestock_area_scaler(
            year=self.baseline_year, system='Pig_Poultry', abatement=self.abatement_type
        )

        return pig_and_poultry_area["area"].item()
    
    def get_crop_area(self):
        """
        Get the area for Crop systems.

        Returns:
            float: The area value in hectares.
        """
        crop_area = self.data_manager_class.get_crop_scaler(
            year=self.baseline_year,gas="CO2e", abatement=self.abatement_type
        )

        return crop_area["area"].item()


    def get_total_static_ag_area(self):
        """
        Get the total area for all static agricultural systems.

        Returns:
            float: The total area value in hectares.
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
            year=self.baseline_year, system='Sheep', item='meat',abatement=self.abatement_type
        )

        return sheep_protein["value"].item() * self.sheep_protein
    

    def get_pig_and_poultry_protein(self):
        """
        Get the protein value for Pig and Poultry systems.

        Returns:
            float: The protein value in kg.
        """
        pig_and_poultry_protein = self.data_manager_class.get_static_livestock_protein_scaler(
            year=self.baseline_year, system='Pig_Poultry',item='meat', abatement=self.abatement_type
        )

        return pig_and_poultry_protein["value"].item() * self.pig_and_poultry_protein
    
    def get_crop_protein(self):
        """
        Get the protein value for Crop systems.

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
    
