from ...commands import BasicCommand


class GraphCreateCommand(BasicCommand):

    NAME = 'graph'

    DESCRIPTION = BasicCommand.FROM_FILE()

    SYNOPSIS = ('mng graph create chn')

    EXAMPLES = ()

    SUBCOMMANDS = []

    ARG_TABLE = [
        {
            'name': 'graph-name',
            'help_text': ('Um nome que irá compor o uid do gráfico.'
                'Não utilizar acentos, substituir espaços em branco por'
                ' _ (underline) e tamanho máximo é 10 caracteres.'),
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
            'action': 'store',
            'required': False,
            'cli_type_name': 'string' #,
            # 'positional_arg': True
        },
    ]
