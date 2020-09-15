# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
import pprint
from mng.helper.formatting import format_dict2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def tlist(api, args):
    """Request for list tables
    """
    pp = pprint.PrettyPrinter(indent=2, compact=False, sort_dicts=False)

    if args.routes:
        pp.pprint({
            'note': {
                'route': '/api/note/', 
                'method': 
                    ['GET', 'POST', 'PUT']
            },
            'comment': {
                'route': '/api/comment/', 
                'method': 
                    ['GET', 'POST', 'DELETE']
            },
            'inventory': {
                'route': '/api/inventory', 
                'method': 
                    ['GET', 'POST']
            }})
    elif args.table:
        if 'note' in args.table:
            response = await api.get_json('/api/note/')
        elif 'comment' in args.table:
            response = await api.get_json('/api/comment/')
        elif 'inventory' in args.table:
            response = await api.get_json('/api/inventory/')
        else: 
            return False

        [pp.pprint(_) for _ in response] if isinstance(response, list) else pp.pprint(response)
    else:
        print('arguments not found')
        return True

    return True


def setup_tlist(subparsers):
    parser = subparsers.add_parser('list', help="listar dados salvos. (notes, comments, hosts)")
    parser.add_argument('-t', '--table', help='nome da tabela para listagem')
    parser.add_argument('--routes', action='store_true', help='listar todas as rotas e nome de tabelas')
    parser.set_defaults(func=tlist)
