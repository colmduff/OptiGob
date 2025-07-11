import unittest
from optigob.budget_model.emissions_budget import EmissionsBudget
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestBudget(unittest.TestCase):

    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.budget = EmissionsBudget(self.data_manager)

    def test_emission_values(self):
        total_emission_co2e = self.budget._get_total_emission_co2e()
        split_gas_emissions_total = self.budget._split_gas_emissions_total_budget_co2e()
        total_emission_ch4 = self.budget._get_total_emission_ch4()
        total_emission_n2o = self.budget._get_total_emission_n2o()
        total_emission_co2 = self.budget._get_total_emission_co2()
        total_agriculture_co2e_emission = self.budget.total_agriculture_co2e_emission()
        co2e_emission_categories = self.budget.get_co2e_emission_categories()
        total_co2e_emission = self.budget.get_total_co2e_emission()

        print(f"Total Emission CO2e: {total_emission_co2e}")
        print(f"Split Gas Emissions Total: {split_gas_emissions_total}")
        print(f"Total Emission CH4: {total_emission_ch4}")
        print(f"Total Emission N2O: {total_emission_n2o}")
        print(f"Total Emission CO2: {total_emission_co2}")
        print(f"Total Agriculture CO2e Emission: {total_agriculture_co2e_emission}")
        print(f"CO2e Emission Categories: {co2e_emission_categories}")
        print(f"Total CO2e Emission: {total_co2e_emission}")

        self.assertIsNotNone(total_emission_co2e, "Total Emission CO2e is None")
        self.assertIsNotNone(split_gas_emissions_total, "Split Gas Emissions Total is None")
        self.assertIsNotNone(total_emission_ch4, "Total Emission CH4 is None")
        self.assertIsNotNone(total_emission_n2o, "Total Emission N2O is None")
        self.assertIsNotNone(total_emission_co2, "Total Emission CO2 is None")
        self.assertIsNotNone(total_agriculture_co2e_emission, "Total Agriculture CO2e Emission is None")
        self.assertIsNotNone(co2e_emission_categories, "CO2e Emission Categories is None")
        self.assertIsNotNone(total_co2e_emission, "Total CO2e Emission is None")

if __name__ == '__main__':
    unittest.main()