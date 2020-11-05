from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config, write_stdout, write_stdout_pprint


class HostUpdateCommand(BasicCommand):

    NAME = 'update'

    DESCRIPTION = None

    SYNOPSIS = None

    EXAMPLES = None

    ARG_TABLE = [
        {
            'name': 'hostid',
            'help_text': ('ID do Host que será feita a atualização.'),
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

        [keys_values.update({keys[x]: values[x]}) for x in range(len(keys))]

        host = self.__update_host(args, keys_values)

        if host is None:
            write_stdout('\n>> Ops... error, see log for more details.')
            return

        print()
        write_stdout_pprint(host, width=60)

    def __update_host(self, args, fields: dict) -> list or None:
        url_update = 'http://%s:%s/api/cmdb/host/%s/' % (lookup_config('address_api'), lookup_config('port_api'), args.hostid)
        headers = {'Authorization': 'Basic %s' % lookup_config('base64auth')}
        print(url_update)
        sucessful, host = request(url_update, method='GET', headers=headers)

        if not sucessful:
            return None

        host.update(fields)

        sucessful, data = request(url_update, data=host, method='PUT', headers=headers)

        return data if sucessful else None
