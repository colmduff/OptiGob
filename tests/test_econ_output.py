import unittest
from optigob.budget_model.econ_output import EconOutput
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestEconOutput(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.budget= EconOutput(self.data_manager)
        
    def test_output_creation(self):
        scenario_protein = self.budget.get_total_scenario_protein_by_sector()
        baseline_protein = self.budget.get_total_baseline_protein_by_sector()
        
        print("Scenario Protein Output:", scenario_protein)
        print("Baseline Protein Output:", baseline_protein)
        
        self.assertIsNotNone(scenario_protein)
        self.assertIsNotNone(baseline_protein)

if __name__ == '__main__':
    unittest.main()

