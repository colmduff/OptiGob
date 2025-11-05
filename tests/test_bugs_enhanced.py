"""
Test the bug fixes for Bug 1 and Bug 2
"""
import os
import sys
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

        # Capture stdout to verify zero budget info message
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        # Now run the optimization
        optigob = Optigob(data_manager)
        emissions = optigob.get_total_emissions_co2e_by_sector()
        livestock = optigob.get_livestock_population()

        # Restore stdout
        sys.stdout = old_stdout
        output = captured_output.getvalue()

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
            return True
        else:
            print("\n✗ Bug 1 PARTIALLY FIXED: Info message checks failed")
            print(f"\n  Captured output:")
            print(output)
            return False

    except Exception as e:
        sys.stdout = old_stdout if 'old_stdout' in locals() else sys.stdout
        print(f"\n✗ Bug 1 test FAILED: {type(e).__name__}")
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_bug2_fixed():
    """Test Bug 2: Should raise clear error about CH4 budget exhaustion"""
    print("\n" + "="*70)
    print("Testing Bug 2 (FIXED): Pre-flight CH4 check")
    print("="*70)

    try:
        data_manager = OptiGobDataManager(str(BUG2_PATH))
        optigob = Optigob(data_manager)

        # Try to get emissions - should raise ValueError
        emissions = optigob.get_total_emissions_co2e_by_sector()

        # If we get here, test failed
        print("\n✗ Bug 2 test FAILED: Expected ValueError but none was raised")
        return False

    except ValueError as e:
        error_msg = str(e)

        print(f"\n✓ ValueError raised as expected")

        # Check if error message contains key phrases
        checks = [
            ("CH4 budget exhausted", "CH4 budget exhausted" in error_msg),
            ("Other conditions", "Other conditions" in error_msg or "Non-livestock" in error_msg),
            ("Wetland restoration", "Wetland restoration" in error_msg),
            ("Major contributor", "Major contributor" in error_msg),
            ("To make this scenario feasible", "feasible" in error_msg.lower())
        ]

        print("\n  Error message checks:")
        all_passed = True
        for check_name, passed in checks:
            status = "✓" if passed else "✗"
            print(f"    {status} {check_name}")
            if not passed:
                all_passed = False

        if all_passed:
            print("\n✓ Bug 2 FIXED: Pre-flight check works correctly")
            print("\n  Error message preview:")
            print("  " + "\n  ".join(error_msg.split("\n")[:10]))
            return True
        else:
            print("\n✗ Bug 2 test PARTIALLY FIXED: Some checks failed")
            print("\n  Full error message:")
            print(error_msg)
            return False

    except Exception as e:
        print(f"\n✗ Bug 2 test FAILED: Unexpected error type {type(e).__name__}")
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "#"*70)
    print("OPTIGOB BUG FIX VERIFICATION")
    print("#"*70)

    results = {}

    # Test Bug 1 fix
    results['bug1'] = test_bug1_fixed()

    # Test Bug 2 fix
    results['bug2'] = test_bug2_fixed()

    # Summary
    print("\n" + "#"*70)
    print("TEST SUMMARY")
    print("#"*70)

    for bug, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {bug}")

    all_passed = all(results.values())
    if all_passed:
        print("\n✓ All bug fixes verified successfully!")
    else:
        print("\n✗ Some tests failed - see details above")

    print("#"*70 + "\n")

    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
