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
    "id": 1
}

GET_DATA_HISTORY = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": "extend",
        "history": 0,
        "itemids": [],
        "limit": 100
    },
    "auth": "",
    "id": 1
}
