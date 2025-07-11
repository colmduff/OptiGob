import unittest
from optigob.budget_model.landarea_budget import LandAreaBudget
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestBudget(unittest.TestCase):

    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.budget = LandAreaBudget(self.data_manager)

    def test_get_baseline_agriculture_area(self):
        result = self.budget.get_baseline_agriculture_area()
        print("Baseline Agriculture Area:", result)
        self.assertIsNotNone(result)

    def test_get_total_baseline_land_area_by_sector(self):
        result = self.budget.get_total_baseline_land_area_by_aggregated_sector()
        print("Total Baseline Land Area by Sector:", result)
        self.assertIsNotNone(result)

    def test_get_scenario_agriculture_area(self):
        result = self.budget.get_scenario_agriculture_area()
        print("Scenario Agriculture Area:", result)
        self.assertIsNotNone(result)

    def test_get_total_scenario_land_area_by_sector(self):
        result = self.budget.get_total_scenario_land_area_by_aggregated_sector()
        print("Total Scenario Land Area by Sector:", result)
        self.assertIsNotNone(result)

    def test_get_total_scenario_land_area_by_aggregated_sector(self):
        result = self.budget.get_total_scenario_land_area_by_aggregated_sector()
        print("Total Scenario Land Area by Aggregated Sector:", result)
        self.assertIsInstance(result, dict)

    def test_get_total_scenario_land_area_by_disaggregated_sector(self):
        result = self.budget.get_total_scenario_land_area_by_disaggregated_sector()
        print("Total Scenario Land Area by Disaggregated Sector:", result)
        self.assertIsInstance(result, dict)

    def test_get_total_baseline_land_area_by_aggregated_sector(self):
        result = self.budget.get_total_baseline_land_area_by_aggregated_sector()
        print("Total Baseline Land Area by Aggregated Sector:", result)
        self.assertIsInstance(result, dict)

    def test_get_total_baseline_land_area_by_disaggregated_sector(self):
        result = self.budget.get_total_baseline_land_area_by_disaggregated_sector()
        print("Total Baseline Land Area by Disaggregated Sector:", result)
        self.assertIsInstance(result, dict)

    def test_get_total_baseline_hnv_land_area_disaggregated_by_sector(self):
        result = self.budget.get_total_baseline_hnv_land_area_disaggregated_by_sector()
        print("Total Baseline HNV Land Area by Disaggregated Sector:", result)
        self.assertIsInstance(result, dict)

    def test_get_total_scenario_hnv_land_area_disaggregated_by_sector(self):
        result = self.budget.get_total_scenario_hnv_land_area_disaggregated_by_sector()
        print("Total Scenario HNV Land Area by Disaggregated Sector:", result)
        self.assertIsInstance(result, dict)

if __name__ == '__main__':
    unittest.main()