"""
livestock_budget
================

This module contains the LivestockBudget class, which is responsible for managing and optimizing livestock populations, emissions, protein yields, and land use within the FORESIGHT framework. The class integrates with data managers and optimization models to compute livestock-related budgets and outputs under various scenarios.

Classes:
    - LivestockBudget: Manages and optimizes livestock populations, emissions, protein, and land use.

Methods:
    - __init__(self, optigob_data_manager, net_zero_budget=None, split_gas_budget=None): Initialize the LivestockBudget class and set up all required budgets, data managers, and scenario parameters.
    - _get_total_area_commitment(self): Calculate the total area commitment for all land uses that compete with livestock (rewetted, afforested, biomethane, willow, protein crops).
    - _load_optimisation_outputs(self): Load and cache the livestock optimisation outputs if not already loaded.
    - _get_total_non_livestock_emission_ch4(self): Calculate total CH4 emissions from all relevant land uses and sectors in the scenario.
    - get_ch4_budget(self): Calculate the CH4 budget for the scenario, based on baseline emissions and the split gas fraction.
    - get_split_gas_ch4_emission(self): Calculate the remaining CH4 budget after accounting for all scenario emissions, under the split gas approach.
    - get_optimisation_outputs(self): Run the livestock population optimisation for the current scenario and constraints.
    - get_dairy_population(self): Get the optimised dairy cow population for the scenario.
    - get_beef_population(self): Get the optimised beef cow population for the scenario.
    - _get_scaled_beef_population(self): Get the beef cow population, scaled by the emission scaler for the scenario.
    - _get_scaled_dairy_population(self): Get the dairy cow population, scaled by the emission scaler for the scenario.
    - get_dairy_cows_co2_emission(self): Calculate the total CO2 emissions from dairy cows for the scenario.
    - get_dairy_cows_ch4_emission(self): Calculate the total CH4 emissions from dairy cows for the scenario.
    - get_dairy_cows_n2o_emission(self): Calculate the total N2O emissions from dairy cows for the scenario.
    - get_dairy_cows_co2e_emission(self): Calculate the total CO2e emissions from dairy cows for the scenario.
    - get_beef_cows_co2_emission(self): Calculate the total CO2 emissions from beef cows for the scenario.
    - get_beef_cows_ch4_emission(self): Calculate the total CH4 emissions from beef cows for the scenario.
    - get_beef_cows_n2o_emission(self): Calculate the total N2O emissions from beef cows for the scenario.
    - get_beef_cows_co2e_emission(self): Calculate the total CO2e emissions from beef cows for the scenario.
    - get_total_co2_emission(self): Calculate the total CO2 emissions from all livestock (dairy and beef) for the scenario.
    - get_total_ch4_emission(self): Calculate the total CH4 emissions from all livestock (dairy and beef) for the scenario.
    - get_total_n2o_emission(self): Calculate the total N2O emissions from all livestock (dairy and beef) for the scenario.
    - get_total_co2e_emission(self): Calculate the total CO2e emissions from all livestock (dairy and beef) for the scenario.
    - get_dairy_cows_area(self): Calculate the total land area required for dairy cows.
    - get_beef_cows_area(self): Calculate the total land area required for beef cows.
    - get_total_area(self): Calculate the total land area required for all livestock (dairy and beef).
    - get_total_beef_protein(self): Calculate the total protein production from beef and dairy+beef systems for the scenario.
    - get_total_milk_protein(self): Calculate the total milk protein production from dairy cows for the scenario.
    - get_hnv_area(self): Calculate the area of high nature value (HNV) grassland managed by beef cows, including both beef and dairy+beef systems.
"""

from optigob.livestock.livestock_optimisation import LivestockOptimisation
from optigob.budget_model.baseline_emissions import BaselineEmission
from optigob.other_land.other_land_budget import OtherLandBudget
from optigob.forest.forest_budget import ForestBudget
from optigob.bioenergy.bioenergy_budget import BioEnergyBudget
from optigob.protein_crops.protein_crops_budget import ProteinCropsBudget
from optigob.static_ag.static_ag_budget import StaticAgBudget
from optigob.logger import get_logger

