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
        '\n'
        'Listando todos os gráficos já criados\n'
        '\n'
        "   [ { 'caption': 'CPU Analysis',\n"
        "       'client': None,\n"
        "       'id': 11,\n"
        "       'schema': '[{\"name\": \"Time\", \"type\": \"date\", \"format\": '\n"
        '                 "%Y-%m-%d %H:%M"}, {"name": "title", \n'
        '                 "type": "number"}]\n'
        "       'subcaption': 'Usage',\n"
        "       'uid': '319a_usage_cpu_vm0',\n"
        "       'yAxis_format_prefix': '%/min',\n"
        "       'yAxis_plot_type': 'line',\n"
        "       'yAxis_plot_value': 'usage cpu is',\n"
        "       'yAxis_title': 'usage_cpu_vm0'}]\n"
    )

    SUBCOMMANDS = [
        {'name': 'create', 'command_class': GraphCreateCommand},
        {'name': 'list', 'command_class': GraphListCommand},
        {'name': 'put', 'command_class': GraphPutCommand},
    ]

    ARG_TABLE = []

    def _run_main(self, parsed_args, parsed_globals):
        self._display_help(parsed_args, parsed_globals)
