"""
Logging Examples for Optigob
==============================

This script demonstrates how to use logging in optigob.
It's not a test - it's a practical guide showing different logging configurations.

Run this script to see how different logging settings affect output.
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path so we can import optigob
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR.parent))

from optigob.logger import configure_logging, get_logger
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager


def example_1_default_logging():
    """
    Example 1: Default Logging Configuration

    Shows INFO level and above messages with detailed format.
    This is the recommended setting for normal use.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Default Logging (INFO level, detailed format)")
    print("="*70)

    # Configure with defaults
    configure_logging(level=logging.INFO)

    print("\nRunning scenario with split_gas=False but split_gas_frac=0.3...")
    print("You should see a WARNING about the ignored parameter.\n")

    # This will trigger a warning about split_gas_frac being ignored
    data_manager = OptiGobDataManager({
        'split_gas': False,
        'split_gas_frac': 0.3,  # This will be ignored and warned about
        'AR': 5,
        'target_year': 2050,
        'baseline_year': 2020,
        'abatement_scenario': 1,
        'abatement_type': 1,
        'livestock_ratio_type': 'dairy_per_beef',
        'livestock_ratio_value': 1.5,
        'forest_harvest_intensity': 0.5,
        'afforestation_rate_kha_per_year': 5,
        'broadleaf_fraction': 0.5,
        'organic_soil_fraction': 0.1,
        'beccs_included': False,
        'wetland_restored_frac': 0.1,
        'organic_soil_under_grass_frac': 0.1,
        'biomethane_included': False,
        'protein_crop_included': False,
        'protein_crop_multiplier': 1.0,
        'beccs_willow_area_multiplier': 0,
        'pig_and_poultry_multiplier': 1.0,
        'baseline_dairy_pop': 1500000,
        'baseline_beef_pop': 1000000
    })

    print("\n✓ Example 1 complete. You saw a detailed warning message.\n")


def example_2_quiet_mode():
    """
    Example 2: Quiet Mode (Warnings Only)

    Only shows WARNING level and above.
    Good for batch processing where you only care about problems.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Quiet Mode (WARNING level only)")
    print("="*70)

    # Only show warnings and errors
    configure_logging(level=logging.WARNING)

    print("\nRunning the same scenario...")
    print("You should still see the WARNING (same as Example 1).\n")

    data_manager = OptiGobDataManager({
        'split_gas': False,
        'split_gas_frac': 0.3,
        'AR': 5,
        'target_year': 2050,
        'baseline_year': 2020,
        'abatement_scenario': 1,
        'abatement_type': 1,
        'livestock_ratio_type': 'dairy_per_beef',
        'livestock_ratio_value': 1.5,
        'forest_harvest_intensity': 0.5,
        'afforestation_rate_kha_per_year': 5,
        'broadleaf_fraction': 0.5,
        'organic_soil_fraction': 0.1,
        'beccs_included': False,
        'wetland_restored_frac': 0.1,
        'organic_soil_under_grass_frac': 0.1,
        'biomethane_included': False,
        'protein_crop_included': False,
        'protein_crop_multiplier': 1.0,
        'beccs_willow_area_multiplier': 0,
        'pig_and_poultry_multiplier': 1.0,
        'baseline_dairy_pop': 1500000,
        'baseline_beef_pop': 1000000
    })

    print("\n✓ Example 2 complete. Only warnings shown (INFO messages suppressed).\n")


def example_3_simple_format():
    """
    Example 3: Simple Format (No Timestamps)

    Shows messages without timestamps or module names.
    Good for Jupyter notebooks where you want clean output.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Simple Format (no timestamps)")
    print("="*70)

    # Simple format
    configure_logging(
        level=logging.WARNING,
        format_style="simple"
    )

    print("\nRunning the same scenario...")
    print("You should see the warning, but without timestamp/module name.\n")

    data_manager = OptiGobDataManager({
        'split_gas': False,
        'split_gas_frac': 0.3,
        'AR': 5,
        'target_year': 2050,
        'baseline_year': 2020,
        'abatement_scenario': 1,
        'abatement_type': 1,
        'livestock_ratio_type': 'dairy_per_beef',
        'livestock_ratio_value': 1.5,
        'forest_harvest_intensity': 0.5,
        'afforestation_rate_kha_per_year': 5,
        'broadleaf_fraction': 0.5,
        'organic_soil_fraction': 0.1,
        'beccs_included': False,
        'wetland_restored_frac': 0.1,
        'organic_soil_under_grass_frac': 0.1,
        'biomethane_included': False,
        'protein_crop_included': False,
        'protein_crop_multiplier': 1.0,
        'beccs_willow_area_multiplier': 0,
        'pig_and_poultry_multiplier': 1.0,
        'baseline_dairy_pop': 1500000,
        'baseline_beef_pop': 1000000
    })

    print("\n✓ Example 3 complete. Simple format shown.\n")


