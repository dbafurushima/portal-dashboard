from ...commands import BasicCommand
from .create import EnvironmentCreateCommand
from .list import EnvironmentListCommand


class EnvironmentCommand(BasicCommand):

	NAME = 'environment'

	DESCRIPTION = BasicCommand.FROM_FILE()

	SYNOPSIS = None

	EXAMPLES = (
		'Criar um novo ambiente para o cliente "021"\n'
		'\n'
		'   $ mng environment create elk 21\n'
		'\nListando ``Environments``\n'
		'\n'
		'   $ mng configure list\n'
        '\n'
        "   [ { 'hosts': [],\n"
        "       'id': 1,\n"
        "       'inventory': 1,\n"
        "       'name': 'mini-kube'}]\n"
	)

	SUBCOMMANDS = [
		{'name': 'create', 'command_class': EnvironmentCreateCommand},
		{'name': 'list', 'command_class': EnvironmentListCommand},
	]

	ARG_TABLE = []

	def _run_main(self, parsed_args, parsed_globals):
		# call help
		self._display_help(parsed_args, parsed_globals)
