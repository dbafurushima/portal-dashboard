import time
import json
import pprint
import aiohttp

from mng.helper.get_info import get_machine_infos
from mng.helper.argument_parser import check_subcommand, check_args

ACTIONS = {
    'create': [
        {'arg': '--inventory-id',
        'value': 'inventory'}],
    'list': [],
    'update': [
        {'arg': '--iv-key',
        'value': 'ivkey'},
        {'arg': '--iv-value',
        'value': 'ivvalue'}],
    'help':[]}

HELP = {
    'create': {'text': 'Criar um objeto Host a partir das configurações '
               'da sua máquina.',
               'args': [act['arg'] for act in ACTIONS['create']]},
    'list': {'text': 'Listar todos os Hosts que existem na base de dados.',
             'args': []},
    'update': {'text': 'Atualizar algum campo do objeto. Pode ser utilizado '
               'para relacionar objetos 1-N.',
               'args': [act['arg'] for act in ACTIONS['update']]}
}


async def host(api, args):
    pp = pprint.PrettyPrinter(indent=2, compact=True, width=71, sort_dicts=False)

    if not check_subcommand(args.action, ACTIONS): return
    
    available, _ = check_args(vars(args), ACTIONS[args.action])
    if not available: return
    
    if args.action == 'help':
        pp.pprint(HELP)
        return
    
    if args.action == 'create':
        data_post = get_machine_infos()
        data_post['enterprise'] = args.inventory

        if args.json:
            print(json.dumps(data_post))

        response = None
        try:
            response = await api.post_json('/api/host/', data_post)
            pp.pprint(response)
        except aiohttp.client_exceptions.ClientConnectorError:
            print('ops, API offline ou você não tem conexão com a internet...')
        return True if isinstance(response, dict) else False
    elif args.action == 'list':
        response = await api.get_json('/api/cmdb/host/')
        [pp.pprint(_) for _ in response] if isinstance(response, list) else pp.pprint(response)

    return True

def setup_host(subparsers):
    parser = subparsers.add_parser('host', help="operações relacionadas aos hosts. [create, update, list]")

    parser.add_argument(
        'action',
        metavar="{%s}" % (', '.join([act[0] for act in ACTIONS.items()])),
        help="escolha um entre os subcommando válidos.")
    parser.add_argument(
        '--inventory-id',
        dest='inventory',
        type=int,
        help="id do inventário do cliente para cadastro.")
    parser.add_argument(
        '--iv-key',
        metavar='KEY',
        dest='ivkey',
        type=str,
        help="nome do campo que terá o valor alterado.")
    parser.add_argument(
        '--iv-value',
        metavar='VALUE',
        dest='ivvalue',
        type=str,
        help="novo valor para o campo.")

    parser.set_defaults(func=host)
