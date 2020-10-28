from ...commands import BasicCommand
from .create import GraphCreateCommand
from .list import GraphListCommand
from .put import GraphPutCommand


class GraphicCommand(BasicCommand):
    NAME = 'graph'

    DESCRIPTION = BasicCommand.FROM_FILE()

    SYNOPSIS = ('mng graph {create, list, put}')

    EXAMPLES = ()

    SUBCOMMANDS = [
        {'name': 'create', 'command_class': GraphCreateCommand},
        {'name': 'list', 'command_class': GraphListCommand},
        {'name': 'put', 'command_class': GraphPutCommand},
    ]

    ARG_TABLE = []

    def _run_main(self, parsed_args, parsed_globals):
        self._display_help(parsed_args, parsed_globals)
