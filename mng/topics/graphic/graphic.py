from ...commands import BasicCommand
from .create import GraphCreateCommand
from .list import GraphListCommand
from .put import GraphPutCommand


class GraphicCommand(BasicCommand):
    NAME = 'graph'

    DESCRIPTION = BasicCommand.FROM_FILE()

    SYNOPSIS = (' $ mng graph {create, list, put}')

    EXAMPLES = (
        'Criar um gráfico para representar o uso de CPU da VM01\n'
        '\n'
        '   $ mng graph create usage_cpu --title "Usage CPU VM01" --prefix "%/s"\n'
        '\n'
        'Alimentar o gráfico criado acima\n'
        '\n'
        '   $ mng graph put "gid" "2020-11-04 21:03,01;2020-11-04 21:04,2"\n'
    )

    SUBCOMMANDS = [
        {'name': 'create', 'command_class': GraphCreateCommand},
        {'name': 'list', 'command_class': GraphListCommand},
        {'name': 'put', 'command_class': GraphPutCommand},
    ]

    ARG_TABLE = []

    def _run_main(self, parsed_args, parsed_globals):
        self._display_help(parsed_args, parsed_globals)
