from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config, write_stdout, write_stdout_pprint


class GraphListCommand(BasicCommand):
    
    NAME = 'list'

    DESCRIPTION = (
        'Lista todos os gráficos já criados.')

    SYNOPSIS = ' $ mng graph list'

    EXAMPLES = (
        '   $ mng graph list\n'
        '\n'
        "   [ { 'caption': 'CPU Analysis',\n"
    	"       'client': None,\n"
    	"       'id': 11,\n"
	    "       'schema': '[{\"name\": \"Time\", \"type\": \"date\", \"format\": '\n"
	    '                 "%Y-%m-%d %H:%M"}, {"name": "title", \n'
	    '                 "type": "number"}]\n'
	    "       'subcaption': 'Usage',\n"
	    "       'uid': '319a_usage_cpu_vm0',\n"
	    "       'yAxis_format_prefix': '%/min',\n"
	    "       'yAxis_plot_type': 'line',\n"
	    "       'yAxis_plot_value': 'usage cpu is',\n"
	    "       'yAxis_title': 'usage_cpu_vm0'}]\n"
    )


    def _run_main(self, args, parsed_globals) -> None:
        environments = self.__list_environment(args)

        if environments is None:
            write_stdout('\n>> Ops... error, see log for more details.')
            return

        print()
        write_stdout_pprint(environments, width=60)

    def __list_environment(self, args) -> list or None:
        url = 'http://%s:%s/api/charts/charts/' % (lookup_config('address_api'), lookup_config('port_api'))

        sucessful, data = request(
            url,
            method='GET',
            headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
        )

        return data if sucessful else None

