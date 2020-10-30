import configparser

from . import config_path

from typing import Any


def lookup_config(name) -> Any or None:
    # Then try to look up the variable in the config file.
    config = configparser.ConfigParser()
    config.read(config_path)
    value = config['default'][name]

    if value is not None:
        return value
    
    return None
