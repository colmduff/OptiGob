import unittest
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
from optigob.optigob import Optigob

class TestOptigob(unittest.TestCase):
    def setUp(self):
        self.data = './data/sip.json'
        self.data_manager =OptiGobDataManager(self.data)


    def test_optigob_functionality(self):
        result = Optigob(self.data_manager)

        print(result.get_baseline_beef_population())
        print(result.get_baseline_dairy_population())
      
        self.assertIsNotNone(result.get_baseline_beef_population())
        self.assertIsNotNone(result.get_baseline_dairy_population())





if __name__ == '__main__':
    unittest.main()
