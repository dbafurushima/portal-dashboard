import os
import sys
import time
import sched
import psutil
import tempfile

from .utils import debug, save_working_status
from .utils_exceptions import ChoicePerTimeIsNotValid
from .utils_constants import (CHOICES_PER_TIME, DEFAULT_BACKUP, DEFAULT_THROW, DEFAULT_TURN,
    CHOICES_PRIORITY, DEFAULT_WORKER_PATH)
from ._load_work import WORKER


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

    def __start_running():
        while True:
            for i in range(turn):
                sch.enter(wait * i, priority, _cpu, argument=(_callback_cpu, backup))
            sch.run()
            if not loop: break
        WORKER.update(os.getpid())
        debug('ending process with pid %s' % os.getpid())

    debug('schedule cpu metrics to be sent %s times within a interval %s' % (turn, per))

    newpid = os.fork()

    if newpid == 0:
        WORKER.put(
            os.getpid(), {'turn': turn, 'per': per, 'backup': backup, 'priority': priority})
        __start_running()
        print('running', WORKER.running)
        print('stopped', WORKER.stopped)