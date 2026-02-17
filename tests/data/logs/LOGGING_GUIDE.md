# Logging Guide for Optigob

**Author:** Optigob Development Team
**Last Updated:** November 2024
**For:** Users and developers unfamiliar with Python logging

---

## Table of Contents

1. [What is Logging?](#what-is-logging)
2. [Why We Added Logging to Optigob](#why-we-added-logging-to-optigob)
3. [How Logging Works in Optigob](#how-logging-works-in-optigob)
4. [The Five Logging Levels](#the-five-logging-levels)
5. [Quick Start Examples](#quick-start-examples)
6. [Common Use Cases](#common-use-cases)
7. [Under the Hood (Technical Details)](#under-the-hood-technical-details)
8. [Troubleshooting](#troubleshooting)

---

## What is Logging?

**Logging** is a way for programs to send messages to users while they're running. Think of it like a diary that the program writes in real-time.

Instead of:
```python
print("Starting calculation...")
print("Warning: Something unusual happened")
print("Error: Cannot proceed")
```

We use:
```python
logger.info("Starting calculation...")
logger.warning("Warning: Something unusual happened")
logger.error("Error: Cannot proceed")
```

### Why is logging better than print?

1. **Control**: Users can turn messages on/off without changing code
2. **Filtering**: Show only warnings, or show everything including debug info
3. **Destinations**: Send messages to files, console, or both
4. **Context**: Automatically includes timestamps, module names, etc.
5. **Standards**: Every Python developer knows how to work with logs

---

## Why We Added Logging to Optigob

Optigob performs complex optimization calculations. Sometimes scenarios produce zero livestock not because of a bug, but because of the constraints you've set. We need to tell you:

- **INFO**: "Zero CO2e budget available, so zero livestock is correct"
- **WARNING**: "CH4 budget exhausted by other land uses"
- **ERROR**: "Invalid parameter value detected"

With logging, you can:
- Run batch analyses without stopping on warnings
- Save all messages to a file for later review
- Turn off INFO messages when you don't need them
- Debug problems by enabling DEBUG level

---

## How Logging Works in Optigob

### The Architecture

```
optigob (root logger)
    ├── optigob.data_manager
    ├── optigob.livestock
    ├── optigob.forest
    └── ... (other modules)
```

Every optigob module gets its own logger (like `optigob.livestock`), but you can control them all together through the root `optigob` logger.

### Where We Use Logging

1. **Parameter Validation** (`optigob_data_manager.py`)
   - Warns when you set conflicting parameters
   - Example: `split_gas_frac` when `split_gas=False`

2. **Budget Exhaustion** (`livestock_budget.py`)
   - Warns when CH4 budget is exhausted
   - Informs when CO2e budget is zero
   - Explains why zero livestock is the result

3. **Future**: Will add logging to more modules as needed

---

## The Five Logging Levels

Python's logging has five levels, from most to least severe:

### 1. DEBUG (Level 10)
**What**: Very detailed diagnostic information
**When**: Only during development or troubleshooting
**Example**: "Querying database: year=2050, scenario=1"

### 2. INFO (Level 20)
**What**: General informational messages
**When**: Confirming things are working as expected
**Example**: "Zero CO2e budget for livestock - this is expected given your constraints"

### 3. WARNING (Level 30) ⚠️
**What**: Something unexpected but not blocking
**When**: The program continues but you should be aware
**Example**: "Parameter ignored" or "Zero CH4 budget - returning zero livestock"

### 4. ERROR (Level 40) ❌
**What**: Serious problem preventing a function from working
**When**: Something failed
**Example**: "Invalid parameter value: split_gas_frac must be in range (0, 1)"

### 5. CRITICAL (Level 50) 💥
**What**: System-level failure
**When**: The entire program might crash
**Example**: "Database file not found"

---

## Quick Start Examples

### Example 1: Default Behavior (Show Everything)

```python
from optigob.logger import configure_logging
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
import logging

# Set up logging to show INFO and above
configure_logging(level=logging.INFO)

# Run your analysis
data_manager = OptiGobDataManager('./data/my_scenario.yaml')
optigob = Optigob(data_manager)
results = optigob.get_total_emissions_co2e_by_sector()
```

**Output:**
```
2024-11-05 10:15:32 - optigob.data_manager - WARNING - Parameter Validation Warning:
  split_gas=False but split_gas_frac=0.3
  The split_gas_frac parameter is IGNORED when split_gas=False.
  Set split_gas_frac=0 or remove it to avoid confusion.

2024-11-05 10:15:35 - optigob.livestock - INFO -
INFO: Zero CO2e budget for livestock.

Your scenario's non-livestock land uses produce NET EMISSIONS:
  Total non-livestock emissions:  7091.18 kt CO2e
  Net-zero target budget:            0.00 kt CO2e
  ─────────────────────────────────────────────────────
  CO2e budget available for livestock:     0.00 kt

...
```

---

### Example 2: Quiet Mode (Only Warnings and Errors)

```python
from optigob.logger import configure_logging
import logging

# Only show warnings and errors
configure_logging(level=logging.WARNING)

# INFO messages will not appear
# WARNING messages will still appear
```

**Use this when**: Running batch jobs where you only care about problems.

---

### Example 3: Save Logs to a File

```python
from optigob.logger import configure_logging
import logging

# Log everything to both console and file
configure_logging(
    level=logging.INFO,
    log_to_file='optigob_analysis.log'
)

# Now all messages go to console AND to optigob_analysis.log
```

**Use this when**: You want to review logs later or share them for debugging.

---

### Example 4: Simple Format (No Timestamps)

```python
from optigob.logger import configure_logging
import logging

# Simple format: just the message
configure_logging(
    level=logging.INFO,
    format_style="simple"
)

# Output will be just: "INFO: Zero CO2e budget for livestock..."
# Without: "2024-11-05 10:15:35 - optigob.livestock - INFO - ..."
```

**Use this when**: Working in Jupyter notebooks where timestamps clutter the output.

---

### Example 5: Advanced Control (For Experts)

```python
import logging

# Get the optigob logger directly
optigob_logger = logging.getLogger("optigob")

# Set different levels for different modules
logging.getLogger("optigob.livestock").setLevel(logging.WARNING)  # Quiet
logging.getLogger("optigob.forest").setLevel(logging.DEBUG)      # Verbose

# Or turn off all optigob logging
optigob_logger.setLevel(logging.CRITICAL)  # Only show critical errors
```

---

## Common Use Cases

### Use Case 1: Interactive Analysis (Jupyter Notebook)

You want to see important messages but keep output clean:

```python
from optigob.logger import configure_logging
import logging

# Show warnings but in simple format
configure_logging(
    level=logging.WARNING,
    format_style="simple"
)
```

---

### Use Case 2: Debugging a Problem

Something's wrong and you need to see everything:

```python
from optigob.logger import configure_logging
import logging

# Show EVERYTHING and save to file
configure_logging(
    level=logging.DEBUG,
    log_to_file='debug.log'
)

# Now you'll see internal operations
```

---

### Use Case 3: Batch Processing

Running 100 scenarios overnight:

```python
from optigob.logger import configure_logging
import logging

# Only warnings/errors, save to file
configure_logging(
    level=logging.WARNING,
    log_to_file='batch_run.log'
)

# Check batch_run.log in the morning to see if any warnings
```

---

### Use Case 4: Silent Mode

You know what you're doing and don't want any messages:

```python
import logging

# Turn off all optigob logging
logging.getLogger("optigob").setLevel(logging.CRITICAL)

# Now you'll only see critical failures
```

---

## Under the Hood (Technical Details)

### How We Implemented Logging

#### 1. Created a Logger Module (`src/optigob/logger.py`)

This module provides two functions:

- **`get_logger(name)`**: Returns a logger for a specific module
- **`configure_logging(...)`**: Quick setup with sensible defaults

#### 2. Each Module Gets a Logger

At the top of each module:

```python
from optigob.logger import get_logger

logger = get_logger("livestock")  # Creates 'optigob.livestock' logger
```

#### 3. Replaced Print/Warnings with Logger Calls

**Before:**
```python
print("INFO: Zero CO2e budget for livestock...")
warnings.warn("Parameter ignored", UserWarning)
```

**After:**
```python
logger.info("Zero CO2e budget for livestock...")
logger.warning("Parameter ignored")
```

### What Changed from Our Previous Implementation

| Old Approach | New Approach | Why Changed |
|-------------|--------------|-------------|
| `raise ValueError(...)` for CH4 exhaustion | `logger.warning(...)` and continue | Consistent with CO2e behavior, allows exploration |
| `warnings.warn(...)` for parameters | `logger.warning(...)` | Standard Python practice |
| `print(info_msg)` for zero budget | `logger.info(info_msg)` | User-controllable output |

### Logger Hierarchy

```
logging (Python root)
    └── optigob (our root)
            ├── optigob.data_manager
            ├── optigob.livestock
            ├── optigob.forest
            └── ...
```

By default, `configure_logging()`:
1. Sets level on `optigob` logger
2. Adds handler to write to console (and optionally file)
3. Sets `propagate=False` to avoid duplicate messages

---

## Troubleshooting

### I'm not seeing any messages!

**Solution 1**: Call `configure_logging()` before importing optigob modules:

```python
from optigob.logger import configure_logging
import logging

configure_logging(level=logging.INFO)  # Do this FIRST

from optigob.optigob import Optigob  # Then import
```

**Solution 2**: Check if you set level too high:

```python
# This will hide INFO messages:
configure_logging(level=logging.WARNING)

# Use INFO to see general messages:
configure_logging(level=logging.INFO)
```

---

### I'm seeing duplicate messages!

This can happen if you call `configure_logging()` multiple times.

**Solution**: Call it once at the start of your script:

```python
from optigob.logger import configure_logging
import logging

configure_logging(level=logging.INFO)  # Once only!

# Don't call it again in the same session
```

---

### Messages appear but with no formatting

You're seeing raw Python logging output. This means no handler was configured.

**Solution**: Call `configure_logging()`:

```python
from optigob.logger import configure_logging
import logging

configure_logging()  # Uses default INFO level with detailed format
```

---

### I want to see messages in Jupyter but not when I import in scripts

Use environment variables or configuration files:

```python
import os
import logging
from optigob.logger import configure_logging

# Only configure if running interactively
if 'IPYTHON' in dir() or os.getenv('JUPYTER'):
    configure_logging(level=logging.INFO)
else:
    configure_logging(level=logging.WARNING)
```

---

### The log file is too large

Log files grow over time. Either:

1. **Clear it periodically**: Delete the file manually
2. **Use rotating logs** (advanced):

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("optigob")
handler = RotatingFileHandler(
    'optigob.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=3            # Keep 3 old versions
)
logger.addHandler(handler)
```

---

## Summary: What You Need to Remember

1. **Call `configure_logging()` once** at the start of your script
2. **Choose your level**:
   - `logging.INFO` - see everything (default)
   - `logging.WARNING` - only warnings/errors (quiet)
   - `logging.DEBUG` - see internal operations (verbose)
3. **Save to file** if you want to review later: `log_to_file='mylog.log'`
4. **Messages you'll see**:
   - Parameter validation warnings
   - Zero budget explanations (INFO or WARNING)
   - Future: optimizer status, data loading, etc.

---

## Example: Complete Workflow

```python
# analysis.py - Complete example with logging

from optigob.logger import configure_logging
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
import logging

# Step 1: Configure logging
configure_logging(
    level=logging.INFO,
    log_to_file='my_analysis.log'
)

# Step 2: Run your analysis
data_manager = OptiGobDataManager('./data/scenario.yaml')
optigob = Optigob(data_manager)

# Step 3: Get results
emissions = optigob.get_total_emissions_co2e_by_sector()
livestock = optigob.get_livestock_population()

print("Analysis complete!")
print(f"Scenario dairy: {livestock['scenario']['dairy']}")
print(f"Scenario beef: {livestock['scenario']['beef']}")

# Check my_analysis.log for any warnings or messages
```

---

## Questions?

If you have questions about logging:
1. Review the examples in `tests/logging_example.py`
2. Check this guide
3. See Python's official logging documentation: https://docs.python.org/3/library/logging.html

**Remember**: Logging is there to help you understand what optigob is doing. You have full control over what you see!
