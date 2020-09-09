import asyncio
import aiohttp
import ujson
import pprint
import getpass


pp = pprint.PrettyPrinter(indent=2, compact=False, width=51, sort_dicts=False)
cprint = lambda h, b: (print(h), pp.pprint(b))

uri_base = 'http://zabbix.dbafurushima.com.br/api_jsonrpc.php'
headers_json = {'Content-Type': 'application/json-rpc'}

_login_data_json = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "Admin",
            "password": "admin"
        },
        "id": 1,
        "auth": None
    }

_get_graph = {
    "jsonrpc": "2.0",
    "method": "graph.get",
    "params": {
        "output": "extend",
        "hostids": [10326]
    },
    "auth": "",
    "id": 0
}

_get_graphitem = {
    "jsonrpc": "2.0",
    "method": "graphitem.get",
    "params": {
        "output": "extend",
        "graphids": [31359]
    },
    "auth": "",
    "id": 0
}

_get_history = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": "extend",
        "history": 0,
        "itemids": "31359",
        "limit": 10
    },
    "auth": "",
    "id": 0
}

_get_hosts = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "filter": {
            "name": [
                "PORTALDOC - ORASRV9"
            ]
        }
    },
    "auth": "",
    "id": 0
}

_user_token = ""
_user_id = 0


async def post(url, data_json, headers=None):
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.post(url, json=data_json, headers=headers) as resp:
            raw_data = await resp.json()
    
    pp.pprint(raw_data)
    return raw_data
 

async def _get_token(uri, user, passwd):

    _login_data_json["params"]["user"] = user
    _login_data_json["params"]["password"] = passwd

    token = await post(uri, _login_data_json, headers=headers_json)

    return token.get('id', 0), token.get('result', None)


async def get_graph():
    _get_graphitem["auth"] = _user_token
    _get_graphitem["id"] = _user_id

    # _get_graph["params"]["graphids"] = itemids

    cprint('request body json >>> \n', _get_graphitem)

    return await post(uri_base, _get_graphitem, headers=headers_json)


async def get_history():
    _get_history["auth"] = _user_token
    _get_history["id"] = _user_id

    # _get_graph["params"]["graphids"] = itemids

    cprint('request body json >>> \n', _get_history)

    return await post(uri_base, _get_history, headers=headers_json)


async def get_hosts():
    _get_hosts["auth"] = _user_token
    _get_hosts["id"] = _user_id

    cprint('request body json >>> \n', _get_hosts)

    return await post(uri_base, _get_hosts, headers=headers_json)


async def entry_point(user, passwd):
    global _user_id
    global _user_token

    _user_id, _user_token = await _get_token(uri_base, user, passwd)

    await get_history()


if __name__ == '__main__':
    import os

    user = 'paulo_dev' # input('user: ')
    if not os.getenv('ZABBIX_PASSWORD'):
        passwd = getpass.getpass(prompt='password: ', stream=None)
    else:
        passwd = os.getenv('ZABBIX_PASSWORD')

    loop = asyncio.get_event_loop()
    task = loop.create_task(entry_point(user, passwd))
    loop.run_until_complete(task)
