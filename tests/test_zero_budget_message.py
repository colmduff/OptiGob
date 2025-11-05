"""
Test to verify the zero CO2e budget informational message appears.
"""
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
import sys
from io import StringIO

def test_zero_budget_info_message():
    """Test that the informational message appears for zero CO2e budget."""

    print("\n" + "="*70)
    print("Testing Zero CO2e Budget Informational Message")
    print("="*70)

    # Load bug1 scenario
    data_manager = OptiGobDataManager('./tests/data/sip_bug1.yaml')

    # Capture stdout to verify message appears
    captured_output = StringIO()
    sys.stdout = captured_output

    # Initialize Optigob - this will trigger the optimization
    optigob = Optigob(data_manager)

    # Get livestock population (this calls get_optimisation_outputs internally)
    livestock_pop = optigob.get_livestock_population()
    dairy_pop = livestock_pop.get("Dairy", 0)
    beef_pop = livestock_pop.get("Beef", 0)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Get the captured output
    output = captured_output.getvalue()

    # Verify the message appeared
    print("\nCaptured Output:")
    print("─" * 70)
    print(output)
    print("─" * 70)

    # Verify key elements of the message
    print("\nVerifying message content:")

    checks = {
        "INFO header": "INFO: Zero CO2e budget for livestock" in output,
        "Net emissions explanation": "NET EMISSIONS" in output,
        "Budget breakdown": "Non-livestock emission breakdown" in output,
        "Zero livestock result": "Zero livestock is the only feasible solution" in output,
        "Actionable suggestions": "To allow livestock production:" in output,
        "Wetland restoration": "Wetland restoration" in output,
        "Static agriculture": "Static agriculture" in output,
    }

    all_passed = True
    for check_name, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check_name}: {passed}")
        if not passed:
            all_passed = False

    # Verify populations are zero
    print(f"\nPopulation results:")
    print(f"  Dairy population: {dairy_pop:.2f}")
    print(f"  Beef population: {beef_pop:.2f}")

    assert dairy_pop == 0, f"Expected 0 dairy, got {dairy_pop}"
    assert beef_pop == 0, f"Expected 0 beef, got {beef_pop}"

    if all_passed:
        print("\n" + "="*70)
        print("✓ All checks passed! Zero budget message works correctly.")
        print("="*70 + "\n")
    else:
        raise AssertionError("Some message checks failed")

if __name__ == "__main__":
    test_zero_budget_info_message()
