import unittest
from optigob.forest.forest_budget import ForestBudget
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestForestBudget(unittest.TestCase):

    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.forest_budget = ForestBudget(self.data_manager)

    def test_get_afforestation_offset(self):
        result = self.forest_budget.get_afforestation_offset()
        self.assertIsNotNone(result)

    def test_get_hwp_offset(self):
        result = self.forest_budget.get_hwp_offset()
        self.assertIsNotNone(result)

    def test_get_ccs_offset(self):
        result = self.forest_budget.get_ccs_offset()
        self.assertIsNotNone(result)

    def test_total_emission_offset(self):
        result = self.forest_budget.total_emission_offset()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
