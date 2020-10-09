import time
import json
import pprint
import aiohttp
from mng.helper.argument_parser import check_subcommand, check_args

ACTIONS = {
    'create': [
        {'arg': '--instance-name',
            'value': 'instance_name'}
    ],
    'list': [],
    'help':[]}

HELP = {
    'create': {'text': 'Cria uma instância de um Host.',
               'args': [act['arg'] for act in ACTIONS['create']]},
    'list': {'text': 'Lista todas as instâncias de todos os Hosts.',
             'args': []},
}


async def instance(api, args):
    pp = pprint.PrettyPrinter(indent=2, compact=True, width=60, sort_dicts=False)

    if not check_subcommand(args.action, ACTIONS): return

    available, _ = check_args(vars(args), ACTIONS[args.action])
    if not available: return

    if args.action == 'help':
        pp.pprint(HELP)
        return
    
    if args.action == 'create':

        data_post = {
            "name": args.instance_name,
            "service": None if args.iservice_id == 0 else args.iservice_id,
            "host": None if args.ihost_id == 0 else args.ihost_id,
            "database": args.idatabase,
            "private_ip": args.iprivate_ip
        }

        if args.json:
            print(json.dumps(data_post))

        response = None
        try:
            response = await api.post_json('/api/cmdb/instance/', data_post)
            pp.pprint(response)
        except aiohttp.client_exceptions.ClientConnectorError:
            print('ops, API offline ou você não tem conexão com a internet...')

        return True if isinstance(response, dict) else False

    elif args.action == 'list':
        response = await api.get_json('/api/cmdb/instance/')
        [pp.pprint(_) for _ in response] if isinstance(response, list) else pp.pprint(response)

    return True


def setup_instance(subparsers):
    parser = subparsers.add_parser(
        'instance',
        help="operações relacionadas as Instâncias. [create, list]")

    parser.add_argument(
        'action',
        metavar="{%s}" % (', '.join([act[0] for act in ACTIONS.items()])),
        help="escolha um entre os subcommando válidos.")

    parser.add_argument(
        '--instance-name',
        dest='instance_name',
        metavar='NAME',
        help="Nome para instância de um host.")
    parser.add_argument(
        '--service-id',
        metavar='ID',
        dest='iservice_id',
        type=int,
        default=0,
        help="ID do serviço que a instância compõem.")
    parser.add_argument(
        '--host-id',
        metavar='ID',
        type=int,
        dest='ihost_id',
        default=0,
        help="ID do host que a instância pertence.")
    parser.add_argument(
        '--database-name',
        metavar='NAME',
        dest='idatabase',
        default='',
        help="Nome (identificador) do database da instância.")
    parser.add_argument(
        '--private-ip',
        metavar='IPv4/IPv6',
        dest='iprivate_ip',
        default='',
        help="IP privado da instância.")

    parser.set_defaults(func=instance)
