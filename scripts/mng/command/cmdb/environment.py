# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
import pprint
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def environment(api, args):
    pp = pprint.PrettyPrinter(indent=2, compact=True, width=40, sort_dicts=False)

    data_post = {
        "name": args.env_name,
        "inventory": args.inventory_id
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


def setup_environment(subparsers):
    parser = subparsers.add_parser('env', help="Criar ambientes.")
    parser.add_argument('env_name', help="Nome para o novo ambiênte.")
    parser.add_argument('inventory_id', help="ID o inventário ao qual o ambiênte irá pertencer.")
    parser.set_defaults(func=environment)
