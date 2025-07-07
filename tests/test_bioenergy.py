import unittest
from optigob.bioenergy.bioenergy_budget import BioEnergyBudget
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestBioEnergyBudget(unittest.TestCase):

    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.bio_energy_budget = BioEnergyBudget(self.data_manager)

    def test_get_ad_ag_area(self):
        result = self.bio_energy_budget.get_ad_ag_area()
        self.assertIsNotNone(result)

    def test_get_ad_ag_co2_emission(self):
        result = self.bio_energy_budget.get_ad_ag_co2_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ccs_co2_emission(self):
        result = self.bio_energy_budget.get_ad_ccs_co2_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ag_ch4_emission(self):
        result = self.bio_energy_budget.get_ad_ag_ch4_emission()
        self.assertIsNotNone(result)


    def test_get_ad_ccs_ch4_emission(self):
        result = self.bio_energy_budget.get_ad_ccs_ch4_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ag_n2o_emission(self):
        result = self.bio_energy_budget.get_ad_ag_n2o_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ccs_n2o_emission(self):
        result = self.bio_energy_budget.get_ad_ccs_n2o_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ag_co2e_emission(self):
        result = self.bio_energy_budget.get_ad_ag_co2e_emission()
        self.assertIsNotNone(result)

    def test_get_ad_ccs_co2e_emission(self):
        result = self.bio_energy_budget.get_ad_ccs_co2e_emission()
        self.assertIsNotNone(result)

    def test_get_total_biomethane_area(self):
        result = self.bio_energy_budget.get_total_biomethane_area()
        self.assertIsNotNone(result)

    def test_get_total_willow_area(self):
        result = self.bio_energy_budget.get_total_willow_area()
        self.assertIsNotNone(result)

    def test_get_willow_bioenergy_hnv_area(self):
        result = self.bio_energy_budget.get_willow_bioenergy_hnv_area()
        self.assertIsNotNone(result)

    def test_get_ad_bioenergy_output(self):
        result = self.bio_energy_budget.get_ad_bioenergy_output()
        self.assertIsNotNone(result)

    def test_get_willow_bioenergy_output(self):
        result = self.bio_energy_budget.get_willow_bioenergy_output()
        self.assertIsNotNone(result)

    def test_get_willow_beccs_co2_emission(self):
        result = self.bio_energy_budget.get_willow_beccs_co2_emission()
        self.assertIsNotNone(result)

    def test_get_total_ccs_co2_emission(self):
        result = self.bio_energy_budget.get_total_ccs_co2_emission()
        self.assertIsNotNone(result)

    def test_get_total_ccs_co2e_emission(self):
        result = self.bio_energy_budget.get_total_ccs_co2e_emission()
        self.assertIsNotNone(result)

    def test_get_total_ccs_ch4_emission(self):
        result = self.bio_energy_budget.get_total_ccs_ch4_emission()
        self.assertIsNotNone(result)

    def test_get_total_ccs_n2o_emission(self):
        result = self.bio_energy_budget.get_total_ccs_n2o_emission()
        self.assertIsNotNone(result)

    def test_get_biomethane_co2e_total(self):
        result = self.bio_energy_budget.get_biomethane_co2e_total()
        self.assertIsNotNone(result)

    def test_get_biomethane_co2_total(self):
        result = self.bio_energy_budget.get_biomethane_co2_total()
        self.assertIsNotNone(result)

    def test_get_biomethane_ch4_total(self):
        result = self.bio_energy_budget.get_biomethane_ch4_total()
        self.assertIsNotNone(result)

    def test_get_biomethane_n2o_total(self):
        result = self.bio_energy_budget.get_biomethane_n2o_total()
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()