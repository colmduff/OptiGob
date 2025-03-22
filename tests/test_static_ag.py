import unittest
from optigob.static_ag.static_ag_budget import StaticAgBudget
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestStaticAgBudget(unittest.TestCase):

    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.static_ag_budget = StaticAgBudget(self.data_manager)

    def test_get_pig_and_poultry_co2_emission(self):
        result = self.static_ag_budget.get_pig_and_poultry_co2_emission()
        self.assertIsInstance(result, float)


    def test_get_pig_and_poultry_ch4_emission(self):
        result = self.static_ag_budget.get_pig_and_poultry_ch4_emission()
        self.assertIsInstance(result, float)

    def test_get_pig_and_poultry_n2o_emission(self):
        result = self.static_ag_budget.get_pig_and_poultry_n2o_emission()
        self.assertIsInstance(result, float)

    def test_get_pig_and_poultry_co2e_emission(self):
        result = self.static_ag_budget.get_pig_and_poultry_co2e_emission()
        self.assertIsInstance(result, float)

    def test_get_sheep_co2_emission(self):
        result = self.static_ag_budget.get_sheep_co2_emission()
        self.assertIsInstance(result, float)

    def test_get_sheep_ch4_emission(self):
        result = self.static_ag_budget.get_sheep_ch4_emission()
        self.assertIsInstance(result, float)

    def test_get_sheep_n2o_emission(self):
        result = self.static_ag_budget.get_sheep_n2o_emission()
        self.assertIsInstance(result, float)

    def test_get_sheep_co2e_emission(self):
        result = self.static_ag_budget.get_sheep_co2e_emission()
        self.assertIsInstance(result, float)

    def test_get_crop_co2_emission(self):
        result = self.static_ag_budget.get_crop_co2_emission()
        self.assertIsInstance(result, float)

    def test_get_crop_ch4_emission(self):
        result = self.static_ag_budget.get_crop_ch4_emission()
        self.assertIsInstance(result, float)

    def test_get_crop_n2o_emission(self):
        result = self.static_ag_budget.get_crop_n2o_emission()
        self.assertIsInstance(result, float)

    def test_get_crop_co2e_emission(self):
        result = self.static_ag_budget.get_crop_co2e_emission()
        self.assertIsInstance(result, float)

    def test_get_total_static_ag_co2e(self):
        result = self.static_ag_budget.get_total_static_ag_co2e()
        self.assertIsInstance(result, float)

    def test_get_total_static_ag_co2(self):
        result = self.static_ag_budget.get_total_static_ag_co2()
        self.assertIsInstance(result, float)

    def test_get_total_static_ag_ch4(self):
        result = self.static_ag_budget.get_total_static_ag_ch4()
        self.assertIsInstance(result, float)

    def test_get_total_static_ag_n2o(self):
        result = self.static_ag_budget.get_total_static_ag_n2o()
        self.assertIsInstance(result, float)

    def test_get_sheep_area(self):
        result = self.static_ag_budget.get_sheep_area()

        print(f"sheep area: {result}")
        self.assertIsInstance(result, float)

    def test_get_pig_and_poultry_area(self):
        result = self.static_ag_budget.get_pig_and_poultry_area()

        print(f"pig and poultry area: {result}")
        self.assertIsInstance(result, float)

    def test_get_crop_area(self):
        result = self.static_ag_budget.get_crop_area()

        print(f"crop area: {result}")
        self.assertIsInstance(result, float)

    def test_get_total_static_ag_area(self):
        result = self.static_ag_budget.get_total_static_ag_area()

        print(f"total static ag area: {result}")
        self.assertIsInstance(result, float)


if __name__ == '__main__':
    unittest.main()
