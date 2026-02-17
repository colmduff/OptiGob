
# Bug 1: Zero CO2e Budget Communication Plan

**Generated:** 2025-11-05

---

## Confirmed Issue

**CO2e Budget:** **0.00 kt** (CONFIRMED via test_co2e_budget_confirmation.py)

### Why the Budget is Zero

```
Non-livestock emission components:
  Static agriculture:      2,417.95 kt CO2e (emissions)
  Forest offset:            -542.87 kt CO2e (sequestration)
  Wetland restoration:     5,075.00 kt CO2e (emissions)
  Anaerobic digestion:       141.10 kt CO2e (emissions)
  ──────────────────────────────────────────────────
  TOTAL non-livestock:     7,091.18 kt CO2e

Budget Logic (emissions_budget.py:218-220):
  if total_emission > 0:
      total_emission = 0  # Net-zero target = no budget for livestock
```

### Current User Experience

**What happens:**
1. User runs scenario with `split_gas=false`
2. Optimizer runs successfully (status: "ok")
3. Returns: `Dairy_animals: 0`, `Beef_animals: 0`
4. **NO explanation of WHY**

**Problem:** User sees zero livestock but doesn't understand the constraint. Using the "CO2e currency" metaphor: **you can't buy livestock with 0 currency**.

---

## Proposed Solutions

### Option 1: Pre-flight Check with Informational Warning (RECOMMENDED)

**Similar to Bug 2 CH4 check, but non-blocking**

**Location:** `livestock_budget.py`, in `get_optimisation_outputs()` method, before the `if self.split_gas_approach:` block

**Implementation:**
```python
def get_optimisation_outputs(self):
    """Run the livestock population optimisation..."""
    area_commitment = self._get_total_area_commitment()

    # Pre-flight check for standard (non-split-gas) approach
    if not self.split_gas_approach:
        if self.net_zero_budget <= 0:
            # Get individual emission sources for detailed message
            static_ag = self.static_ag_budget.get_total_static_ag_co2e()
            forest = self.forest_budget.total_emission_offset()
            wetland = self.other_land_budget.get_wetland_restoration_emission_co2e()
            ad_ag = self.bio_energy_budget.get_ad_ag_co2e_emission()
            protein_crop = self.protein_crops_budget.get_crop_emission_co2e()
            beccs = self.bio_energy_budget.get_total_ccs_co2e_emission()

            total_non_livestock = static_ag + forest + wetland + ad_ag + protein_crop + beccs

            warning_msg = (
                f"INFO: Zero CO2e budget for livestock.\n\n"
                f"Your scenario's non-livestock land uses produce NET EMISSIONS:\n"
                f"  Total non-livestock emissions: {total_non_livestock:8.2f} kt CO2e\n"
                f"  Net-zero target budget:        {0.0:8.2f} kt CO2e\n"
                f"  ───────────────────────────────────────────────────────\n"
                f"  CO2e budget available for livestock: {self.net_zero_budget:8.2f} kt\n\n"
                f"Non-livestock emission breakdown:\n"
                f"  • Static agriculture:    {static_ag:8.2f} kt CO2e\n"
                f"  • Wetland restoration:   {wetland:8.2f} kt CO2e\n"
                f"  • Anaerobic digestion:   {ad_ag:8.2f} kt CO2e\n"
                f"  • Forest offset:         {forest:8.2f} kt CO2e\n"
                f"  • Protein crops:         {protein_crop:8.2f} kt CO2e\n"
                f"  • BECCS:                 {beccs:8.2f} kt CO2e\n\n"
                f"Result: Zero livestock is the only feasible solution.\n\n"
                f"To allow livestock production:\n"
                f"  1. Increase forest sequestration (higher afforestation rate)\n"
                f"  2. Reduce wetland restoration area\n"
                f"  3. Reduce static agriculture emissions\n"
                f"  4. Enable BECCS to create negative emissions\n"
            )

            print(warning_msg)  # Print to stdout for user visibility

    # Continue with existing optimization logic...
    if self.split_gas_approach:
        # ... existing CH4 check code ...
    else:
        # ... existing net-zero optimization call ...
```

**Characteristics:**
- ✅ Non-blocking (still runs optimization, returns 0 livestock)
- ✅ Clear explanation of constraints
- ✅ Shows exactly where the budget went
- ✅ Provides actionable suggestions
- ✅ Uses accessible "currency" metaphor
- ⚠️ Warning goes to stdout, might be missed in some contexts

---

### Option 2: Enhanced Return Message in OptimisationResult

**Add context to the result object when zero livestock is optimal**

**Location:** `livestock_optimisation.py`, in `optimise_livestock_pop()` method

