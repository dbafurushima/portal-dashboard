import configparser
import pprint

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


def write_stdout(msg: str) -> None:
	print(msg)


def write_stdout_pprint(text: Any, indent=2, compact=False, width=51) -> None:
	pp = pprint.PrettyPrinter(indent=indent, compact=compact, width=width)
	pp.pprint(text)
