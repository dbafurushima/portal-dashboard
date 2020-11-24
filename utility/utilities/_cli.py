from .cpu import cpu
from .utils_exceptions import (ResourceNotIsValid)
from .utils_constants import (CHOICES_TYPE_RESOURCE)


def _cli(
        resource: str,
        turn: int = None,
        per: str = None,
        backup: bool = None) -> None:

    if resource not in CHOICES_TYPE_RESOURCE:
        raise ResourceNotIsValid

    if resource.lower() == 'cpu':
        cpu(turn=turn, per=per, backup=backup, throw=False)