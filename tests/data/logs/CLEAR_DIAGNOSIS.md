# Clear Bug Diagnosis

**Generated:** 2025-11-04

---

## Bug 1: Input Validation Issue (sip_bug1.yaml)

### Configuration
```yaml
split_gas: false
split_gas_frac: 0.3  # ← Shouldn't be here!
```

### What's Actually Happening

**Is `split_gas_frac` being used?** **NO!**

The code flow:
1. `split_gas=false` → Takes the `else` branch in `livestock_budget.py` line 226-235
2. **No CH4 budget is calculated** (line 130-131 are skipped)
3. Optimizer is called **without** `ch4_budget` parameter
4. Pyomo model gets **ONLY ONE constraint**: CO2e ≤ 0.00 kt
5. **No CH4 constraint is added** to the model

```
livestock_budget.py lines 127-131:
  self.split_gas_approach = False  # From input
  self.split_gas_frac = 0.3        # LOADED but...

  if self.split_gas_approach:      # False, so this is SKIPPED
      self.ch4_budget = ...         # NEVER EXECUTED
```

### Result: Zero Livestock

**Is this correct?** **YES!**

- Net-zero emissions budget: **0.00 kt CO2e**
- Land available for livestock: **2,450,492.87 ha** (plenty of land)
- **Both land AND emissions constraints are applied to Pyomo**
- Emissions constraint is the limiting factor (zero budget)
- Zero livestock is the correct solution
- **This is NOT a calculation bug**

**Constraint verification:**
```
Pyomo model receives 3 constraints:
1. Area: (beef × area_per_beef) + (dairy × area_per_dairy) ≤ 2,450,492.87 ha
2. Emissions: (beef × co2e_per_beef) + (dairy × co2e_per_dairy) ≤ 0 kt
3. Ratio: dairy = 30 × beef

With emissions budget = 0, only solution is beef = 0, dairy = 0
```

### The Actual Issue

**Input validation only:** `split_gas_frac=0.3` should not be present (or should be 0/None) when `split_gas=false`. It's confusing but doesn't affect calculations.

**Fix needed:** Validation warning or error when `split_gas=false` but `split_gas_frac ≠ 0`

---

## Bug 2: Negative CH4 Budget → Crash (sip_bug2.yaml)

### Configuration
```yaml
split_gas: true
split_gas_frac: 0.8  # 80% reduction target
```

### The Math Problem

**Step 1: Calculate CH4 target**
- Baseline CH4: **679.35 kt**
- Target (20% of baseline): 679.35 × (1 - 0.8) = **135.87 kt**

**Step 2: Non-livestock CH4 emissions (FIXED, not optimized)**

| Source | CH4 (kt) | % of Target |
|--------|----------|-------------|
| **Wetland restoration** | **156.00** | **114.8%** ← Exceeds entire target! |
| Static agriculture | 33.04 | 24.3% |
| Anaerobic digestion | 5.00 | 3.7% |
| Protein crops | 0.00 | 0.0% |
| BECCS | 0.00 | 0.0% |
| **TOTAL** | **194.05** | **142.9%** |

**Step 3: CH4 budget for livestock**
```
135.87 (target) - 194.05 (non-livestock) = -58.18 kt (NEGATIVE!)
```

### Why This is Impossible

**Wetland restoration alone (156.00 kt) exceeds the entire CH4 target (135.87 kt)!**

You cannot have livestock with negative emissions. The scenario is mathematically impossible **before Pyomo even runs**.

### The Code Bug

**Location:** `livestock_optimisation.py` line 139-144

```python
if 'infeasible' in termination or beef_units is None or dairy_units is None:
    print("Optimization infeasible: No feasible solution...")
    # ← MISSING RETURN STATEMENT!

# Code continues and crashes here:
total_dairy_animals = dairy_units * self.scalar(...)  # dairy_units is None!
```

The infeasibility is detected but code doesn't return, so it tries to multiply `None * float` → TypeError

### Fixes Needed

1. **Pre-flight validation** in `livestock_budget.py`: Check if CH4 budget is negative before calling optimizer
2. **Return statement** in `livestock_optimisation.py`: Return error result after detecting infeasibility (line 141)
3. **User-friendly error message**: Explain WHY scenario is infeasible (which sources exceed budget)

---

## Summary

### Bug 1: Validation Issue Only
- `split_gas_frac` is **not used** when `split_gas=false` ✓
- Zero livestock is **correct** given zero emissions budget ✓
- Only issue: confusing to have `split_gas_frac≠0` when `split_gas=false`
- **Fix:** Input validation warning/error

### Bug 2: Mathematical Impossibility + Poor Error Handling
- **Wetland restoration (156 kt) alone exceeds the entire CH4 target (135.87 kt)**
- CH4 budget for livestock is **negative (-58.18 kt)**
- Scenario is impossible before optimization runs
- Code detects infeasibility but **crashes instead of returning error**
- **Fixes:**
  1. Pre-validate CH4 budget is positive
  2. Add missing return statement after infeasibility detection
  3. Provide clear error message identifying the problematic sources

---

## Detailed Logs

Full enhanced logs with complete Pyomo details:
- Bug 1: `bug1_enhanced_20251104_105710.log`
- Bug 2: `bug2_enhanced_20251104_105710.log`
