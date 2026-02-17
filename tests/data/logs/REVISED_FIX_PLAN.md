# Revised Bug Fix Plan

**Based on enhanced diagnosis - 2025-11-04**

---

## Bug 1: Input Validation for split_gas_frac

### Issue
When `split_gas=false`, the parameter `split_gas_frac` should be None or 0, but currently accepts any value (e.g., 0.3). This is confusing to users even though it doesn't affect calculations.

### Fix

**File:** `src/optigob/resource_manager/optigob_data_manager.py`

**Add validation method:**

```python
def _validate_input_parameters(self):
    """Validate that input parameters are consistent"""
    split_gas = self.standard_input_parameters.get('split_gas', False)
    split_gas_frac = self.standard_input_parameters.get('split_gas_frac')

    # Warn if split_gas_frac is set when split_gas is False
    if not split_gas and split_gas_frac is not None and split_gas_frac != 0:
        import warnings
        warnings.warn(
            f"Parameter Validation Warning:\n"
            f"  split_gas=False but split_gas_frac={split_gas_frac}\n"
            f"  The split_gas_frac parameter is IGNORED when split_gas=False.\n"
            f"  Set split_gas_frac=0 or remove it to avoid confusion.",
            UserWarning,
            stacklevel=2
        )

    # Validate split_gas_frac range when split_gas is True
    if split_gas:
        if split_gas_frac is None or split_gas_frac < 0 or split_gas_frac >= 1:
            raise ValueError(
                f"Parameter Error:\n"
                f"  split_gas=True requires split_gas_frac in range (0, 1).\n"
                f"  Got: split_gas_frac={split_gas_frac}"
            )

def __init__(self, sip):
    # ... existing loading code ...

    # Add validation call at end of __init__
    self._validate_input_parameters()
```

**Testing:**
- `split_gas=false, split_gas_frac=0.3` → Should emit warning
- `split_gas=false, split_gas_frac=0` → Should NOT warn
- `split_gas=true, split_gas_frac=0.8` → Should pass
- `split_gas=true, split_gas_frac=None` → Should raise ValueError

---

## Bug 2 Fix #1: Pre-flight CH4 Budget Validation

### Issue
Negative CH4 budget is not caught before calling optimizer, leading to infeasible optimization.

### Fix

**File:** `src/optigob/livestock/livestock_budget.py`

**Method:** `get_optimisation_outputs()` (line 205)

**Add pre-flight check:**

