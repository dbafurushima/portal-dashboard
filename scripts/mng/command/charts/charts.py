"""
Basic usage:

python mngcli.py charts create --clientid-to-chart 1 \
    --chart-name "usage_network" \
    --columns 10 \
    --prefix "/s" \
    --title "Usage Network per second" \
    --about "network" \
    --data-format "Y-m-d H:M:S"

python mngcli.py charts put --chartid 0 \ 
    --value "2020-10-08 20:10:04,14 2020-10-08 20:10:05,11 2020-10-08 20:10:06,12"
"""
import aiohttp
import asyncio
import re
import time
import json
import pprint
import uuid
import logging

from pathlib import Path
from functools import partial

from mng.helper.argument_parser import check_subcommand, check_args
from mng.helper.regexp import reDATATIME1, reDATATIME2, reDATATIME3, reDATATIME4

from rich.console import Console
from rich.markdown import Markdown

reXP = [reDATATIME1, reDATATIME2, reDATATIME3, reDATATIME4]

ACTIONS = {
    'create': [
        {'arg': '--clientid-to-chart',
            'value': 'clientid'},
        {'arg': '--chart-name',
            'value': 'chart_name'}
    ],
    'put': [
        {'arg': '--chartid',
            'value': 'chartid_to_put'},
        {'arg': '--value',
            'value': 'new_value'},
        {'arg': '--file',
            'value': 'file_with_data'},
    ],
    'list': [],
    'help':[]}

HELP = {
    'create': {'text': 'Cria um gráfico para um cliente. Para maior praticidade '
                       'foram definidos apenas dois parâmetros obrigatórios, mas '
                       'com os parâmetros opcionais pode obter maior customização.',
               'args': [act['arg'] for act in ACTIONS['create']]},
    'put': {'text': 'Adiciona dado(s) a um gráfico, deverá ser utilizado com o parâmetro'
                       '--value ou --file que define a origem dos dados.',
               'args': [act['arg'] for act in ACTIONS['put']]},
    'list': {'text': 'Lista todos os gráficos existentes no *portald*.',
             'args': []},
}


