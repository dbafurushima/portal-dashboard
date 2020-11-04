from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config, write_stdout, write_stdout_pprint


class EnvironmentCreateCommand(BasicCommand):

	NAME = 'create'

	DESCRIPTION = BasicCommand.FROM_FILE(
		'environment',
        '_create_description.rst')

	SYNOPSIS = (' $ mng environment create envname inventoryid')

	EXAMPLES = BasicCommand.FROM_FILE(
		'environment',
        '_create_example.rst')

	SUBCOMMANDS = []

	ARG_TABLE = [
		{
			'name': 'envname',
			'help_text': ('Nome para o inventário. Deve ser curto, de preferência \n.'
				'o nome do serviço que ela compõem. Ex: Protheus'),
			'action': 'store',
			'cli_type_name': 'string',
			'positional_arg': True
		},
		{
			'name': 'inventoryid',
			'help_text': ('Inventário do cliente em que o ambiente está inserido.'),
			'action': 'store',
			'cli_type_name': 'integer',
			'positional_arg': True
		}
	]

	def _run_main(self, args, parsed_globals):
		environment = self.__create_environment(args)

		if environment is None:
			write_stdout('\n>> Ops... error, see log for more details.')
			return

		write_stdout('\n>> Successfully created.\n')
		write_stdout_pprint(environment, width=60)

	def __create_environment(self, args):
		url = 'http://%s:%s/api/cmdb/environment/' % (lookup_config('address_api'), lookup_config('port_api'))

		data_post = {
			"name": args.envname,
			"inventory": args.inventoryid
		}

		sucessful, data = request(
			url,
			data_post,
			method='POST',
			headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
		)

		return data if sucessful else None