```python
def get_optimisation_outputs(self):
    """
    Run the livestock population optimisation for the current scenario and constraints.

    Returns:
        dict: Dictionary of optimised livestock populations and related outputs.

    Raises:
        ValueError: If the scenario is mathematically infeasible before optimization.
    """
    area_commitment = self._get_total_area_commitment()

    if self.split_gas_approach:
        # Pre-flight feasibility check
        ch4_baseline_total = self.baseline_emission.get_total_ch4_emission()
        ch4_target = ch4_baseline_total * (1 - self.split_gas_frac)
        non_livestock_ch4 = self._get_total_non_livestock_emission_ch4()
        ch4_budget_for_livestock = ch4_target - non_livestock_ch4

        if ch4_budget_for_livestock <= 0:
            # Get individual sources for detailed error message
            static_ag_ch4 = self.static_ag_budget.get_total_static_ag_ch4()
            wetland_ch4 = self.other_land_budget.get_wetland_restoration_emission_ch4()
            ad_ch4 = self.bio_energy_budget.get_ad_ag_ch4_emission()
            protein_ch4 = self.protein_crop_budget.get_crop_emission_ch4()
            beccs_ch4 = self.bio_energy_budget.get_total_ccs_ch4_emission()

            sources = [
                ("Wetland restoration", wetland_ch4),
                ("Static agriculture", static_ag_ch4),
                ("Anaerobic digestion", ad_ch4),
                ("Protein crops", protein_ch4),
                ("BECCS", beccs_ch4),
            ]
            sources_sorted = sorted(sources, key=lambda x: x[1], reverse=True)

            error_msg = (
                f"Scenario is INFEASIBLE: CH4 budget exhausted by other land use conditions.\n\n"
                f"The problem:\n"
                f"  CH4 target (with {self.split_gas_frac*100:.0f}% reduction):  {ch4_target:8.2f} kt\n"
                f"  Non-livestock CH4 emissions:                {non_livestock_ch4:8.2f} kt\n"
                f"  ─────────────────────────────────────────────────────\n"
                f"  CH4 budget available for livestock:         {ch4_budget_for_livestock:8.2f} kt\n\n"
                f"Other conditions have used up the available CH4 budget:\n"
            )

            for source_name, value in sources_sorted:
                if value > 0:
                    pct = (value / ch4_target) * 100
                    error_msg += f"  • {source_name:25s}: {value:7.2f} kt ({pct:5.1f}% of target)\n"

            # Identify the major contributors
            major_contributors = [name for name, val in sources_sorted if val > ch4_target * 0.5]
            if major_contributors:
                error_msg += f"\nMajor contributor(s): {', '.join(major_contributors)}\n"

            error_msg += (
                f"\nTo make this scenario feasible, you can:\n"
                f"  1. Reduce split_gas_frac (currently {self.split_gas_frac}) to allow more CH4\n"
                f"  2. Reduce wetland restoration area (currently {self.rewetted_area:.0f} ha)\n"
                f"  3. Reduce biomethane/AD area (currently {self.biomethane_area:.0f} ha)\n"
                f"  4. Use split_gas=False for standard CO2e accounting instead\n"
            )

            raise ValueError(error_msg)

        return self.optimisation.optimise_livestock_pop(
            ratio_type=self.get_livestock_ratio_type,
            ratio_value=self.livestock_ratio_value,
            year=self.target_year,
            scenario=self.scenario,
            abatement=self.abatement,
            emissions_budget=self.split_gas_budget,
            area_commitment=area_commitment,
            ch4_budget=self.ch4_budget
        )
    else:
        return self.optimisation.optimise_livestock_pop(
            ratio_type=self.get_livestock_ratio_type,
            ratio_value=self.livestock_ratio_value,
            year=self.target_year,
            scenario=self.scenario,
            abatement=self.abatement,
            area_commitment=area_commitment,
            emissions_budget=self.net_zero_budget
        )
```

**Testing:**
- Bug 2 scenario → Should raise clear ValueError BEFORE calling optimizer
- Feasible scenarios → Should pass through to optimizer

---

## Bug 2 Fix #2: Handle Infeasible Optimization Results

### Issue
Missing return statement after detecting infeasibility causes TypeError crash.

### Fix

**File:** `src/optigob/livestock/livestock_optimisation.py`

**Method:** `optimise_livestock_pop()` (line 139)

**Add return statement:**

```python
def optimise_livestock_pop(self, ...):
    # ... existing code up to line 138 ...

    # ==== 3. Wrap up result: always return OptimisationResult ====
    termination = str(result.solver.termination_condition).lower()
    beef_units = model.x.value
    dairy_units = model.y.value

    # Check for infeasibility
    if 'infeasible' in termination or beef_units is None or dairy_units is None:
        error_msg = (
            "Optimization infeasible: No feasible solution exists.\n"
            "This should have been caught by pre-flight checks.\n"
            "If you see this error, there may be numerical issues with the optimizer."
        )

        # Return an error result instead of crashing
        return OptimisationResult({
            "status": "infeasible",
            "message": error_msg,
            "Dairy_animals": 0,
            "Beef_animals": 0,
            "Scenario": scenario,
            "Year": year,
            "Emissions_budget_CO2e": emissions_budget,
            "Dairy_emissions_CO2e": 0,
            "Beef_emissions_CO2e": 0
        })

    # --- Otherwise, return the solution as usual, with status "ok" ---
    total_dairy_animals = dairy_units * self.scalar(co2e_dairy_scaler["pop"])
    total_beef_animals = beef_units * self.scalar(co2e_beef_scaler["pop"])

    # ... rest of existing code ...
```

