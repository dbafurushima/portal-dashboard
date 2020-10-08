import aiohttp
import time
import json
import pprint
from mng.helper.argument_parser import check_subcommand, check_args

ACTIONS = {
    'create': [
        {'arg': '--env-name',
            'value': 'env_name'},
        {'arg': '--inventory-id',
            'value': 'inventoryid'},
    ],
    'list': [],
    'help':[]}

HELP = {
    'create': {'text': 'Cria uma nova instância de Ambiente. (Envronment)',
               'args': [act['arg'] for act in ACTIONS['create']]},
    'list': {'text': 'Lista todos os ambientes de todos os clientes.',
             'args': []},
}


async def environment(api, args):
    pp = pprint.PrettyPrinter(indent=2, compact=True, width=60, sort_dicts=False)

    if not check_subcommand(args.action, ACTIONS): return

    available, _ = check_args(vars(args), ACTIONS[args.action])
    if not available: return

    if args.action == 'help':
        pp.pprint(HELP)
        return

    if args.action == 'create':
        data_post = {
            "name": args.env_name,
            "inventory": args.inventoryid
        }

        if args.json:
            print(json.dumps(data_post))
        
        response = None
        try:
            response = await api.post_json('/api/cmdb/environment/', data_post)
            pp.pprint(response)
        except aiohttp.client_exceptions.ClientConnectorError:
            print('ops, API offline ou você não tem conexão com a internet...')

        return True if isinstance(response, dict) else False

    elif args.action == 'list':
        response = await api.get_json('/api/cmdb/environment/')
        [pp.pprint(_) for _ in response] if isinstance(response, list) else pp.pprint(response)

    return True


def setup_environment(subparsers):
    parser = subparsers.add_parser(
        'env',
        help="operações relacionadas aos Ambientes (Envronment). [create, list]")

    parser.add_argument(
        'action',
        metavar="{%s}" % (', '.join([act[0] for act in ACTIONS.items()])),
        help="escolha um entre os subcommando válidos.")

    parser.add_argument(
        '--env-name',
        dest='env_name',
        metavar='NAME',
        help="Nome para o novo ambiênte.")
    parser.add_argument(
        '--inventory-id',
        dest='inventoryid',
        metavar='ID',
        help="ID o inventário ao qual o ambiênte irá pertencer.")

    parser.set_defaults(func=environment)
