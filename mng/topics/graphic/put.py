import os.path
import re
import json
import datetime

from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config, write_stdout, write_stdout_pprint
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
		self.__put_data(args)

	def __put_data(self, args):
		"""A partir de uma string ou arquivo com os dados será realizado uma
		validação dos mesmo para que corresponda ao padrão correto, em seguida
		seram feitos posts indiviuais com cada "dado", caso algum falhe você
		poderá enviar novamente ou ignora-lo
		"""
		re_data = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')
		addr, port = lookup_config('address_api'), lookup_config('port_api')

		# URL para obter o index correto da proxima informação enviada
		# o index é uma primary key secundária, para ordenar os dados
		# e possibilitar a alteração sem que os dados fique inconsistentes.
		url_get_index = 'http://%s:%s/api/charts/data/filter/' % (addr, port)
		# URL para obter o id do gráfico a partir do uid passado pelo usuário
		url_get_id = 'http://%s:%s/api/charts/charts/' % (addr, port)
		# URL que serão feitos os posts para adicionar novos dados
		url_post_data = 'http://%s:%s/api/charts/data/' % (addr, port)

		headers = {'Authorization': 'Basic %s' % lookup_config('base64auth')}

		gid, failed, failed_agin = None, list(), list()

		if os.path.isfile(args.value):
			lines = open(args.value, errors='ignore').read()
		else:
			lines = args.value

		for rxp in rexp:
			# Scroll through the date regex patterns until you find
			# the first correspondent
			raw_data = re.findall(rxp, lines)
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
			# Percorre todos os dados faz requisições POST para cada um
			#
			# Futuramente esse comportamento será modificado por:
			# 	1. Lentidão entre requisições.
			# 	2. Vulneravel a falhas entre requisições.
			# 	3. Pouco viável para grande quantidade de requisições.
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

		if not failed:
			# Se todos as requisições forem efetuadas com sucesso.
			write_stdout('\n>> success sending data to the chart.\n')

		write_stdout('\tsuccessfully sent: %s' % (len(raw_data) - len(failed)))
		write_stdout('\tnot sent: %s\n' % len(failed))
		write_stdout_pprint(raw_data[:10])

		def __try_again(payloads: list, failed_agin: list) -> bool:
			"""Faz backup dos dados que não foram enviados com sucesso para
			uma posterior tentativa de envio.
			Tenta realizar o envio dos restantes caso o usuário deseje.
			"""
			now = datetime.datetime.now()

			with open('%s.%s' % (now.strftime('%Y_%m_%d-%H-%M-%S'), 'failed'), 'w', encoding='utf-8') as f:
				json.dump(payloads, f, ensure_ascii=False, indent=4)

			write_stdout('\n>> Dados que não foram com sucesso::')
			write_stdout_pprint(json.dumps(failed))

			try_again = input('deseja tentar enviar novamente? (Y/n): ', 'Y')

			if try_again == 'Y':
				for json_data in payloads:
					sucessful, _ = request(url_post_data, data=json_data, headers=headers)
					print('[%s] %s' % (sucessful, json_data))
					if not sucessful:
						failed_agin.append(data)

			return True if failed_agin else False

		if failed: # try...
			__try_again(failed, failed_agin)

		if failed_agin: # try again...
			__try_again(failed_agin, [])
