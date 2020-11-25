import urllib.request
import urllib.parse
import json
import logging

from typing import Dict, Any

logger = logging.getLogger(__name__)


def request(uri: str, data: Dict[str, Any] or str = None, params: dict = None,
        headers: Dict[str, str or int] = {}, method: str = 'POST') -> dict:

    if data:
        headers['Content-Type'] = 'application/json'

    if isinstance(data, dict):
        data = json.dumps(data).encode('utf-8')

    if params is not None:
        params = urllib.parse.urlencode(params)
        uri += '?%s' % params

    req = urllib.request.Request(uri, data, headers, method=method)

    if isinstance(data, dict):
        data = json.dumps(data).encode('utf-8')
    elif isinstance(data, str):
        data = data.encode('utf-8')

    body = None
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read().decode('utf-8', errors='ignore'))
    except urllib.error.HTTPError as err:
            logger.error('urllib.error.HTTPError: %s' % err)
    except TimeoutError as err:
        logger.error('TimeoutError: %s' % err)
    except urllib.error.URLError as err:
        logger.error('urllib.error.URLError: %s' % err)
    except Exception as err:
        logger.error('not cataloged error: %s' % err)

    return body