**This is a safety net** - with Fix #1 in place, this should rarely be triggered. But it prevents crashes if somehow an infeasible scenario makes it to the optimizer.

**Testing:**
- Even if pre-flight check is bypassed, should return error result instead of crashing

---

## Bug 2 Fix #3: Check Error Result in Calling Code

### Issue
Calling code doesn't check if optimization returned an error status.

### Fix

**File:** `src/optigob/livestock/livestock_budget.py`

**Method:** `_load_optimisation_outputs()` (line 150)

**Check result status:**

```python
def _load_optimisation_outputs(self):
    """
    Load and cache the livestock optimisation outputs if not already loaded.

    Returns:
        dict: Dictionary of optimisation results for livestock populations and constraints.

    Raises:
        ValueError: If optimization was infeasible.
    """
    if self._optimisation_outputs is None:
        self._optimisation_outputs = self.get_optimisation_outputs()

        # Check if optimization was feasible
        if not self._optimisation_outputs.feasible:
            raise ValueError(
                f"Livestock optimization failed:\n{self._optimisation_outputs.get('message', 'Unknown error')}"
            )

    return self._optimisation_outputs
```

**Testing:**
- Infeasible results should raise clear ValueError
- Feasible results should work as before

---

## Implementation Order

1. **Fix Bug 2 #1 first** (pre-flight check) - Prevents most cases
2. **Fix Bug 2 #2 second** (safety net) - Handles edge cases
3. **Fix Bug 2 #3 third** (error propagation) - Clean error messages
4. **Fix Bug 1 last** (validation) - User experience improvement

---

## Testing

**Test file:** `tests/test_bug_fixes.py`

```python
import pytest
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

def test_bug1_validation_warning():
    """Bug 1: split_gas_frac with split_gas=false should warn"""
    with pytest.warns(UserWarning, match="split_gas_frac.*IGNORED"):
        data_manager = OptiGobDataManager('tests/data/sip_bug1.yaml')

def test_bug2_negative_ch4_budget():
    """Bug 2: Negative CH4 budget should raise clear error"""
    with pytest.raises(ValueError, match="CH4 budget for livestock.*negative"):
        data_manager = OptiGobDataManager('tests/data/sip_bug2.yaml')
        optigob = Optigob(data_manager)
        optigob.get_total_emissions_co2e_by_sector()

def test_bug1_zero_livestock_acceptable():
    """Bug 1: Zero livestock is correct with zero budget"""
    # This should complete without error
    data_manager = OptiGobDataManager('tests/data/sip_bug1.yaml')
    optigob = Optigob(data_manager)
    livestock = optigob.get_livestock_population()

    assert livestock['scenario']['dairy'] == 0
    assert livestock['scenario']['beef'] == 0
    # This is correct, not a bug!
```

---

## Documentation Updates

After fixes are implemented, update:

1. `INPUT_VARIABLES.md` - Clarify that `split_gas_frac` only applies when `split_gas=true`
2. `CLAUDE.md` - Add error handling section
3. Docstrings in modified files
4. Add troubleshooting guide for common infeasibility scenarios

---

## Summary

### Bug 1: Validation Only
- **Current behavior:** split_gas_frac is loaded but ignored when split_gas=false
- **Fix:** Add validation warning to prevent user confusion
- **Complexity:** Low (simple validation)

### Bug 2: Pre-flight Check + Error Handling
- **Current behavior:** Crashes with TypeError on infeasible scenarios
- **Root cause:** Negative CH4 budget (wetland restoration alone exceeds target)
- **Fixes:**
  1. Check CH4 budget before optimizer (primary fix)
  2. Handle infeasible results gracefully (safety net)
  3. Propagate errors with clear messages
- **Complexity:** Medium (3 related fixes)

Both fixes are focused, well-scoped, and don't change core calculation logic.
