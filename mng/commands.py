# https://github.com/aws/aws-cli/blob/develop/awscli/customizations/commands.py
import os

from pathlib import Path
from collections import OrderedDict

from mng import root_module
from .argparser import ArgTableArgParser
from .arguments import CustomArgument
from .help import HelpCommand


class _FromFile(object):

    def __init__(self, *paths, **kwargs):
        """
        ``**kwargs`` can contain a ``root_module`` argument
        that contains the root module where the file contents
        should be searched.  This is an optional argument, and if
        no value is provided, will default to ``mng``.  This means
        that by default we look for examples in the ``mng`` module.
        """
        self.filename = None
        if paths:
            self.filename = os.path.join(*paths)
        if 'root_module' in kwargs:
            self.root_module = kwargs['root_module']
        else:
            self.root_module = str(root_module)


class CLICommand(object):
    """Interface for a CLI command.

    This class represents a top level CLI command
    (``mng charts``, ``mng cmdb``, ``mng config``).
    """

    @property
    def name(self):
        # Subclasses must implement a name.
        raise NotImplementedError("name")

    @name.setter
    def name(self, value):
        # Subclasses must implement setting/changing the cmd name.
        raise NotImplementedError("name")

    @property
    def lineage(self):
        # Represents how to get to a specific command using the CLI.
        # It includes all commands that came before it and itself in
        # a list.

        # Representa como chegar a um comando específico usando a CLI.
        # Inclui todos os comandos anteriores e ele próprio em
        # uma lista.
        return [self]
    
    @lineage.setter
    def lineage(self, value):
        self._lineage = value

    @property
    def lineage_names(self):
        # Represents the lineage of a command in terms of command ``name``
        # Representa a linhagem de um comando em termos de comando `` nome``
        return [cmd.name for cmd in self.lineage]

    def __call__(self, args, parsed_globals):
        """Invoke CLI operation.

        :type args: str
        :param args: The remaining command line args.

        :type parsed_globals: ``argparse.Namespace``
        :param parsed_globals: The parsed arguments so far.

        :rtype: int
        :return: The return code of the operation.  This will be used
            as the RC code for the ``mng`` process.

        """
        # Subclasses are expected to implement this method.
        pass

    def create_help_command(self):
        # Subclasses are expected to implement this method if they want
        # help docs.
        return None

    @property
    def arg_table(self):
        return {}


