# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
import pprint
import aiohttp
from mng.helper.get_info import get_machine_infos
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def host(api, args):
    """Request for add note
    """
    pp = pprint.PrettyPrinter(indent=2, compact=False, sort_dicts=False)

    data_post = get_machine_infos()

    if args.json:
        print(json.dumps(data_post))
    
    response = None
    try:
        response = await api.post_json('/api/host/', data_post)
        pp.pprint(response)
    except aiohttp.client_exceptions.ClientConnectorError:
        print('ops, API offline ou você não tem conexão com a internet...')

    return True if isinstance(response, dict) else False

def setup_host(subparsers):
    parser = subparsers.add_parser('host', help="cadastrar um novo host.")
    parser.set_defaults(func=host)
