import os
import sys
import time
import sched
import psutil
import tempfile

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

    def _cpu(callback, bk: bool = False):
        hit = psutil.cpu_percent(interval=1)
        callback(hit)

    sch = sched.scheduler(time.time, time.sleep) if sch is None else sch

    try:
        wait = CHOICES_PER_TIME[per]
    except KeyError:
        raise ChoicePerTimeIsNotValid()

    turn, loop = (1, True) if turn <= 0 else (turn, False)

    while True:
        for i in range(turn):
            sch.enter(wait * i, priority, _cpu, argument=(_callback_cpu, backup))
        sch.run()
        if not loop: break