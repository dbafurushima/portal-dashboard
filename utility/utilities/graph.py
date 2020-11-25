from .http import request
from .utils import debug
from .utils_constants import DEFAULT_URL_BASE_API, DEFAULT_HEADERS
from .utils_exceptions import GraphDoesNotExist

uribase, headers = DEFAULT_URL_BASE_API, DEFAULT_HEADERS


def get_graph_by_id(gid: int, throw: bool = False):
    graph = request(
        uri=uribase+'/api/charts/charts/'+  gid, headers=headers, method='GET')
    
    if throw and (graph is None):
        raise GraphDoesNotExist('No graph returned, check and ID exists.')

    return graph


def get_graph_by_uid(uid: str, throw: bool = False):
    response = request(uri=uribase+'/api/charts/charts/', headers=headers, method='GET')

    for graph in response:
        if graph.get('uid') == uid:
            return graph
    debug('o gráfico com uid "%s" não existe.' % uid)

    if throw:
        raise GraphDoesNotExist('No graph returned, check and UID exists.')

    return None


def put_data_to_graph(data: dict):
    return request(
        uri=uribase+'/api/charts/data/',
        data=data,
        headers=headers,
        method='POST')


def get_index_graph(gid: int):
    response = request(
        uri=uribase+'/api/charts/data/filter/',
        method='GET',
        params={'chartid': gid},
        headers=headers)
    return response[-1].get('index') + 1 if response else  0