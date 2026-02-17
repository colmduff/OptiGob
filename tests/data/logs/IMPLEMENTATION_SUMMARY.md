# Logging Implementation Summary

**Date:** November 5, 2024
**Changes:** Added logging system to optigob

---

## What Was Done

### 1. Created Logger Module (`src/optigob/logger.py`)

This is the central logging module that all other optigob modules use.

**Two main functions:**

#### `get_logger(name)`
- Returns a logger for a specific module
- Creates hierarchical logger names like `optigob.livestock`, `optigob.data_manager`
- All optigob loggers are under the root `optigob` logger

**Example:**
```python
from optigob.logger import get_logger
logger = get_logger("my_module")  # Creates "optigob.my_module" logger
logger.info("Hello!")
```

#### `configure_logging(level, log_to_file, format_style)`
- Quick setup function for users
- Configures what messages appear and where they go
- Parameters:
  - `level`: How much to show (DEBUG, INFO, WARNING, ERROR)
  - `log_to_file`: Optional filename to save logs
  - `format_style`: "detailed" (with timestamps) or "simple" (just message)

**Example:**
```python
from optigob.logger import configure_logging
import logging

# Show INFO and above, save to file
configure_logging(level=logging.INFO, log_to_file='my_run.log')
```

---

### 2. Updated OptiGobDataManager (`src/optigob/resource_manager/optigob_data_manager.py`)

**Changed:**
- Added: `from optigob.logger import get_logger`
- Added: `logger = get_logger("data_manager")`
- Changed: `warnings.warn(...)` → `logger.warning(...)`

**What it does:**
- Warns when `split_gas_frac` is set but `split_gas=False`
- Message is now controllable by user via logging level

---

### 3. Updated LivestockBudget (`src/optigob/livestock/livestock_budget.py`)

**Changed:**
- Added: `from optigob.logger import get_logger`
- Added: `logger = get_logger("livestock")`
- Changed: `raise ValueError(...)` → `logger.warning(...)` (for CH4 exhaustion)
- Changed: `print(info_msg)` → `logger.info(info_msg)` (for zero CO2e budget)

**What it does:**
- Warns when CH4 budget is exhausted (no longer raises error)
- Informs when CO2e budget is zero
- Both scenarios now continue with zero livestock instead of stopping

**Why this change:**
- Consistent behavior: Both zero budget scenarios now work the same way
- User-friendly: Allows batch processing without manual intervention
- Still informative: Clear messages explain what happened

---

## Files Created

### 1. `src/optigob/logger.py`
- Core logging module
- Well-documented with docstrings
- Simple interface for both users and developers

### 2. `tests/data/logs/LOGGING_GUIDE.md`
- Comprehensive guide for users unfamiliar with logging
- Explains what logging is and why it's useful
- Shows the 5 logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Provides examples for common use cases
- Troubleshooting section
- Written for someone who has never used logging before

### 3. `tests/logging_example.py`
- Executable examples demonstrating logging
- 6 different examples covering common scenarios:
  1. Default logging (INFO level)
  2. Quiet mode (WARNING only)
  3. Simple format (no timestamps)
  4. Logging to file
  5. Silent mode (no logging)
  6. Custom logger in your own code
- Can be run interactively or referenced as documentation
- Ready to be added to README.md

### 4. `tests/data/logs/IMPLEMENTATION_SUMMARY.md` (this file)
- Technical summary of what was implemented
- Quick reference for you

---

## How It Works

### The Logger Hierarchy

```
optigob (root logger)
    ├── optigob.data_manager
    ├── optigob.livestock
    ├── optigob.forest
    └── ... (future modules)
```

When a user calls `configure_logging()`:
1. It configures the root `optigob` logger
2. All child loggers inherit the configuration
3. Messages go to console (and optionally to file)

### Message Flow

```
Module code:
    logger.warning("Something happened")
        ↓
Python logging system:
    - Checks if level is enabled (e.g., WARNING ≥ INFO)
    - If yes, formats message
    - Sends to all handlers (console, file, etc.)
        ↓
User sees:
    2024-11-05 10:15:32 - optigob.livestock - WARNING - Something happened
```

---

## What Changed from Previous Implementation

| Scenario | Old Behavior | New Behavior | Why |
|----------|-------------|--------------|-----|
| `split_gas_frac` set incorrectly | `warnings.warn()` | `logger.warning()` | Standard Python practice, user-controllable |
| CH4 budget exhausted | `raise ValueError()` | `logger.warning()` + continue | Consistent with CO2e behavior, allows exploration |
| Zero CO2e budget | `print()` | `logger.info()` | User-controllable output |

**Key improvement:** Both zero budget scenarios now behave consistently - they warn/inform and continue with zero livestock instead of stopping execution.

---

## How to Use (Quick Reference)

### For Users

**Basic usage:**
```python
from optigob.logger import configure_logging
import logging

# At the start of your script
configure_logging(level=logging.INFO)

# Then use optigob normally
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

data_manager = OptiGobDataManager('./data/scenario.yaml')
optigob = Optigob(data_manager)
results = optigob.get_total_emissions_co2e_by_sector()
```