**Implementation:**
```python
# After getting optimization results (line 160+)
total_dairy_animals = dairy_units * self.scalar(co2e_dairy_scaler["pop"])
total_beef_animals = beef_units * self.scalar(co2e_beef_scaler["pop"])

# Check if result is zero livestock due to zero budget
info_message = None
if total_dairy_animals == 0 and total_beef_animals == 0 and emissions_budget == 0:
    info_message = (
        "Zero livestock result: CO2e emissions budget is 0.00 kt. "
        "Non-livestock land uses have exhausted the available emissions budget. "
        "Increase sequestration or reduce other emissions to allow livestock."
    )

out = {
    "status": "ok",
    "Dairy_animals": total_dairy_animals,
    "Beef_animals": total_beef_animals,
    "info_message": info_message,  # New field
    # ... rest of output ...
}
```

**Characteristics:**
- ✅ Non-blocking
- ✅ Message attached to result object
- ⚠️ Less detailed than Option 1
- ⚠️ Might not be displayed unless explicitly checked

---

### Option 3: Hybrid Approach (MOST COMPREHENSIVE)

**Combine both approaches:**
1. Pre-flight informational message (Option 1) with full breakdown
2. Enhanced result metadata (Option 2) for programmatic access

**Benefits:**
- ✅ Immediate user feedback via stdout
- ✅ Programmatic access via result object
- ✅ Detailed breakdown + actionable suggestions
- ⚠️ Most code changes

---

## Recommended Approach

**Implement Option 1** (Pre-flight informational message)

### Why Option 1?

1. **Consistent with Bug 2 fix:** Same pattern as CH4 budget exhaustion check
2. **Proactive:** Warns users before optimization runs
3. **Educational:** Shows budget breakdown, helps users understand constraints
4. **Actionable:** Provides specific suggestions to make scenario feasible
5. **Non-blocking:** Doesn't prevent calculation, just informs

### Message Design Principles

Using the "CO2e currency" metaphor (as suggested by user):

**Clear analogy:**
> "Think of the CO2e budget as currency to buy livestock. Your scenario has **0.00 kt** of currency available because non-livestock land uses produce net emissions."

**Key components:**
1. **The constraint:** CO2e budget = 0.00 kt
2. **Why it's zero:** Net emissions from other land uses
3. **Where the budget went:** Breakdown by sector
4. **What it means:** Zero livestock is correct result
5. **How to fix:** Specific actions to create budget

---

## Implementation Checklist

- [ ] Add pre-flight check in `livestock_budget.py:get_optimisation_outputs()`
- [ ] Add helper method `_get_non_livestock_co2e_breakdown()` if needed
- [ ] Add informational message formatting (use consistent style with Bug 2)
- [ ] Update tests in `test_bugs_enhanced.py` to verify message appears
- [ ] Add test for edge case: very small budget (< 0.01 kt)
- [ ] Update CHANGELOG.md
- [ ] Verify warning doesn't break existing workflows

---

## Test Coverage

**New test cases needed:**

1. **Zero budget warning appears:**
   - Run bug1 scenario
   - Verify stdout contains "Zero CO2e budget for livestock"
   - Verify breakdown shows all sources

2. **Small budget (edge case):**
   - Create scenario with budget = 0.001 kt
   - Verify behavior (warn or not?)

3. **Negative budget (shouldn't happen but check):**
   - Mock scenario with negative budget
   - Verify appropriate error/warning

---

## Alternative: User-Facing Documentation

If code changes are too invasive, consider:

1. **FAQ entry:** "Why does my scenario return zero livestock?"
2. **Troubleshooting guide:** Common constraint issues
3. **Tutorial:** Understanding emissions budgets

**However:** Code-level messaging is still recommended for better UX.

---

## Example Output (Option 1)

```
INFO: Zero CO2e budget for livestock.

Your scenario's non-livestock land uses produce NET EMISSIONS:
  Total non-livestock emissions:     7,091.18 kt CO2e
  Net-zero target budget:                0.00 kt CO2e
  ───────────────────────────────────────────────────────
  CO2e budget available for livestock:   0.00 kt

Non-livestock emission breakdown:
  • Wetland restoration:   5,075.00 kt CO2e
  • Static agriculture:    2,417.95 kt CO2e
  • Anaerobic digestion:     141.10 kt CO2e
  • Forest offset:          -542.87 kt CO2e
  • Protein crops:             0.00 kt CO2e
  • BECCS:                     0.00 kt CO2e

Result: Zero livestock is the only feasible solution.

To allow livestock production:
  1. Increase forest sequestration (higher afforestation rate)
  2. Reduce wetland restoration area (currently 268000 ha)
  3. Reduce static agriculture emissions
  4. Enable BECCS to create negative emissions

Running optimization... (result will be 0 dairy, 0 beef)
```

---

## Next Steps

1. **Review plan with user** - get feedback on approach
2. **Implement Option 1** - add pre-flight check
3. **Add tests** - verify messaging works
4. **Document** - update CHANGELOG and user docs
5. **Consider Option 3** - add result metadata if useful
