from ...commands import BasicCommand
from .add import CommentAddCommand
from .list import CommentListCommand


class CommentCommand(BasicCommand):

	NAME = 'comment'

	DESCRIPTION = ('Utilitário para comentários em anotações')

	SYNOPSIS = None

	EXAMPLES = None

	SUBCOMMANDS = [
		{
			'name': 'add',
			'command_class': CommentAddCommand
		},
		{
			'name': 'list',
			'command_class': CommentListCommand
		}
	]

	ARG_TABLE = []

	def _run_main(self, args, parsed_globals) -> None:
		self._display_help(parsed_args, parsed_globals)