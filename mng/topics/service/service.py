from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config, write_stdout, write_stdout_pprint


class ServiceCreateCommand(BasicCommand):

	NAME = 'create'

	DESCRIPTION = BasicCommand.FROM_FILE(
		'service',
		'create',
        '_description.rst')

	SYNOPSIS = BasicCommand.FROM_FILE(
		'service',
		'create',
        '_synopsis.rst')

	EXAMPLES = BasicCommand.FROM_FILE(
		'service',
		'create',
        '_examples.rst')

	SUBCOMMANDS = []

	ARG_TABLE = [
		{
			'name': 'name',
			'help_text': ('Nome para o serviço.'),
			'action': 'store',
			'cli_type_name': 'string',
			'positional_arg': True
		},
		{
			'name': 'ip',
			'help_text': ('Porta externa que o serviço final utilizará.'),
			'action': 'store',
			'cli_type_name': 'string',
			'required': False
		},
		{
			'name': 'port',
			'help_text': ('Porta externa que o serviço final utilizará.'),
			'action': 'store',
			'cli_type_name': 'integer',
			'required': False
		},
		{
			'name': 'dns',
			'help_text': ('Endereço DNS pelo qual o serviço responderá.'),
			'action': 'store',
			'cli_type_name': 'string',
			'required': False
		}
	]

	def _run_main(self, args, parsed_globals):
		service = self.__create_service(args)

		if service is None:
			write_stdout('\n>> Ops... error, see log for more details.')
			return

		write_stdout('\n>> Successfully created.\n')
		write_stdout_pprint(service, width=60)

	def __create_service(self, args):
		url = 'http://%s:%s/api/cmdb/service/' % (lookup_config('address_api'), lookup_config('port_api'))

		data_post = {
            "name": args.name,
            "ip": args.ip,
            "port": args.port,
            "dns": "" if not args.dns else args.dns
        }

		sucessful, data = request(
			url,
			data_post,
			method='POST',
			headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
		)

		return data if sucessful else None


class ServiceListCommand(BasicCommand):

    NAME = 'list'

    DESCRIPTION = (
        'Lista todos os ``Services`` de todos '
        'os clientes cadastrados.')

    SYNOPSIS = ' $ mng service list'

    EXAMPLES = (
        '   $ mng service list\n'
        '\n'
        "   [ { 'dns': 'postgres.intranet.com',\n"
    	"       'id': 1,\n"
    	"       'name': 'PostgresSQL',\n"
    	"       'port': 321},\n"
  		"     {'dns': None, 'id': 2, 'name': 'MINIKUBE', 'port': None},\n"
  		"     { 'dns': 'dev.protheus.intranet.com',\n"
    	"       'id': 3,\n"
    	"       'name': 'Protheus - dev',\n"
    	"       'port': 443}]\n"
    )


    def _run_main(self, args, parsed_globals) -> None:
        services = self.__list_services(args)

        if services is None:
            write_stdout('\n>> Ops... error, see log for more details.')
            return

        print()
        write_stdout_pprint(services, width=60)
        print()

    def __list_services(self, args) -> list or None:
        url = 'http://%s:%s/api/cmdb/service/' % (lookup_config('address_api'), lookup_config('port_api'))

        sucessful, data = request(
            url,
            method='GET',
            headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
        )

        return data if sucessful else None


class ServiceUpdateCommand(BasicCommand):

    NAME = 'update'

    DESCRIPTION = 'Atualizar campos do objeto ``Service``.'

    SYNOPSIS = ' $ mng service update serviceid value key'

    EXAMPLES = ('mng service update 03 "name" "Protheus (dev)"')

    ARG_TABLE = [
        {
            'name': 'serviceid',
            'help_text': ('ID do Service que será feita a atualização.'),
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

        service = self.__update_service(args, keys_values)

        if service is None:
            write_stdout('\n>> Ops... error, see log for more details.')
            return

        print()
        write_stdout_pprint(service, width=60)
        print()

    def __update_service(self, args, fields: dict) -> list or None:
        url_update = 'http://%s:%s/api/cmdb/service/%s/' % (lookup_config('address_api'), lookup_config('port_api'), args.serviceid)
        headers = {'Authorization': 'Basic %s' % lookup_config('base64auth')}

        sucessful, service = request(url_update, method='GET', headers=headers)

        if not sucessful:
            return None
        service.update(fields)

        sucessful, data = request(url_update, data=service, method='PUT', headers=headers)

        return data if sucessful else None


class ServiceCommand(BasicCommand):

	NAME = 'service'

	DESCRIPTION = BasicCommand.FROM_FILE(
		'service',
        '_description.rst')

	SYNOPSIS = (' $ mng service {create, list, update}')

	EXAMPLES = None

	SUBCOMMANDS = [
		{'name': 'create', 'command_class': ServiceCreateCommand},
		{'name': 'list', 'command_class': ServiceListCommand},
		{'name': 'update', 'command_class': ServiceUpdateCommand},
	]

	ARG_TABLE = []

	def _run_main(self, parsed_args, parsed_globals):
		# call help
		self._display_help(parsed_args, parsed_globals)
