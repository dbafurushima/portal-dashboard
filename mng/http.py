import urllib.request
import urllib.parse
import json
import logging

from .errors import Errors

from typing import Dict, Any


def request(
        uri: str,
        data: Dict[str, Any] or str = None,
        params: dict = None,
        headers: Dict[str, str or int] = {},
        method: str = 'POST',) -> tuple:
    """Function that will make requests to the API to send or consult the information.

    Args:
        uri (str): [description]
        data (Dict[str, Any]orstr, optional): [description]. Defaults to None.
        params ([type], optional): [description]. Defaults to None.
        headers (Dict[str, str or int], optional): [description]. Defaults to {}.
        method (str): [description]. Defaults to 'POST'.

    Returns:
        tuple: [description]
    """

    if data:
        headers['Content-Type'] = 'application/json'

    if isinstance(data, dict):
        data = json.dumps(data).encode('utf-8')

    if params is not None:
        params = urllib.parse.urlencode(params)
        uri += '?%s' % params

    req = urllib.request.Request(uri, data, headers)

    body = None
    did_it_work = False

    if isinstance(data, dict):
        data = json.dumps(data).encode('utf-8')
    elif isinstance(data, str):
        data = data.encode('utf-8')

    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read().decode('utf-8', errors='ignore'))
    except urllib.error.HTTPError as err:
        if '401' in err:
            logging.warning(Errors.name_and_error(Errors.HTTP_401_UNAUTHORIZED))
        else:
            logging.warning('urllib.error.HTTPError: %s' % err)
    except TimeoutError as err:
        logging.warning('warning: %s' % err)
    except urllib.error.URLError:
        logging.warning(Errors.name_and_error(Errors.UNABLE_TO_CONNECT_SERVER))
    except Exception as err:
        logging.warning('not cataloged error: %s' % err)
    else:
        did_it_work = True

    return did_it_work, body
