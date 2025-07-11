"""
BaselineLivestock Module
========================

This module defines the BaselineLivestock class, which is responsible for calculating
various emissions and area usage for dairy and beef cows based on baseline data.

Class:
    BaselineLivestock

Methods:
    __init__(self, optigob_data_manager): Initializes the BaselineLivestock instance.
    get_dairy_cows_co2_emission(self): Calculates CO2 emissions for dairy cows.
    get_dairy_cows_ch4_emission(self): Calculates CH4 emissions for dairy cows.
    get_dairy_cows_n2o_emission(self): Calculates N2O emissions for dairy cows.
    get_dairy_cows_co2e_emission(self): Calculates CO2e emissions for dairy cows.
    get_beef_cows_co2_emission(self): Calculates CO2 emissions for beef cows.
    get_beef_cows_ch4_emission(self): Calculates CH4 emissions for beef cows.
    get_beef_cows_n2o_emission(self): Calculates N2O emissions for beef cows.
    get_beef_cows_co2e_emission(self): Calculates CO2e emissions for beef cows.
    get_total_co2_emission(self): Calculates total CO2 emissions for dairy and beef cows.
    get_total_ch4_emission(self): Calculates total CH4 emissions for dairy and beef cows.
    get_total_n2o_emission(self): Calculates total N2O emissions for dairy and beef cows.
    get_total_co2e_emission(self): Calculates total CO2e emissions for dairy and beef cows.
    get_dairy_cows_area(self): Calculates area usage for dairy cows.
    get_beef_cows_area(self): Calculates area usage for beef cows.
    get_total_area(self): Calculates total area usage for dairy and beef cows.
    get_total_beef_protein(self): Calculates total protein production for beef and dairy+beef systems.
    get_total_milk_protein(self): Calculates total milk protein production for dairy cows.
"""

