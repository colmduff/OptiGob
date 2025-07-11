# Installation Guide

This guide will help you install and set up the `optigob` package for development or use in your own projects.

## Requirements

- Python 3.9 or higher
- [Poetry](https://python-poetry.org/) (recommended for development)
- (Optional) [pip](https://pip.pypa.io/) for standard installation
- (Optional) [conda](https://docs.conda.io/) for environment management

## Quick Install (for Users)

You can install the latest release from PyPI:

```bash
pip install optigob
```

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

3. **Install dependencies and the package in editable mode:**

    ```bash
    poetry install
    ```

4. **Activate the Poetry shell (optional):**

    ```bash
    poetry shell
    ```

5. **Run tests to verify your installation:**

    ```bash
    poetry run pytest
    ```

## Optional: Using Conda

If you prefer conda for environment management:

```bash
conda create -n optigob python=3.10
conda activate optigob
pip install poetry
poetry install
```

## Updating the Package

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

- [OptiGob Documentation](https://github.com/colmduff/OptiGob#readme)
- [Poetry Documentation](https://python-poetry.org/docs/)

If you have any questions or need help, please open an issue on GitHub or contact the maintainers.
