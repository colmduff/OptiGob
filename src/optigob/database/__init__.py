import os


def get_local_dir():
    """Gets the directory containing this script

    Returns:
        str: full path to the the script's directory
    """
    return os.path.dirname(os.path.realpath(__file__))