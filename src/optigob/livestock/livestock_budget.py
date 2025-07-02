"""
livestock_budget
================

This module contains the LivestockBudget class, which is responsible for managing and optimizing livestock populations and their associated emissions and land use. The class interacts with data managers and optimization models to achieve these goals.

Classes:
    - LivestockBudget

Methods:
    - __init__(self, optigob_data_manager, net_zero_budget=None, split_gas_budget=None): Initialize the LivestockBudget class.
    - _get_total_area_commitment(self): Calculate the total area commitment based on various land use areas.
    - _load_optomisation_outputs(self): Load optimization outputs if not already loaded.
    - get_ch4_budget(self): Calculate the CH4 budget based on the baseline emissions and split gas fraction.
    - get_optomisation_outputs(self): Get the optimization outputs for livestock population.
    - get_dairy_population(self): Get the optimized dairy population.
    - get_beef_population(self): Get the optimized beef population.
    - _get_scaled_beef_population(self): Get the scaled beef population based on emission scalers.
    - _get_scaled_dairy_population(self): Get the scaled dairy population based on emission scalers.
    - get_dairy_cows_co2_emission(self): Calculate the CO2 emissions for dairy cows (kt).
    - get_dairy_cows_ch4_emission(self): Calculate the CH4 emissions for dairy cows (kt).
    - get_dairy_cows_n2o_emission(self): Calculate the N2O emissions for dairy cows (kt).
    - get_dairy_cows_co2e_emission(self): Calculate the CO2e emissions for dairy cows (kt).
    - get_beef_cows_co2_emission(self): Calculate the CO2 emissions for beef cows (kt).
    - get_beef_cows_ch4_emission(self): Calculate the CH4 emissions for beef cows (kt).
    - get_beef_cows_n2o_emission(self): Calculate the N2O emissions for beef cows (kt).
    - get_beef_cows_co2e_emission(self): Calculate the CO2e emissions for beef cows (kt).
    - get_total_co2_emission(self): Calculate the total CO2 emissions for all livestock (kt).
    - get_total_ch4_emission(self): Calculate the total CH4 emissions for all livestock (kt).
    - get_total_n2o_emission(self): Calculate the total N2O emissions for all livestock (kt).
    - get_total_co2e_emission(self): Calculate the total CO2e emissions for all livestock (kt).
    - get_dairy_cows_area(self): Calculate the land area required for dairy cows.
    - get_beef_cows_area(self): Calculate the land area required for beef cows.
    - get_total_area(self): Calculate the total land area required for all livestock.
    - get_total_beef_protein(self): Calculate the total protein production for beef and dairy+beef systems.
    - get_total_milk_protein(self): Calculate the total milk protein production for dairy cows.
"""

from optigob.livestock.livestock_optimisation import LivestockOptimisation
from optigob.budget_model.baseline_emssions import BaselineEmission
from optigob.other_land.other_land_budget import OtherLandBudget
from optigob.forest.forest_budget import ForestBudget
from optigob.bioenergy.bioenergy_budget import BioEnergyBudget
from optigob.protein_crops.protein_crops_budget import ProteinCropsBudget

