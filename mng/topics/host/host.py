from ...commands import BasicCommand
from ...http import request
from ...utils import (
	lookup_config, write_stdout, write_stdout_pprint,
	get_machine_infos
)

from .update import HostUpdateCommand
from .list import HostListCommand


class HostCommand(BasicCommand):

	NAME = 'host'

	DESCRIPTION = BasicCommand.FROM_FILE()

	SYNOPSIS = None

	EXAMPLES = BasicCommand.FROM_FILE()

	SUBCOMMANDS = [
		{'name': 'update', 'command_class': HostUpdateCommand},
		{'name': 'list', 'command_class': HostListCommand},
	]

	ARG_TABLE = []

	def _run_main(self, args, parsed_globals) -> None:
		host = self.__register_my_host(args)

		if host is None:
			write_stdout('\n>> Ops... error, see log for more details.')
			return

		write_stdout('\n>> Successfully created.\n')
		write_stdout_pprint(host, width=100, indent=2)

	def __register_my_host(self, args) -> dict or None:
		url = 'http://%s:%s/api/cmdb/host/' % (lookup_config('address_api'), lookup_config('port_api'))

		data_post = get_machine_infos()

		sucessful, data = request(
			url,
			data_post,
			method='POST',
			headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
		)

		return data if sucessful else None
