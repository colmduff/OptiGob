import unittest
from optigob.substitution.substitution import Substitution
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestSubstitution(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)
        self.substitution = Substitution(self.data_manager)
        # Set required attributes for forest methods if not set by data_manager
        self.substitution.target_year = getattr(self.data_manager, 'get_target_year', lambda: 2050)()
        self.substitution.afforestation_rate = getattr(self.data_manager, 'get_afforestation_rate_kha_per_year', lambda: 2)()
        self.substitution.broadleaf_fraction = getattr(self.data_manager, 'get_broadleaf_fraction', lambda: 0.5)()
        self.substitution.organic_soil_fraction = getattr(self.data_manager, 'get_organic_soil_fraction_forest', lambda: 0.15)()
        self.substitution.harvest_rate = getattr(self.data_manager, 'get_forest_harvest_intensity', lambda: 'high')()

    def test_get_ad_substitution_co2_emission(self):
        try:
            result = self.substitution.get_ad_substitution_co2_emission()
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Exception raised: {e}")

    def test_get_ad_substitution_ch4_emission(self):
        try:
            result = self.substitution.get_ad_substitution_ch4_emission()
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Exception raised: {e}")

    def test_get_ad_substitution_n2o_emission(self):
        try:
            result = self.substitution.get_ad_substitution_n2o_emission()
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Exception raised: {e}")

    def test_get_ad_substitution_co2e_emission(self):
        try:
            result = self.substitution.get_ad_substitution_co2e_emission()
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Exception raised: {e}")

    def test_get_forest_substitution_offset_co2e(self):
        try:
            result = self.substitution.get_forest_substitution_offset_co2e()
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Exception raised: {e}")

    def test_get_willow_substitution_offset_co2e(self):
        try:
            result = self.substitution.get_willow_substitution_offset_co2e()
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Exception raised: {e}")

if __name__ == '__main__':
    unittest.main()
