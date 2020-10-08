from mng.helper.argument_parser import check_subcommand, check_args


ACTIONS = {
    'action1': [
        {'arg': '--argv1',
        'value': 'argv1'}],
    'action2': [],
    'help':[]}

HELP = {
    'action1': {'text': 'text, text, text',
               'args': [act['arg'] for act in ACTIONS['action1']]},
    'action2': {'text': 'text, text, text.',
             'args': []},
}
