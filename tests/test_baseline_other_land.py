import unittest
from unittest.mock import MagicMock
from optigob.other_land.baseline_other_land import BaselineOtherLand

class TestBaselineOtherLand(unittest.TestCase):
    def setUp(self):
        self.mock_data_manager = MagicMock()
        self.mock_data_manager.get_baseline_year.return_value = 2020
        self.mock_data_manager.get_wetland_restored_fraction.return_value = 0.5
        self.mock_data_manager.get_organic_soil_under_grass_fraction.return_value = 0.3

        # Mock DataFrame with proper filtering chain for emission methods
        mock_df = MagicMock()
        # Setup for the filtering chain: df[df["ghg"] == "something"]["emission_value"].item()
        mock_filtered_df = MagicMock()
        mock_series = MagicMock()
        mock_series.item.return_value = 42.0
        mock_filtered_df.__getitem__.return_value = mock_series
        mock_df.__getitem__.return_value = mock_filtered_df
        
        # For direct access: df["column"].item()
        mock_df.__getitem__.return_value.item.return_value = 42.0
        
        self.mock_data_manager.get_organic_soil_emission_scaler.return_value = mock_df
        self.mock_data_manager.get_organic_soil_area_scaler.return_value = mock_df

        self.baseline_other_land = BaselineOtherLand(self.mock_data_manager)

    def test_get_wetland_restoration_emission_co2e(self):
        self.assertIsInstance(self.baseline_other_land.get_wetland_restoration_emission_co2e(), float)

    def test_get_wetland_restoration_emission_ch4(self):
        self.assertIsInstance(self.baseline_other_land.get_wetland_restoration_emission_ch4(), float)

    def test_get_wetland_restoration_emission_n2o(self):
        self.assertIsInstance(self.baseline_other_land.get_wetland_restoration_emission_n2o(), float)

    def test_get_wetland_restoration_emission_co2(self):
        self.assertIsInstance(self.baseline_other_land.get_wetland_restoration_emission_co2(), float)

    def test_get_drained_organic_soil_area(self):
        self.assertIsInstance(self.baseline_other_land.get_drained_organic_soil_area(), float)

    def test_get_rewetted_organic_area(self):
        self.assertIsInstance(self.baseline_other_land.get_rewetted_organic_area(), float)

    def test_get_drained_wetland_area(self):
        self.assertIsInstance(self.baseline_other_land.get_drained_wetland_area(), float)

    def test_get_rewetted_wetland_area(self):
        self.assertIsInstance(self.baseline_other_land.get_rewetted_wetland_area(), float)

    def test_get_near_natural_wetland_area(self):
        self.assertIsInstance(self.baseline_other_land.get_near_natural_wetland_area(), float)

    def test_get_total_other_land_area(self):
        self.assertIsInstance(self.baseline_other_land.get_total_other_land_area(), float)

    def test_get_rewetted_organic_hnv_area(self):
        self.assertIsInstance(self.baseline_other_land.get_rewetted_organic_hnv_area(), float)

    def test_get_rewetted_wetland_hnv_area(self):
        self.assertIsInstance(self.baseline_other_land.get_rewetted_wetland_hnv_area(), float)

    def test_get_near_natural_wetland_hnv_area(self):
        self.assertIsInstance(self.baseline_other_land.get_near_natural_wetland_hnv_area(), float)

    def test_get_total_other_land_hnv_area(self):
        self.assertIsInstance(self.baseline_other_land.get_total_other_land_hnv_area(), float)

if __name__ == '__main__':
    unittest.main()
