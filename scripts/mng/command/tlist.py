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
    pp = pprint.PrettyPrinter(indent=2, compact=False, width=41, sort_dicts=False)

    if args.routes:
        pp.pprint({
            'routes': {'CMDB': ['/api/note/', '/api/inventory/', '/api/comment/', '/api/env/'],
            'Charts': ['/api_charts/charts/', '/api_charts/data/']}})
    elif args.item:
        # Anotações e comentários
        if 'note' in args.item:
            response = await api.get_json('/api/note/')
        elif 'comment' in args.item:

        # Inventário e clientes
            response = await api.get_json('/api/comment/')
        elif 'inventory' in args.item:
            response = await api.get_json('/api/inventory/')
        elif 'env' in args.item:
            response = await api.get_json('/api/env/')

        # Gráficos
        elif 'chart' in args.item:
            response = await api.get_json('/api_charts/charts/')
        elif 'data' in args.item:
            response = await api.get_json('/api_charts/data/')

        else: 
            return False

        [pp.pprint(_) for _ in response] if isinstance(response, list) else pp.pprint(response)
    else:
        print('arguments not found')
        return True

    return True


def setup_tlist(subparsers):
    parser = subparsers.add_parser('list', help="listar dados salvos. (notes, comments, hosts)")

    parser.add_argument('-i', '--item', help='nome da tabela para listagem')
    parser.add_argument('--routes', action='store_true', help='listar todas as rotas e nome de tabelas')

    parser.set_defaults(func=tlist)
