import sched
from .utils_constants import (DEFAULT_BACKUP, DEFAULT_THROW, DEFAULT_TURN, CHOICES_PRIORITY)


def mem(
        graph: int or str,
        turn: int = DEFAULT_TURN,
        per: str = 'second', # CHOICES_PER_TIME.keys()[3],
        backup: bool = DEFAULT_BACKUP,
        throw: bool = DEFAULT_THROW,
        priority: int = CHOICES_PRIORITY[0],
        sch: sched.scheduler = None) -> None:
    pass