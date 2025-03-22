# optigob

A land use change and environmental assessment tool based on preconfigured data animal population numbers based on negative emissions allowance

## Installation

```bash
$ pip install optigob
```

## Usage

Here is a short example of how to use the `Optigob` class:

```python
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager


def main():
    data = './data/sip.yaml'
    # Initialize the data manager
    data_manager = OptiGobDataManager(data)

    # Create an instance of Optigob
    optigob = Optigob(data_manager)

    # Get baseline and target populations
    print(optigob.get_total_emissions_co2e_by_sector())

    print(optigob.get_total_emissions_co2e_by_sector_df())

    print(optigob.get_total_land_area_by_sector())

    print(optigob.get_total_land_area_by_sector_df())

if __name__ == '__main__':
    main()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`optigob` was created by Colm Duffy. It is licensed under the terms of the MIT license.

## Credits

`optigob` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
