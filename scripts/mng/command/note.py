# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
import pprint
import aiohttp
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def note(api, args):
    """Request for add note
    """
    pp = pprint.PrettyPrinter(indent=2, compact=False, sort_dicts=False)

    data_post = {
        "subject": args.subject,
        "timestamp": str(time.time()),
        "msg": args.text
    }

    if args.json:
        pp.pprint(data_post)

    response = None
    try:
        response = await api.post_json('/api/message/', data_post)
        pp.pprint(response)
    except aiohttp.client_exceptions.ClientConnectorError:
        print('ops, API offline ou você não tem conexão com a internet...')
    
    return True if isinstance(response, dict) else False

def setup_note(subparsers):
    parser = subparsers.add_parser('note', help="adicionar anotação.")
    parser.add_argument('subject', help='assunto da anotação')
    parser.add_argument('text', help='texto da anotação')
    parser.set_defaults(func=note)
