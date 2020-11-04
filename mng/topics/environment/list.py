from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config, write_stdout, write_stdout_pprint


class EnvironmentListCommand(BasicCommand):

    NAME = 'list'

    DESCRIPTION = (
        'Lista todos os ``Environments`` (ambientes) de todos '
        'os clientes cadastrados.')

    SYNOPSIS = ' $ mng environment list'

    EXAMPLES = (
        '   $ mng configure list\n'
        '\n'
        "   [ { 'hosts': [],\n"
        "       'id': 1,\n"
        "       'inventory': 1,\n"
        "       'name': 'mini-kube'}]\n"
    )


    def _run_main(self, args, parsed_globals) -> None:
        environments = self.__list_environment(args)

        if environments is None:
            write_stdout('\n>> Ops... error, see log for more details.')
            return

        print()
        write_stdout_pprint(environments, width=60)

    def __list_environment(self, args) -> list or None:
        url = 'http://%s:%s/api/cmdb/environment/' % (lookup_config('address_api'), lookup_config('port_api'))

        sucessful, data = request(
            url,
            method='GET',
            headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
        )

        return data if sucessful else None
