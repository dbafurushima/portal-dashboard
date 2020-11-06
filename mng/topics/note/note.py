import time

from ...commands import BasicCommand
from ...http import request
from ...utils import (lookup_config, write_stdout, write_stdout_pprint)

from .comment import NoteCommentCommand


class NoteCommand(BasicCommand):

	NAME = 'note'

	DESCRIPTION = ('Utilitário para anotações.')

	SYNOPSIS = ' $ mng note subject text'

	EXAMPLES = (
		'Criar uma nota\n'
		'\n'
		' $ mng note "dev" "desenvolvimento do comando de notas"\n'
		'\n'
		'    >> Successfully created.\n'
		'\n'
		"    {  'id': 1,\n"
    	"       'msg': 'desenvolvimento do comando de notas',\n"
    	"       'subject': 'dev',\n"
    	"       'timestamp': '1604624940.758522'}\n"
	)

	SUBCOMMANDS = [
		{'name': 'comment', 'command_class': NoteCommentCommand}
	]

	ARG_TABLE = [
		{
	        'name': 'subject',
	        'help_text': ('Assusto para nota. Deve ser uma pequena frase ou \n'
	        	'palavra que descreva sobre o que será a anotação.'),
	        'action': 'store',
	        'cli_type_name': 'string',
	        'positional_arg': True
	    },
	    {
	        'name': 'text',
	        'help_text': ('Corpo da mensagem. Deve conter no máximo 255 caracteres.'),
	        'action': 'store',
	        'cli_type_name': 'string',
	        'positional_arg': True
	    }
	]

	def _run_main(self, args, parsed_globals) -> None:
		print(parsed_globals)
		note = self.__create_note(args)

		if note is None:
			write_stdout('\n>> Ops... error, see log for more details.')
			return

		write_stdout('\n>> Successfully created.\n')
		write_stdout_pprint(note, width=100, indent=4)

	def __create_note(self, args) -> dict or None:
		url = 'http://%s:%s/api/note/' % (lookup_config('address_api'), lookup_config('port_api'))

		data_post = {
	        "subject": args.subject,
	        "timestamp": str(time.time()),
	        "msg": args.text
	    }

		sucessful, data = request(
			url,
			data_post,
			method='POST',
			headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
		)

		return data if sucessful else None
