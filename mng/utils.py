import configparser
import pprint
import os
import platform
import socket
import psutil

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


def get_machine_infos() -> bool:
    try:
        cpufreq = psutil.cpu_freq()
        cpufreq_max = f'{cpufreq.max:.2f}'
    except:
        cpufreq_max = None

    return {
        'os_name': os.name,
        'arch': platform.machine(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'hostname': socket.gethostname(),
        'ram': str(round(psutil.virtual_memory().total / (1024.0 **3))),
        'cores': psutil.cpu_count(logical=True),
        'frequency': cpufreq_max,
        'private_ip': socket.gethostbyname(socket.gethostname())
    }
