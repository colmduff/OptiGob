import unittest
from optigob.optimisation.livestock_optimisation import LivestockOptimisation
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestLivestockOptimisation(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager =OptiGobDataManager(self.data)
        self.optimiser = LivestockOptimisation(self.data_manager)

    def test_optimise_livestock_pop(self):
        gas = "CO2"
        emissions_budget = 1000
        dairy_beef_ratio = 2
        year = 2023
        scenario = 1

        result = self.optimiser.optimise_livestock_pop(
            gas, emissions_budget, dairy_beef_ratio, year, scenario
        )

        dairy_units = result["Dairy_animals"]
        beef_units = result["Beef_animals"]

        dairy_emissions = result["Dairy_emissions"]
        beef_emissions = result["Beef_emissions"]

        self.assertIsNotNone(dairy_units)
        self.assertIsNotNone(beef_units)
        self.assertAlmostEqual(dairy_units / 10000, 2 * (beef_units / 10000))
        self.assertAlmostEqual((dairy_emissions) + (beef_emissions), emissions_budget)

if __name__ == "__main__":
    unittest.main()
