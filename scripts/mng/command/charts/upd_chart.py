# =============================================================================
#  IMPORTS
# =============================================================================
import time
import json
import pprint
import uuid
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def upd_chart(api, args):
	pp = pprint.PrettyPrinter(indent=2, compact=False, sort_dicts=False)

	response = await api.get_json('/api_charts/data/filter/', [('chartid', args.chartid)])
	
	if response:
		index = response[-1].get('index') + 1
	else:
		index = 1

	data_json = {
    	"index": index,
    	"value": json.dumps(args.value.split(',')),
    	"chart": args.chartid
	}

	pp.pprint(data_json)

	response = await api.post_json('/api_charts/data/', data_json)

	pp.pprint(response)


def setup_upd_chart(subparsers):
	parser = subparsers.add_parser("upd_chart", help="Adicionar dados a um gráfico.")

	parser.add_argument("chartid", type=int, help="ID do gráfico onde o valor será adicionado.")
	parser.add_argument("value", type=str, help=("Valor a ser adicionado, deverá seguir a "
									   "estrutura definida em *schema* na criação do gráfico."))

	parser.set_defaults(func=upd_chart)
