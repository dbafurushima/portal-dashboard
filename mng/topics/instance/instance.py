from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config, write_stdout, write_stdout_pprint


class InstanceCreateCommand(BasicCommand):

	NAME = 'create'

	DESCRIPTION = BasicCommand.FROM_FILE(
		'instance',
		'create',
        '_description.rst')

	SYNOPSIS = ('mng instance create name\n'
		'    [--serviceid <integer>]\n'
		'    [--hostid <integer>]\n'
		'    [--database <string>]\n'
		'    [--ip <string>]')

	EXAMPLES = BasicCommand.FROM_FILE(
		'instance',
		'create',
        '_examples.rst')

	SUBCOMMANDS = []

	ARG_TABLE = [
		{
			'name': 'name',
			'help_text': ('Nome para identificar instância.'),
			'action': 'store',
			'cli_type_name': 'string',
			'positional_arg': True
		},
		{
			'name': 'serviceid',
			'help_text': ('ID do serviço que ela compõem.'),
			'action': 'store',
			'default': 0,
			'cli_type_name': 'integer',
			'required': False
		},
		{
			'name': 'hostid',
			'help_text': ('ID do ``Host`` que a instância pertence.'),
			'action': 'store',
			'cli_type_name': 'integer',
			'default': 0,
			'required': False
		},
		{
			'name': 'database',
			'help_text': ('Nome do database.'),
			'action': 'store',
			'cli_type_name': 'string',
			'required': False
		},
		{
			'name': 'ip',
			'help_text': ('Endereço IP ou DNS caso a instância possua.'),
			'action': 'store',
			'cli_type_name': 'string',
			'required': False
		}
	]

	def _run_main(self, args, parsed_globals):
		instance = self.__create_instance(args)

		if instance is None:
			write_stdout('\n>> Ops... error, see log for more details.')
			return

		write_stdout('\n>> Successfully created.\n')
		write_stdout_pprint(instance, width=60)
		print()

	def __create_instance(self, args):
		url = 'http://%s:%s/api/cmdb/instance/' % (lookup_config('address_api'), lookup_config('port_api'))

		data_post = {
            "name": args.name,
            "service": None if args.serviceid == 0 else args.serviceid,
            "host": None if args.hostid == 0 else args.hostid,
            "database": args.database,
            "private_ip": args.ip
        }

		sucessful, data = request(
			url,
			data_post,
			method='POST',
			headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
		)

		return data if sucessful else None


class InstanceListCommand(BasicCommand):

    NAME = 'list'

    DESCRIPTION = (
        'Lista todos as instâncias de todos '
        'os clientes cadastrados.')

    SYNOPSIS = ' $ mng instance list'

    EXAMPLES = BasicCommand.FROM_FILE(
		'instance',
		'list',
        '_examples.rst')


    def _run_main(self, args, parsed_globals) -> None:
        instances = self.__list_instances(args)

        if instances is None:
            write_stdout('\n>> Ops... error, see log for more details.')
            return

        print()
        write_stdout_pprint(instances, width=60)
        print()

    def __list_instances(self, args) -> list or None:
        url = 'http://%s:%s/api/cmdb/instance/' % (lookup_config('address_api'), lookup_config('port_api'))

        sucessful, data = request(
            url,
            method='GET',
            headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
        )

        return data if sucessful else None


class InstanceUpdateCommand(BasicCommand):

    NAME = 'update'

    DESCRIPTION = 'Atualizar campos do objeto ``Instance``.'

    SYNOPSIS = ' $ mng instance update instanceid value key'

    EXAMPLES = ('mng instance update 01 "name" "VM01 - VirtualBox"')

    ARG_TABLE = [
        {
            'name': 'instanceid',
            'help_text': ('ID da instância que será feita a atualização.'),
            'action': 'store',
            'cli_type_name': 'integer',
            'positional_arg': True
        },
        {
            'name': 'key',
            'help_text': ('O(s) nome(s) do(s) campo(s) que será(ão) atualizado(s).\n'
                'Esse campo pode receber uma lista ou string caso seja uma lista as \n'
                'chaves deveram ser separado por "," \n'
                'os quais teram que ter seu valor correspondente no próximo argumento.'),
            'action': 'store',
            'cli_type_name': 'list',
            'positional_arg': True
        },
        {
            'name': 'value',
            'help_text': ('O(s) novo(s) valor(res) que será(ão) atualizado(s).\n'
                'Esse campo pode receber uma lista ou string caso seja uma lista os \n'
                'valores deveram ser separado por "," \n'
                'e o número de valores deveram corresponder ao número de ``keys``.'),
            'action': 'store',
            'cli_type_name': 'list',
            'positional_arg': True
        },
    ]

    def _run_main(self, args, parsed_globals) -> None:
        keys = args.value.split(',')
        values = args.key.split(',')

        keys_values = {}

        [keys_values.update({values[x]: keys[x]}) for x in range(len(keys))]

        instance = self.__update_instance(args, keys_values)

        if instance is None:
            write_stdout('\n>> Ops... error, see log for more details.')
            return

        print()
        write_stdout_pprint(instance, width=60)
        print()

    def __update_instance(self, args, fields: dict) -> list or None:
        url_update = 'http://%s:%s/api/cmdb/instance/%s/' % (lookup_config('address_api'), lookup_config('port_api'), args.instanceid)
        headers = {'Authorization': 'Basic %s' % lookup_config('base64auth')}

        sucessful, instance = request(url_update, method='GET', headers=headers)

        if not sucessful:
            return None
        instance.update(fields)

        sucessful, data = request(url_update, data=instance, method='PUT', headers=headers)

        return data if sucessful else None


class InstanceCommand(BasicCommand):

	NAME = 'instance'

	DESCRIPTION = BasicCommand.FROM_FILE(
		'service',
        '_description.rst')

	SYNOPSIS = (' $ mng instance {create, list, update}')

	EXAMPLES = None

	SUBCOMMANDS = [
		{'name': 'create', 'command_class': InstanceCreateCommand},
		{'name': 'list', 'command_class': InstanceListCommand},
		{'name': 'update', 'command_class': InstanceUpdateCommand},
	]

	ARG_TABLE = []

	def _run_main(self, parsed_args, parsed_globals):
		self._display_help(parsed_args, parsed_globals)
