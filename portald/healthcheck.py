import urllib.request
import json
import environ
import sys

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent


def print_and_exit(msg):
    sys.exit(msg)


def decode_bytes_to_utf8(text: bytes):
    """bytes to str with utf-8 encoding and ignore erros

    >>> type(decode_bytes_to_utf8(b'how are you'))
    <class 'str'>

    :param text:
    :return:
    """
    if isinstance(text, bytes):
        return text.decode('utf-8', errors='ignore')
    return text


def load_config() -> dict:    
    config_file = BASE_DIR / 'portald' / '.env'

    if not config_file.exists():
        config_file = BASE_DIR / '.env'
        if not config_file.exists():
            print_and_exit('.env file in path "%s" not found...' % config_file)

    env = environ.Env(DEBUG=(bool, False))
    env.read_env('%s' % config_file)

    return {
        'debug': env('DEBUG_MODE', default=False),
        'zabbix_url': env('ZABBIX_URL', default='undefined'),
        'zabbix_user': env('ZABBIX_USER', default='undefined'),
        'zabbix_passwd': env('ZABBIX_PASSWORD', default='undefined')
    }


def zabbix_connection(url: str, user: str, passwd: str) -> bool:
    LOGIN_DATA = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "",
            "password": ""
        },
        "id": 1,
        "auth": None
    }
    LOGIN_DATA.update({'params': {'user': user, 'password': passwd}})
    payload = json.dumps(LOGIN_DATA)

    req = urllib.request.Request(url, data=payload.encode('utf-8'),
                                 headers={'content-type': 'application/json-rpc'})

    try:
        with urllib.request.urlopen(req) as response:
            body = response.read()
    except urllib.error.HTTPError as err:
        print('\t- está inacessível... %s' % err)
        return False
    else:
        response = json.loads(decode_bytes_to_utf8(body))

        if not response.get('result'):
            print('\t- não foi possível autenticar usuário %s' % user)

        return True


def main():
    config = load_config()
    print('\n========================')
    print(' Health Check [PortalD] ')
    print('========================')
    print('\n\tTestando conexão com Zabbix...')
    try:
        zabbix_connection(config.get('zabbix_url'), config.get('zabbix_user'), config.get('zabbix_passwd'))
    except (KeyError, ValueError) as err:
        print('make sure the .env file contains the information needed for the test. For more details: %' % err)
    print("\n========================\n")


if __name__ == '__main__':
    main()