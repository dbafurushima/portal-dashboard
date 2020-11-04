import sys

from .argparser import MainArgParser, CommandAction, ArgTableArgParser
from .topics.configure.configure import ConfigureCommand
from .topics.graphic.graphic import GraphicCommand
from .topics.environment import EnvironmentCommand
from .topics.man import ManCommand
from .version import __version__

from collections import OrderedDict


def main():
    command_table = OrderedDict()
    argument_table = OrderedDict()
    description = None

    command_table['help'] = ManCommand(command_table)

    command_table['configure'] = ConfigureCommand()
    command_table['graph'] = GraphicCommand()
    command_table['environment'] = EnvironmentCommand()

    parser = MainArgParser(command_table, __version__, description, argument_table, prog="mng")

    args = sys.argv[1:]
    parsed_args, remaining = parser.parse_known_args(args)
    # print('parsed_args: %s\nremaining: %s' % (parsed_args, remaining))
    command_table[parsed_args.command](remaining, parsed_args)

    return 0
