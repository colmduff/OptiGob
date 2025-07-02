import unittest
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
from optigob.other_land.other_land_budget import OtherLandBudget

class TestOtherLandBudget(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)

        self.budget = OtherLandBudget(self.data_manager)

    def test_get_wetland_restoration_emission_co2e(self):
        result = self.budget.get_wetland_restoration_emission_co2e()
        self.assertIsNotNone(result)

    def test_get_wetland_restoration_emission_ch4(self):
        result = self.budget.get_wetland_restoration_emission_ch4()
        self.assertIsNotNone(result)

    def test_get_wetland_restoration_emission_n2o(self):
        result = self.budget.get_wetland_restoration_emission_n2o()
        self.assertIsNotNone(result)

    def test_get_wetland_restoration_emission_co2(self):
        result = self.budget.get_wetland_restoration_emission_co2()
        self.assertIsNotNone(result)

    def test_get_drained_organic_soil_area(self):
        result = self.budget.get_drained_organic_soil_area()
        self.assertIsNotNone(result)

    def test_get_rewetted_organic_area(self):
        result = self.budget.get_rewetted_organic_area()
        self.assertIsNotNone(result)

    def test_get_drained_wetland_area(self):
        result = self.budget.get_drained_wetland_area()
        self.assertIsNotNone(result)

    def test_get_rewetted_wetland_area(self):
        result = self.budget.get_rewetted_wetland_area()
        self.assertIsNotNone(result)

    def test_get_near_natural_wetland_area(self):
        result = self.budget.get_near_natural_wetland_area()
        self.assertIsNotNone(result)

    def test_get_total_other_land_area(self):
        result = self.budget.get_total_other_land_area()
        self.assertIsNotNone(result)

    def test_get_rewetted_organic_hnv_area(self):
        result = self.budget.get_rewetted_organic_hnv_area()
        self.assertIsNotNone(result)

    def test_get_rewetted_wetland_hnv_area(self):
        result = self.budget.get_rewetted_wetland_hnv_area()
        self.assertIsNotNone(result)

    def test_get_near_natural_wetland_hnv_area(self):
        result = self.budget.get_near_natural_wetland_hnv_area()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
