import unittest
from optigob.budget_model.baseline_emissions import BaselineEmission
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestBudget(unittest.TestCase):

    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.budget = BaselineEmission(self.data_manager)

    def test_get_co2e_emission_categories(self):
        result = self.budget.get_co2e_emission_categories()
        print("CO2e Emission Categories: ", result)
        self.assertIsNotNone(result)

    def test_get_co2e_emission_categories(self):
        result = self.budget.get_co2e_emission_categories()
        print("CO2e Emission Categories: ", result)
        self.assertIsNotNone(result)

    def test_get_ch4_emission_categories(self):
        result = self.budget.get_ch4_emission_categories()
        print("CH4 Emission Categories: ", result)
        self.assertIsNotNone(result)

    def test_get_n2o_emission_categories(self):
        result = self.budget.get_n2o_emission_categories()
        print("N2O Emission Categories: ", result)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()