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

GET_DATA_GRAPH = {
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

GET_DATA_HISTORY = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": "extend",
        "history": 0,
        "itemids": "31359",
        "limit": 100
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
