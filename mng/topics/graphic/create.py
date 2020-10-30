from .fusion_charts import FusionChart
from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config


class GraphCreateCommand(BasicCommand):

    NAME = 'create'

    DESCRIPTION = BasicCommand.FROM_FILE('graph', 'create', '_description.rst')

    SYNOPSIS = BasicCommand.FROM_FILE('graph', 'create', '_synopsis.rst')

    EXAMPLES = BasicCommand.FROM_FILE('graph', 'create', '_examples.rst')

    SUBCOMMANDS = []

    ARG_TABLE = [
        {
            'name': 'graph_name',
            'help_text': ('Um nome que irá compor o uid do gráfico. \n'
                'Não utilizar acentos, substituir espaços em branco por \n'
                '_ (underline) e tamanho máximo é 10 caracteres.'),
            'action': 'store',
            'cli_type_name': 'string',
            # 'dest': 'graph_name',
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
    ]

    def _run_main(self, args, parsed_globals):
        # print('GraphCreateCommand._run_main().args: %s' % args)
        # print('GraphCreateCommand._run_main().parsed_globals: %s' % parsed_globals)
        # print()
        # print(vars(args))

        fc = FusionChart(
            name=args.graph_name,
            title=args.title,
            caption=args.caption,
            subcaption=args.subcaption,
            prefix=args.prefix,
            format=args.stftime,
            type_graph=args.type_graph,
            description_value=args.description_value
        )

        url = 'http://%s:%s/api/charts/charts/' % (lookup_config('address_api'), lookup_config('port_api'))

        fc.pprint
        print(url)
        response = request(url, fc.__dict__, method='POST', headers={'Authorization': 'Basic %s' % lookup_config('base64auth')})
        print(response)
