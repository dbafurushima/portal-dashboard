# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
import pprint
import re

from pathlib import Path

from mng.helper.regexp import reDATATIME1, reDATATIME2, reDATATIME3, reDATATIME4

reXP = [reDATATIME1, reDATATIME2, reDATATIME3, reDATATIME4]
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def upd_chart(api, args):
	if (not args.file) and (not args.value):

		print('Você deve utilizar a opção  --value ou --file com os dados!')
		return False

	re_data = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')

	if args.value:
		for rexp in reXP:
			raw_data = re.findall(rexp, args.value)
			if raw_data: break
	else:
		path = Path(args.file)
		for rexp in reXP:
			raw_data = re.findall(rexp, open(path).read())
			if raw_data: break

	pp = pprint.PrettyPrinter(indent=2, compact=False, sort_dicts=False)
	again = '[!] falha ao enviar valor %s, deseja tentar novamente ou continuar? (T)ry / (C)ontinue '

	try:
		chart_filter = {'value': int(args.chart), 'key': 'chartid'}
	except ValueError:
		chart_filter = {'key': 'chartuid', 'value': args.chart}

	if args.index == 0:
		response = await api.get_json('/api/charts/data/filter/', [(chart_filter.get('key'), chart_filter.get('value'))])
		
		if response:
			index = response[-1].get('index') + 1
		else:
			index = 1
	else:
		index = args.index

	async def send_data(uri, data):
		return await api.post_json(uri, data)

	failed = set()

	async def try_again(response):
		if response:
			return
		choice = input(again % data) or 'T'
		if choice.lower() == 'c':
			failed.add(json.dumps(data_json))
			return
		response = await send_data('/api/charts/data/', data_json)
		return await try_again(response)

	for data in raw_data:

		if not re_data.match(data):
			# mudar para pegar ano atual
			data = '2020-'+data

		data_json = {
	    	"index": index,
	    	"value": data,
	    	"chart": int(args.chart)
		}

		response = await send_data('/api/charts/data/', data_json)

		await try_again(response)

		index += 1
	print('[-] dados que falharam:', failed)


def setup_upd_chart(subparsers):
	parser = subparsers.add_parser("upd-chart", help="Adicionar dados a um gráfico.")

	parser.add_argument("chart", help="ID ou UID do gráfico onde o valor será adicionado.")
	parser.add_argument("--value", type=str, help=("Valor a ser adicionado, deverá seguir a "
									   			 "estrutura definida em *schema* na criação do gráfico."
									   			 "Se você for enviar apenas um valor deverá ser separado "
									   			 "por virgula, ex: 2020-10-1,90. Se for mais de um valor: "
									   			 "\"2020-10-1,90 2020-10-2,60\","
									   			 "utilizando espaço como separador."), default='')

	parser.add_argument('--file', type=str, default='', help='Caminho do arquivo com os valores.')

	parser.add_argument('--index', type=int, default=0, help="Escolher o index do valor manualmete.")

	parser.set_defaults(func=upd_chart)
