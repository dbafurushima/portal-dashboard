from ...commands import BasicCommand
from ...http import request
from ...utils import (lookup_config, write_stdout, write_stdout_pprint)


class CommentAddCommand(BasicCommand):

	NAME = 'add'

	DESCRIPTION = ('Adicionar um comentário a uma anotação.')

	SYNOPSIS = ' $ mng comment add noteid text'

	EXAMPLES = None

	SUBCOMMANDS = []

	ARG_TABLE = [
		{
	        'name': 'noteid',
	        'help_text': ('ID da anotação que será feito o comentário.'),
	        'action': 'store',
	        'cli_type_name': 'integer',
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
		comment = self.__create_comment(args)

		if comment is None:
			write_stdout('\n>> Ops... error, see log for more details.')
			return

		write_stdout('\n>> Successfully created.\n')
		write_stdout_pprint(comment, width=100, indent=4)

	def __create_comment(self, args) -> dict or None:
		url = 'http://%s:%s/api/comment/' % (lookup_config('address_api'), lookup_config('port_api'))

		data_post = {
	        "note": args.noteid,
	        "comment": args.text
	    }

		sucessful, data = request(
			url,
			data_post,
			method='POST',
			headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
		)

		return data if sucessful else None
