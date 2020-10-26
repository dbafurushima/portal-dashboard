from ...commands import BasicCommand
from .list import ChartListCommand
from .put import ChartPutCommand


class ChartsCommand(BasicCommand):
    NAME = 'charts'
    DESCRIPTION = BasicCommand.FROM_FILE()
    SYNOPSIS = ('mng charts')
    EXAMPLES = ()
    SUBCOMMANDS = [
        # {'name': 'list', 'command_class': ChartListCommand},
        # {'name': 'put', 'command_class': ChartPutCommand}
    ]

    ARG_TABLE = [
        {
            'name': 'cid',
            'help_text': 'ID do cliente para qual será o gráfico.',
            'action': 'store',
            'required': False,
            'cli_type_name': 'int',
            'positional_arg': True
        },
        {
            'name': 'chn',
            'help_text': ('Um nome que irá compor o uid do gráfico.'
                'Não utilizar acentos, substituir espaços em branco por'
                ' _ (underline) e tamanho máximo é 10 caracteres.'),
            'action': 'store',
            'required': False,
            'cli_type_name': 'string',
            'positional_arg': True
        },
    ]

    def _run_main(self, parsed_args, parsed_globals):
        print('ChartsCommand._run_main()')
