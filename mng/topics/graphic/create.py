from ...commands import BasicCommand


class GraphCreateCommand(BasicCommand):

    NAME = 'graph'

    DESCRIPTION = BasicCommand.FROM_FILE()

    SYNOPSIS = BasicCommand.FROM_FILE('graph', 'create', '_synopsis.rst') # BasicCommand.FROM_FILE()  # ('mng graph create chn')

    EXAMPLES = BasicCommand.FROM_FILE('graph', 'create', '_examples.rst')

    SUBCOMMANDS = []

    ARG_TABLE = [
        {
            'name': 'graph-name',
            'help_text': ('Um nome que irá compor o uid do gráfico. '
                'Não utilizar acentos, substituir espaços em branco por '
                '_ (underline) e tamanho máximo é 10 caracteres.'),
            'action': 'store',
            # 'required': True,
            'cli_type_name': 'string',
            'positional_arg': True
        },
        {
            'name': 'cid',
            'help_text': 'ID do cliente para qual será o gráfico.',
            'action': 'store',
            'required': False,
            'cli_type_name': 'int' #,
            # 'positional_arg': True
        },
        {
            'name': 'title',
            'help_text': 'Titulo para o gráfico. (capition_text)',
            'default': 'default',
            'action': 'store',
            'required': False,
            'cli_type_name': 'string',
            'group_name': 'fusioncharts'
        },
        {
            'name': 'prefix',
            'help_text': 'Prefixo para os valores. Ex: $ (yAxis_format_prefix)',
            'default': '',
            'action': 'store',
            'required': False,
            'cli_type_name': 'string',
            'group_name': 'fusioncharts'
        },
        {
            'name': 'data-format',
            'help_text': 'Um strftime que todos os dados deveram conter. (default=Y-m-d H-M)',
            'default': 'Y-m-d H-M',
            'action': 'store',
            'dest': 'format',
            'required': False,
            'cli_type_name': 'string',
            'group_name': 'fusioncharts'
        },
    ]

    def _run_main(self, args, parsed_globals):
        print('GraphCreateCommand._run_main()')