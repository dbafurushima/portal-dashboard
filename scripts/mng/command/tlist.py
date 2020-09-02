# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
from pprint import pprint
from mng.helper.formatting import format_dict2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def tlist(api, args):
    """Request for list tables
    """
    if 'message' in args.table:
        response = await api.get_json('/api/message/')
    elif 'comment' in args.table:
        response = await api.get_json('/api/comment/')
    else:
        return False

    [print(format_dict2str(_)) for _ in response] if isinstance(response, list) else pprint(response)
    return True


def setup_tlist(subparsers):
    parser = subparsers.add_parser('list', help="listar dados salvos. (message ou comment)")
    parser.add_argument('table', help='nome da tabela para listagem')
    parser.set_defaults(func=tlist)
