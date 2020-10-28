from ..commands import BasicCommand


class ManCommand(BasicCommand):

    NAME = 'help'
    DESCRIPTION = BasicCommand.FROM_FILE()
    SYNOPSIS = None
    SUBCOMMANDS = []
    ARG_TABLE = []

    def __init__(self, table_command):
        super(ManCommand, self).__init__()
        self.table_command = table_command

    def _run_main(self, parsed_args, parsed_globals):
        self._display_help(parsed_args, parsed_globals)
        for commmand in self.table_command:
            if str(commmand) != 'help':
                print(' * %s\n' % commmand)
