# Installation Guide

This guide will help you install and set up the `optigob` package for development or use in your own projects.

## Requirements

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/) (recommended for development)
- (Optional) [pip](https://pip.pypa.io/) for standard installation
- (Optional) [conda](https://docs.conda.io/) for environment management

## Quick Install (for Users)

You can install the latest release from PyPI:

```bash
pip install optigob
```

OptiGob requires a solver to run optimizations. The recommended option is
**HiGHS**, which you can install alongside optigob:

```bash
pip install "optigob[solvers]"
```

Alternatively, install just optigob and choose your own Pyomo-compatible solver
from the list provided below.


## Development Install (Recommended for Contributors)

1. **Clone the repository:**

    ```bash
    git clone https://github.com/colmduff/OptiGob.git
    cd OptiGob
    ```

2. **Install Poetry (if not already installed):**

    ```bash
    pip install poetry
    ```

3. **Install dependencies and the project (local-path install):**

    ```bash
    poetry install
    ```

    Poetry installs the project from your working directory (PEP 660
    editable-style), so local code changes are reflected immediately without
    a separate `-e` flag.

    To include the recommended HiGHS solver:

    ```bash
    poetry install -E solvers
    ```

4. **Run commands in the Poetry environment:**

    You have two options:

    - **Use `poetry run` prefix** (recommended for single commands):
      ```bash
      poetry run pytest
      poetry run python tests/example.py
      ```

    - **Or activate the Poetry shell** (for multiple commands in one session):
      ```bash
      poetry shell
      pytest
      python tests/example.py
      exit  # to leave the Poetry shell when done
      ```

## Optional: Using Conda

If you prefer conda for environment management:

```bash
conda create -n optigob python=3.12
conda activate optigob
pip install poetry
poetry install
```

To include the recommended HiGHS solver:

```bash
poetry install -E solvers
```

## Using Alternative Solvers

OptiGob requires a Pyomo-compatible solver to run optimizations. While **HiGHS** is
the recommended built-in option (install with `pip install highspy` or
`poetry install --with solvers`), you can use any solver supported by Pyomo.

To use a different solver, specify the `solver_name` parameter in your configuration:

```python
from optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

data = {
    # ... your scenario parameters ...
    'solver_name': 'glpk'  # Use GLPK instead of HiGHS
}
data_manager = OptiGobDataManager(data)
optigob = Optigob(data_manager)
```

For a complete list of available Pyomo-compatible solvers, see the
[Pyomo documentation](https://pyomo.readthedocs.io/en/stable/getting_started/solvers.html).

To use a specific solver, ensure it is installed in your environment, then
specify it via `solver_name`.

To update to the latest version from PyPI:

```bash
pip install --upgrade optigob
```

Or, if using Poetry in development mode:

```bash
poetry update
```

## Troubleshooting

- If you encounter issues with dependencies, try updating Poetry and pip.
- For platform-specific issues, please check the [GitHub Issues](https://github.com/colmduff/OptiGob/issues) page.

## Additional Resources

- [OptiGob Documentation](https://optigob.readthedocs.io/en/latest/)
- [Poetry Documentation](https://python-poetry.org/docs/)

If you have any questions or need help, please open an issue on GitHub or contact the maintainers.
