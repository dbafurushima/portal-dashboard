# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
from pprint import pprint
from mng.helper.get_info import get_machine_infos
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def host(api, args):
    """Request for add note
    """
    data_post = get_machine_infos()

    if args.json:
        print(json.dumps(data_post))
    
    response = await api.post_json('/api/host/', data_post)
    pprint(response)
    
    return True if isinstance(response, dict) else False

def setup_host(subparsers):
    parser = subparsers.add_parser('host', help="cadastrar um novo host.")
    parser.set_defaults(func=host)
