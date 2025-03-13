import unittest
from optigob.resource_manager.database_manager import DatabaseManager
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.data_manager = DatabaseManager()

    def test_get_livestock_scalers(self):
        livestock_scalers = self.data_manager.get_livestock_scalers()
        print(livestock_scalers)
        self.assertIsNotNone(livestock_scalers)

    def test_get_livestock_scalers_external_db(self):
        external_db_path = './data/test_db.db'
        data_manager = DatabaseManager(database_path=external_db_path)
        livestock_scalers = data_manager.get_livestock_scalers()
        print(livestock_scalers)
        self.assertIsNotNone(livestock_scalers)

class TestLivestockScalerDataManager(unittest.TestCase):
    def setUp(self):
        self.livestock_scaler_data_manager = OptiGobDataManager()

    def test_get_livestock_scaler(self):
        scaler = self.livestock_scaler_data_manager.get_livestock_scaler(
            year=2020, system='Dairy', gas='CO2', scenario=1
        )
        
        self.assertIsNotNone(scaler)

if __name__ == '__main__':
    unittest.main()