logger = get_logger("livestock")



class LivestockBudget:
    """
    The LivestockBudget class manages and optimizes livestock populations, emissions, protein yields, and land use within the FORESIGHT framework.
    It integrates with data managers and optimization models to compute livestock-related budgets, emissions, protein yields, and land requirements under various scenarios.

    Attributes:
        net_zero_budget (float or None): Emissions budget for net zero scenarios.
        split_gas_budget (float or None): Emissions budget for split gas scenarios.
        data_manager_class: Instance of the data manager for accessing scenario and scaler data.
        optimisation (LivestockOptimisation): Optimisation engine for livestock populations.
        baseline_emission (BaselineEmission): Baseline emissions calculator.
        other_land_budget (OtherLandBudget): Budget for other land uses.
        forest_budget (ForestBudget): Budget for forest land uses.
        bio_energy_budget (BioEnergyBudget): Budget for bioenergy land uses.
        protein_crop_budget (ProteinCropsBudget): Budget for protein crop land uses.
        static_ag_budget (StaticAgBudget): Budget for static agriculture land uses.
        rewetted_area (float): Area of rewetted organic soils (ha).
        afforested_area (float): Area for afforestation (ha).
        biomethane_area (float): Area for biomethane production (ha).
        willow_area (float): Area for willow production (ha).
        protein_crop_area (float): Area for protein crops (ha).
        _milk_protein (float): Protein content scaler for milk.
        _beef_protein (float): Protein content scaler for beef.
        target_year (int): Target year for scenario.
        scenario (str): Abatement scenario name.
        abatement (str): Abatement type.
        get_livestock_ratio_type (str): Type of livestock ratio constraint.
        livestock_ratio_value (float): Value for livestock ratio constraint.
        split_gas_approach (bool): Whether split gas approach is used.
        split_gas_frac (float): Fraction for split gas approach.
        ch4_baseline (float): Baseline CH4 emissions (kt).
        ch4_budget (float): CH4 budget for split gas approach (kt).
        _optimisation_outputs (dict or None): Cached optimisation outputs.
    """
    def __init__(self, optigob_data_manager,
                 net_zero_budget=None,
                 split_gas_budget=None):
        """
        Initialize the LivestockBudget class and set up all required budgets, data managers, and scenario parameters.

        Args:
            optigob_data_manager: Instance of the data manager for accessing all scenario, scaler, and input data.
            net_zero_budget (float, optional): Emissions budget for net zero scenarios. Defaults to None.
            split_gas_budget (float, optional): Emissions budget for split gas scenarios. Defaults to None.
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
        self.static_ag_budget = StaticAgBudget(self.data_manager_class)


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

        if self.split_gas_approach:
            self.ch4_budget = self.get_split_gas_ch4_emission()

        self._optimisation_outputs = None

       

    def _get_total_area_commitment(self):
        """
        Calculate the total area commitment for all land uses that compete with livestock (rewetted, afforested, biomethane, willow, protein crops).

        Returns:
            float: Total area commitment in hectares (ha).
        """
        return (float(self.rewetted_area +
                self.afforested_area +
                self.biomethane_area +
                self.protein_crop_area+
                self.willow_area))

    def _load_optimisation_outputs(self):
        """
        Load and cache the livestock optimisation outputs if not already loaded.

        Returns:
            dict: Dictionary of optimisation results for livestock populations and constraints.

        Raises:
            ValueError: If optimization was infeasible.
        """
        # Load optimization outputs if not already loaded.
        if self._optimisation_outputs is None:
            self._optimisation_outputs = self.get_optimisation_outputs()

            # Check if optimization was feasible
            if not self._optimisation_outputs.feasible:
                raise ValueError(
                    f"Livestock optimization failed:\n{self._optimisation_outputs.get('message', 'Unknown error')}"
                )

        return self._optimisation_outputs
    

    def _get_total_non_livestock_emission_ch4(self):
        """
        Calculate total CH4 (methane) emissions from all relevant land uses and sectors in the scenario.

        Returns:
            float: Total CH4 emissions in kilotonnes (kt).
        """

        static_ag_emission = self.static_ag_budget.get_total_static_ag_ch4()
        other_land_emission = self.other_land_budget.get_wetland_restoration_emission_ch4()
        ad_ag_emission = self.bio_energy_budget.get_ad_ag_ch4_emission()
        protein_crop_emission = self.protein_crop_budget.get_crop_emission_ch4()
        beccs_emission =self.bio_energy_budget.get_total_ccs_ch4_emission()

        return static_ag_emission + other_land_emission + beccs_emission + protein_crop_emission + ad_ag_emission
      
    def get_ch4_budget(self):
        """
        Calculate the CH4 (methane) budget for the scenario, based on baseline emissions and the split gas fraction.

        Returns:
            float: CH4 budget in kilotonnes (kt).
        """
        return self.baseline_emission.get_total_ch4_emission() * (1-self.split_gas_frac)

    def get_split_gas_ch4_emission(self):
        """
        Calculate the remaining CH4 (methane) budget after accounting for all scenario emissions, under the split gas approach.

        Returns:
            float: Remaining CH4 budget in kilotonnes (kt).
        """
        target_year_emission = self._get_total_non_livestock_emission_ch4()

        base_emission_target = self.get_ch4_budget()

        budget =base_emission_target - target_year_emission

        return budget


    def get_optimisation_outputs(self):
        """
        Run the livestock population optimisation for the current scenario and constraints.

        Returns:
            dict: Dictionary of optimised livestock populations and related outputs.

        Raises:
            ValueError: If the scenario is mathematically infeasible before optimization.
        """
        area_commitment = self._get_total_area_commitment()

        if self.split_gas_approach:
            # Pre-flight feasibility check for CH4 budget
            ch4_baseline_total = self.baseline_emission.get_total_ch4_emission()
            ch4_target = ch4_baseline_total * (1 - self.split_gas_frac)
            non_livestock_ch4 = self._get_total_non_livestock_emission_ch4()
            ch4_budget_for_livestock = ch4_target - non_livestock_ch4

            if ch4_budget_for_livestock <= 0:
                # Get individual sources for detailed warning message
                static_ag_ch4 = self.static_ag_budget.get_total_static_ag_ch4()
                wetland_ch4 = self.other_land_budget.get_wetland_restoration_emission_ch4()
                ad_ch4 = self.bio_energy_budget.get_ad_ag_ch4_emission()
                protein_ch4 = self.protein_crop_budget.get_crop_emission_ch4()
                beccs_ch4 = self.bio_energy_budget.get_total_ccs_ch4_emission()

                sources = [
                    ("Wetland restoration", wetland_ch4),
                    ("Static agriculture", static_ag_ch4),
                    ("Anaerobic digestion", ad_ch4),
                    ("Protein crops", protein_ch4),
                    ("BECCS", beccs_ch4),
                ]
                sources_sorted = sorted(sources, key=lambda x: x[1], reverse=True)

                warning_msg = (
                    f"\nWARNING: Zero CH4 budget for livestock.\n\n"
                    f"Your scenario's CH4 budget has been exhausted by other land uses:\n"
                    f"  CH4 target (with {self.split_gas_frac*100:.0f}% reduction):  {ch4_target:8.2f} kt\n"
                    f"  Non-livestock CH4 emissions:                {non_livestock_ch4:8.2f} kt\n"
                    f"  ─────────────────────────────────────────────────────\n"
                    f"  CH4 budget available for livestock:         {ch4_budget_for_livestock:8.2f} kt\n\n"
                    f"Other conditions have used up the available CH4 budget:\n"
                )

                for source_name, value in sources_sorted:
                    if value > 0:
                        pct = (value / ch4_target) * 100
                        warning_msg += f"  • {source_name:25s}: {value:7.2f} kt ({pct:5.1f}% of target)\n"

                # Identify the major contributors
                major_contributors = [name for name, val in sources_sorted if val > ch4_target * 0.5]
                if major_contributors:
                    warning_msg += f"\nMajor contributor(s): {', '.join(major_contributors)}\n"

                warning_msg += (
                    f"\nResult: Zero livestock is the only feasible solution.\n\n"
                    f"To allow livestock production, you can try some of the following:\n"
                    f"  1. Reduce split_gas_frac (currently {self.split_gas_frac}) to allow more CH4\n"
                    f"  2. Reduce wetland restoration area (currently {self.rewetted_area:.0f} ha)\n"
                    f"  3. Reduce biomethane/AD area (currently {self.biomethane_area:.0f} ha)\n"
                    f"  4. Use split_gas=False for standard CO2e accounting instead\n"
                )

                logger.warning(warning_msg)

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
            # Pre-flight information for zero CO2e budget
            if self.net_zero_budget <= 0:
                # Get individual sources for detailed informational message
                static_ag_co2e = self.static_ag_budget.get_total_static_ag_co2e()
                forest_co2e = self.forest_budget.total_emission_offset()
                wetland_co2e = self.other_land_budget.get_wetland_restoration_emission_co2e()
                ad_co2e = self.bio_energy_budget.get_ad_ag_co2e_emission()
                protein_co2e = self.protein_crop_budget.get_crop_emission_co2e()
                beccs_co2e = self.bio_energy_budget.get_total_ccs_co2e_emission()

                total_non_livestock = static_ag_co2e + forest_co2e + wetland_co2e + ad_co2e + protein_co2e + beccs_co2e

                # Sort sources by absolute magnitude for better readability
                sources = [
                    ("Wetland restoration", wetland_co2e),
                    ("Static agriculture", static_ag_co2e),
                    ("Anaerobic digestion", ad_co2e),
                    ("Forest offset", forest_co2e),
                    ("Protein crops", protein_co2e),
                    ("BECCS", beccs_co2e),
                ]
                sources_sorted = sorted(sources, key=lambda x: abs(x[1]), reverse=True)

                info_msg = (
                    f"\nINFO: Zero CO2e budget for livestock.\n\n"
                    f"Your scenario's non-livestock land uses produce NET EMISSIONS, leaving no budget for livestock:\n"
                    f"  Total non-livestock emissions: {total_non_livestock:8.2f} kt CO2e\n"
                    f"  Net-zero target budget:        {0.0:8.2f} kt CO2e\n"
                    f"  ─────────────────────────────────────────────────────\n"
                    f"  CO2e budget available for livestock: {self.net_zero_budget:8.2f} kt\n\n"
                    f"Non-livestock emission breakdown:\n"
                )

                for source_name, value in sources_sorted:
                    if value != 0:
                        info_msg += f"  • {source_name:25s}: {value:8.2f} kt CO2e\n"

                info_msg += (
                    f"\nResult: Zero livestock is the only feasible solution.\n\n"
                    f"To allow livestock production, you can try:\n"
                    f"  1. Increase forest sequestration (higher afforestation rate)\n"
                    f"  2. Reduce wetland restoration area (currently {self.rewetted_area:.0f} ha)\n"
                    f"  3. Reduce static agriculture emissions\n"
                    f"  4. Enable BECCS to create negative emissions\n"
                )

                logger.info(info_msg)

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
        Get the optimised dairy cow population for the scenario.

        Returns:
            float: Number of dairy cows.
        """
        return self._load_optimisation_outputs()["Dairy_animals"]


    def get_beef_population(self):
        """
        Get the optimised beef cow population for the scenario.

        Returns:
            float: Number of beef cows.
        """
        return self._load_optimisation_outputs()["Beef_animals"]
    
    def _get_scaled_beef_population(self):
        """
        Get the beef cow population, scaled by the emission scaler for the scenario.

        Returns:
            float: Scaled beef cow population.
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
        Get the dairy cow population, scaled by the emission scaler for the scenario.

        Returns:
            float: Scaled dairy cow population.
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
        Calculate the total CO2 emissions from dairy cows for the scenario.

        Returns:
            float: CO2 emissions from dairy cows in kilotonnes (kt).
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
        Calculate the total CH4 emissions from dairy cows for the scenario.

        Returns:
            float: CH4 emissions from dairy cows in kilotonnes (kt).
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
        Calculate the total N2O emissions from dairy cows for the scenario.

        Returns:
            float: N2O emissions from dairy cows in kilotonnes (kt).
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
        Calculate the total CO2e (CO2 equivalent) emissions from dairy cows for the scenario.

        Returns:
            float: CO2e emissions from dairy cows in kilotonnes (kt).
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
        Calculate the total CO2 emissions from beef cows for the scenario.

        Returns:
            float: CO2 emissions from beef cows in kilotonnes (kt).
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
        Calculate the total CH4 emissions from beef cows for the scenario.

        Returns:
            float: CH4 emissions from beef cows in kilotonnes (kt).
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
        Calculate the total N2O emissions from beef cows for the scenario.

        Returns:
            float: N2O emissions from beef cows in kilotonnes (kt).
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
        Calculate the total CO2e (CO2 equivalent) emissions from beef cows for the scenario.

        Returns:
            float: CO2e emissions from beef cows in kilotonnes (kt).
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
        Calculate the total CO2 emissions from all livestock (dairy and beef) for the scenario.

        Returns:
            float: Total CO2 emissions in kilotonnes (kt).
        """
        return self.get_dairy_cows_co2_emission() + self.get_beef_cows_co2_emission()
    
    def get_total_ch4_emission(self):
        """
        Calculate the total CH4 emissions from all livestock (dairy and beef) for the scenario.

        Returns:
            float: Total CH4 emissions in kilotonnes (kt).
        """
        return self.get_dairy_cows_ch4_emission() + self.get_beef_cows_ch4_emission()
    
    def get_total_n2o_emission(self):
        """
        Calculate the total N2O emissions from all livestock (dairy and beef) for the scenario.

        Returns:
            float: Total N2O emissions in kilotonnes (kt).
        """
        return self.get_dairy_cows_n2o_emission() + self.get_beef_cows_n2o_emission()
    
    def get_total_co2e_emission(self):
        """
        Calculate the total CO2e (CO2 equivalent) emissions from all livestock (dairy and beef) for the scenario.

        Returns:
            float: Total CO2e emissions in kilotonnes (kt).
        """
        return self.get_dairy_cows_co2e_emission() + self.get_beef_cows_co2e_emission()
    

    def get_dairy_cows_area(self):
        """
        Calculate the total land area required for dairy cows, using the area scaler and scaled population.

        Returns:
            float: Land area for dairy cows in hectares (ha).
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
        Calculate the total land area required for beef cows, including both beef and dairy+beef systems.

        Returns:
            float: Land area for beef cows in hectares (ha).
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

        total_beef_area = beef_area['area'] * self._get_scaled_beef_population() 
        total_dairy_beef_area = dairy_beef_area['area'] * self._get_scaled_dairy_population()
    
        return total_beef_area + total_dairy_beef_area


    def get_total_area(self):
        """
        Calculate the total land area required for all livestock (dairy and beef).

        Returns:
            float: Total land area in hectares (ha).
        """
        return self.get_dairy_cows_area() + self.get_beef_cows_area()
     

    def get_total_beef_protein(self):
        """
        Calculate the total protein production from beef and dairy+beef systems for the scenario.

        Returns:
            float: Total beef protein production in kilograms (kg).
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

        total_beef_protein = beef_protein["value"].item() * self._get_scaled_beef_population()
                         
        total_dairy_protein = dairy_beef_protein["value"].item() * self._get_scaled_dairy_population()
        
        return (total_beef_protein + total_dairy_protein) * self._beef_protein
    
    
    def get_total_milk_protein(self):
        """
        Calculate the total milk protein production from dairy cows for the scenario.

        Returns:
            float: Total milk protein production in kilograms (kg).
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
        Calculate the area of high nature value (HNV) grassland managed by beef cows, including both beef and dairy+beef systems.

        Returns:
            float: HNV area in hectares (ha).
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

        total_beef_area = (beef_area['hnv_area'] * self._get_scaled_beef_population())
        total_dairy_area = (dairy_beef_area['hnv_area'] * self._get_scaled_dairy_population())

        return total_beef_area + total_dairy_area