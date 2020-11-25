import sys
from .cpu import cpu
from .utils_exceptions import (ResourceNotIsValid)
from .utils_constants import (CHOICES_TYPE_RESOURCE, DEFAULT_API_USER, DEFAULT_API_PASSWD, DEFAULT_MESSAGE_SET_ENVVARS)


def _cli(
        graph: int,
        resource: str,
        turn: int = None,
        per: str = None,
        backup: bool = None) -> None:

    if resource not in CHOICES_TYPE_RESOURCE:
        raise ResourceNotIsValid

    if (DEFAULT_API_USER == 'None') or (DEFAULT_API_PASSWD == 'None'):
        sys.exit(DEFAULT_MESSAGE_SET_ENVVARS)

    if resource.lower() == 'cpu':
        cpu(graph=graph, turn=turn, per=per, backup=backup, throw=False)