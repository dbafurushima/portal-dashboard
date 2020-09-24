# =============================================================================
#  IMPORTS
# =============================================================================
from mng.helper.log import app_log
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def configure(api, _):
    """Configure or update information in the tool configuration file
    """
    result = api.configure()
    return result['configured']

def setup_configure(subparsers):
    parser = subparsers.add_parser('configure', help="reconfigurar ferramenta.")
    parser.set_defaults(func=configure)
