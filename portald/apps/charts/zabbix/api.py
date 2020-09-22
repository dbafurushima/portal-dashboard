import json
import pprint
import urllib.request
from datetime import datetime
from .data_info_requests import GET_DATA_HISTORY, LOGIN_DATA
from django.conf import settings
from .utils import decode_bytes_to_utf8, json_decode

debug = pprint.PrettyPrinter(indent=2, width=41, compact=False)
uribase = settings.ZABBIX_URL


class Zabbix:
    """
    Zabbix class for API consumption
    """

    def __init__(self, user, password):
        self.__api_user = user
        self.__api_password = password

        self.api_token = None

        self._auth_zabbix(user, password)

    def _auth_zabbix(self, user: str, passwd: str) -> None:
        """
        Authenticates to the zabbix API and sets the TOKEN in the class variable

        >>> zb = Zabbix(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        >>> type(zb.api_token)
        <class 'str'>
        >>> len(zb.api_token) > 1
        True

        :param user: username for zabbix login
        :param passwd: password for zabbix login
        :return:
        """
        payload = LOGIN_DATA

        payload['params']['user'] = user
        payload['params']['password'] = passwd

        payload = json.dumps(payload)
        raw_data = json_decode(Zabbix.raw_post(payload))

        self.api_token = raw_data['result']

    def _set_token(self, payload):
        """
        Add authentication token in the payload that will be used in a request

        >>> zb = Zabbix(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        >>> data_with_token = zb._set_token({'auth': None})
        >>> type(data_with_token['auth'])
        <class 'str'>

        :param payload:
        :return:
        """
        if self.api_token is None:
            self._auth_zabbix(self.__api_user, self.__api_password)
        payload['auth'] = self.api_token
        return payload

    @classmethod
    def raw_post(cls, payload: str) -> str:
        """
        Makes a POST request to the Zabbix API with a * payload * that is passed as a parameter

        :param payload: json encode data in str
        :return: json data
        """
        req = urllib.request.Request(uribase, data=payload.encode('utf-8'),
                                     headers={'content-type': 'application/json-rpc'})

        with urllib.request.urlopen(req) as response:
            body = response.read()
        return decode_bytes_to_utf8(body)

    def get_history_from_itemids(self, itemids):
        """
        returns the "N" history of a chart's values from an ID

        >>> zb = Zabbix(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        >>> data = zb.get_history_from_itemids('31359')
        >>> type(data)
        <class 'list'>
        >>> len(data) > 0
        True

        :param itemids:
        :return:
        """

        payload = self._set_token(GET_DATA_HISTORY)
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

        raw_data = json_decode(self.raw_post(json.dumps(payload)))
        f_data = [_raw_data_to_chart_data(d) for d in raw_data.get('result')]

        return [[int(d.get('timestamp')), float(d.get('value'))] for d in f_data]
