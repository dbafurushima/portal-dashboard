import json
import pprint
import urllib.request
from datetime import datetime
from jdata import GET_DATA_HISTORY, LOGIN_DATA


pp = pprint.PrettyPrinter(indent=2, width=41, compact=False, sort_dicts=True)
uribase = 'http://zabbix.dbafurushima.com.br/api_jsonrpc.php'
headers_json = {'Content-Type': 'application/json-rpc'}

_user_token = ""
_user_id = 0

def json_decode(text: str):
    if isinstance(text, str):
        return json.loads(text)
    return text

def _decode_bytes_to_utf8(text: bytes):
    if isinstance(text, bytes):
        return text.decode('utf-8', errors='ignore')
    return text

def _post_request(uri, data):

    data = json.dumps(data) if isinstance(data, dict) else data
    data = data.encode('utf-8') if isinstance(data, str) else data
    
    req = urllib.request.Request(uri, data=data, headers={'content-type': 'application/json-rpc'})
    with urllib.request.urlopen(req) as response:
        body = response.read()
    return _decode_bytes_to_utf8(body)

def get_token_api(user, passwd):
    global _user_id
    global _user_token

    def _get_token_api(user, passwd):
        payload = LOGIN_DATA
        payload["params"]["user"] = user
        payload["params"]["password"] = passwd

        raw_data = json_decode(_post_request(uribase, payload))

        return raw_data.get('id', 0), raw_data.get('result', None)

    _user_id, _user_token = _get_token_api(user, passwd)

def _set_auth_token_api(data):
    data["auth"] = _user_token
    data["id"] = _user_id
    return data

def get_history_from_itemids(itemids):
    data = _set_auth_token_api(GET_DATA_HISTORY)
    data["params"]["itemids"] = itemids

    def _raw_data_to_chart_data(raw_data):
        dt = datetime.fromtimestamp(int(raw_data.get('clock')))
        return {
            'datetime': dt,
            'data_info': {
                'm': dt.minute,
                's': dt.second,
                'h': dt.hour,
                'd': dt.day,
                'formatter': f'{dt.day}-{dt.hour}-{dt.minute}'
            },
            'value': raw_data.get('value')
        }

    raw_data = json_decode(_post_request(uribase, data=data))
    data = raw_data.get('result')
    fdata = [_raw_data_to_chart_data(d) for d in data]

    list_values_and_categories = [(d.get('data_info').get('formatter'), float(d.get('value'))) for d in fdata]
    return list_values_and_categories


if __name__ == '__main__':
    import os, getpass

    user = 'paulo_dev' # input('user: ')
    if not os.getenv('ZABBIX_PASSWORD'):
        passwd = getpass.getpass(prompt='password: ', stream=None)
    else:
        passwd = os.getenv('ZABBIX_PASSWORD')
    
    get_token_api(user, passwd)

    data = get_history_from_itemids("31359")
    print([c for c, v in data])
    print([v for c, v in data])
