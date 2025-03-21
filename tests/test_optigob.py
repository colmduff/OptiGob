import unittest
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
from optigob.optigob import Optigob

class TestOptigob(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)

    def test_optigob_functionality(self):
        result = Optigob(self.data_manager)

        # Baseline emissions
        print("\nBaseline CO2e Emissions by Sector:\n", result.get_baseline_co2e_emissions_by_sector())
        print("\nBaseline CH4 Emissions by Sector:\n", result.get_baseline_ch4_emissions_by_sector())
        print("\nBaseline N2O Emissions by Sector:\n", result.get_baseline_n2o_emissions_by_sector())
        print("\nBaseline CO2 Emissions by Sector:\n", result.get_baseline_co2_emissions_by_sector())
        print("\nBaseline CO2e Emissions Total:\n", result.get_baseline_co2e_emissions_total())
        print("\nBaseline CO2 Emissions Total:\n", result.get_baseline_co2_emissions_total())
        print("\nBaseline CH4 Emissions Total:\n", result.get_baseline_ch4_emissions_total())
        print("\nBaseline N2O Emissions Total:\n", result.get_baseline_n2o_emissions_total())

        self.assertIsNotNone(result.get_baseline_co2e_emissions_by_sector())
        self.assertIsNotNone(result.get_baseline_ch4_emissions_by_sector())
        self.assertIsNotNone(result.get_baseline_n2o_emissions_by_sector())
        self.assertIsNotNone(result.get_baseline_co2_emissions_by_sector())
        self.assertIsNotNone(result.get_baseline_co2e_emissions_total())
        self.assertIsNotNone(result.get_baseline_co2_emissions_total())
        self.assertIsNotNone(result.get_baseline_ch4_emissions_total())
        self.assertIsNotNone(result.get_baseline_n2o_emissions_total())

        # Scenario emissions
        print("\nScenario CO2e Emissions by Sector:\n", result.get_scenario_co2e_emissions_by_sector())
        print("\nScenario CH4 Emissions by Sector:\n", result.get_scenario_ch4_emissions_by_sector())
        print("\nScenario N2O Emissions by Sector:\n", result.get_scenario_n2o_emissions_by_sector())
        print("\nScenario CO2 Emissions by Sector:\n", result.get_scenario_co2_emissions_by_sector())

        self.assertIsNotNone(result.get_scenario_co2e_emissions_by_sector())
        self.assertIsNotNone(result.get_scenario_ch4_emissions_by_sector())
        self.assertIsNotNone(result.get_scenario_n2o_emissions_by_sector())
        self.assertIsNotNone(result.get_scenario_co2_emissions_by_sector())

        

if __name__ == '__main__':
    unittest.main()