class BasicCommand(CLICommand):
    """Basic top level command with no subcommands.
    If you want to create a new command, subclass this and
    provide the values documented below.
    Se você deseja criar um novo comando, subclasse este e
    forneça os valores documentados abaixo.
    """

    # This is the name of your command, so if you want to
    # create an 'mng mycommand ...' command, the NAME would be
    # 'mycommand'
    NAME = 'commandname'
    # This is the description that will be used for the 'help'
    # command.
    DESCRIPTION = 'describe the command'
    # This is optional, if you are fine with the default synopsis
    # (the way all the built in operations are documented) then you
    # can leave this empty.
    SYNOPSIS = ''
    # If you want to provide some hand written examples, you can do
    # so here.  This is written in RST format.  This is optional,
    # you don't have to provide any examples, though highly encouraged!
    EXAMPLES = ''
    # If your command has arguments, you can specify them here.  This is
    # somewhat of an implementation detail, but this is a list of dicts
    # where the dicts match the kwargs of the CustomArgument's __init__.
    # For example, if I want to add a '--argument-one' and an
    # '--argument-two' command, I'd say:
    #
    # ARG_TABLE = [
    #     {'name': 'argument-one', 'help_text': 'This argument does foo bar.',
    #      'action': 'store', 'required': False, 'cli_type_name': 'string',},
    #     {'name': 'argument-two', 'help_text': 'This argument does some other thing.',
    #      'action': 'store', 'choices': ['a', 'b', 'c']},
    # ]
    #
    # A `schema` parameter option is available to accept a custom JSON
    ARG_TABLE = []
    # If you want the command to have subcommands, you can provide a list of
    # dicts.  We use a list here because we want to allow a user to provide
    # the order they want to use for subcommands.
    # SUBCOMMANDS = [
    #     {'name': 'subcommand1', 'command_class': SubcommandClass},
    #     {'name': 'subcommand2', 'command_class': SubcommandClass2},
    # ]
    # The command_class must subclass from ``BasicCommand``.
    SUBCOMMANDS = []

    FROM_FILE = _FromFile
    # You can set the DESCRIPTION, SYNOPSIS, and EXAMPLES to FROM_FILE
    # and we'll automatically read in that data from the file.
    # This is useful if you have a lot of content and would prefer to keep
    # the docs out of the class definition.  For example:
    #
    # DESCRIPTION = FROM_FILE
    #
    # will set the DESCRIPTION value to the contents of
    # mng/examples/<command name>/_description.rst
    # The naming conventions for these attributes are:
    #
    # DESCRIPTION = mng/examples/<command name>/_description.rst
    # SYNOPSIS = mng/examples/<command name>/_synopsis.rst
    # EXAMPLES = mng/examples/<command name>/_examples.rst
    #
    # You can also provide a relative path and we'll load the file
    # from the specified location:
    #
    # DESCRIPTION = mng/examples/<filename>
    #
    # For example:
    #
    # DESCRIPTION = FROM_FILE('command, 'subcommand, '_description.rst')
    # DESCRIPTION = 'mng/examples/command/subcommand/_description.rst'
    #

    # At this point, the only other thing you have to implement is a _run_main
    # method (see the method for more information).

    def __init__(self, subcommand_table={}):
        self._arg_table = None
        self._subcommand_table = None

    def __call__(self, args, parsed_globals):
        # args são os args restantes não analisados.
        # Podemos ser capazes de analisar esses argumentos, então precisamos criar
        # um analisador de argumentos e analise-os.
        # print('self.arg_table: %s' % self.arg_table)
        # print('self.subcommand_table: %s' % self.subcommand_table)

        parser = ArgTableArgParser(self.arg_table, self.subcommand_table)
        parsed_args, remaining = parser.parse_known_args(args)

        # Unpack arguments
        for key, value in vars(parsed_args).items():
            cli_argument = None

            # Convert the name to use dashes instead of underscore
            # as these are how the parameters are stored in the
            # `arg_table`.
            xformed = key.replace('_', '-')
            # print('mng.commands.BasicCommand.__call__().xformed: %s' % xformed)
            if xformed in self.ARG_TABLE:
                cli_argument = self.ARG_TABLE[xformed]
                # print('mng.commands.BasicCommand.__call__().cli_argument: %s' % cli_argument)

        if hasattr(parsed_args, 'help'):
            self._display_help(parsed_args, parsed_globals)
        elif getattr(parsed_args, 'subcommand', None) is None:
            # No subcommand was specified so call the main
            # function for this top level command.
            if remaining:
                raise ValueError("Unknown options: %s" % ','.join(remaining))
            return self._run_main(parsed_args, parsed_globals)
        else:
            return self.subcommand_table[parsed_args.subcommand](remaining,
                                                                    parsed_globals)

    def _display_help(self, parsed_args, parsed_globals):
        # print('BasicComand._display_help()')
        help_command = self.create_help_command()
        help_command(parsed_args, parsed_globals)

    def create_help_command(self):
        command_help_table = {}
        if self.SUBCOMMANDS:
            command_help_table = self.create_help_command_table()
        return BasicHelp(self, command_table=command_help_table, arg_table=self.arg_table)

    def create_help_command_table(self):
        """
        Create the command table into a form that can be handled by the
        BasicDocHandler.
        """
        commands = {}
        for command in self.SUBCOMMANDS:
            commands[command['name']] = command['command_class']()
        self._add_lineage(commands)
        return commands

    def _add_lineage(self, command_table):
        for command in command_table:
            command_obj = command_table[command]
            command_obj.lineage = self.lineage + [command_obj]

    def _run_main(self, parsed_args, parsed_globals):
        # Subclasses should implement this method.
        # parsed_globals are the parsed global args (things like region,
        # profile, output, etc.)
        # parsed_args are any arguments you've defined in your ARG_TABLE
        # that are parsed.  These will come through as whatever you've
        # provided as the 'dest' key.  Otherwise they default to the
        # 'name' key.  For example: ARG_TABLE[0] = {"name": "foo-arg", ...}
        # can be accessed by ``parsed_args.foo_arg``.
        raise NotImplementedError("_run_main")

    def _build_subcommand_table(self):
        subcommand_table = OrderedDict()

        for subcommand in self.SUBCOMMANDS:
            subcommand_name = subcommand['name']
            subcommand_class = subcommand['command_class']
            subcommand_table[subcommand_name] = subcommand_class()

        return subcommand_table

    def _build_arg_table(self):
        arg_table = OrderedDict()

        for arg_data in self.ARG_TABLE:
            custom_argument = CustomArgument(**arg_data)
            arg_table[arg_data['name']] = custom_argument

        return arg_table

    @property
    def subcommand_table(self):
        if self._subcommand_table is None:
            self._subcommand_table = self._build_subcommand_table()
        return self._subcommand_table

    @property
    def arg_table(self):
        if self._arg_table is None:
            self._arg_table = self._build_arg_table()
        return self._arg_table


