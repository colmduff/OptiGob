import unittest
from optigob.livestock.baseline_livestock import BaselineLivestock
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestBaselineLivestock(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.baseline = BaselineLivestock(self.data_manager)

    def test_get_dairy_cows_co2_emission(self):
        result = self.baseline.get_dairy_cows_co2_emission()
        print(f"dairy co2: {result}")
        self.assertIsNotNone(result)

    def test_get_dairy_cows_ch4_emission(self):
        result = self.baseline.get_dairy_cows_ch4_emission()
        print(f"dairy ch4: {result}")
        self.assertIsNotNone(result)

    def test_get_dairy_cows_n2o_emission(self):
        result = self.baseline.get_dairy_cows_n2o_emission()
        print(f"dairy n2o: {result}")
        self.assertIsNotNone(result)

    def test_get_dairy_cows_co2e_emission(self):
        result = self.baseline.get_dairy_cows_co2e_emission()
        print(f"dairy co2e: {result}")
        self.assertIsNotNone(result)

    def test_get_beef_cows_co2_emission(self):
        result = self.baseline.get_beef_cows_co2_emission()
        print(f"beef co2: {result}")
        self.assertIsNotNone(result)

    def test_get_beef_cows_ch4_emission(self):
        result = self.baseline.get_beef_cows_ch4_emission()
        print(f"beef ch4: {result}")
        self.assertIsNotNone(result)

    def test_get_beef_cows_n2o_emission(self):
        result = self.baseline.get_beef_cows_n2o_emission()
        print(f"beef n2o: {result}")
        self.assertIsNotNone(result)

    def test_get_beef_cows_co2e_emission(self):
        result = self.baseline.get_beef_cows_co2e_emission()
        print(f"beef co2e: {result}")
        self.assertIsNotNone(result)

    def test_get_total_co2_emission(self):
        result = self.baseline.get_total_co2_emission()
        print(f"total co2: {result}")
        self.assertIsNotNone(result)

    def test_get_total_ch4_emission(self):
        result = self.baseline.get_total_ch4_emission()
        print(f"total ch4: {result}")
        self.assertIsNotNone(result)

    def test_get_total_n2o_emission(self):
        result = self.baseline.get_total_n2o_emission()
        print(f"total n2o: {result}")
        self.assertIsNotNone(result)

    def test_get_total_co2e_emission(self):
        result = self.baseline.get_total_co2e_emission()
        print(f"total co2e: {result}")
        self.assertIsNotNone(result)

    def test_get_dairy_cows_area(self):
        result = self.baseline.get_dairy_cows_area()
        print(f"dairy area: {result}")
        self.assertIsNotNone(result)

    def test_get_beef_cows_area(self):
        result = self.baseline.get_beef_cows_area()
        print(f"beef area: {result}")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()