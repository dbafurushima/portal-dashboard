import argparse
import sys
import six

from .version import __version__

from difflib import get_close_matches

MNG_CLI_MESSAGE = (
    'Note: MNG CLI (v%s) é um utilitário linha de comando multiplataforma '
    'escrito em python, utilizado para auxiliar a aplicação web portald para '
    'trazer uma máxima flexibilidade. \n'
    'Manual completo em: https://github.com/dbafurushima/portal-dashboard/wiki/MNG-CLI\n'
    % __version__
)

HELP_BLURB = (
    "To see help text, you can run:\n"
    "\n"
    "  mng help\n"
    "  mng <command> help\n"
    "  mng <command> <subcommand> help\n"
)

USAGE = (
    "usage: mng [options] <command> <subcommand> "
    "[<subcommand> ...] [parameters]\n"
    "%s" % HELP_BLURB
)

# more_info = "\r%s\n\n" % MNG_CLI_MESSAGE
# if len(sys.argv) == 1:
#     USAGE = more_info + USAGE


class CommandAction(argparse.Action):
    """Custom action for CLI command arguments

    Allows the choices for the argument to be mutable. The choices
    are dynamically retrieved from the keys of the referenced command
    table.

    Permite que as opções do argumento sejam mutáveis. As opções
    são recuperadas dinamicamente das chaves da tabela de comando
    referenciada.
    """
    def __init__(self, option_strings: str, dest: str, command_table: dict, **kwargs):
        self.command_table = command_table
        super(CommandAction, self).__init__(
            option_strings, dest, choices=self.choices, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

    @property
    def choices(self):
        return list(self.command_table.keys())

    @choices.setter
    def choices(self, val):
        # argparse.Action will always try to set this value upon
        # instantiation, but this value should be dynamically
        # generated from the command table keys. So make this a
        # NOOP if argparse.Action tries to set this value.

        # argparse.Action sempre tentará definir esse valor em
        # instanciação, mas este valor deve ser dinamicamente
        # gerado a partir das chaves da tabela de comando. Então faça disso um
        # NOOP se argparse.Action tentar definir este valor.
        pass


class CLIArgParser(argparse.ArgumentParser):
    Formatter = argparse.RawTextHelpFormatter

    # When displaying invalid choice error messages,
    # this controls how many options to show per line.

    # Ao exibir mensagens de erro de escolha inválida,
    # isso controla quantas opções mostrar por linha.
    # ex:
    # command 1          |  command2
    ChoicesPerLine = 2

    def _check_value(self, action, value):
        """
        It's probably not a great idea to override a "hidden" method
        but the default behavior is pretty ugly and there doesn't
        seem to be any other way to change it.s

        Provavelmente não é uma boa ideia substituir um método "oculto"
        mas o comportamento padrão é muito feio e não há
        parece haver outra maneira de mudá-lo.
        """
        # converted value must be one of the choices (if specified)
        if action.choices is not None and value not in action.choices:
            msg = ['Invalid choice, valid choices are:\n']
            for i in range(len(action.choices))[::self.ChoicesPerLine]:
                current = []
                for choice in action.choices[i:i+self.ChoicesPerLine]:
                    current.append('%-40s' % choice)
                msg.append(' | '.join(current))
            possible = get_close_matches(value, action.choices, cutoff=0.8)
            if possible:
                extra = ['\n\nInvalid choice: %r, maybe you meant:\n' % value]
                for word in possible:
                    extra.append('  * %s' % word)
                msg.extend(extra)
            raise argparse.ArgumentError(action, '\n'.join(msg))

    def parse_known_args(self, args, namespace=None):
        parsed, remaining = super(CLIArgParser, self).parse_known_args(args, namespace)
        terminal_encoding = getattr(sys.stdin, 'encoding', 'utf-8')
        if terminal_encoding is None:
            # In some cases, sys.stdin won't have an encoding set,
            # (e.g if it's set to a StringIO).  In this case we just
            # default to utf-8.

            # Em alguns casos, sys.stdin não terá um conjunto de codificação,
            # (por exemplo, se estiver definido como StringIO). Neste caso, nós apenas
            # padrão para utf-8.
            terminal_encoding = 'utf-8'
        for arg, value in vars(parsed).items():
            if isinstance(value, six.binary_type):
                setattr(parsed, arg, value.decode(terminal_encoding))
            elif isinstance(value, list):
                encoded = []
                for v in value:
                    if isinstance(v, six.binary_type):
                        encoded.append(v.decode(terminal_encoding))
                    else:
                        encoded.append(v)
                setattr(parsed, arg, encoded)
        return parsed, remaining


class MainArgParser(CLIArgParser):
    Formatter = argparse.RawTextHelpFormatter

    def __init__(self, command_table, version_string,
                 description, argument_table, prog=None):
        super(MainArgParser, self).__init__(
            formatter_class=self.Formatter,
            add_help=False,
            conflict_handler='resolve',
            description=description,
            usage=USAGE,
            prog=prog)
        self._build(command_table, version_string, argument_table)

    def _create_choice_help(self, choices):
        help_str = ''
        for choice in sorted(choices):
            help_str += '* %s\n' % choice
        return help_str

    def _build(self, command_table, version_string, argument_table):
        for argument_name in argument_table:
            argument = argument_table[argument_name]
            argument.add_to_parser(self)
        self.add_argument('--version', action="version",
                          version=version_string,
                          help='Display the version of this tool')
        self.add_argument('command', action=CommandAction,
                          command_table=command_table)


class ServiceArgParser(CLIArgParser):

    def __init__(self, operations_table, service_name):
        super(ServiceArgParser, self).__init__(
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False,
            conflict_handler='resolve',
            usage=USAGE)
        self._build(operations_table)
        self._service_name = service_name

    def _build(self, operations_table):
        self.add_argument('operation', action=CommandAction,
                          command_table=operations_table)


class ArgTableArgParser(CLIArgParser):
    """CLI arg parser based on an argument table."""

    def __init__(self, argument_table, command_table=None):
        # command_table is an optional subcommand_table.  If it's passed
        # in, then we'll update the argparse to parse a 'subcommand' argument
        # and populate the choices field with the command table keys.

        # command_table é uma subcommand_table opcional. Se passou
        # in, então vamos atualizar o argparse para analisar um argumento 'subcomando'
        # e preencha o campo de opções com as chaves da tabela de comandos.
        super(ArgTableArgParser, self).__init__(
            formatter_class=self.Formatter,
            add_help=False,
            usage=USAGE,
            conflict_handler='resolve')
        if command_table is None:
            command_table = {}
        self._build(argument_table, command_table)

    def _build(self, argument_table, command_table):
        for arg_name in argument_table:
            argument = argument_table[arg_name]
            argument.add_to_parser(self)
        if command_table:
            self.add_argument('subcommand', action=CommandAction,
                              command_table=command_table, nargs='?')

    def parse_known_args(self, args, namespace=None):
        if len(args) == 1 and args[0] == 'help':
            namespace = argparse.Namespace()
            namespace.help = 'help'
            return namespace, []
        else:
            return super(ArgTableArgParser, self).parse_known_args(
                args, namespace)
