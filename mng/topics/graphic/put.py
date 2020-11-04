import re
import pprint

from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config
from ...errors import error_to_user

rexp = [
	r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\s?\d{1,2}', # -> 2020-10-05 16:52:01, 79
	r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2},\s?\d{1,2}', # -> 2020-10-05 16:53, 80
	r'\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\s?\d{1,2}', # -> 10-05 16:52:01, 79
	r'\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2},\s?\d{1,2}', # -> 10-05 16:52, 79
]


class GraphPutCommand(BasicCommand):
	NAME = 'put'

	DESCRIPTION = BasicCommand.FROM_FILE(
		'graph',
		'put',
		'_description.rst')

	SYNOPSIS = 'mng put gid value [--index]'

	EXAMPLES = BasicCommand.FROM_FILE(
		'graph',
		'put',
		'_examples.rst')

	SUBCOMMANDS = []

	ARG_TABLE = [
		{
			'name': 'gid',
			'help_text': ('Graph ID (gid) ao qual os dados serão adicionado.\n'
				'Você pode também utilizar o UID do gráfico gerado na criação do gráfico.'),
			'action': 'store',
			'cli_type_name': 'string',
			'positional_arg': True
		},
		{
			'name': 'value',
			'help_text': ('Valor para ser adicionado. Pode ser uma string ou o caminho de \n'
				'um arquivo com os dados.'),
			'action': 'store',
			'cli_type_name': 'string',
			'positional_arg': True
		},
		{
			'name': 'index',
			'help_text': ('Escolher o index para o dado manualmete. Caso não seja utilizado \n'
				'será consultado e criado automaticamente.'),
			'action': 'store',
			'cli_type_name': 'integer',
			'required': False,
			'default': 0
		}
	]

	def _run_main(self, args, parsed_globals):
		pp = pprint.PrettyPrinter(indent=2, compact=False, width=51)
		re_data = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')
		addr, port = lookup_config('address_api'), lookup_config('port_api')

		url_get_index = 'http://%s:%s/api/charts/data/filter/' % (addr, port)
		url_get_id = 'http://%s:%s/api/charts/charts/' % (addr, port)
		url_post_data = 'http://%s:%s/api/charts/data/' % (addr, port)
		headers = {'Authorization': 'Basic %s' % lookup_config('base64auth')}

		gid = None
		failed = list()

		for rxp in rexp:
			# Scroll through the date regex patterns until you find
			# the first correspondent
			raw_data = re.findall(rxp, args.value)
			if raw_data:
				break

		if re.findall(r'^\d{1,3}$', args.gid):
			# If it is not possible to convert the gid to an integer
			# then the user is using the UID
			graph_filter = {'value': int(args.gid), 'key': 'chartid'}
		else:
			graph_filter = {'key': 'chartuid', 'value': args.gid}
			# Obtains chart ID from the UID so that POST requests can be
			# made to add charts to a chart.
			sucessful, response = request(
				url_get_id,
				method='GET',
				headers=headers)

			for graph in response:
				if graph.get('uid') == args.gid:
					gid = graph.get('id')
			if gid is None:
				error_to_user('o gráfico com uid "%s" não existe.' % args.gid)
				return

		if args.index == 0:
			# User does not define manual index
			sucessful, response = request(
				url_get_index,
				method='GET',
				params={graph_filter.get('key'): graph_filter.get('value')},
				headers=headers)
			# The index will be 0 if there is no data on the chart
			index = response[-1].get('index') + 1 if response else  0
		else:
			index = args.index

		for data in raw_data:
			if not re_data.match(data):
				data = '2020-'+data
			data_json = {
				"index": index,
				"value": data,
				"chart": gid
			}
			sucessful, response = request(
				url_post_data,
				data=data_json,
				headers=headers)

			if not sucessful:
				failed.append(data_json)
			index += 1

		print('\n>> success sending data to the chart.\n')
		print('\tsuccessfully sent: %s' % (len(raw_data) - len(failed)))
		print('\tnot sent: %s\n' % len(failed))
		pp.pprint(raw_data)
