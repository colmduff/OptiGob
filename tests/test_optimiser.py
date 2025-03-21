import unittest
from optigob.livestock.livestock_optimisation import LivestockOptimisation
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestLivestockOptimisation(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.optimiser = LivestockOptimisation(self.data_manager)

    def test_optimise_livestock_pop(self):
        emissions_budget = 3000
        dairy_beef_ratio = 2
        year = 2050
        scenario = 1
        abatement = "baseline"

        result = self.optimiser.optimise_livestock_pop(
            dairy_beef_ratio, year, scenario, abatement, emissions_budget
        )

        dairy_units = result["Dairy_animals"]
        beef_units = result["Beef_animals"]

        dairy_emissions = result["Dairy_emissions_CO2e"]
        beef_emissions = result["Beef_emissions_CO2e"]

        self.assertIsNotNone(dairy_units)
        self.assertIsNotNone(beef_units)

        print("###")
        print("Dairy units: ", dairy_units)
        print("Beef units: ", beef_units)
        print("Dairy emissions: ", dairy_emissions)
        print("Beef emissions: ", beef_emissions)



    def test_optimise_with_ch4_budget(self):
        emissions_budget = 5000
        ch4_budget = 350
        dairy_beef_ratio = 2
        year = 2050
        scenario = 1
        abatement = "baseline"

        result = self.optimiser.optimise_livestock_pop(
            dairy_beef_ratio, year, scenario, abatement, emissions_budget, ch4_budget
        )

        dairy_units = result["Dairy_animals"]
        beef_units = result["Beef_animals"]

        dairy_emissions = result["Dairy_emissions_CO2e"]
        beef_emissions = result["Beef_emissions_CO2e"]
        dairy_ch4_emissions = result["Dairy_emissions_CH4"]
        beef_ch4_emissions = result["Beef_emissions_CH4"]

        self.assertIsNotNone(dairy_units)
        self.assertIsNotNone(beef_units)
        #self.assertAlmostEqual(dairy_units / 10000, 2 * (beef_units / 10000))
       
        print("###")
        print("Dairy units: ", dairy_units)
        print("Beef units: ", beef_units)
        print("Dairy emissions: ", dairy_emissions)
        print("Beef emissions: ", beef_emissions)
        print("Dairy CH4 emissions: ", dairy_ch4_emissions)
        print("Beef CH4 emissions: ", beef_ch4_emissions)
        print("total emissions_co2e: ", dairy_emissions + beef_emissions)
        print("total emissions_ch4: ", dairy_ch4_emissions + beef_ch4_emissions)
        

    def test_optimise_different_scenario(self):
        emissions_budget = 3000
        dairy_beef_ratio = 3
        year = 2050
        scenario = 2
        abatement = "baseline"

        result = self.optimiser.optimise_livestock_pop(
            dairy_beef_ratio, year, scenario, abatement, emissions_budget
        )

        dairy_units = result["Dairy_animals"]
        beef_units = result["Beef_animals"]

        dairy_emissions = result["Dairy_emissions_CO2e"]
        beef_emissions = result["Beef_emissions_CO2e"]

        self.assertIsNotNone(dairy_units)
        self.assertIsNotNone(beef_units)

        print("###")
        print("Dairy units: ", dairy_units)
        print("Beef units: ", beef_units)
        print("Dairy emissions: ", dairy_emissions)
        print("Beef emissions: ", beef_emissions)
        print("total emissions: ", dairy_emissions + beef_emissions)



if __name__ == "__main__":
    unittest.main()