class BaselineLivestock:
    def __init__(self, optigob_data_manager):
        """
        Initialize the BaselineLivestock instance with the provided data manager.

        Args:
            optigob_data_manager: An instance of the data manager class to fetch baseline data.
        """
        self.data_manager_class = optigob_data_manager

        self.baseline_year = self.data_manager_class.get_baseline_year()
        self.dairy_cows = self.data_manager_class.get_baseline_dairy_population()
        self.beef_cows = self.data_manager_class.get_baseline_beef_population()
        self.scenario = 1
        self.abatement = "baseline"

        self._milk_protein = self.data_manager_class.get_protein_content_scaler("milk")
        self._beef_protein = self.data_manager_class.get_protein_content_scaler("beef")

    def get_dairy_cows_co2_emission(self):
        """
        Calculate the CO2 emissions for dairy cows.

        Returns:
            float: The CO2 emissions for dairy cows in kilotons (kt).
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
        Calculate the CH4 emissions for dairy cows.

        Returns:
            float: The CH4 emissions for dairy cows in kilotons (kt).
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
        Calculate the N2O emissions for dairy cows.

        Returns:
            float: The N2O emissions for dairy cows in kilotons (kt).
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
        Calculate the CO2e emissions for dairy cows.

        Returns:
            float: The CO2e emissions for dairy cows in kilotons (kt).
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
        Calculate the CO2 emissions for beef cows.

        Returns:
            float: The CO2 emissions for beef cows in kilotons (kt).
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
        Calculate the CH4 emissions for beef cows.

        Returns:
            float: The CH4 emissions for beef cows in kilotons (kt).
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
        Calculate the N2O emissions for beef cows.

        Returns:
            float: The N2O emissions for beef cows in kilotons (kt).
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
        Calculate the CO2e emissions for beef cows.

        Returns:
            float: The CO2e emissions for beef cows in kilotons (kt).
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
        Calculate the total CO2 emissions for both dairy and beef cows.

        Returns:
            float: The total CO2 emissions in kilotons (kt).
        """
        return self.get_dairy_cows_co2_emission() + self.get_beef_cows_co2_emission()
    
    def get_total_ch4_emission(self):
        """
        Calculate the total CH4 emissions for both dairy and beef cows.

        Returns:
            float: The total CH4 emissions in kilotons (kt).
        """
        return self.get_dairy_cows_ch4_emission() + self.get_beef_cows_ch4_emission()
    
    def get_total_n2o_emission(self):
        """
        Calculate the total N2O emissions for both dairy and beef cows.

        Returns:
            float: The total N2O emissions in kilotons (kt).
        """
        return self.get_dairy_cows_n2o_emission() + self.get_beef_cows_n2o_emission()
    
    def get_total_co2e_emission(self):
        """
        Calculate the total CO2e emissions for both dairy and beef cows.

        Returns:
            float: The total CO2e emissions in kilotons (kt).
        """
        return self.get_dairy_cows_co2e_emission() + self.get_beef_cows_co2e_emission()
    


    def get_dairy_cows_area(self):
        """
        Calculate the area usage for dairy cows.

        Returns:
            float: The area usage for dairy cows.
        """
        dairy_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.baseline_year,
            system='Dairy',
            scenario=self.scenario,
            abatement=self.abatement
        )

        return dairy_area['area'] * self.dairy_cows
    
    def get_beef_cows_area(self):
        """
        Calculate the area usage for beef cows.

        Returns:
            float: The area usage for beef cows.
        """
        beef_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.baseline_year,
            system='Beef',
            scenario=self.scenario,
            abatement=self.abatement
        )

                # Extracting the area for Dairy and Dairy+Beef systems
        dairy_beef_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.baseline_year,
            system='Dairy+Beef',
            scenario=self.scenario,
            abatement=self.abatement
        )

        total_area = (beef_area['area'] * self.beef_cows) + (dairy_beef_area['area'] * self.dairy_cows)

        return total_area


    def get_total_area(self):
        """
        Calculate the total area usage for both dairy and beef cows.

        Returns:
            float: The total area usage.
        """
        return self.get_dairy_cows_area() + self.get_beef_cows_area()
    

    def get_total_beef_protein(self):
        """
        Calculate the total protein production for beef and dairy+beef systems.

        Returns:
            float: The total protein production for beef and dairy+beef systems in kg.
        """
        beef_protein = self.data_manager_class.get_livestock_protein_scaler(
            year=self.baseline_year,
            system='Beef',
            item="beef",
            scenario=self.scenario,
            abatement=self.abatement
        )

        dairy_beef_protein = self.data_manager_class.get_livestock_protein_scaler(
            year=self.baseline_year,
            system='Dairy',
            item="beef",
            scenario=self.scenario,
            abatement=self.abatement
        )

        total_protein = ((beef_protein["value"].item() * self.beef_cows) + (dairy_beef_protein["value"].item()) * self.dairy_cows) * self._beef_protein
        
        return total_protein
    

    def get_total_milk_protein(self):
        """
        Calculate the total milk protein production for dairy cows.

        Returns:
            float: The total milk protein production for dairy cows in kg.
        """
        dairy_protein = self.data_manager_class.get_livestock_protein_scaler(
            year=self.baseline_year,
            system='Dairy',
            item="milk",
            scenario=self.scenario,
            abatement=self.abatement
        )

        total_protein = (dairy_protein["value"].item() * self.dairy_cows) * self._milk_protein
        
        return total_protein
    
    def get_hnv_area(self):
        """
        Calculate the area of high nature value (HNV) managed by beef cows.

        Returns:
            float: The HNV area in hectares.
        """

        beef_hnv_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.baseline_year,
            system='Beef',
            scenario=self.scenario,
            abatement=self.abatement
        )

        dairy_beef_hnv_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.baseline_year,
            system='Dairy+Beef',
            scenario=self.scenario,
            abatement=self.abatement
        )   

        return (beef_hnv_area["hnv_area"]* self.beef_cows) + (dairy_beef_hnv_area["hnv_area"] * self.dairy_cows)
    