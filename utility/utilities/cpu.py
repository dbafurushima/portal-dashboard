import sys
import sched
import time
import psutil

from .utils_exceptions import ChoicePerTimeIsNotValid
from .utils_constants import (CHOICES_PER_TIME, DEFAULT_BACKUP, DEFAULT_THROW, DEFAULT_TURN,
    CHOICES_PRIORITY)


def _callback_cpu(cpu_usage: int) -> None:
    print(cpu_usage)


def cpu(
        turn: int = DEFAULT_TURN,
        per: str = 'second', # CHOICES_PER_TIME.keys()[3],
        backup: bool = DEFAULT_BACKUP,
        throw: bool = DEFAULT_THROW,
        priority: int = CHOICES_PRIORITY[0],
        sch: sched.scheduler = None) -> None:

    def _cpu(callback):
        callback(
            psutil.cpu_percent(interval=1))

    sch = sched.scheduler(time.time, time.sleep) if sch is None else sch

    try:
        wait = CHOICES_PER_TIME[per]
    except KeyError:
        raise ChoicePerTimeIsNotValid()

    turn, loop = (1, True) if turn <= 0 else (turn, False)

    while True:
        for i in range(turn):
            sch.enter(wait * i, priority, _cpu, argument=(_callback_cpu,))
        sch.run()
        if not loop: break

"""
sch = sched.scheduler(time.time, time.sleep)

def print_time(a='default'):
    print("From print_time", time.time(), a)

def print_some_times():
    print(time.time())
    sch.enter(10, 1, print_time)
    sch.enter(5, 2, print_time, argument=('positional',))
    sch.enter(5, 1, print_time, kwargs={'a': 'keyword'})
    sch.run()
    print(time.time())

print_some_times()


print(psutil.cpu_times())
# scputimes(user=77482.65625, system=26069.40625, idle=210989.296875, interrupt=2322.171875, dpc=1059.484375)
print(psutil.cpu_percent(interval=1))
# 30.9
print(psutil.cpu_percent(interval=1, percpu=True))
# [13.8, 31.2, 23.4, 20.3]

mem = psutil.virtual_memory()
print(mem.available)
# 2320539648
print(mem.percent)
# 72.1
print(mem.free)
# 2359754752

print(psutil.disk_partitions())
# [sdiskpart(device='C:\\', mountpoint='C:\\', fstype='NTFS', opts='rw,fixed')]
print(psutil.disk_usage('C:\\'))
# sdiskusage(total=225638981632, used=179749240832, free=45889740800, percent=79.7)

print(psutil.disk_io_counters(perdisk=True))
# {'PhysicalDrive0': sdiskio(read_count=2195561, write_count=1171751, read_bytes=59462397440, write_bytes=40137938432, read_time=12511, write_time=1888)}

"""