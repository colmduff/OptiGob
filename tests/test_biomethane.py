import unittest
from optigob.biomethane.biomethane_budget import BioMethaneBudget
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestForestBudget(unittest.TestCase):

    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.biomethane_budget = BioMethaneBudget(self.data_manager)

    def test_get_ad_ag_area(self):
        result = self.biomethane_budget.get_ad_ag_area()
        self.assertIsNotNone(result)

    def test_get_ad_substitution_area(self):
        result = self.biomethane_budget.get_ad_substitution_area()
        self.assertIsNotNone(result)

    def test_get_ad_ccs_area(self):
        result = self.biomethane_budget.get_ad_ccs_area()
        self.assertIsNotNone(result)

    def test_get_ad_ag_co2_emission(self):
        result = self.biomethane_budget.get_ad_ag_co2_emission()
        self.assertIsNotNone(result)

    def test_get_ad_substitution_co2_emission(self):
        result = self.biomethane_budget.get_ad_substitution_co2_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ccs_co2_emission(self):
        result = self.biomethane_budget.get_ad_ccs_co2_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ag_ch4_emission(self):
        result = self.biomethane_budget.get_ad_ag_ch4_emission()
        self.assertIsNotNone(result)

    def test_get_ad_substitution_ch4_emission(self):
        result = self.biomethane_budget.get_ad_substitution_ch4_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ccs_ch4_emission(self):
        result = self.biomethane_budget.get_ad_ccs_ch4_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ag_n2o_emission(self):
        result = self.biomethane_budget.get_ad_ag_n2o_emission()
        self.assertIsNotNone(result)

    def test_get_ad_substitution_n2o_emission(self):
        result = self.biomethane_budget.get_ad_substitution_n2o_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ccs_n2o_emission(self):
        result = self.biomethane_budget.get_ad_ccs_n2o_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ag_co2e_emission(self):
        result = self.biomethane_budget.get_ad_ag_co2e_emission()
        self.assertIsNotNone(result)

    def test_get_ad_substitution_co2e_emission(self):
        result = self.biomethane_budget.get_ad_substitution_co2e_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ccs_co2e_emission(self):
        result = self.biomethane_budget.get_ad_ccs_co2e_emission()
        self.assertIsNotNone(result)

    def test_get_total_biomethane_area(self):
        result = self.biomethane_budget.get_total_biomethane_area()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()