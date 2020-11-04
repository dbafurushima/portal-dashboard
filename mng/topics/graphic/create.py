import pprint

from .fusion_charts import FusionChart
from ._argv_create import ArgTableCreate

from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config
from ...errors import Errors


class GraphCreateCommand(BasicCommand):

    NAME = 'create'

    DESCRIPTION = BasicCommand.FROM_FILE(
        'graph',
        'create',
        '_description.rst')

    SYNOPSIS = BasicCommand.FROM_FILE(
        'graph',
        'create',
        '_synopsis.rst')

    EXAMPLES = BasicCommand.FROM_FILE(
        'graph',
        'create',
        '_examples.rst')

    SUBCOMMANDS = []

    ARG_TABLE = ArgTableCreate

    def _run_main(self, args, parsed_globals):
        graph = self.create_graph(args)

        if graph is None:
            print('\n>> Ops... error, see log for more details.')
            return

        pp = pprint.PrettyPrinter(indent=2, width=60, compact=True)
        print('\n>> Successfully created.\n')
        pp.pprint(graph)

    def create_graph(self, args):
        """Create a graph making a post in the API from parameters passed
        by the user and with FusionChart class.
        """
        fusion_chart = FusionChart(
            name=args.graph_name,
            title=args.title,
            caption=args.caption,
            subcaption=args.subcaption,
            prefix=args.prefix,
            format=args.stftime,
            type_graph=args.type_graph,
            description_value=args.description_value
        )

        url = 'http://%s:%s/api/charts/charts/' % (lookup_config('address_api'), lookup_config('port_api'))

        sucessful, data = request(
            url,
            fusion_chart.__dict__,
            method='POST',
            headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
        )

        return data if sucessful else None
