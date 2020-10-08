async def init(api, _):
    """Initialize tool for use
    """
    result = api.init()
    return result['initialized']

def setup_init(subparsers):
    parser = subparsers.add_parser(
        'init',
        help=("inicializar ferramenta, criar arquivo de configuração "
              "e atualizado com as informações necessárias."))
    parser.set_defaults(func=init)