async def charts(api, args):
    pp = pprint.PrettyPrinter(indent=2, compact=True, width=71)

    if args.action == 'help':
        console = Console()
        with open(Path(__file__).parent.joinpath('../', '../', 'resources', 'CHARTS_HELP.md'), encoding="utf-8") as readme:
            markdown = Markdown(readme.read())
        console.print(markdown)
        return


    if not check_subcommand(args.action, ACTIONS): return

    available, _ = check_args(vars(args), ACTIONS[args.action])
    if not available: return
    
    if args.action == 'help':
        pp.pprint(HELP)
        return
    
    if args.action == 'create':

        step_uid = str(uuid.uuid4()).split('-')[1]
        step_name = args.chart_name[:10].replace(' ', '_')

        strf = '-'.join('%'+i for i in args.format.split('-'))
        if ' ' in strf:
            day, hour = strf.split(' ')
            nhour = ':'.join('%'+i for i in hour.split(':'))
            strf = ' '.join([day, nhour])

        re_data = re.compile(r'^%m')
        if re_data.match(strf):
            strf = '%Y-'+strf

        chart_json_data = {
            "client": args.clientid,
            "uid": '%s_%s' % (step_uid, step_name),
            "caption_text": args.title,
            "yAxis_plot_value": args.plot_value,
            "yAxis_plot_type": args.yAxis_plot_type,
            "yAxis_title": args.chart_name,
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
                response = await api.post_json('/api/charts/charts/', chart_json_data)
                pp.pprint(response)
            except aiohttp.client_exceptions.ClientConnectorError:
                print('ops, API offline ou você não tem conexão com a internet...')

        return True if isinstance(response, dict) else False
    
    elif args.action == 'put':
        if (not args.file_with_data) and (not args.new_value):
            print('Você deve utilizar a opção --value ou --file com os dados.')
            return False

        re_data = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')

        if args.new_value:
            for rexp in reXP:
                raw_data = re.findall(rexp, args.new_value)
                if raw_data: break
        else:
            path = Path(args.file_with_data)
            for rexp in reXP:
                raw_data = re.findall(rexp, open(path).read())
                if raw_data: break

        pp = pprint.PrettyPrinter(indent=2, compact=False)
        again = '[!] falha ao enviar valor %s, deseja tentar novamente ou continuar? (T)ry / (C)ontinue '

        try:
            chart_filter = {'value': int(args.chartid_to_put), 'key': 'chartid'}
        except ValueError:
            chart_filter = {'key': 'chartuid', 'value': args.chartid_to_put}

        if args.fix_index == 0:
            response = await api.get_json('/api/charts/data/filter/', [(chart_filter.get('key'), chart_filter.get('value'))])

            index = response[-1].get('index') + 1 if response else  0
            # if response:
            #    index = response[-1].get('index') + 1
            # else:
            #    index = 1
        else:
            index = args.fix_index

        failed = set()

        async def send_data(data):
            response = await api.post_json('/api/charts/data/', data)
            if response:
                return True
            else:
                failed.add(json.dumps(data))

        """
        async def try_again(response):
            if response:
                return
            choice = input(again % data) or 'T'
            if choice.lower() == 'c':
                failed.add(json.dumps(data_json))
                return
            response = await send_data('/api/charts/data/', data_json)
            return await try_again(response)
        """
        funcs = []

        for data in raw_data:
            if not re_data.match(data):
                # mudar para pegar ano atual
                data = '2020-'+data
            data_json = {
                "index": index,
                "value": data,
                "chart": int(args.chartid_to_put)
            }
            # response = await send_data('/api/charts/data/', data_json)
            # funcs.append(partial(send_data, data=data_json))
            funcs.append(data_json)

            # await try_again(response)s
            index += 1

        # print(tuple(funcs))
        # await asyncio.gather(
        #     *tuple(funcs)
        # )
        # completed, pending = await asyncio.wait(funcs)
        # loop = asyncio.get_event_loop()

        # for data in funcs:
        #     loop.create_task(send_data(data))

        # pending = asyncio.all_tasks()
        # group = asyncio.gather(*pending, return_exceptions=True)
        # results = loop.run_until_complete(group)
        MAX_CONN = 10

        def chunks(lista, n):
            for i in range(0, len(lista), n):
                yield lista[i:i + n]

        for raw_data in list(chunks(funcs, MAX_CONN)):
            coroutines = [send_data(data) for data in raw_data]
            completed, pending = await asyncio.wait(coroutines)

            for item in completed:
                pass

        if failed:
            coroutines = [send_data(json.loads(data)) for data in failed]
            completed, pending = await asyncio.wait(coroutines)
        else:
            print('[+] dados enviado com sucesso!')

    elif args.action == 'list':
        response = await api.get_json('/api/charts/charts/')
        [pp.pprint(_) for _ in response] if isinstance(response, list) else pp.pprint(response)

    return True


def setup_charts(subparsers):
    parser = subparsers.add_parser(
        'charts',
        help="operações relacionadas aos gráficos e dados do mesmo. [create, put, list]\n\n")

    parser.add_argument(
        'action',
        metavar="{%s}" % (', '.join([act[0] for act in ACTIONS.items()])),
        help="escolha um entre os subcommando válidos.")

    parser.add_argument(
        '-cid',
        '--clientid-to-chart',
        metavar='ID',
        dest='clientid',
        help='Cliente para qual será o gráfico. Apenas ele terá visualização.')

    parser.add_argument(
        '-chn',
        '--chart-name',
        metavar='NAME',
        dest='chart_name',
        help=('Um nome que irá compor o uid do gráfico.'
              'Não utilizar acentos, substituir espaços em branco por'
              ' _ (underline) e tamanho máximo é 10 caracteres.'))

    parser.add_argument(
        '-t',
        '--title',
        metavar='NAME',
        dest='title',
        default='default',
        help='Titulo para o gráfico. (capition_text)')

    parser.add_argument(
        '-p',
        '--prefix',
        metavar='PREFIX',
        dest='prefix',
        default='',
        help='Prefixo para os valores. Ex: $ (yAxis_format_prefix)')

    parser.add_argument(
        '-fmt',
        '--data-format',
        metavar='stftime',
        dest='format',
        default="Y-m-d H-M",
        help='Um strftime que todos os dados deveram conter. (default=Y-m-d H-M)')

    parser.add_argument(
        '-tch',
        '--type-chart',
        metavar='TYPE',
        default='line',
        dest='yAxis_plot_type',
        help='Tipo do gráficos, valores aceitaveis [line] (yAxis_plot_type)')

    parser.add_argument(
        '--type-data',
        metavar='TYPE',
        dest='type_data',
        default='number',
        help='Tipo dos dados do gráfico. (default=number)')

    parser.add_argument(
        '--about',
        metavar='NAME',
        dest='about',
        help='Nome ou pequena frase que dirá sobre o que o gráfico é. Ex: Uso da CPU')

    parser.add_argument(
        '--plot-value',
        metavar='VALUE',
        dest='plot_value',
        default='default',
        help='yAxis plot value.')
    
    parser.add_argument(
        '--max-height',
        metavar='HEIGHT',
        dest='max_height',
        type=int,
        default=450,
        help='Tamanho máximo em pixel que o gráfico ocuparar no eixo X na página web.')

    parser.add_argument(
        '--max-width',
        metavar='WIDTH',
        dest='max_width',
        type=int,
        default=700,
        help='Tamanho máximo em pixel que o gráfico ocupar no eixo Y na página web.')

    parser.add_argument(
        '--columns',
        metavar='SIZE',
        dest='columns',
        default='12',
        help='Número de colunas que o gráfico ocupara na tela [6 - 12] (default 12), componente css do Bootstrap.')
    
    parser.add_argument(
        '--chartid',
        dest='chartid_to_put',
        help="ID ou UID do gráfico onde o valor será adicionado.")

    parser.add_argument(
        '--value',
        type=str,
        default='',
        dest='new_value',
        help=("Valor a ser adicionado, deverá seguir a "
              "estrutura definida em *schema* na criação do gráfico."
              "Se você for enviar apenas um valor deverá ser separado "
              "por virgula, ex: 2020-10-1,90. Se for mais de um valor: "
              "\"2020-10-1,90 2020-10-2,60\","
              "utilizando espaço como separador."))

    parser.add_argument(
        '--file',
        type=str,
        default='',
        dest='file_with_data',
        help='Caminho do arquivo com os valores.')

    parser.add_argument(
        '--index',
        type=int,
        default=0,
        dest='fix_index',
        help="Escolher o index do valor manualmete.")

    parser.set_defaults(func=charts)
