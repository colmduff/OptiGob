import unittest
from unittest.mock import MagicMock
from optigob.protein_crops.protein_crops_budget import ProteinCropsBudget

class TestProteinCropsBudget(unittest.TestCase):
    def setUp(self):
        # Mock the data manager
        self.mock_data_manager = MagicMock()
        self.mock_data_manager.get_target_year.return_value = 2030
        self.mock_data_manager.get_abatement_type.return_value = 'baseline'
        self.mock_data_manager.get_protein_crop_multiplier.return_value = 1.0

        # Mock return values for emissions and protein yield
        mock_area_df = MagicMock()
        mock_area_df.__getitem__.return_value.item.return_value = 100.0
        self.mock_data_manager.get_protein_crop_emission_scaler.return_value = mock_area_df
        self.mock_data_manager.get_protein_crop_protein_scaler.return_value = mock_area_df

        self.budget = ProteinCropsBudget(self.mock_data_manager)

    def test_get_crop_area(self):
        result = self.budget.get_crop_area()
        self.assertIsInstance(result, float)

    def test_get_crop_emission_ch4(self):
        result = self.budget.get_crop_emission_ch4()
        self.assertIsInstance(result, float)

    def test_get_crop_emission_n2o(self):
        result = self.budget.get_crop_emission_n2o()
        self.assertIsInstance(result, float)

    def test_get_crop_emission_co2(self):
        result = self.budget.get_crop_emission_co2()
        self.assertIsInstance(result, float)

    def test_get_crop_emission_co2e(self):
        result = self.budget.get_crop_emission_co2e()
        self.assertIsInstance(result, float)

    def test_get_crop_protein_yield(self):
        result = self.budget.get_crop_protein_yield()
        self.assertIsInstance(result, float)

    def test_methods_return_zero_if_not_included(self):
        self.budget.protein_crop_included = False
        self.assertEqual(self.budget.get_crop_area(), 0)
        self.assertEqual(self.budget.get_crop_emission_ch4(), 0)
        self.assertEqual(self.budget.get_crop_emission_n2o(), 0)
        self.assertEqual(self.budget.get_crop_emission_co2(), 0)
        self.assertEqual(self.budget.get_crop_emission_co2e(), 0)
        self.assertEqual(self.budget.get_crop_protein_yield(), 0)

    def test_methods_return_float_if_included(self):
        self.budget.protein_crop_included = True
        self.assertIsInstance(self.budget.get_crop_area(), float)
        self.assertIsInstance(self.budget.get_crop_emission_ch4(), float)
        self.assertIsInstance(self.budget.get_crop_emission_n2o(), float)
        self.assertIsInstance(self.budget.get_crop_emission_co2(), float)
        self.assertIsInstance(self.budget.get_crop_emission_co2e(), float)
        self.assertIsInstance(self.budget.get_crop_protein_yield(), float)

if __name__ == '__main__':
    unittest.main()
