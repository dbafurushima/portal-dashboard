# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
import pprint
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def instance(api, args):
    pp = pprint.PrettyPrinter(indent=2, compact=True, width=40, sort_dicts=False)

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


def setup_instance(subparsers):
    parser = subparsers.add_parser('instance', help="Criar um instância de um Host.")
    parser.add_argument('instance_name', help="Nome para instância de um host.")
    parser.add_argument('--service-id', metavar='ID', dest='iservice_id', type=int, default=0, help="ID do serviço que a instância compõem.")
    parser.add_argument('--host-id', metavar='ID', type=int, dest='ihost_id', default=0, help="ID do host que a instância pertence.")
    parser.add_argument('--database-name', metavar='NAME', dest='idatabase', default='', help="Nome (identificador) do database da instância.")
    parser.add_argument('--private-ip', metavar='IPv4/IPv6', dest='iprivate_ip', default='', help="IP privado da instância.")
    parser.set_defaults(func=instance)