**Common configurations:**
```python
# Default (recommended)
configure_logging(level=logging.INFO)

# Quiet (only warnings and errors)
configure_logging(level=logging.WARNING)

# Save to file
configure_logging(level=logging.INFO, log_to_file='my_analysis.log')

# Simple format for Jupyter
configure_logging(level=logging.INFO, format_style="simple")

# Silent (no messages)
import logging
logging.getLogger("optigob").setLevel(logging.CRITICAL)
```

### For Developers (Adding Logging to New Modules)

```python
# At the top of your module
from optigob.logger import get_logger

logger = get_logger("my_module_name")

# Then use throughout your module
logger.debug("Detailed diagnostic info")
logger.info("General information")
logger.warning("Something unexpected but not critical")
logger.error("An error occurred")
```

---

## Messages Users Will See

### 1. Parameter Validation Warning (data_manager)
```
WARNING - Parameter Validation Warning:
  split_gas=False but split_gas_frac=0.3
  The split_gas_frac parameter is IGNORED when split_gas=False.
  Set split_gas_frac=0 or remove it to avoid confusion.
```

### 2. Zero CH4 Budget (livestock)
```
WARNING: Zero CH4 budget for livestock.

Your scenario's CH4 budget has been exhausted by other land uses:
  CH4 target (with 80% reduction):    135.87 kt
  Non-livestock CH4 emissions:        194.05 kt
  ─────────────────────────────────────────────────────
  CH4 budget available for livestock:  -58.18 kt

Other conditions have used up the available CH4 budget:
  • Wetland restoration      :  156.00 kt (114.8% of target)
  • Static agriculture       :   33.04 kt ( 24.3% of target)
  ...

Result: Zero livestock is the only feasible solution.

To allow livestock production:
  1. Reduce split_gas_frac (currently 0.8) to allow more CH4
  2. Reduce wetland restoration area (currently 268000 ha)
  ...
```

### 3. Zero CO2e Budget (livestock)
```
INFO: Zero CO2e budget for livestock.

Your scenario's non-livestock land uses produce NET EMISSIONS:
  Total non-livestock emissions:  7091.18 kt CO2e
  Net-zero target budget:            0.00 kt CO2e
  ─────────────────────────────────────────────────────
  CO2e budget available for livestock:     0.00 kt

Non-livestock emission breakdown:
  • Wetland restoration      :  5075.00 kt CO2e
  • Static agriculture       :  2417.95 kt CO2e
  ...

Result: Zero livestock is the only feasible solution.

To allow livestock production:
  1. Increase forest sequestration (higher afforestation rate)
  2. Reduce wetland restoration area (currently 268000 ha)
  ...
```

---

## Testing

### Manual Test
```bash
# From optigob directory
.venv/bin/python tests/logging_example.py
```

This will run 6 interactive examples showing different logging configurations.

### Verify in Your Code
```python
from optigob.logger import configure_logging, get_logger
import logging

configure_logging(level=logging.INFO)
logger = get_logger("test")

logger.info("This should appear")
logger.warning("This should also appear")
logger.debug("This should NOT appear (level too low)")
```

---

## Future Enhancements

Potential additions for the future:

1. **More modules**: Add logging to forest, bioenergy, etc.
2. **Progress indicators**: Log optimization progress
3. **Performance metrics**: Log timing information with DEBUG level
4. **Structured logging**: Add JSON output for machine parsing
5. **Rotating file handlers**: Prevent log files from growing too large

---

## Documentation for Users

### What to Add to README.md

Add a section like this:

```markdown
## Logging

Optigob uses Python's standard logging module to provide informative messages about your scenarios.

### Quick Start

```python
from optigob.logger import configure_logging
import logging

# Show all informational messages (recommended)
configure_logging(level=logging.INFO)

# Only show warnings and errors (quiet mode)
configure_logging(level=logging.WARNING)

# Save logs to a file
configure_logging(level=logging.INFO, log_to_file='my_analysis.log')
```

### Examples

See `tests/logging_example.py` for complete examples of different logging configurations.

### Learn More

For a comprehensive guide to logging, see `tests/data/logs/LOGGING_GUIDE.md`.
```

---

## Summary

**What was implemented:**
- ✅ Complete logging system with `logger.py` module
- ✅ Updated 2 modules to use logging (data_manager, livestock)
- ✅ Changed Bug 2 from error to warning (consistent with Bug 1)
- ✅ Comprehensive documentation for beginners
- ✅ Executable examples for users
- ✅ Tested and working

**Benefits:**
- Users control what messages they see
- Batch processing won't stop on warnings
- Messages can be saved to files
- Professional, standard Python practice
- Easy to extend to other modules

**For you as maintainer:**
- Simple to add logging to new modules (3 lines of code)
- All logging centrally controlled
- Easy to debug with DEBUG level
- Follows Python best practices
