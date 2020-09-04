import os
import platform
import socket
import psutil


def get_machine_infos() -> bool:
    cpufreq = psutil.cpu_freq()
    return {
        'os_name': os.name,
        'arch': platform.machine(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'hostname': socket.gethostname(),
        'ram': str(round(psutil.virtual_memory().total / (1024.0 **3))),
        'cores': psutil.cpu_count(logical=True),
        'frequency': f'{cpufreq.max:.2f}'
    }


if __name__ == '__main__':
    print(get_machine_infos())
