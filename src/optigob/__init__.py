# read version from installed package
from importlib.metadata import version
__version__ = version("optigob")

from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
from optigob.input_helper import InputHelper
from optigob.logger import configure_logging, get_logger