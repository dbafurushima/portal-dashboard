# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
import pprint
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def service(api, args):
    pp = pprint.PrettyPrinter(indent=2, compact=True, width=40, sort_dicts=False)

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


def setup_service(subparsers):
    parser = subparsers.add_parser('service', help="Criar um serviço final.")

    parser.add_argument('service_name', help="Nome para o novo serviço.")
    parser.add_argument('port', type=int, help="Porta que o serviço irá utilizar.")
    parser.add_argument('--dns', metavar='NAME', default='', help="DNS/IP do serviço, pode ser externo ou interno.")

    parser.set_defaults(func=service)
