# =============================================================================
#  IMPORTS
# =============================================================================
# from os import getenv
# =============================================================================
#  FUNCTIONS
# =============================================================================
def init(api, args):
    """Initialize tool for use
    """
    pass

def setup_init(subparsers):
    parser = subparsers.add_parser('init', help="initialize tool for use.")
    parser.set_defaults(func=init)
