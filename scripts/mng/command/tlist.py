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
        pp.pprint({'routes': [('api', {'note': '/api/note', 'comment': '/api/comment'}),
                  ('cmdb', {'inventory': '/api/cmdb/inventory/', 'env': '/api/cmdb/environment/',
                           'service': '/api/cmdb/service/', 'instance': '/api/cmdb/instance/',
                           'host': '/api/cmdb/host/'}),
                  ('charts', {'chart': '/api/charts/charts/', 'data': '/api/charts/data/'})]})

    elif args.item:
        # Anotações e comentários
        if 'note' in args.item:
            response = await api.get_json('/api/note/')
        elif 'comment' in args.item:
            response = await api.get_json('/api/comment/')

        # Inventário e clientes
        elif 'inventory' in args.item:
            response = await api.get_json('/api/cmdb/inventory/')
        elif 'env' in args.item:
            response = await api.get_json('/api/cmdb/environment/')
        elif 'service' in args.item:
            response = await api.get_json('/api/cmdb/service/')
        elif 'host' in args.item:
            response = await api.get_json('/api/cmdb/host/')
        elif 'instance' in args.item:
            response = await api.get_json('/api/cmdb/instance/')

        # Gráficos
        elif 'chart' in args.item:
            response = await api.get_json('/api/charts/charts/')
        elif 'data' in args.item:
            response = await api.get_json('/api/charts/data/')

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
