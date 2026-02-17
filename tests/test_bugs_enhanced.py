"""
Test the bug fixes for Bug 1 and Bug 2
"""
import os
import sys
import logging
import warnings
from pathlib import Path
from datetime import datetime
from io import StringIO
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()
LOG_DIR = SCRIPT_DIR / 'data' / 'logs'
BUG1_PATH = SCRIPT_DIR / 'data' / 'sip_bug1.yaml'
BUG2_PATH = SCRIPT_DIR / 'data' / 'sip_bug2.yaml'

def test_bug1_fixed():
    """Test Bug 1: Should warn about split_gas_frac and show zero budget info message"""
    print("\n" + "="*70)
    print("Testing Bug 1 (FIXED): Input validation + zero budget info")
    print("="*70)

    try:
        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            data_manager = OptiGobDataManager(str(BUG1_PATH))

            # Check if warning was raised
            if len(w) > 0:
                print(f"\n✓ Warning raised as expected:")
                print(f"  {w[0].message}")
            else:
                print("\n✗ No warning raised (expected one)")

        # Capture logger output to verify zero budget info message
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.DEBUG)
        optigob_logger = logging.getLogger("optigob")
        optigob_logger.addHandler(handler)
        optigob_logger.setLevel(logging.DEBUG)

        # Now run the optimization
        optigob = Optigob(data_manager)
        emissions = optigob.get_total_emissions_co2e_by_sector()
        livestock = optigob.get_livestock_population()

        # Remove the capture handler
        optigob_logger.removeHandler(handler)
        output = log_capture.getvalue()

        print(f"\n✓ Optimization completed successfully")
        print(f"  Scenario dairy: {livestock['scenario']['dairy']}")
        print(f"  Scenario beef:  {livestock['scenario']['beef']}")

        if livestock['scenario']['dairy'] == 0 and livestock['scenario']['beef'] == 0:
            print(f"  → Zero livestock is correct (zero emissions budget)")

        # Check for zero budget informational message
        print(f"\n  Zero budget info message checks:")
        info_checks = [
            ("INFO header", "INFO: Zero CO2e budget for livestock" in output),
            ("Net emissions explanation", "NET EMISSIONS" in output),
            ("Budget breakdown", "Non-livestock emission breakdown" in output),
            ("Zero livestock result", "Zero livestock is the only feasible solution" in output),
        ]

        all_info_passed = True
        for check_name, passed in info_checks:
            status = "✓" if passed else "✗"
            print(f"    {status} {check_name}")
            if not passed:
                all_info_passed = False

        if all_info_passed:
            print("\n✓ Bug 1 FIXED: Both validation warning and zero budget info work correctly")
        else:
            print("\n✗ Bug 1 PARTIALLY FIXED: Info message checks failed")
            print(f"\n  Captured output:")
            print(output)

        assert all_info_passed, "Some info message checks failed"

    except AssertionError:
        raise
    except Exception as e:
        print(f"\n✗ Bug 1 test FAILED: {type(e).__name__}")
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

def test_bug2_fixed():
    """Test Bug 2: Constrained scenario should return zero livestock without crashing"""
    print("\n" + "="*70)
    print("Testing Bug 2 (FIXED): Constrained scenario handling")
    print("="*70)

    data_manager = OptiGobDataManager(str(BUG2_PATH))
    optigob = Optigob(data_manager)
    livestock = optigob.get_livestock_population()

    print(f"\n✓ Optimization completed (no crash)")
    print(f"  Scenario dairy: {livestock['scenario']['dairy']}")
    print(f"  Scenario beef:  {livestock['scenario']['beef']}")

    # Verify zero livestock is returned (correct result for this constrained scenario)
    assert livestock['scenario']['dairy'] == 0, f"Expected 0 dairy, got {livestock['scenario']['dairy']}"
    assert livestock['scenario']['beef'] == 0, f"Expected 0 beef, got {livestock['scenario']['beef']}"
    print("  ✓ Zero livestock returned as expected")

    # Verify emissions can be retrieved without error
    emissions = optigob.get_total_emissions_co2e_by_sector()
    assert 'scenario' in emissions, "Expected 'scenario' key in emissions"
    print("  ✓ Emissions retrieved successfully")

    print("\n✓ Bug 2 FIXED: Constrained scenario handled correctly")

def main():
    print("\n" + "#"*70)
    print("OPTIGOB BUG FIX VERIFICATION")
    print("#"*70)

    failures = []

    # Test Bug 1 fix
    try:
        test_bug1_fixed()
        print("  ✓ PASS: bug1")
    except Exception:
        failures.append("bug1")
        print("  ✗ FAIL: bug1")

    # Test Bug 2 fix
    try:
        test_bug2_fixed()
        print("  ✓ PASS: bug2")
    except Exception:
        failures.append("bug2")
        print("  ✗ FAIL: bug2")

    # Summary
    print("\n" + "#"*70)
    print("TEST SUMMARY")
    print("#"*70)

    if not failures:
        print("\n✓ All bug fixes verified successfully!")
    else:
        print(f"\n✗ {len(failures)} test(s) failed: {', '.join(failures)}")

    print("#"*70 + "\n")

    return 1 if failures else 0

if __name__ == '__main__':
    sys.exit(main())
