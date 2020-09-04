#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#===============================================================================
#  IMPORTS
#===============================================================================
from asyncio import get_event_loop
from mng import __version__
from mng.api import MNGApi
from mng.command import *
from mng.helper.log import app_log
from mng.helper.exception import MNGException
from mng.helper.argument_parser import MNGArgumentParser
# =============================================================================
#  GLOBALS
# =============================================================================
BANNER = r"""
 ███▄ ▄███▓ ███▄    █   ▄████ 
▓██▒▀█▀ ██▒ ██ ▀█   █  ██▒ ▀█▒
▓██    ▓██░▓██  ▀█ ██▒▒██░▄▄▄░
▒██    ▒██ ▓██▒  ▐▌██▒░▓█  ██▓
▒██▒   ░██▒▒██░   ▓██░░▒▓███▀▒ v{}
░ ▒░   ░  ░░ ▒░   ▒ ▒  ░▒   ▒ 
░  ░      ░░ ░░   ░ ▒░  ░   ░ 
░      ░      ░   ░ ░ ░ ░   ░ 
       ░            ░       ░  
""".format(__version__)
# =============================================================================
#  FUNCTIONS
# =============================================================================
def parse_args():
    """Parse command line arguments
    """
    parser = MNGArgumentParser(banner=BANNER, description="Um CLI para gerenciamento de inventários, hosts e notas.")
    # -- add subparsers
    subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')
    subparsers.required = True
    setup_init(subparsers)
    setup_configure(subparsers)
    setup_note(subparsers)
    setup_comment(subparsers)
    setup_tlist(subparsers)
    setup_host(subparsers)

    # -- parse args and pre-process if needed
    return parser.parse_args()

async def main():
    """Main function
    """
    args = parse_args()
    try:
        api = MNGApi()
        rcode = 0 if await args.func(api, args) else 1
    except MNGException as exc:
        app_log.critical(f"critical error: {exc.args[0]}")
        rcode = 1
    except:
        app_log.exception("Ouch... unhandled exception... (>_<)")
        rcode = 2
    return rcode

def app():
    """MNG-cli script entry point
    """
    loop = get_event_loop()
    rcode = loop.run_until_complete(main())
    loop.close()
    return rcode
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    exit(app())
