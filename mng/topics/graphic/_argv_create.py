ArgTableCreate = [
    {
        'name': 'graph_name',
        'help_text': ('Um nome que irá compor o uid do gráfico. \n'
            'Não utilizar acentos, substituir espaços em branco por \n'
            '_ (underline) e tamanho máximo é 10 caracteres.'),
        'action': 'store',
        'cli_type_name': 'string',
        'positional_arg': True
    },
    {
        'name': 'cid',
        'help_text': 'ID do cliente para qual será o gráfico.',
        'action': 'store',
        'required': False,
        'cli_type_name': 'int'
    },
    {
        'name': 'title',
        'help_text': 'Titulo que ficará na vertical a esquerda do gráfico. (yAxis_title)',
        'default': 'title',
        'action': 'store',
        'required': False,
        'cli_type_name': 'string',
        'group_name': 'fusioncharts'
    },
    {
        'name': 'caption',
        'help_text': 'Titulo para o gráfico. (capition)',
        'default': 'capition',
        'action': 'store',
        'required': False,
        'cli_type_name': 'string',
        'group_name': 'fusioncharts'
    },
    {
        'name': 'subcaption',
        'help_text': 'Subtitulo para o gráfico. (subcaption)',
        'default': 'subcaption',
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
        'name': 'stftime',
        'help_text': 'Um strftime que todos os dados deveram conter. (default=Y-m-d H-M)',
        'default': 'Y-m-d H-M',
        'action': 'store',
        'dest': 'stftime',
        'required': False,
        'cli_type_name': 'string',
        'group_name': 'fusioncharts'
    },
    {
        'name': 'type-graph',
        'help_text': 'Tipo do gráficos, valores aceitaveis [line] (yAxis_plot_type)',
        'default': 'line',
        'action': 'store',
        'dest': 'type_graph',
        'required': False,
        'cli_type_name': 'string',
        'group_name': 'fusioncharts'
    },
    {
        'name': 'description-value',
        'help_text': 'Descrição para valor na gráfico. (yAxis.plot.value)',
        'default': 'description value',
        'action': 'store',
        'dest': 'description_value',
        'required': False,
        'cli_type_name': 'string',
        'group_name': 'fusioncharts'
    },
    {
        'name': 'itemid',
        'help_text': 'ITEMID do gráfico no Zabbix para criação de uma replica do mesmo.',
        'default': None,
        'action': 'store',
        'dest': 'itemid',
        'required': False,
        'cli_type_name': 'integer',
        'group_name': 'zabbix'
    },
    {
        'name': 'n-data',
        'help_text': 'Número de registros que será consultado a API do Zabbix para criação do gráfico.',
        'default': None,
        'action': 'store',
        'dest': 'ndata',
        'required': False,
        'cli_type_name': 'integer',
        'group_name': 'zabbix'
    },
]