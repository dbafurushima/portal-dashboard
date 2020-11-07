from ...commands import BasicCommand
from .add import NoteAddCommand
from .list import NoteListCommand


class NoteCommand(BasicCommand):

	NAME = 'notes'

	DESCRIPTION = ('Utilitário para anotações.')

	SYNOPSIS = None

	EXAMPLES = (
		'Adicionar uma nova anotação com assusto "dev"\n'
		'\n'
		' $ mng notes add "dev" "desenvolvimento do comando de notas"\n'
		'\n'
		'    >> Successfully created.\n'
		'\n'
		"    {  'id': 1,\n"
    	"       'msg': 'desenvolvimento do comando de notas',\n"
    	"       'subject': 'dev',\n"
    	"       'timestamp': '1604624940.758522'}\n"
    	'\n'
    	'Listando anotações criadas\n'
    	'\n'
    	' $ mng notes list\n'
    	'\n'
    	"[   {   'comments': [],\n"
        "	'id': 9,\n"
        "	'msg': \"atualizar documentação do comando 'dev'\",\n"
        "	'subject': 'dev',\n"
        "	'timestamp': '2020-11-06 22:06:28'}]\n"
	)

	SUBCOMMANDS = [
		{'name': 'list', 'command_class': NoteListCommand},
		{'name': 'add', 'command_class': NoteAddCommand},
	]

	ARG_TABLE = []

	def _run_main(self, args, parsed_globals) -> None:
		self._display_help(args, parsed_globals)