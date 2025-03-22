import unittest
from optigob.resource_manager.database_manager import DatabaseManager
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.data_manager = DatabaseManager()

    def test_get_livestock_scalers(self):
        livestock_scalers = self.data_manager.get_livestock_emission_scaler_table()
        print(livestock_scalers)
        self.assertIsNotNone(livestock_scalers)

    def test_get_livestock_scalers_external_db(self):
        external_db_path = './data/test_db.db'
        data_manager = DatabaseManager(database_path=external_db_path)
        livestock_scalers = data_manager.get_livestock_emission_scaler_table()
        print(livestock_scalers)
        self.assertIsNotNone(livestock_scalers)

    def test_get_forest_scalers(self):
        forest_scalers = self.data_manager.get_forest_scaler_table()
        print(forest_scalers)
        self.assertIsNotNone(forest_scalers)

    def test_get_static_forest_scalers(self):
        static_forest_scalers = self.data_manager.get_static_forest_scaler_table()
        print(static_forest_scalers)
        self.assertIsNotNone(static_forest_scalers)

    def test_get_ccs_scalers(self):
        ccs_scalers = self.data_manager.get_ccs_scaler_table()
        print(ccs_scalers)
        self.assertIsNotNone(ccs_scalers)

    def test_get_hwp_scalers(self):
        hwp_scalers = self.data_manager.get_hwp_scaler_table()
        print(hwp_scalers)
        self.assertIsNotNone(hwp_scalers)

    def test_get_substitution_scalers(self):
        substitution_scalers = self.data_manager.get_substitution_scaler_table()
        print(substitution_scalers)
        self.assertIsNotNone(substitution_scalers)

class TestLivestockScalerDataManager(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.livestock_scaler_data_manager = OptiGobDataManager(self.data)

    def test_get_livestock_scaler(self):
        scaler = self.livestock_scaler_data_manager.get_livestock_emission_scaler(
            year=2020, system='Dairy', gas='CO2', scenario=1, abatement='baseline'
        )
        
        self.assertIsNotNone(scaler)

class TestForestScalerDataManager(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager = OptiGobDataManager(self.data)

    def test_get_forest_scalers(self):
        forest_scalers = self.data_manager.get_forest_scaler(
            target_year=2050,
            affor_rate=2,
            broadleaf_frac=0.5,
            organic_soil_frac=0.15,
            harvest="high"
        )
        print(forest_scalers)
        self.assertIsNotNone(forest_scalers)

    def test_get_static_forest_scalers(self):
        static_forest_scalers = self.data_manager.get_static_forest_scaler(
            target_year=2050,
            harvest="high"
        )
        print(static_forest_scalers)
        self.assertIsNotNone(static_forest_scalers)

    def test_get_ccs_scalers(self):
        ccs_scalers = self.data_manager.get_ccs_scaler(
            target_year=2050,
            affor_rate=2,
            broadleaf_frac=0.5,
            organic_soil_frac=0.15,
            harvest="high"
        )
        print(ccs_scalers)
        self.assertIsNotNone(ccs_scalers)

    def test_get_hwp_scalers(self):
        hwp_scalers = self.data_manager.get_hwp_scaler(
            target_year=2050,
            affor_rate=2,
            broadleaf_frac=0.5,
            organic_soil_frac=0.15,
            harvest="high"
        )
        print(hwp_scalers)
        self.assertIsNotNone(hwp_scalers)

    def test_get_substitution_scalers(self):
        substitution_scalers = self.data_manager.get_substitution_scaler(
            target_year=2050,
            affor_rate=2,
            broadleaf_frac=0.5,
            organic_soil_frac=0.15,
            harvest="high"
        )
        print(substitution_scalers)
        self.assertIsNotNone(substitution_scalers)

    def test_get_ad_area_scalers(self):
        ad_scalers = self.data_manager.get_ad_area_scaler(
            target_year=2050
        )
        print(ad_scalers)
        self.assertIsNotNone(ad_scalers)

    def test_get_ad_emission_scalers(self):
        ad_emission_scalers = self.data_manager.get_ad_emission_scaler(
            target_year=2050
        )
        print(ad_emission_scalers)
        self.assertIsNotNone(ad_emission_scalers)

    def test_get_organic_soil_emission_scalers(self):
        organic_soil_emission_scalers = self.data_manager.get_organic_soil_emission_scaler(
            target_year=2050,
            wetland_restored_frac=0.5,
            organic_soil_under_grass_frac=0

        )
        print(organic_soil_emission_scalers)
        self.assertIsNotNone(organic_soil_emission_scalers)

    def test_get_crop_emission_scalers(self):
        crop_emission_scalers = self.data_manager.get_crop_scaler(
            year=2050,gas='CO2', abatement='baseline'

        )
        print(crop_emission_scalers)
        self.assertIsNotNone(crop_emission_scalers)


if __name__ == '__main__':
    unittest.main()
