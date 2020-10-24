import time
import json
import pprint
import aiohttp

from mng.helper.argument_parser import check_subcommand, check_args

ACTIONS = {
    'create': [
        {'arg': '--service-name',
            'value': 'service_name'},
        {'arg': '--port',
            'value': 'port'},
    ],
    'update': [
        {'arg': '--service-id',
            'value': 'serviceid'},
        {'arg': '--key',
            'value': 'key'},
        {'arg': '--value',
            'value': 'value'},
    ],
    'list': [],
    'help':[]}

HELP = {
    'create': {'text': 'Cria um serviço final. Que pode ser composto '
                       'Por várias Instâncias',
               'args': [act['arg'] for act in ACTIONS['create']]},
    'update': {'text': 'Atualizar algum campo do objeto. Pode ser utilizado '
               'para relacionar objetos 1-N.',
               'args': [act['arg'] for act in ACTIONS['update']]},
    'list': {'text': 'Lista todos os serviços de todos os clientes.',
             'args': []},
}


async def service(api, args):
    pp = pprint.PrettyPrinter(indent=2, compact=True, width=60)

    if not check_subcommand(args.action, ACTIONS): return

    available, _ = check_args(vars(args), ACTIONS[args.action])
    if not available: return

    if args.action == 'help':
        pp.pprint(HELP)
        return

    if args.action == 'create':

        data_post = {
            "name": args.service_name,
            "port": args.port,
            "dns": "" if not args.dns else args.dns
        }

        if args.json:
            print(json.dumps(data_post))

        response = None
        try:
            response = await api.post_json('/api/cmdb/service/', data_post)
            pp.pprint(response)
        except aiohttp.client_exceptions.ClientConnectorError:
            print('ops, API offline ou você não tem conexão com a internet...')
        return True if isinstance(response, dict) else False

    elif args.action == 'list':
        response = await api.get_json('/api/cmdb/service/')
        [pp.pprint(_) for _ in response] if isinstance(response, list) else pp.pprint(response)

    elif args.action == 'update':
        service = await api.get_json('/api/cmdb/service/%s/' % args.serviceid)
        print('change %s=%s to %s=%s' % (args.key, service[args.key], args.key, args.value))
        icontinue = input('Tem certeza que deseja continuar? (Y/n) ') or 'Y'
        if icontinue != 'Y':
            return False

        service.update({args.key: int(args.value)})

        response = None
        try:
            response = await api.put_json('/api/cmdb/service/%s/' % args.serviceid, service)
            pp.pprint(response)
        except aiohttp.client_exceptions.ClientConnectorError:
            print('ops, API offline ou você não tem conexão com a internet...')
        return True if isinstance(response, dict) else False

    return True


def setup_service(subparsers):
    parser = subparsers.add_parser(
        'service',
        help="operações relacionadas aos Serviços. [create, list]")

    parser.add_argument(
        'action',
        metavar="{%s}" % (', '.join([act[0] for act in ACTIONS.items()])),
        help="escolha um entre os subcommando válidos.")

    parser.add_argument(
        '--service-name',
        metavar='NAME',
        dest='service_name',
        help="Nome para o novo serviço.")
    parser.add_argument(
        '--port',
        type=int,
        metavar='NUM',
        help="Porta que o serviço irá utilizar.")
    parser.add_argument(
        '--dns',
        metavar='NAME',
        default='',
        help="DNS/IP do serviço, pode ser externo ou interno.")
    parser.add_argument(
        '-s',
        '--service-id',
        dest='serviceid',
        metavar='ID',
        type=int,
        help="ID do Serviço para edição de um campo.")
    parser.add_argument(
        '-k',
        '--key',
        metavar='KEY',
        dest='key',
        type=str,
        help="nome do campo que terá o valor alterado.")
    parser.add_argument(
        '-v',
        '--value',
        metavar='VALUE',
        dest='value',
        type=str,
        help="novo valor para o campo.")

    parser.set_defaults(func=service)