class BasicHelp(HelpCommand):

    def __init__(self, command_object, command_table, arg_table,
                 event_handler_class=None):
        super(BasicHelp, self).__init__(command_object,
                                        command_table, arg_table)
        # This is defined in HelpCommand so we're matching the
        # casing here.
        self.EventHandlerClass = event_handler_class

        # These are public attributes that are mapped from the command
        # object.  These are used by the BasicDocHandler below.
        self._description = command_object.DESCRIPTION
        self._synopsis = command_object.SYNOPSIS
        self._examples = command_object.EXAMPLES

    @property
    def name(self):
        return self.obj.NAME

    @property
    def description(self):
        return self._get_doc_contents('_description')

    @property
    def synopsis(self):
        return self._get_doc_contents('_synopsis')

    @property
    def examples(self):
        return self._get_doc_contents('_examples')

    @property
    def event_class(self):
        return '.'.join(self.obj.lineage_names)

    def _get_doc_contents(self, attr_name):
        value = getattr(self, attr_name)
        if isinstance(value, BasicCommand.FROM_FILE):
            if value.filename is not None:
                trailing_path = value.filename
            else:
                trailing_path = os.path.join(self.name, attr_name + '.rst')
            root_module = value.root_module
            doc_path = os.path.join(
                os.path.abspath(os.path.dirname(root_module)),
                'examples', trailing_path)
            with open(doc_path, encoding='utf-8') as f:
                return f.read()
        else:
            return value

    def __call__(self, args, parsed_globals):
        # Create an event handler for a Provider Document
        # instance = self.EventHandlerClass(self)
        # Now generate all of the events for a Provider document.
        # We pass ourselves along so that we can, in turn, get passed
        # to all event handlers.
        # docevents.generate_events(self.session, self)
        # self.renderer.render(self.doc.getvalue())
        # instance.unregister()
        # TODO HELP
        # print('BasicHelp.__call__()')
        # print('BasicHelp.__call__().self.command_table: %s' % self.command_table)
        if self.synopsis:
            print('\n%s\n%s\n' % (self.name, '^'*len(self.name)))

        if self.description:
            print(self.description)

        if self.synopsis:
            print('\nSynopsis\n********\n')
            print(self.synopsis)

        if self.command_table:
            print('\n\nAvailable Commands\n******************\n')
            for command in self.command_table:
                print('  - %s' % command)

        if self.examples:
            print('\n\nExamples\n********\n')
            print(self.examples)
