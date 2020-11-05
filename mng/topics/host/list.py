from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config, write_stdout, write_stdout_pprint


class HostListCommand(BasicCommand):

    NAME = 'list'

    DESCRIPTION = (
        'Lista todos os ``Hosts`` de todos '
        'os clientes cadastrados.\n'
        'Também serão listados os itens que estão contidos no **Host** \n'
        'Como os *objetos* ``Instances`` e ``Service``.')

    SYNOPSIS = ' $ mng host list'

    EXAMPLES = BasicCommand.FROM_FILE(
        'host',
        'list',
        '_examples.rst')

    def _run_main(self, args, parsed_globals) -> None:
        hots = self.__list_hosts(args)

        if hots is None:
            write_stdout('\n>> Ops... error, see log for more details.')
            return

        print()
        write_stdout_pprint(hots, width=60)

    def __list_hosts(self, args) -> list or None:
        url = 'http://%s:%s/api/cmdb/host/' % (lookup_config('address_api'), lookup_config('port_api'))

        sucessful, data = request(
            url,
            method='GET',
            headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
        )

        return data if sucessful else None