def example_4_logging_to_file():
    """
    Example 4: Logging to File

    Saves all log messages to a file in addition to console.
    Good for keeping records of your analyses.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Logging to File")
    print("="*70)

    log_file = SCRIPT_DIR / 'data' / 'logs' / 'example_output.log'

    # Log to both console and file
    configure_logging(
        level=logging.INFO,
        log_to_file=str(log_file)
    )

    print(f"\nLogging to: {log_file}")
    print("Running scenario... Check the log file after.\n")

    data_manager = OptiGobDataManager({
        'split_gas': False,
        'split_gas_frac': 0.3,
        'AR': 5,
        'target_year': 2050,
        'baseline_year': 2020,
        'abatement_scenario': 1,
        'abatement_type': 1,
        'livestock_ratio_type': 'dairy_per_beef',
        'livestock_ratio_value': 1.5,
        'forest_harvest_intensity': 0.5,
        'afforestation_rate_kha_per_year': 5,
        'broadleaf_fraction': 0.5,
        'organic_soil_fraction': 0.1,
        'beccs_included': False,
        'wetland_restored_frac': 0.1,
        'organic_soil_under_grass_frac': 0.1,
        'biomethane_included': False,
        'protein_crop_included': False,
        'protein_crop_multiplier': 1.0,
        'beccs_willow_area_multiplier': 0,
        'pig_and_poultry_multiplier': 1.0,
        'baseline_dairy_pop': 1500000,
        'baseline_beef_pop': 1000000
    })

    print(f"\n✓ Example 4 complete. Check {log_file} for the log output.\n")


def example_5_silent_mode():
    """
    Example 5: Silent Mode

    Turns off all optigob logging.
    Good when you're confident in your inputs and don't want any messages.
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Silent Mode (no logging)")
    print("="*70)

    # Turn off all logging
    logging.getLogger("optigob").setLevel(logging.CRITICAL)

    print("\nRunning the same scenario...")
    print("You should NOT see any warning messages.\n")

    data_manager = OptiGobDataManager({
        'split_gas': False,
        'split_gas_frac': 0.3,  # Normally warns, but we won't see it
        'AR': 5,
        'target_year': 2050,
        'baseline_year': 2020,
        'abatement_scenario': 1,
        'abatement_type': 1,
        'livestock_ratio_type': 'dairy_per_beef',
        'livestock_ratio_value': 1.5,
        'forest_harvest_intensity': 0.5,
        'afforestation_rate_kha_per_year': 5,
        'broadleaf_fraction': 0.5,
        'organic_soil_fraction': 0.1,
        'beccs_included': False,
        'wetland_restored_frac': 0.1,
        'organic_soil_under_grass_frac': 0.1,
        'biomethane_included': False,
        'protein_crop_included': False,
        'protein_crop_multiplier': 1.0,
        'beccs_willow_area_multiplier': 0,
        'pig_and_poultry_multiplier': 1.0,
        'baseline_dairy_pop': 1500000,
        'baseline_beef_pop': 1000000
    })

    print("\n✓ Example 5 complete. No messages shown (silent mode).\n")


def example_6_custom_logger():
    """
    Example 6: Advanced - Using Logger Directly

    Shows how to get a logger and use it in your own code.
    Good for adding logging to your analysis scripts.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Using Logger in Your Own Code")
    print("="*70)

    # Configure logging first
    configure_logging(level=logging.INFO)

    # Get a logger for your script
    my_logger = get_logger("my_analysis")

    print("\nDemonstrating different log levels:\n")

    my_logger.debug("This is a DEBUG message (not shown unless level=DEBUG)")
    my_logger.info("This is an INFO message - general information")
    my_logger.warning("This is a WARNING message - something unexpected")
    my_logger.error("This is an ERROR message - something failed")

    print("\n✓ Example 6 complete. You can use logger in your own scripts.\n")


def main():
    """
    Run all examples to demonstrate logging functionality.
    """
    print("\n" + "#"*70)
    print("OPTIGOB LOGGING EXAMPLES")
    print("#"*70)
    print("\nThese examples demonstrate different logging configurations.")
    print("Each example shows a different use case for logging in optigob.")
    print("\nFor detailed explanation, see: tests/data/logs/LOGGING_GUIDE.md")

    # Run each example
    try:
        example_1_default_logging()
        input("Press Enter to continue to Example 2...")

        example_2_quiet_mode()
        input("Press Enter to continue to Example 3...")

        example_3_simple_format()
        input("Press Enter to continue to Example 4...")

        example_4_logging_to_file()
        input("Press Enter to continue to Example 5...")

        example_5_silent_mode()
        input("Press Enter to continue to Example 6...")

        example_6_custom_logger()

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")

    print("\n" + "#"*70)
    print("ALL EXAMPLES COMPLETE")
    print("#"*70)
    print("\nKey Takeaways:")
    print("1. Use configure_logging() at the start of your script")
    print("2. Choose your level: INFO (default), WARNING (quiet), DEBUG (verbose)")
    print("3. Save to file with log_to_file parameter")
    print("4. Use simple format for Jupyter notebooks")
    print("5. You have full control over what you see!")
    print("\nFor more details, see: tests/data/logs/LOGGING_GUIDE.md")
    print("#"*70 + "\n")


if __name__ == '__main__':
    main()
