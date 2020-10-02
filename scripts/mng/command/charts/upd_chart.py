# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
import pprint
import re

from pathlib import Path
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def upd_chart(api, args):
	if (not args.file) and (not args.value):

		print('Você deve utilizar a opção  --value ou --file com os dados!')
		return False

	re_data = r'(\(?[0-9]{4}-[0-9]{1,2}-[0-9]{1,2},[0-9]{1,5}\)?)'

	if args.value:
		raw_data = re.findall(re_data, args.value)
	else:
		path = Path(args.file)
		raw_data = re.findall(re_data, open(path).read())

	pp = pprint.PrettyPrinter(indent=2, compact=False, sort_dicts=False)
	again = '[!] falha ao enviar valor %s, deseja tentar novamente ou continuar? (T)ry / (C)ontinue '

	if args.index == 0:
		response = await api.get_json('/api_charts/data/filter/', [('chartid', args.chartid)])
		
		if response:
			index = response[-1].get('index') + 1
		else:
			index = 1
	else:
		index = args.index

	async def send_data(uri, data):
		return await api.post_json(uri, data)

	failed = set()

	for data in raw_data:

		data_json = {
	    	"index": index,
	    	"value": data,
	    	"chart": args.chartid
		}

		response = await send_data('/api_charts/data/', data_json)

		if not response:
			choice = input(again % data) or 'T'
			while choice.lower() != 'c':
				response = await send_data('/api_charts/data/', data_json)
				if response:
					break
				else:
					choice = input(again % data) or 'T'
					if choice.lower() == 'c':
						failed.add(json.dumps(data_json))
						break
		index += 1
	print('[-] dados que falharam:', failed)


def setup_upd_chart(subparsers):
	parser = subparsers.add_parser("upd_chart", help="Adicionar dados a um gráfico.")

	parser.add_argument("chartid", type=int, help="ID do gráfico onde o valor será adicionado.")
	parser.add_argument("--value", type=str, help=("Valor a ser adicionado, deverá seguir a "
									   			 "estrutura definida em *schema* na criação do gráfico."
									   			 "Se você for enviar apenas um valor deverá ser separado "
									   			 "por virgula, ex: 2020-10-1,90. Se for mais de um valor: "
									   			 "\"(2020-10-1,90),(2020-10-2,60)\". "
									   			 "Também é possível enviar sem a utilização de aspas: "
									   			 "2020-10-1,90,2020-10-2,10,2020-10-3,60"), default='')

	parser.add_argument('--file', type=str, default='', help='Caminho do arquivo com os valores.')

	parser.add_argument('--index', type=int, default=0, help="Escolher o index do valor manualmete")

	parser.set_defaults(func=upd_chart)
