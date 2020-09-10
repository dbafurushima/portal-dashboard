import json
import pprint
import urllib.request
from datetime import datetime
from .data_info_requests import GET_DATA_HISTORY, LOGIN_DATA
from django.conf import settings
from .utils import decode_bytes_to_utf8, json_decode

debug = pprint.PrettyPrinter(indent=2, width=41, compact=False, sort_dicts=True)
uribase = settings.ZABBIX_URL

_user_token = ""
_user_id = 0


def _set_auth_token_api(payload):
    payload["auth"] = _user_token
    payload["id"] = _user_id
    return payload


def _post_request(uri, payload):
    payload = json.dumps(payload) if isinstance(payload, dict) else payload
    payload = payload.encode('utf-8') if isinstance(payload, str) else payload

    req = urllib.request.Request(uri, data=payload, headers={'content-type': 'application/json-rpc'})
    with urllib.request.urlopen(req) as response:
        body = response.read()
    return decode_bytes_to_utf8(body)


def get_token_api():
    global _user_id
    global _user_token

    payload = LOGIN_DATA
    payload["params"]["user"] = settings.ZABBIX_USER
    payload["params"]["password"] = settings.ZABBIX_PASSWORD

    raw_data = json_decode(_post_request(uribase, payload))

    _user_id, _user_token = raw_data.get('id', 0), raw_data.get('result', None)


def _logged_in_zabbix():
    get_token_api() if _user_token == '' else None


def get_history_from_itemids(itemids):
    _logged_in_zabbix()

    payload = _set_auth_token_api(GET_DATA_HISTORY)
    payload["params"]["itemids"] = itemids

    def _raw_data_to_chart_data(d):
        dt = datetime.fromtimestamp(int(d.get('clock')))
        return {
            'timestamp': d.get('clock'),
            'data_info': {
                'm': dt.minute,
                's': dt.second,
                'h': dt.hour,
                'd': dt.day,
                'formatter': f'{dt.day}-{dt.hour}-{dt.minute}'
            },
            'value': d.get('value')
        }

    raw_data = json_decode(_post_request(uribase, payload))
    data = raw_data.get('result')
    fdata = [_raw_data_to_chart_data(d) for d in data]

    list_values_and_categories = [[int(d.get('timestamp')), float(d.get('value'))] for d in fdata]
    return list_values_and_categories