class LivestockBudget:
    def __init__(self, optigob_data_manager,
                 net_zero_budget=None,
                 split_gas_budget=None):
        """
        Initialize the LivestockBudget class.

        Parameters:
        - optigob_data_manager: Data manager class instance for accessing data.
        - net_zero_budget: Budget for net zero emissions (optional).
        - split_gas_budget: Budget for split gas emissions (optional).
        """
        
        self.net_zero_budget = net_zero_budget
        self.split_gas_budget = split_gas_budget
        self.data_manager_class = optigob_data_manager
        self.optimisation = LivestockOptimisation(self.data_manager_class)
        self.baseline_emission = BaselineEmission(self.data_manager_class)

        #load areas
        self.other_land_budget = OtherLandBudget(self.data_manager_class)
        self.forest_budget = ForestBudget(self.data_manager_class)
        self.bio_energy_budget = BioEnergyBudget(self.data_manager_class)
        self.protein_crop_budget = ProteinCropsBudget(self.data_manager_class)

        self.rewetted_area = self.other_land_budget.get_rewetted_organic_area()
        self.afforested_area = self.forest_budget.get_afforestation_area()
        self.biomethane_area = self.bio_energy_budget.get_total_biomethane_area()
        self.willow_area = self.bio_energy_budget.get_total_willow_area()
        self.protein_crop_area = self.protein_crop_budget.get_crop_area()

        self._milk_protein = self.data_manager_class.get_protein_content_scaler("milk")
        self._beef_protein = self.data_manager_class.get_protein_content_scaler("beef")

        self.target_year = self.data_manager_class.get_target_year()
        self.scenario = self.data_manager_class.get_abatement_scenario()
        self.abatement = self.data_manager_class.get_abatement_type()
        self.get_livestock_ratio_type = self.data_manager_class.get_livestock_ratio_type()
        self.livestock_ratio_value = self.data_manager_class.get_livestock_ratio_value()
        
        self.split_gas_approach = self.data_manager_class.get_split_gas()
        self.split_gas_frac = self.data_manager_class.get_split_gas_fraction()

        self.ch4_baseline = self.baseline_emission.get_total_ch4_emission()

        if self.split_gas_approach:
            self.ch4_budget = self.get_ch4_budget()

        self._optomisation_outputs = None

    def _get_total_area_commitment(self):
        """
        Calculate the total area commitment based on various land use areas.

        Returns:
        - Total area commitment.
        """
        return (float(self.rewetted_area +
                self.afforested_area +
                self.biomethane_area +
                self.protein_crop_area+
                self.willow_area))

    def _load_optomisation_outputs(self):
        """
        Load optimization outputs if not already loaded.

        Returns:
        - Optimization outputs.
        """
        if self._optomisation_outputs is None:
            self._optomisation_outputs = self.get_optomisation_outputs()
        return self._optomisation_outputs
    
    def get_ch4_budget(self):
        """
        Calculate the CH4 budget based on the baseline emissions and split gas fraction.

        Returns:
        - CH4 budget.
        """
        return self.ch4_baseline * (1-self.split_gas_frac)


    def get_optomisation_outputs(self):
        """
        Get the optimization outputs for livestock population.

        Returns:
        - Optimization outputs.
        """
        area_commitment = self._get_total_area_commitment()


        if self.split_gas_approach:
            return self.optimisation.optimise_livestock_pop(
                ratio_type=self.get_livestock_ratio_type,
                ratio_value=self.livestock_ratio_value,
                year=self.target_year,
                scenario=self.scenario,
                abatement= self.abatement,
                emissions_budget=self.split_gas_budget,
                area_commitment=area_commitment,
                ch4_budget=self.ch4_budget
            )
        else:
            return self.optimisation.optimise_livestock_pop(
                ratio_type=self.get_livestock_ratio_type,
                ratio_value=self.livestock_ratio_value,
                year=self.target_year,
                scenario=self.scenario,
                abatement=self.abatement,
                area_commitment=area_commitment,
                emissions_budget=self.net_zero_budget
            )
        

    def get_dairy_population(self):
        """
        Get the optimized dairy population.

        Returns:
        - Dairy population.
        """
        return self._load_optomisation_outputs()["Dairy_animals"]


    def get_beef_population(self):
        """
        Get the optimized beef population.

        Returns:
        - Beef population.
        """
        return self._load_optomisation_outputs()["Beef_animals"]
    
    def _get_scaled_beef_population(self):
        """
        Get the scaled beef population based on emission scalers.

        Returns:
        - Scaled beef population.
        """
        scale = self.data_manager_class.get_livestock_emission_scaler(
            year=self.target_year,
            system='Beef',
            gas="CO2",
            scenario=self.scenario,
            abatement=self.abatement
        )


        return self.get_beef_population() / scale["pop"]
    
    def _get_scaled_dairy_population(self):
        """
        Get the scaled dairy population based on emission scalers.

        Returns:
        - Scaled dairy population.
        """
        scale = self.data_manager_class.get_livestock_emission_scaler(
            year=self.target_year,
            system='Dairy',
            gas="CO2",
            scenario=self.scenario,
            abatement=self.abatement
        )

        return self.get_dairy_population() / scale["pop"]
    

    def get_dairy_cows_co2_emission(self):
        """
        Calculate the CO2 emissions for dairy cows (kt).

        Returns:
        - CO2 emissions for dairy cows.
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
        Calculate the CH4 emissions for dairy cows (kt).

        Returns:
        - CH4 emissions for dairy cows.
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
        Calculate the N2O emissions for dairy cows (kt).

        Returns:
        - N2O emissions for dairy cows.
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
        Calculate the CO2e emissions for dairy cows (kt).

        Returns:
        - CO2e emissions for dairy cows.
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
        Calculate the CO2 emissions for beef cows (kt).

        Returns:
        - CO2 emissions for beef cows.
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
        Calculate the CH4 emissions for beef cows (kt).

        Returns:
        - CH4 emissions for beef cows.
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
        Calculate the N2O emissions for beef cows (kt).

        Returns:
        - N2O emissions for beef cows.
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
        Calculate the CO2e emissions for beef cows (kt).

        Returns:
        - CO2e emissions for beef cows.
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
        Calculate the total CO2 emissions for all livestock (kt).

        Returns:
        - Total CO2 emissions.
        """
        return self.get_dairy_cows_co2_emission() + self.get_beef_cows_co2_emission()
    
    def get_total_ch4_emission(self):
        """
        Calculate the total CH4 emissions for all livestock (kt).

        Returns:
        - Total CH4 emissions.
        """
        return self.get_dairy_cows_ch4_emission() + self.get_beef_cows_ch4_emission()
    
    def get_total_n2o_emission(self):
        """
        Calculate the total N2O emissions for all livestock (kt).

        Returns:
        - Total N2O emissions.
        """
        return self.get_dairy_cows_n2o_emission() + self.get_beef_cows_n2o_emission()
    
    def get_total_co2e_emission(self):
        """
        Calculate the total CO2e emissions for all livestock (kt).

        Returns:
        - Total CO2e emissions.
        """
        return self.get_dairy_cows_co2e_emission() + self.get_beef_cows_co2e_emission()
    

    def get_dairy_cows_area(self):
        """
        Calculate the land area required for dairy cows.

        Returns:
        - Land area for dairy cows.
        """
        dairy_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.target_year,
            system='Dairy',
            scenario=self.scenario,
            abatement=self.abatement
        )


        return dairy_area['area'] * self._get_scaled_dairy_population()
    
    def get_beef_cows_area(self):
        """
        Calculate the land area required for beef cows.

        Returns:
        - Land area for beef cows.
        """
        beef_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.target_year,
            system='Beef',
            scenario=self.scenario,
            abatement=self.abatement
        )
        dairy_beef_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.target_year,
            system='Dairy+Beef',
            scenario=self.scenario,
            abatement=self.abatement
        )

        total_area = beef_area['area'] + dairy_beef_area['area']

        return total_area * self._get_scaled_beef_population()


    def get_total_area(self):
        """
        Calculate the total land area required for all livestock.

        Returns:
        - Total land area.
        """
        return self.get_dairy_cows_area() + self.get_beef_cows_area()
     

    def get_total_beef_protein(self):
        """
        Calculate the total protein production for beef and dairy+beef systems.

        Returns:
            float: The total protein production for beef and dairy+beef systems in kg.
        """
        beef_protein = self.data_manager_class.get_livestock_protein_scaler(
            year=self.target_year,
            system='Beef',
            item="beef",
            scenario=self.scenario,
            abatement=self.abatement
        )

        dairy_beef_protein = self.data_manager_class.get_livestock_protein_scaler(
            year=self.target_year,
            system='Dairy',
            item="beef",
            scenario=self.scenario,
            abatement=self.abatement
        )

        total_protein = (beef_protein["value"].item()  + dairy_beef_protein["value"].item()) * self._get_scaled_beef_population()
        
        return total_protein * self._beef_protein
    
    
    def get_total_milk_protein(self):
        """
        Calculate the total milk protein production for dairy cows.

        Returns:
            float: The total milk protein production for dairy cows in kg.
        """
        dairy_protein = self.data_manager_class.get_livestock_protein_scaler(
            year=self.target_year,
            system='Dairy',
            item="milk",
            scenario=self.scenario,
            abatement=self.abatement
        )

        total_protein = dairy_protein["value"].item() * self._get_scaled_dairy_population()
        
        return total_protein * self._milk_protein
    
    def get_hnv_area(self):
        """
        Calculate the area of high nature value (HNV) managed by beef cows.

        Returns:
            float: The HNV area in hectares.
        """
        beef_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.target_year,
            system='Beef',
            scenario=self.scenario,
            abatement=self.abatement
        )
        dairy_beef_area = self.data_manager_class.get_livestock_area_scaler(
            year=self.target_year,
            system='Dairy+Beef',
            scenario=self.scenario,
            abatement=self.abatement
        )

        total_area = beef_area['hnv_area'] + dairy_beef_area['hnv_area']

        return total_area * self._get_scaled_beef_population()