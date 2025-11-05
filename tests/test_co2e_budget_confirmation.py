"""
Test to confirm the CO2e budget value in bug1 scenario.
"""
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
from optigob.budget_model.emissions_budget import EmissionsBudget

def test_bug1_co2e_budget():
    """Confirm that bug1 scenario has 0 CO2e budget."""

    # Load bug1 scenario
    data_manager = OptiGobDataManager('./tests/data/sip_bug1.yaml')

    # Create emissions budget to check the calculation
    emissions_budget = EmissionsBudget(data_manager)

    # Get the net_zero_budget value
    net_zero_budget = emissions_budget.net_zero_budget

    print(f"\n{'='*70}")
    print(f"Bug 1 Scenario CO2e Budget Analysis")
    print(f"{'='*70}")
    print(f"\nConfiguration:")
    print(f"  split_gas: {data_manager.get_split_gas()}")
    print(f"  split_gas_frac: {data_manager.get_split_gas_fraction()}")
    print(f"  target_year: {data_manager.get_target_year()}")

    print(f"\nEmissions Budget Calculation:")
    print(f"  net_zero_budget passed to livestock optimizer: {net_zero_budget:.2f} kt CO2e")

    # Get the raw budget before abs() to understand the calculation
    raw_budget = emissions_budget._get_total_emission_co2e_budget()
    print(f"  Raw budget (before abs):                      {raw_budget:.2f} kt CO2e")

    # Get individual components
    print(f"\nNon-livestock emission components:")
    static_ag = emissions_budget.static_ag_budget.get_total_static_ag_co2e()
    forest = emissions_budget.forest_budget.total_emission_offset()
    wetland = emissions_budget.other_land_budget.get_wetland_restoration_emission_co2e()
    beccs = emissions_budget._get_total_beccs_co2e()
    protein_crop = emissions_budget.protein_crops_budget.get_crop_emission_co2e()
    ad_ag = emissions_budget.bio_energy_budget.get_ad_ag_co2e_emission()

    print(f"  Static agriculture:      {static_ag:10.2f} kt CO2e")
    print(f"  Forest offset:           {forest:10.2f} kt CO2e")
    print(f"  Wetland restoration:     {wetland:10.2f} kt CO2e")
    print(f"  BECCS:                   {beccs:10.2f} kt CO2e")
    print(f"  Protein crops:           {protein_crop:10.2f} kt CO2e")
    print(f"  Anaerobic digestion:     {ad_ag:10.2f} kt CO2e")
    print(f"  {'─'*50}")
    total_non_livestock = static_ag + forest + wetland + beccs + protein_crop + ad_ag
    print(f"  TOTAL non-livestock:     {total_non_livestock:10.2f} kt CO2e")

    print(f"\nBudget Logic:")
    if total_non_livestock > 0:
        print(f"  Total is POSITIVE (net emissions) → Budget set to 0")
    else:
        print(f"  Total is NEGATIVE (net sequestration) → Budget = abs({total_non_livestock:.2f})")

    print(f"\n{'='*70}")
    print(f"CONFIRMATION: CO2e budget for livestock = {net_zero_budget:.2f} kt")
    print(f"{'='*70}\n")

    # Assert for automated testing
    assert net_zero_budget == 0.0, f"Expected 0.0 kt, got {net_zero_budget} kt"
    print("✓ Confirmed: CO2e budget is exactly 0.00 kt\n")

if __name__ == "__main__":
    test_bug1_co2e_budget()
