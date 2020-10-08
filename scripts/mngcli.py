#!/usr/bin/env python3
# -!- encoding:utf8 -!-

import argparse

from asyncio import get_event_loop

from mng import __version__
from mng.api import MNGApi
from mng.command import *
from mng.helper.log import app_log
from mng.helper.exception import MNGException
from mng.helper.argument_parser import MNGArgumentParser, USAGE, MNG_CLI_MESSAGE, EXAMPLE_USAGE


def parse_args():
    """Parse command line arguments
    """
    parser = MNGArgumentParser(
        description=MNG_CLI_MESSAGE,
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=52),
        epilog=EXAMPLE_USAGE)
    # -- add subparsers
    subparsers = parser.add_subparsers(
        dest='command',
        metavar='COMMAND',
        help=('O comando está relacionado a um item do sistema, \n'
              '\tselecione um da listagem a baixo e em seguida \n'
              '\tescolha uma operação.\n'))
    subparsers.required = True

    setup_init(subparsers)
    setup_configure(subparsers)
    
    setup_note(subparsers)
    setup_comment(subparsers)
    # setup_tlist(subparsers)

    # setup_create_chart(subparsers)
    # setup_upd_chart(subparsers)
    
    # setup_environment(subparsers)
    setup_host(subparsers)
    # setup_instance(subparsers)
    # setup_service(subparsers)

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


if __name__ == '__main__':
    exit(app())
