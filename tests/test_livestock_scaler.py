import unittest
from optigob.resource_manager.database_manager import DatabaseManager
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestLivestockScalerDataManager(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.livestock_scaler_data_manager = OptiGobDataManager(self.data)

    def test_get_livestock_scaler1(self):
        scaler = self.livestock_scaler_data_manager.get_livestock_emission_scaler(
            year=2020, system='Dairy', gas='CO2', scenario=1, abatement='baseline'
        )
        
        self.assertIsNotNone(scaler)

    def test_get_livestock_scaler2(self):
        scaler = self.livestock_scaler_data_manager.get_livestock_emission_scaler(
            year=2020, system='Dairy', gas='CO2', scenario=2, abatement='baseline'
        )
        
        self.assertIsNotNone(scaler)

    def test_get_livestock_scaler3(self):
        scaler = self.livestock_scaler_data_manager.get_livestock_emission_scaler(
            year=2020, system='Dairy', gas='CO2', scenario=3, abatement='baseline'
        )
        
        self.assertIsNotNone(scaler)


    def test_get_livestock_hnv_area_scaler_beef(self):
        scaler = self.livestock_scaler_data_manager.get_livestock_area_scaler(
            year=2020, system='Beef', scenario=1, abatement='baseline'
        )
        self.assertIsNotNone(scaler)

    def test_get_livestock_hnv_area_scaler_dairy_beef(self):
        scaler = self.livestock_scaler_data_manager.get_livestock_area_scaler(
            year=2020, system='Dairy+Beef', scenario=1, abatement='baseline'
        )
        self.assertIsNotNone(scaler)



if __name__ == '__main__':
    unittest.main()
