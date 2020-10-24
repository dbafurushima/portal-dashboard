from argparse import ArgumentParser
from mng import __version__
from .log import app_log, log_enable_debug, log_enable_logging

from typing import Dict, Any, List, Tuple

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

MNG_CLI_MESSAGE = (
    'MNG CLI é um utilitário linha de comando multiplataforma\n'
    'escrito em python, utilizado para auxiliar a aplicação web *portald* para \n'
    'trazer uma máxima flexibilidade. \n'
    'instruções de instalação em: https://github.com/dbafurushima/portal-dashboard'
)

USAGE = (
    "mng [options] <command> <subcommand> "
    "[parameters]\n"
)

EXAMPLE_USAGE = (
    "Ex. Criar um novo objeto Host: \n\t$ mng --debug host create --inventory-id 1"
)


def check_subcommand(subcommand: Any, list_of_subcommands: Dict[str, list]) -> bool:
    """Verifica de o usuário passou um subcomando válido

    Args:
        subcommand (Any): [description]
        list_of_subcommands (Dict[str, list]): [description]

    Returns:
        bool: [description]
    """
    if subcommand in [act[0] for act in list_of_subcommands.items()]:
        return True
    print(' ❌ Ops... escolha uma ação válida.')
    return False

def check_args(args: Dict[str, Any], expected: List[str]) -> Tuple[bool, List[str]]:
    """Checa de o script foi chamado com todos os argumentos
    necessário, caso não será retornado uma lista com os que estão faltando.

    Args:
        args (Dict[str, Any]): [description]
        expected (List[str]): [description]

    Returns:
        Tuple[bool, List[str]]: [description]
    """
    if not expected:
        return (True, [])

    lack_of_arguments = list(map(lambda exp: exp['arg'],
        list(filter(lambda exp: args.get(exp['value'], None) is None, expected))))

    if lack_of_arguments:
        print('os seguintes comandos são necessários: \n\t%s' % ('\n\t'.join(lack_of_arguments)))
    return (False, lack_of_arguments) if lack_of_arguments else (True, [])


class MNGArgumentParser(ArgumentParser):
    """A specialised argument parser to define common arguments
    """
    def __init__(self, *args, **kwargs):
        self._banner = kwargs.get('banner')
        if self._banner:
            del kwargs['banner']
        super().__init__(*args, **kwargs)
        self.add_argument('-j', '--show-json', dest='json', action='store_true', help="exibir json do data_post da requisição para API.")
        # self.add_argument('-q', '--quiet', action='store_true', help="disable logging")
        self.add_argument('-d', '--debug', action='store_true', help="enable debug messages.")

    def parse_args(self):
        """Print the banner, parse arguments and configure some helpers using generic arguments
        """
        args = super().parse_args()
        log_enable_debug(args.debug)
        if self._banner and args.debug:
            print(self._banner)
        # log_enable_logging(not args.quiet)
        # app_log.debug(args)
        return args
