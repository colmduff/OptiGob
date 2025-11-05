"""
test_input_validation.py
========================

This test module verifies the input parameter validation functionality in OptiGobDataManager.

It tests validation for three parameter groups:
1. Forest parameters (afforestation_rate, broadleaf_fraction, organic_soil_fraction, forest_harvest_intensity)
2. Organic soil parameters (wetland_restored_frac, organic_soil_under_grass_frac)
3. Abatement/productivity parameters (abatement_type, abatement_scenario)

The validation ensures that only parameter combinations present in the database are accepted.
"""

from pathlib import Path
import pytest
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
from optigob.input_helper import InputHelper
from optigob.logger import configure_logging
import logging

if not Path('./logs').exists():
    Path('./logs').mkdir(parents=True, exist_ok=True)
    
LOGPATH = str(Path('.') / 'logs' / 'input_validation.log')

# Log to both console and file
configure_logging(
    level=logging.INFO,
    log_to_file=str(LOGPATH)
)

class TestForestParameterValidation:
    """Test validation of forest parameter combinations."""

    def get_base_params(self):
        """Return minimal valid parameters for testing."""
        return {
            'AR': 5,
            'split_gas': False,
            'target_year': 2030,
            'abatement_type': 'frontier',
            'abatement_scenario': 9,
            'livestock_ratio_type': 'dairy_per_beef',
            'livestock_ratio_value': 10,
            'baseline_year': 2020,
            'baseline_dairy_pop': 156.8,
            'baseline_beef_pop': 98.4,
        }

    def test_valid_forest_combination(self):
        """Test that a valid forest combination is accepted."""
        params = self.get_base_params()
        params.update({
            'afforestation_rate_kha_per_year': 16.0,
            'broadleaf_fraction': 0.3,
            'organic_soil_fraction': 0.0,
            'forest_harvest_intensity': 'low'
        })
        # Should not raise
        data_manager = OptiGobDataManager(params)
        assert data_manager is not None

    def test_invalid_forest_combination_wrong_organic_soil_frac(self):
        """Test that an invalid forest combination (wrong organic_soil_fraction) is rejected."""
        params = self.get_base_params()
        params.update({
            'afforestation_rate_kha_per_year': 16.0,
            'broadleaf_fraction': 0.3,
            'organic_soil_fraction': 0.5,  # Invalid - not in database
            'forest_harvest_intensity': 'low'
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Forest Parameter Combination" in str(exc_info.value)
        assert "organic_soil_fraction: 0.5" in str(exc_info.value)

    def test_invalid_forest_combination_wrong_broadleaf(self):
        """Test that an invalid forest combination (wrong broadleaf_fraction) is rejected."""
        params = self.get_base_params()
        params.update({
            'afforestation_rate_kha_per_year': 8.0,
            'broadleaf_fraction': 0.7,  # Invalid - not in database
            'organic_soil_fraction': 0.15,
            'forest_harvest_intensity': 'high'
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Forest Parameter Combination" in str(exc_info.value)
        assert "broadleaf_fraction: 0.7" in str(exc_info.value)

    def test_invalid_forest_combination_wrong_harvest(self):
        """Test that an invalid forest combination (wrong harvest intensity) is rejected."""
        params = self.get_base_params()
        params.update({
            'afforestation_rate_kha_per_year': 16.0,
            'broadleaf_fraction': 0.5,
            'organic_soil_fraction': 0.15,
            'forest_harvest_intensity': 'high'  # Invalid combo with these other params
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Forest Parameter Combination" in str(exc_info.value)

    def test_partial_forest_params_no_validation(self):
        """Test that partial forest parameters don't trigger validation."""
        params = self.get_base_params()
        params.update({
            'afforestation_rate_kha_per_year': 16.0,
            'broadleaf_fraction': 0.3,
            # Missing organic_soil_fraction and forest_harvest_intensity
        })
        # Should not raise - validation only occurs when all 4 params are provided
        data_manager = OptiGobDataManager(params)
        assert data_manager is not None

    def test_all_valid_forest_combinations(self):
        """Test all valid forest combinations from InputHelper."""
        helper = InputHelper()
        forest_combos = helper.filter_combos(input_type='forest')

        # Test first 3 combinations (to keep test fast)
        for i in range(min(3, len(forest_combos))):
            combo = forest_combos.iloc[i]
            params = self.get_base_params()
            params.update({
                'afforestation_rate_kha_per_year': combo['affor_rate_kha-yr'],
                'broadleaf_fraction': combo['broadleaf_frac'],
                'organic_soil_fraction': combo['organic_soil_frac'],
                'forest_harvest_intensity': combo['forest_harvest_intensity']
            })
            # Should not raise
            data_manager = OptiGobDataManager(params)
            assert data_manager is not None


class TestOrganicSoilParameterValidation:
    """Test validation of organic soil parameter combinations."""

    def get_base_params(self):
        """Return minimal valid parameters for testing."""
        return {
            'AR': 5,
            'split_gas': False,
            'target_year': 2030,
            'abatement_type': 'frontier',
            'abatement_scenario': 9,
            'livestock_ratio_type': 'dairy_per_beef',
            'livestock_ratio_value': 10,
            'baseline_year': 2020,
            'baseline_dairy_pop': 156.8,
            'baseline_beef_pop': 98.4,
        }

    def test_valid_organic_soil_combination_1(self):
        """Test valid organic soil combination (0.5, 0.0)."""
        params = self.get_base_params()
        params.update({
            'wetland_restored_frac': 0.5,
            'organic_soil_under_grass_frac': 0.0
        })
        # Should not raise
        data_manager = OptiGobDataManager(params)
        assert data_manager is not None

    def test_valid_organic_soil_combination_2(self):
        """Test valid organic soil combination (0.9, 0.5)."""
        params = self.get_base_params()
        params.update({
            'wetland_restored_frac': 0.9,
            'organic_soil_under_grass_frac': 0.5
        })
        # Should not raise
        data_manager = OptiGobDataManager(params)
        assert data_manager is not None

    def test_valid_organic_soil_combination_3(self):
        """Test valid organic soil combination (0.9, 0.9)."""
        params = self.get_base_params()
        params.update({
            'wetland_restored_frac': 0.9,
            'organic_soil_under_grass_frac': 0.9
        })
        # Should not raise
        data_manager = OptiGobDataManager(params)
        assert data_manager is not None

    def test_invalid_organic_soil_combination(self):
        """Test that an invalid organic soil combination is rejected."""
        params = self.get_base_params()
        params.update({
            'wetland_restored_frac': 0.5,
            'organic_soil_under_grass_frac': 0.5  # Invalid - (0.5, 0.5) not in database
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Organic Soil Parameter Combination" in str(exc_info.value)
        assert "wetland_restored_frac: 0.5" in str(exc_info.value)
        assert "organic_soil_under_grass_frac: 0.5" in str(exc_info.value)

    def test_invalid_organic_soil_combination_wrong_values(self):
        """Test that invalid values are rejected."""
        params = self.get_base_params()
        params.update({
            'wetland_restored_frac': 0.7,
            'organic_soil_under_grass_frac': 0.3
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Organic Soil Parameter Combination" in str(exc_info.value)

    def test_partial_organic_soil_params_no_validation(self):
        """Test that partial organic soil parameters don't trigger validation."""
        params = self.get_base_params()
        params.update({
            'wetland_restored_frac': 0.5,
            # Missing organic_soil_under_grass_frac
        })
        # Should not raise - validation only occurs when both params are provided
        data_manager = OptiGobDataManager(params)
        assert data_manager is not None

    def test_all_valid_organic_soil_combinations(self):
        """Test all valid organic soil combinations from InputHelper."""
        helper = InputHelper()
        organic_combos = helper.filter_combos(input_type='organic_soil')

        # Test all combinations (only 3 total)
        for i in range(len(organic_combos)):
            combo = organic_combos.iloc[i]
            params = self.get_base_params()
            params.update({
                'wetland_restored_frac': combo['wetland_restored_frac'],
                'organic_soil_under_grass_frac': combo['organic_soil_under_grass_frac']
            })
            # Should not raise
            data_manager = OptiGobDataManager(params)
            assert data_manager is not None


class TestAbatementProductivityParameterValidation:
    """Test validation of abatement and productivity parameter combinations."""

    def get_base_params(self):
        """Return minimal valid parameters for testing."""
        return {
            'AR': 5,
            'split_gas': False,
            'target_year': 2030,
            'livestock_ratio_type': 'dairy_per_beef',
            'livestock_ratio_value': 10,
            'baseline_year': 2020,
            'baseline_dairy_pop': 156.8,
            'baseline_beef_pop': 98.4,
        }

    def test_valid_baseline_scenarios(self):
        """Test valid baseline scenarios (1, 2, 3)."""
        for scenario in [1, 2, 3]:
            params = self.get_base_params()
            params.update({
                'abatement_type': 'baseline',
                'abatement_scenario': scenario
            })
            # Should not raise
            data_manager = OptiGobDataManager(params)
            assert data_manager is not None

    def test_valid_macc_scenarios(self):
        """Test valid macc scenarios (4, 5, 6)."""
        for scenario in [4, 5, 6]:
            params = self.get_base_params()
            params.update({
                'abatement_type': 'macc',
                'abatement_scenario': scenario
            })
            # Should not raise
            data_manager = OptiGobDataManager(params)
            assert data_manager is not None

    def test_valid_frontier_scenarios(self):
        """Test valid frontier scenarios (7, 8, 9)."""
        for scenario in [7, 8, 9]:
            params = self.get_base_params()
            params.update({
                'abatement_type': 'frontier',
                'abatement_scenario': scenario
            })
            # Should not raise
            data_manager = OptiGobDataManager(params)
            assert data_manager is not None

    def test_invalid_baseline_with_wrong_scenario(self):
        """Test that baseline with scenario 7 is rejected."""
        params = self.get_base_params()
        params.update({
            'abatement_type': 'baseline',
            'abatement_scenario': 7  # Invalid - should be 1, 2, or 3
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Abatement/Productivity Parameter Combination" in str(exc_info.value)
        assert "abatement_type: baseline" in str(exc_info.value)
        assert "abatement_scenario: 7" in str(exc_info.value)

    def test_invalid_frontier_with_wrong_scenario(self):
        """Test that frontier with scenario 1 is rejected."""
        params = self.get_base_params()
        params.update({
            'abatement_type': 'frontier',
            'abatement_scenario': 1  # Invalid - should be 7, 8, or 9
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Abatement/Productivity Parameter Combination" in str(exc_info.value)
        assert "abatement_type: frontier" in str(exc_info.value)
        assert "abatement_scenario: 1" in str(exc_info.value)

    def test_invalid_abatement_type(self):
        """Test that an invalid abatement type is rejected."""
        params = self.get_base_params()
        params.update({
            'abatement_type': 'super_advanced',  # Invalid type
            'abatement_scenario': 5
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Abatement/Productivity Parameter Combination" in str(exc_info.value)

    def test_partial_abatement_params_no_validation(self):
        """Test that partial abatement parameters don't trigger validation."""
        params = self.get_base_params()
        params.update({
            'abatement_type': 'frontier',
            # Missing abatement_scenario
        })
        # Should not raise - validation only occurs when both params are provided
        data_manager = OptiGobDataManager(params)
        assert data_manager is not None

    def test_all_valid_abatement_combinations(self):
        """Test all valid abatement/productivity combinations from InputHelper."""
        helper = InputHelper()
        abatement_combos = helper.filter_combos(input_type='abatement_and_productivity')

        # Test all combinations (9 total)
        for i in range(len(abatement_combos)):
            combo = abatement_combos.iloc[i]
            params = self.get_base_params()
            params.update({
                'abatement_type': combo['abatement'],
                'abatement_scenario': int(combo['scenario'])
            })
            # Should not raise
            data_manager = OptiGobDataManager(params)
            assert data_manager is not None


class TestCombinedParameterValidation:
    """Test validation with multiple parameter groups combined."""

    def get_base_params(self):
        """Return minimal valid parameters for testing."""
        return {
            'AR': 5,
            'split_gas': False,
            'target_year': 2030,
            'livestock_ratio_type': 'dairy_per_beef',
            'livestock_ratio_value': 10,
            'baseline_year': 2020,
            'baseline_dairy_pop': 156.8,
            'baseline_beef_pop': 98.4,
        }

    def test_all_valid_combinations_together(self):
        """Test valid combinations from all three parameter groups together."""
        params = self.get_base_params()
        params.update({
            # Valid forest params
            'afforestation_rate_kha_per_year': 8.0,
            'broadleaf_fraction': 0.5,
            'organic_soil_fraction': 0.15,
            'forest_harvest_intensity': 'high',
            # Valid organic soil params
            'wetland_restored_frac': 0.9,
            'organic_soil_under_grass_frac': 0.5,
            # Valid abatement params
            'abatement_type': 'frontier',
            'abatement_scenario': 9
        })
        # Should not raise
        data_manager = OptiGobDataManager(params)
        assert data_manager is not None

    def test_invalid_forest_valid_others(self):
        """Test that invalid forest params fail even with valid other params."""
        params = self.get_base_params()
        params.update({
            # Invalid forest params
            'afforestation_rate_kha_per_year': 8.0,
            'broadleaf_fraction': 0.9,  # Invalid
            'organic_soil_fraction': 0.15,
            'forest_harvest_intensity': 'high',
            # Valid organic soil params
            'wetland_restored_frac': 0.9,
            'organic_soil_under_grass_frac': 0.5,
            # Valid abatement params
            'abatement_type': 'frontier',
            'abatement_scenario': 9
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Forest Parameter Combination" in str(exc_info.value)

    def test_valid_forest_invalid_organic_soil(self):
        """Test that invalid organic soil params fail even with valid other params."""
        params = self.get_base_params()
        params.update({
            # Valid forest params
            'afforestation_rate_kha_per_year': 8.0,
            'broadleaf_fraction': 0.5,
            'organic_soil_fraction': 0.15,
            'forest_harvest_intensity': 'high',
            # Invalid organic soil params
            'wetland_restored_frac': 0.7,  # Invalid combination
            'organic_soil_under_grass_frac': 0.3,
            # Valid abatement params
            'abatement_type': 'frontier',
            'abatement_scenario': 9
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Organic Soil Parameter Combination" in str(exc_info.value)

    def test_valid_forest_organic_soil_invalid_abatement(self):
        """Test that invalid abatement params fail even with valid other params."""
        params = self.get_base_params()
        params.update({
            # Valid forest params
            'afforestation_rate_kha_per_year': 8.0,
            'broadleaf_fraction': 0.5,
            'organic_soil_fraction': 0.15,
            'forest_harvest_intensity': 'high',
            # Valid organic soil params
            'wetland_restored_frac': 0.9,
            'organic_soil_under_grass_frac': 0.5,
            # Invalid abatement params
            'abatement_type': 'baseline',
            'abatement_scenario': 9  # Invalid - should be 1, 2, or 3 for baseline
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        assert "Invalid Abatement/Productivity Parameter Combination" in str(exc_info.value)


class TestValidationErrorMessages:
    """Test that validation error messages contain helpful information."""

    def get_base_params(self):
        """Return minimal valid parameters for testing."""
        return {
            'AR': 5,
            'split_gas': False,
            'target_year': 2030,
            'livestock_ratio_type': 'dairy_per_beef',
            'livestock_ratio_value': 10,
            'baseline_year': 2020,
            'baseline_dairy_pop': 156.8,
            'baseline_beef_pop': 98.4,
        }

    def test_forest_error_message_contains_inputhelper_guidance(self):
        """Test that forest validation errors mention InputHelper."""
        params = self.get_base_params()
        params.update({
            'afforestation_rate_kha_per_year': 16.0,
            'broadleaf_fraction': 0.3,
            'organic_soil_fraction': 0.99,  # Invalid
            'forest_harvest_intensity': 'low'
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        error_message = str(exc_info.value)
        assert "InputHelper" in error_message
        assert "filter_combos(input_type='forest')" in error_message

    def test_organic_soil_error_message_contains_inputhelper_guidance(self):
        """Test that organic soil validation errors mention InputHelper."""
        params = self.get_base_params()
        params.update({
            'wetland_restored_frac': 0.1,  # Invalid
            'organic_soil_under_grass_frac': 0.1
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        error_message = str(exc_info.value)
        assert "InputHelper" in error_message
        assert "filter_combos(input_type='organic_soil')" in error_message

    def test_abatement_error_message_contains_valid_combos(self):
        """Test that abatement validation errors list valid combinations."""
        params = self.get_base_params()
        params.update({
            'abatement_type': 'baseline',
            'abatement_scenario': 99  # Invalid
        })
        with pytest.raises(ValueError) as exc_info:
            OptiGobDataManager(params)
        error_message = str(exc_info.value)
        assert "baseline: scenarios 1, 2, 3" in error_message
        assert "macc: scenarios 4, 5, 6" in error_message
        assert "frontier: scenarios 7, 8, 9" in error_message


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v'])
