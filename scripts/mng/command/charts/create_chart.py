# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
import pprint
import uuid
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def create_chart(api, args):
    pp = pprint.PrettyPrinter(indent=2, compact=False, sort_dicts=False)

    step_uid = str(uuid.uuid4()).split('-')[1]
    step_name = args.name[:10].replace(' ', '_')

    strf = '-'.join(f'%{i}' for i in args.format.split('-'))
    if ' ' in strf:
        day, hour = strf.split(' ')
        nhour = ':'.join(f'%{i}' for i in hour.split(':'))
        strf = ' '.join([day, nhour])

    chart_json_data = {
        "client": args.clientid,
        "uid": f'{step_uid}_{step_name}',
        "caption_text": args.title,
        "yAxis_plot_value": args.plot_value,
        "yAxis_plot_type": args.yAxis_plot_type,
        "yAxis_title": args.name,
        "yAxis_format_prefix": args.prefix,
        "max_height": args.max_height,
        "max_width": args.max_width,
        "schema": '[{"name":"Time","type":"date","format":"%s"},{"name":"%s","type":"%s"}]' % \
            (strf, args.about, args.type_data),
        "columns": args.columns
    }

    pp.pprint(chart_json_data)
    continue_post = input('\nAs informações estão corretas? (Y/n) ') or 'Y'
    response = None
    if continue_post == 'Y':
        try:
            response = await api.post_json('/api_charts/charts/', chart_json_data)
            pp.pprint(response)
        except aiohttp.client_exceptions.ClientConnectorError:
            print('ops, API offline ou você não tem conexão com a internet...')

    return True if isinstance(response, dict) else False


def setup_create_chart(subparsers):
    parser = subparsers.add_parser('create-chart', help="Criação de gráficos dinâmicos.")
    parser.add_argument('clientid', type=int, help='ID do cliente para que o gráfico será gerado.')
    parser.add_argument('name', help=('Um nome que irá compor o uid do gráfico.'
                                      'Não utilizar acentos, substituir espaços em branco por'
                                      ' _ (underline) e tamanho máximo é 10 caracteres.'))

    parser.add_argument('--data-format', metavar='stftime', dest='format',
        help='Um strftime que todos os dados deveram conter. (default=Y-m-d)', default="Y-m-d")

    parser.add_argument('--type', metavar='TYPE', default='line', dest='yAxis_plot_type',
        help='Tipo do gráficos, valores aceitaveis [line] (yAxis_plot_type)')
    parser.add_argument('--type-data', metavar='TYPE_NAME', dest='type_data',
        help='Tipo dos dados do gráfico. (default=number)', default='number')

    parser.add_argument('--about', metavar='NAME', dest='about',
        help='Nome ou pequena frase que dirá sobre o que o gráfico é. Ex: Uso da CPU')

    
    parser.add_argument('-t','--title', metavar='NAME', dest='title', default='default', help='Titulo para o gráfico. (capition_text)')
    parser.add_argument('--plot-value', metavar='VALUE', dest='plot_value', default='default',
        help='yAxis plot value')
    parser.add_argument('-p', '--prefix', metavar='PREFIX', dest='prefix', default='',
        help='Prefixo para os valores. Ex: $ (yAxis_format_prefix)')
    
    parser.add_argument('--max-height', metavar='HEIGHT', dest='max_height', type=int, default=450,
        help='Tamanho máximo em pixel que o gráfico ocuparar no eixo X na página web.')
    parser.add_argument('--max-width', metavar='WIDTH', dest='max_width', type=int, default=700,
        help='Tamanho máximo em pixel que o gráfico ocupar no eixo Y na página web.')
    
    parser.add_argument('--columns', metavar='SIZE', dest='columns', default='12',
        help='Número de colunas que o gráfico ocupara na tela [6 - 12] (default 12), componente css do Bootstrap.')

    parser.set_defaults(func=create_chart)
