import unittest
from optigob.livestock.livestock_budget import LivestockBudget
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestForestBudget(unittest.TestCase):

    def setUp(self):
        self.data = './data/sip.yaml'
        self.data_manager = OptiGobDataManager(self.data)
        self.livestock_budget = LivestockBudget(self.data_manager, 1000, 500)


    def test_get_dairy_population(self):
        dairy_population = self.livestock_budget.get_dairy_population()
        print(f"Dairy Population: {dairy_population}")
        self.assertIsNotNone(dairy_population)

    def test_get_beef_population(self):
        beef_population = self.livestock_budget.get_beef_population()
        print(f"Beef Population: {beef_population}")
        self.assertIsNotNone(beef_population)

    def test_get_dairy_cows_co2_emission(self):
        dairy_co2_emission = self.livestock_budget.get_dairy_cows_co2_emission()
        print(f"Dairy Cows CO2 Emission: {dairy_co2_emission}")
        self.assertIsNotNone(dairy_co2_emission)

    def test_get_dairy_cows_ch4_emission(self):
        dairy_ch4_emission = self.livestock_budget.get_dairy_cows_ch4_emission()
        print(f"Dairy Cows CH4 Emission: {dairy_ch4_emission}")
        self.assertIsNotNone(dairy_ch4_emission)

    def test_get_dairy_cows_n2o_emission(self):
        dairy_n2o_emission = self.livestock_budget.get_dairy_cows_n2o_emission()
        print(f"Dairy Cows N2O Emission: {dairy_n2o_emission}")
        self.assertIsNotNone(dairy_n2o_emission)

    def test_get_dairy_cows_co2e_emission(self):
        dairy_co2e_emission = self.livestock_budget.get_dairy_cows_co2e_emission()
        print(f"Dairy Cows CO2e Emission: {dairy_co2e_emission}")
        self.assertIsNotNone(dairy_co2e_emission)

    def test_get_beef_cows_co2_emission(self):
        beef_co2_emission = self.livestock_budget.get_beef_cows_co2_emission()
        print(f"Beef Cows CO2 Emission: {beef_co2_emission}")
        self.assertIsNotNone(beef_co2_emission)

    def test_get_beef_cows_ch4_emission(self):
        beef_ch4_emission = self.livestock_budget.get_beef_cows_ch4_emission()
        print(f"Beef Cows CH4 Emission: {beef_ch4_emission}")
        self.assertIsNotNone(beef_ch4_emission)

    def test_get_beef_cows_n2o_emission(self):
        beef_n2o_emission = self.livestock_budget.get_beef_cows_n2o_emission()
        print(f"Beef Cows N2O Emission: {beef_n2o_emission}")
        self.assertIsNotNone(beef_n2o_emission)

    def test_get_beef_cows_co2e_emission(self):
        beef_co2e_emission = self.livestock_budget.get_beef_cows_co2e_emission()
        print(f"Beef Cows CO2e Emission: {beef_co2e_emission}")
        self.assertIsNotNone(beef_co2e_emission)

    def test_get_total_co2_emission(self):
        total_co2_emission = self.livestock_budget.get_total_co2_emission()
        print(f"Total CO2 Emission: {total_co2_emission}")
        self.assertIsNotNone(total_co2_emission)

    def test_get_total_ch4_emission(self):
        total_ch4_emission = self.livestock_budget.get_total_ch4_emission()
        print(f"Total CH4 Emission: {total_ch4_emission}")
        self.assertIsNotNone(total_ch4_emission)

    def test_get_total_n2o_emission(self):
        total_n2o_emission = self.livestock_budget.get_total_n2o_emission()
        print(f"Total N2O Emission: {total_n2o_emission}")
        self.assertIsNotNone(total_n2o_emission)

    def test_get_total_co2e_emission(self):
        total_co2e_emission = self.livestock_budget.get_total_co2e_emission()
        print(f"Total CO2e Emission: {total_co2e_emission}")
        self.assertIsNotNone(total_co2e_emission)

    def test_get_dairy_cows_area(self):
        result = self.livestock_budget.get_dairy_cows_area()
        print(f"dairy area: {result}")
        self.assertIsNotNone(result)

    def test_get_beef_cows_area(self):
        result = self.livestock_budget.get_beef_cows_area()
        print(f"beef area: {result}")
        self.assertIsNotNone(result)

    def test_get_total_area(self):
        result = self.livestock_budget.get_total_area()
        print(f"total area: {result}")

    def test_get_total_beef_protein(self):
        result = self.livestock_budget.get_total_beef_protein()
        print(f"TOTAL beef protein: {result}")
        self.assertIsNotNone(result)

    def test_get_total_milk_protein(self):
        result = self.livestock_budget.get_total_milk_protein()
        print(f"TOTAL milk protein: {result}")
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()