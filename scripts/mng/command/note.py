# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
from pprint import pprint
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def note(api, args):
    """Request for add note
    """
    data_post = {
        "subject": args.subject,
        "timestamp": str(time.time()),
        "msg": args.text
    }

    if args.json:
        print(json.dumps(data_post))

    response = await api.post_json('/api/message/', data_post)
    pprint(response)
    return True if isinstance(response, dict) else False

def setup_note(subparsers):
    parser = subparsers.add_parser('note', help="adicionar anotação.")
    parser.add_argument('subject', help='assunto da anotação')
    parser.add_argument('text', help='texto da anotação')
    parser.set_defaults(func=note)
