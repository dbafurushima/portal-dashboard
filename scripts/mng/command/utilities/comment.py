# =============================================================================
#  IMPORTS
# =============================================================================
import pprint
import json
import aiohttp
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def comment(api, args):
    """Request for add comment
    """
    pp = pprint.PrettyPrinter(indent=2, compact=False, sort_dicts=False)

    data_post = {
        "message": args.message,
        "comment": args.comment
    }

    if args.json:
        pp.pprint(data_post)

    response = None
    try:
        response = await api.post_json('/api/comment/', data_post)
        pp.pprint(response)
    except aiohttp.client_exceptions.ClientConnectorError:
        print('ops, API offline ou você não tem conexão com a internet...')
    
    return True if isinstance(response, dict) else False

def setup_comment(subparsers):
    parser = subparsers.add_parser('comment', help="adicionar comentário a anotação.\n\n")
    parser.add_argument('message', help='id da mensagem', type=int)
    parser.add_argument('comment', help='comentário na mensagem')
    parser.set_defaults(func=comment)
