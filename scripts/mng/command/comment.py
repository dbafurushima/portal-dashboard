# =============================================================================
#  IMPORTS
# =============================================================================
from pprint import pprint
import json
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def comment(api, args):
    """Request for add comment
    """
    data_post = {
        "message": args.message,
        "comment": args.comment
    }

    if args.json:
        print(json.dumps(data_post))

    response = await api.post_json('/api/comment/', data_post)
    pprint(response)
    return True if isinstance(response, dict) else False

def setup_comment(subparsers):
    parser = subparsers.add_parser('comment', help="adicionar comentário a anotação.")
    parser.add_argument('message', help='id da mensagem', type=int)
    parser.add_argument('comment', help='comentário na mensagem')
    parser.set_defaults(func=comment)
